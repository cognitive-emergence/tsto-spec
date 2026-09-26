"""Binding/02 interoperability fixtures; not a production/domain-policy verifier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import tempfile
from datetime import datetime
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
MARKER = {"version": "02", "spec": "JEP-TSTO-Binding/02"}
WHO = "did:example:binding-02-test-actor"
KID = "urn:example:binding-02:PUBLIC-TEST-KEY-DO-NOT-TRUST"


class BindingFailure(ValueError):
    def __init__(self, code, status="invalid"):
        super().__init__(code)
        self.code, self.status = code, status


def require(condition, code, status="invalid"):
    if not condition:
        raise BindingFailure(code, status)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_core(root):
    pin = json.loads((ROOT / "tests/upstream/jep-core-0.7.json").read_text())
    for path, expected in pin["files"].items():
        require(
            hashlib.sha256((root / path).read_bytes()).hexdigest() == expected,
            "UPSTREAM_PIN_MISMATCH",
        )
    require(
        (root / "schemas/jep-event.schema.json").read_bytes()
        == (ROOT / "tests/upstream/jep-event-0.7.schema.json").read_bytes(),
        "SCHEMA_PIN_MISMATCH",
    )
    spec = importlib.util.spec_from_file_location("jep07", root / "reference-validator/jep_validate_07.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.CORE_PROFILE == "jep-core-0.7", "WRONG_CORE_VERSION")
    return module


def schema(path):
    value = json.loads((ROOT / path).read_text())
    Draft202012Validator.check_schema(value)
    checker = FormatChecker()
    require(
        {"uri", "date-time", "duration"} <= set(checker.checkers),
        "MISSING_FORMAT_DEPENDENCIES",
    )
    return Draft202012Validator(value, format_checker=checker)


def object_digest(core, obj):
    return "sha-256:" + core.b64u(hashlib.sha256(rfc8785.dumps(obj)).digest())


def tref(tsto):
    return {
        "kind": "external_object",
        "type": "TargetStateTransition",
        "spec": "TSTO/00",
        "id": tsto["id"],
        "digest": tsto["integrity"]["value"],
    }


def subject(event):
    return event["what"]["subject"] if event["verb"] == "T" else event["ref"]["value"]


def sign(core, event, key, kid=KID, alg="Ed25519"):
    event = copy.deepcopy(event)
    event.pop("sig", None)
    protected = core.b64u(rfc8785.dumps({"alg": alg, "kid": kid}))
    message = (protected + "." + core.b64u(rfc8785.dumps(event))).encode("ascii")
    event["sig"] = protected + ".." + core.b64u(key.sign(message))
    return event


class FixtureVerifier:
    """Explicit baseline and synthetic actor trust, returning independent checks.

    known is a list, not a last-write-wins identity map: conflicting signed
    payloads and multiple artifacts for the same payload remain observable.
    No network fetch, domain evaluation, authority check or acceptance side effect.
    """

    def __init__(self, core, keys):
        self.core, self.keys = core, keys
        self.core_schema = schema("tests/upstream/jep-event-0.7.schema.json")
        self.binding_schema = schema("schemas/jep-tsto-binding-02.schema.json")
        self.tsto_schema = schema("schemas/tsto-00.schema.json")

    def statement(self, event):
        try:
            self.core_schema.validate(event)
        except ValidationError as exc:
            raise BindingFailure("CORE_SCHEMA") from exc
        result = self.core.validate_event(event, keys=self.keys, trust_profile="inline")
        require(
            result["status"] == "valid",
            result["errors"][0]["code"] if result["errors"] else "CORE",
            result["status"],
        )
        try:
            self.binding_schema.validate(event)
        except ValidationError as exc:
            raise BindingFailure("BINDING_SCHEMA") from exc
        return result

    def validate(self, event, tsto, known):
        result = self.statement(event)
        try:
            self.tsto_schema.validate(tsto)
        except ValidationError as exc:
            raise BindingFailure("TSTO_SCHEMA") from exc
        content = {k: v for k, v in tsto.items() if k != "integrity"}
        require(
            object_digest(self.core, content) == tsto["integrity"]["value"],
            "TSTO_CONTENT_DIGEST",
        )
        require(subject(event) == tref(tsto), "TSTO_REFERENCE")

        # Non-domain temporal and identity invariants from TSTO/00.
        def time(value):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))

        issued = time(tsto["issued_at"])
        validity = tsto["validity"]
        require(
            time(tsto["baseline"]["observed_at"])
            <= issued
            <= time(validity.get("not_before", tsto["issued_at"]))
            <= time(validity["achieve_by"])
            <= time(validity["verify_by"]),
            "TSTO_TIME_ORDER",
        )
        ids = [c["id"] for c in tsto["constraints"]]
        require(len(ids) == len(set(ids)), "TSTO_CONSTRAINT_ID")
        if event["verb"] == "T":
            ident = event["ref"]["value"]
            candidates = [e for e in known if (e["who"], e["id"]) == (ident["who"], ident["id"])]
            require(bool(candidates), "TARGET_UNRESOLVED", "indeterminate")
            for target in candidates:
                self.statement(target)
            require(
                len({self.core.payload_digest(e) for e in candidates}) == 1,
                "TARGET_IDENTITY_CONFLICT",
            )
            if "hash" in event["ref"]:
                require(
                    any(self.core.event_hash(e) == event["ref"]["hash"] for e in candidates),
                    "TARGET_HASH",
                )
            require(all(subject(e) == subject(event) for e in candidates), "TARGET_TSTO")
            # The fixture profile demonstrates delegation termination, not a mandate engine.
            if event["what"]["termination_scope"] == "delegation":
                require(all(e["verb"] == "D" for e in candidates), "TARGET_ROLE")
        if event["verb"] == "V":
            require(
                event["what"]["policy_ref"] == tsto["verification"]["policy"],
                "POLICY_REFERENCE",
            )
        return {
            "core": result,
            "binding_references": "pass",
            "tsto_integrity": "pass",
            "tsto_profile_and_policy": "not_checked",
            "external_truth": "not_checked",
        }


def fixtures(core):
    # Public, deterministic test key. It is not a production credential.
    key = Ed25519PrivateKey.from_private_bytes(
        hashlib.sha256(b"JEP-TSTO-Binding-02-PUBLIC-TEST-ONLY").digest()
    )
    jwk = {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": core.b64u(key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)),
        "actors": [WHO],
    }
    tsto = core.load_json(ROOT / "examples/tsto/valid/ar-invoice-settlement.example.json")
    events = []
    for verb in "JDTV":
        # Historical inputs are read, never rewritten; new events get new identities/signatures.
        event = core.load_json(ROOT / f"examples/binding-01/{verb}-signed.json")
        event.pop("nonce")
        event.update(
            id=f"urn:example:binding-02:{verb}",
            who=WHO,
            ext={"jep-tsto.binding": MARKER},
        )
        event["ref"] = {"type": "tsto:target-state-transition", "value": tref(tsto)}
        if verb == "T":
            event["ref"] = {
                "type": "jep:event",
                "value": {"who": WHO, "id": events[1]["id"]},
                "hash": core.event_hash(events[1]),
            }
            event["what"].pop("target")
        events.append(sign(core, event, key))
    base = copy.deepcopy(events)

    def extra(name, index, mutate, **kwargs):
        event = copy.deepcopy(base[index])
        mutate(event)
        if "id" not in kwargs:
            event["id"] = "urn:example:binding-02:" + name
        return sign(core, event, key, **{k: v for k, v in kwargs.items() if k != "id"})

    events += [
        extra("T-identity-only", 2, lambda e: e["ref"].pop("hash")),
        extra("V-indeterminate", 3, lambda e: e["what"].update(result="INDETERMINATE")),
        extra("V-not-satisfied", 3, lambda e: e["what"].update(result="NOT_SATISFIED")),
        extra(
            "J-unicode-jcs",
            0,
            lambda e: e["what"].update(
                context={
                    "text": "验证 王",
                    "10": 1e-7,
                    "2": 1e20,
                    "\ue000": 1e30,
                    "😀": -0.0,
                }
            ),
        ),
        extra(
            "D-domain-profile",
            1,
            lambda e: e["what"].update(scope={"action": "inspect"}, constraints={"attempts": 2}),
        ),
        extra("D-re-signed", 1, lambda e: None, kid=KID + ":alternate", id=True),
    ]
    hostile = []

    def bad(name, index, mutate, expected, *, resign=True, scenario=None, alg="Ed25519"):
        e = copy.deepcopy(base[index])
        mutate(e)
        if resign:
            e = sign(core, e, key, alg=alg)
        hostile.append(
            {
                "name": name,
                "event": e,
                "expected": expected,
                "resigned": resign,
                "scenario": scenario,
            }
        )

    bad("missing-id", 0, lambda e: e.pop("id"), "CORE_SCHEMA")
    bad(
        "legacy-top-level-nonce",
        0,
        lambda e: e.update(nonce="10000000-0000-4000-8000-000000000001"),
        "CORE_SCHEMA",
    )
    bad("missing-marker", 0, lambda e: e["ext"].clear(), "BINDING_SCHEMA")
    bad(
        "unknown-binding",
        0,
        lambda e: e["ext"]["jep-tsto.binding"].update(version="99"),
        "BINDING_SCHEMA",
    )
    bad(
        "conflicting-marker",
        0,
        lambda e: e["ext"]["jep-tsto.binding"].update(spec="JEP-TSTO-Binding/01"),
        "BINDING_SCHEMA",
    )
    bad(
        "unmerged-candidate-marker",
        0,
        lambda e: e["ext"].update(
            {
                "jep-tsto.binding": {
                    "id": "https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-02.schema.json"
                }
            }
        ),
        "BINDING_SCHEMA",
    )
    bad(
        "mixed-candidate-marker",
        0,
        lambda e: e["ext"].update(
            {"prooftask.binding": {"id": "urn:prooftask:jep-tsto-binding:01-candidate:1"}}
        ),
        "BINDING_SCHEMA",
    )
    bad(
        "old-tsto-carrier",
        0,
        lambda e: e["ref"].update(type="TargetStateTransition"),
        "BINDING_SCHEMA",
    )
    bad(
        "extra-tsto-ref-member",
        0,
        lambda e: e["ref"]["value"].update(extra=True),
        "BINDING_SCHEMA",
    )
    bad(
        "relative-tsto-id",
        0,
        lambda e: e["ref"]["value"].update(id="relative"),
        "BINDING_SCHEMA",
    )
    bad(
        "wrong-tsto-id",
        0,
        lambda e: e["ref"]["value"].update(id="urn:example:other"),
        "TSTO_REFERENCE",
    )
    bad(
        "wrong-tsto-digest",
        0,
        lambda e: e["ref"]["value"].update(digest="sha-256:" + "A" * 43),
        "TSTO_REFERENCE",
    )
    bad(
        "digest-domain-confusion",
        0,
        lambda e: e["ref"]["value"].update(digest="sha256:" + "a" * 64),
        "BINDING_SCHEMA",
    )
    bad("D-missing-scope", 1, lambda e: e["what"].pop("scope"), "CORE_SCHEMA")
    bad("T-hash-only", 2, lambda e: e.update(ref=e["ref"]["hash"]), "BINDING_SCHEMA")
    bad(
        "T-duplicated-target",
        2,
        lambda e: e["what"].update(target=e["ref"]["hash"]),
        "BINDING_SCHEMA",
    )
    bad(
        "T-unresolved-actor",
        2,
        lambda e: e["ref"]["value"].update(who="did:example:other"),
        "TARGET_UNRESOLVED",
    )
    bad(
        "T-wrong-hash",
        2,
        lambda e: e["ref"].update(hash="sha256:" + "a" * 64),
        "TARGET_HASH",
    )
    bad(
        "T-identity-conflict",
        2,
        lambda e: None,
        "TARGET_IDENTITY_CONFLICT",
        scenario="identity-conflict",
    )
    bad(
        "T-wrong-target-subject",
        2,
        lambda e: e["ref"].pop("hash"),
        "TARGET_TSTO",
        scenario="wrong-subject",
    )
    bad(
        "T-wrong-target-role",
        2,
        lambda e: e.update(ref={"type": "jep:event", "value": {"who": WHO, "id": base[0]["id"]}}),
        "TARGET_ROLE",
    )
    bad(
        "V-wrong-policy",
        3,
        lambda e: e["what"]["policy_ref"].update(id="urn:example:other-policy"),
        "POLICY_REFERENCE",
    )
    bad(
        "V-wrong-policy-digest",
        3,
        lambda e: e["what"]["policy_ref"].update(digest="sha-256:" + "A" * 43),
        "POLICY_REFERENCE",
    )
    bad("V-empty-evidence", 3, lambda e: e["what"].update(evidence=[]), "BINDING_SCHEMA")
    bad(
        "V-malformed-evidence",
        3,
        lambda e: e["what"]["evidence"][0].pop("digest"),
        "BINDING_SCHEMA",
    )
    bad("V-wrong-result", 3, lambda e: e["what"].update(result=False), "BINDING_SCHEMA")
    bad(
        "unknown-critical-extension",
        0,
        lambda e: e.update(
            ext_crit=["urn:example:unknown"],
            ext={**e["ext"], "urn:example:unknown": {}},
        ),
        "ERR_UNKNOWN_CRITICAL_EXTENSION",
    )
    bad(
        "wrong-actor-key-binding",
        0,
        lambda e: e.update(who="did:example:other"),
        "ERR_KEY_NOT_BOUND_TO_ACTOR",
    )
    bad(
        "EdDSA-is-not-baseline",
        0,
        lambda e: None,
        "ERR_UNSUPPORTED_SIGNATURE_ALG",
        alg="EdDSA",
    )
    bad(
        "tampered-after-signing",
        0,
        lambda e: e["what"].update(decision="reject"),
        "ERR_SIGNATURE_INVALID",
        resign=False,
    )
    return (
        {
            "note": "Synthetic test trust only. External profile/policy/evidence digests are illustrative. No factual outcome, domain-policy or production acceptance claim.",
            "keys": {KID: jwk, KID + ":alternate": jwk},
            "tsto": tsto,
            "events": events,
            "eventHashes": [core.event_hash(e) for e in events],
            "unsignedCanonicalUtf8": [
                rfc8785.dumps({k: v for k, v in e.items() if k != "sig"}).decode() for e in events
            ],
            "hostile": hostile,
        },
        key,
    )


def expect_failure(operation, expected):
    try:
        operation()
    except BindingFailure as exc:
        require(exc.code == expected, f"WRONG_FAILURE:{exc.code}!={expected}")
        if expected == "TARGET_UNRESOLVED":
            require(exc.status == "indeterminate", "UNRESOLVED_MUST_BE_INDETERMINATE")
    else:
        raise AssertionError("hostile input accepted: " + expected)


def run(core, data, key):
    verifier = FixtureVerifier(core, data["keys"])
    events, tsto = data["events"], data["tsto"]
    for i, event in enumerate(events):
        result = verifier.validate(event, tsto, events)
        require(result["core"]["event_hash"] == data["eventHashes"][i], "FIXTURE_HASH")
        require(
            rfc8785.dumps({k: v for k, v in event.items() if k != "sig"}).decode()
            == data["unsignedCanonicalUtf8"][i],
            "FIXTURE_JCS",
        )
        require(result["tsto_profile_and_policy"] == "not_checked", "POLICY_OVERCLAIM")
    for case in data["hostile"]:
        known = events
        if case["scenario"]:
            target = copy.deepcopy(events[1])
            if case["scenario"] == "identity-conflict":
                target["what"]["delegatee"] = "did:example:different-delegatee"
                known = events + [sign(core, target, key)]
            else:
                target["ref"]["value"]["id"] = "urn:example:other-tsto"
                known = [sign(core, target, key)]
        try:
            expect_failure(
                lambda case=case, known=known: verifier.validate(case["event"], tsto, known), case["expected"]
            )
        except Exception as exc:
            raise AssertionError(case["name"]) from exc
    # Multiple artifacts with identical unsigned content retain one Event Identity.
    require(
        core.payload_digest(events[1]) == core.payload_digest(events[-1]),
        "RESIGN_PAYLOAD",
    )
    require(core.event_hash(events[1]) != core.event_hash(events[-1]), "RESIGN_HASH")
    verifier.validate(events[4], tsto, [events[-1]])  # no pin -> identity resolves
    expect_failure(lambda: verifier.validate(events[2], tsto, [events[-1]]), "TARGET_HASH")
    # Content tampering and TSTO invariants that schemas alone cannot express.
    altered = copy.deepcopy(tsto)
    altered["target"]["claims"][0]["value"] = "tampered"
    expect_failure(lambda: verifier.validate(events[0], altered, events), "TSTO_CONTENT_DIGEST")
    altered = copy.deepcopy(tsto)
    altered["validity"]["verify_by"] = "2000-01-01T00:00:00Z"
    altered["integrity"]["value"] = object_digest(
        core, {k: v for k, v in altered.items() if k != "integrity"}
    )
    event = copy.deepcopy(events[0])
    event["ref"]["value"] = tref(altered)
    expect_failure(
        lambda: verifier.validate(sign(core, event, key), altered, events),
        "TSTO_TIME_ORDER",
    )
    altered = copy.deepcopy(tsto)
    altered["constraints"] = [
        {
            "id": "same",
            "scope": "at_target",
            "predicate": {"op": "exists", "path": "/x", "value": True},
        }
    ] * 2
    altered["integrity"]["value"] = object_digest(
        core, {k: v for k, v in altered.items() if k != "integrity"}
    )
    event["ref"]["value"] = tref(altered)
    expect_failure(
        lambda: verifier.validate(sign(core, event, key), altered, events),
        "TSTO_CONSTRAINT_ID",
    )
    raw_cases = [
        '{"id":"a","id":"b"}',
        '{"x":{"id":"a","id":"b"}}',
        '{"n":NaN}',
        '{"n":1e999}',
        '{"n":9007199254740992}',
        '{"s":"\\ud800"}',
    ]
    for raw in raw_cases:
        try:
            core.parse_json(raw)
        except (ValueError, UnicodeError):
            pass
        else:
            raise AssertionError("invalid JSON accepted")
    # Explicit rejection, never fallback/relabeling, of historical events.
    for verb in "JDTV":
        old = core.load_json(ROOT / f"examples/binding-01/{verb}-signed.json")
        expect_failure(lambda old=old: verifier.validate(old, tsto, events), "CORE_SCHEMA")
    with tempfile.TemporaryDirectory(prefix="binding02-acceptance-") as tmp:
        state = Path(tmp) / "accepted.json"

        def accept(event):
            verifier.validate(event, tsto, events)  # binding checks BEFORE any state mutation
            return core.validate_event(
                event,
                keys=data["keys"],
                trust_profile="inline",
                mode="acceptance",
                acceptance_state=state,
            )

        require(
            accept(events[1])["acceptance"] == {"outcome": "accepted", "effect_applied": True},
            "FIRST_ACCEPTANCE",
        )
        saved = state.read_bytes()
        for event in [events[1], events[-1]]:
            result = accept(event)
            require(
                result["status"] == "valid" and result["checks"]["cryptographic"] == "pass",
                "DUPLICATE_CRYPTO",
            )
            require(
                result["acceptance"] == {"outcome": "already_accepted", "effect_applied": False},
                "DUPLICATE_ACCEPTANCE",
            )
        conflict = copy.deepcopy(events[1])
        conflict["what"]["delegatee"] = "did:example:other"
        result = accept(sign(core, conflict, key))
        require(
            result["errors"][0]["code"] == "ERR_EVENT_ID_CONFLICT"
            and not result["acceptance"]["effect_applied"],
            "ACCEPTANCE_CONFLICT",
        )
        wrong = copy.deepcopy(events[0])
        wrong["ref"]["value"]["id"] = "urn:example:other"
        expect_failure(lambda: accept(sign(core, wrong, key)), "TSTO_REFERENCE")
        require(state.read_bytes() == saved, "REJECTED_INPUT_MUTATED_STATE")
    return {
        "core": "0.7",
        "binding": "02",
        "signedEvents": len(events),
        "hostileEventCasesRejected": len(data["hostile"]),
        "invalidJsonCasesRejected": len(raw_cases),
        "historicalEventsRejected": 4,
        "tstoSemanticFailuresRejected": 3,
        "identityAndArtifactSeparation": True,
        "idempotentAcceptance": True,
        "rejectedInputLeavesStateUnchanged": True,
        "scope": "joint schemas, pinned upstream baseline signatures and synthetic actor trust, exact TSTO integrity/references, T identity/hash resolution, V policy-reference equality; profile/policy/evidence truth not checked",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jep-root",
        type=Path,
        default=ROOT.parent / "jep-core",
        help="checkout containing the pinned Core 0.7 schema and validator",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="regenerate deterministic public fixtures before first publication",
    )
    args = parser.parse_args()
    core = load_core(args.jep_root)
    generated, key = fixtures(core)
    path = ROOT / "examples/binding-02/vectors.json"
    if args.generate:
        dump(path, generated)
        for e in generated["events"][:4]:
            dump(ROOT / f'examples/binding-02/{e["verb"]}-signed.json', e)
    data = core.load_json(path)
    require(data == generated, "FIXTURES_NOT_REPRODUCIBLE")
    for e in data["events"][:4]:
        require(
            core.load_json(ROOT / f'examples/binding-02/{e["verb"]}-signed.json') == e,
            "EXAMPLE_DRIFT",
        )
    print(json.dumps(run(core, data, key), indent=2))


if __name__ == "__main__":
    main()
