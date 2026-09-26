# JEP-TSTO Binding/02

## Binding JEP Core 0.7 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 02 (not a formal standard)**  
**Release date: 2026-09-26**  
**Initiator: Cognitive Emergence**  
**License: Creative Commons Attribution 4.0 International (CC BY 4.0)**  
**Language status: This English text is normative.**

This is the first executable Binding/02 publication. The earlier main-branch
text and unmerged PRs were implementation work, not released signed formats.
BCP 14 requirement words have their usual meaning when capitalized.

---

## Abstract

This document defines how JEP Core 0.7 Judgment, Delegation, Termination,
and Verification events bind to immutable TSTO/00 Target State Transition
Objects.

Binding/02 adopts the JEP Core 0.7 separation between Event Identity
`(who,id)` and Event Hash, the 0.7 verb-specific `what` requirements,
typed references, independent validation checks, idempotent acceptance, and
substantive-neutrality boundary.

This Binding does not modify JEP Core or TSTO Core. It does not establish
external truth, authorization validity, legal liability, causality,
settlement, or automatic payment.

## 1. Dependencies

A conforming implementation MUST independently conform to:

- JEP Core 0.7, `draft-wang-jep-judgment-event-protocol-07`; and
- TSTO/00.

Binding/01 remains a historical JEP Core 0.6 binding and MUST NOT be
silently reinterpreted as Binding/02.

## 2. Layering

| Layer | Responsibility |
| --- | --- |
| TSTO/00 | Immutable target-state-transition object and its Verification Policy. |
| JEP Core 0.7 | Signed J/D/T/V statement, Event Identity, Event Hash, references, and Core validation semantics. |
| Binding/02 | Exact TSTO carrier and verb-specific mapping. |
| JEP trust/profile layer | Actor/key binding, credentials, algorithms, audience, freshness, challenge policy. |
| Chain/mandate layer | Delegation paths, termination cascade, authority consequences, lifecycle state. |
| Settlement/legal layer | Payment, liability, remedies, enforceability, dispute outcomes. |

A valid JEP event establishes only the protocol properties actually
validated. It does not make a TSTO result true merely because the event is
signed.

## 3. TSTO Reference

Binding/02 uses this immutable TSTO reference object:

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

Exactly these five members are REQUIRED; additional members are forbidden.
`id` is an absolute URI. `digest` uses the TSTO/00 SHA-256, unpadded
Base64URL form (`sha-256:` followed by 43 characters).

- `id` MUST equal the TSTO `id`.
- `digest` MUST equal the TSTO integrity digest.
- Resolution MUST use `id + digest` and MUST reject identity/digest
  conflicts.
- A mutable URL alone is not a conforming TSTO reference.

TSTO digest encoding and JEP Event Hash encoding remain distinct domains and
MUST NOT be confused.

## 4. Binding Marker

Each new Binding/02 event MUST carry:

```json
"ext": {
  "jep-tsto.binding": {
    "version": "02",
    "spec": "JEP-TSTO-Binding/02"
  }
}
```

The marker contains exactly `version` and `spec`, with the values above,
and MUST be signed as part of the JEP unsigned event payload. A Schema-URL
`id` marker from Binding/01 or an unpublished 02 proposal is not this marker.
A conflicting historical `prooftask.binding` marker MUST be rejected.

The marker MUST NOT cause a generic JEP Core verifier to claim TSTO
semantics. Binding-aware processors must explicitly select Binding/02.

## 5. TSTO Carrier

For J, D, and V, `ref` MUST identify the bound TSTO:

```json
{
  "type": "tsto:target-state-transition",
  "value": {
    "kind": "external_object",
    "type": "TargetStateTransition",
    "spec": "TSTO/00",
    "id": "urn:uuid:...",
    "digest": "sha-256:..."
  }
}
```

For T, `ref` MUST identify the JEP event whose future reliance is being
terminated. A logical event reference uses Event Identity:

```json
{
  "type": "jep:event",
  "value": {
    "who": "did:example:actor",
    "id": "urn:uuid:..."
  },
  "hash": "sha256:..."
}
```

The optional `hash` pins an exact signed artifact. It is not the stable
event identity. The JEP baseline representation is `sha256:` followed by
64 lowercase hexadecimal characters. Reference objects contain exactly the
members shown (`hash` remains optional).

## 6. Judgment (J)

A TSTO-bound J event MUST:

- use `verb: "J"`;
- carry the TSTO reference in `ref`;
- carry an object-valued `what` with:
  - `claim: "tsto_judgment"`;
  - `decision`, one of `propose`, `accept`, `reject`, or `reassess`;
  - OPTIONAL `reason` and `context`.

A J event records the actor's judgment statement. It does not establish
that the TSTO is externally satisfied, authorized, legally binding, or
eligible for settlement.

## 7. Delegation (D)

A TSTO-bound D event MUST:

- use `verb: "D"`;
- carry the TSTO reference in `ref`;
- carry object-valued `what` with the JEP Core members:
  - `delegatee`;
  - `scope`;
- additionally carry `claim: "tsto_delegation"`;
- MAY carry `constraints`, `expiry`, `termination_conditions`, or
  domain-profile members.

Core 0.7 leaves the representation and interpretation of `scope` and the
optional domain members to the selected profile. Binding/02 does not import
Binding/01's array-only constraints rule. Producers and consumers MUST agree
on that profile; the structural harness does not evaluate its meaning.

The actor in `who` is the declarant. Binding/02 does not prove that the
actor had authority to delegate.

## 8. Termination (T)

A TSTO-bound T event MUST:

- use `verb: "T"`;
- use a typed `jep:event` reference in `ref` to identify the target
  Event Identity;
- MAY include the target Event Hash in `ref.hash` when exact-artifact
  pinning is required;
- carry object-valued `what` with:
  - `claim: "tsto_termination"`;
  - `termination_scope`;
  - `subject`, equal to the affected TSTO reference;
  - OPTIONAL `reason`.

Binding/02 does not duplicate the target Event Identity inside `what`;
legacy `what.target` is forbidden. A consumer MUST resolve both target
`who` and `id`, detect differing unsigned payloads for the same identity,
and compare `ref.hash` to the exact full signed target when a pin is present.
It MUST verify that the resolved target is bound to `what.subject` by
`id + digest`. A missing target is unresolved, not a successful reference
check; an identity, hash or subject mismatch fails the reference check.
The selected domain profile determines eligible target roles and scope.
Historical targets require an explicitly selected historical decoder;
they MUST NOT be relabeled as Binding/02.

A T event records a termination declaration. It does not delete history,
retroactively invalidate the referenced event, or by itself determine a
termination cascade. Cascade and authority consequences belong to a chain,
mandate, or policy layer.

## 9. Verification (V)

A TSTO-bound V event MUST:

- use `verb: "V"`;
- carry the TSTO reference in `ref`;
- carry object-valued `what` with the JEP Core members:
  - `verification_scope`;
  - `result`;
- additionally carry:
  - `claim: "tsto_verification"`;
  - `policy_ref`, identifying the immutable Verification Policy;
  - `evidence`, a non-empty array of immutable evidence references;
  - OPTIONAL `observed_at` and `reason`.

For the standard TSTO three-valued result profile, `what.result` is exactly
one of:

- `SATISFIED`;
- `NOT_SATISFIED`;
- `INDETERMINATE`.

`policy_ref` is the TSTO/00 immutable `id + digest` reference and MUST
equal the bound TSTO's `verification.policy`. Each evidence entry MUST
conform to TSTO/00 section 9. Schema validation cannot establish evidence
availability, admissibility or truth.

`INDETERMINATE` MUST NOT be collapsed into failure. The scoped result is
a signed claim; a consumer's ability to validate that claim is a separate
result. An unavailable required policy or evidence cannot become a
successful policy check merely because the event is cryptographically valid.

A V event records a scoped evaluation result. JEP validity does not itself
establish that the result is factually correct.

## 10. Event Identity and Event Hash

Binding/02 preserves the JEP Core 0.7 distinction:

- Event Identity = `(who,id)`;
- Event Hash = digest of one exact full signed event artifact.

Semantic references to JEP events MUST use Event Identity. Exact-artifact
integrity MAY additionally use Event Hash.

Implementations MUST NOT replace Event Identity with Event Hash merely
because Binding/01 used hash-only termination targets.

## 11. Acceptance and Replay

Binding/02 does not require a Core nonce.

A Binding/02 processor that performs JEP acceptance MUST preserve JEP Core
0.7 idempotent-acceptance semantics: one Event Identity applies its
acceptance effect at most once within one acceptance domain.

The same identity and unsigned payload, including a newly signed artifact,
returns `already_accepted` without applying the effect again. The same
identity with different unsigned content is an identity conflict. Required
Binding and profile checks MUST complete before committing the application
acceptance effect; a rejected or unresolved reference must not consume it.
The identity/state update and that effect require atomic coordination in
the application. This Binding does not define a storage backend.

A trust or interaction profile MAY additionally require nonce, challenge,
sequence, trusted timestamp, transaction identifier, ledger position, or
other freshness/single-use mechanisms.

TSTO settlement or payment consumption is distinct from JEP event
acceptance and may require stronger reservation or single-use rules.

## 12. Validation

A Binding/02 consumer MUST:

1. parse JSON and reject duplicate members;
2. explicitly select JEP Core 0.7 and Binding/02;
3. validate JEP Core structure and verb-specific requirements;
4. verify the applicable JEP signature/conformance profile;
5. perform required JEP Core and trust-profile checks;
6. validate the Binding/02 marker, `ref`, and `what` mapping;
7. resolve the TSTO by `id + digest`;
8. validate TSTO Core and the applicable TSTO Profile;
9. for T, resolve and check the target identity, optional hash and subject;
10. for V, verify the selected Verification Policy and evidence needed for
    the declared scope;
11. return or retain the independent JEP and TSTO results without
    conflating them.

A failed 0.7/Binding-02 validation MUST NOT trigger heuristic fallback to
Binding/01 or JEP Core 0.6.

## 13. Historical Compatibility

Binding/00 and Binding/01 remain immutable historical specifications.

Historical signed bytes, Event Hashes, signatures, and receipts MUST NOT be
rewritten. Migration creates a new JEP Core 0.7 event with a new Event
Identity; it does not mutate an older event.

Mixed histories MAY contain Binding/01 and Binding/02 events, but each event
MUST be decoded according to explicitly selected version metadata.

## 14. Security and Privacy

Implementations must consider:

- actor/key substitution;
- reference substitution;
- Event Identity conflicts;
- exact-artifact hash mismatch;
- replay and repeated acceptance;
- stale or unavailable TSTO baselines;
- evidence correlation and disclosure;
- over-broad verification scope;
- incomplete observed logs;
- malicious or unavailable resolvers;
- policy/version confusion.

Private evidence SHOULD remain behind controlled resolvers when possible.
Stable identifiers and digests may enable correlation.

## 15. Non-goals

Binding/02 does not define task execution, workflow orchestration,
marketplaces, pricing, payment settlement, legal authority, liability,
remedies, arbitration, or automatic enforcement.

## 16. Executable Interoperability Path

Apply the [supplementary Binding Schema](../schemas/jep-tsto-binding-02.schema.json)
**together with** the pinned Core 0.7 Schema. The supplement does not replace
Core validation. URI and date-time formats must be enforced. Additional
`what` members are profile-defined, except the forbidden legacy T target;
unknown top-level event members remain subject to Core rules.

The [repository harness](../scripts/check-binding-02.py) uses the unchanged
Core 0.7 Python validator pinned in
[`tests/upstream/jep-core-0.7.json`](../tests/upstream/jep-core-0.7.json).
Its explicit signature profile is `JEP-Baseline-Ed25519-JWS-JCS-0.7`:
RFC 8785 canonical unsigned payload, detached compact JWS, protected
`alg=Ed25519` and `kid`, with synthetic actor/key binding. `EdDSA` is not an
alias in this profile. No critical extension handler is installed; examples
carry the Binding marker as a noncritical signed extension. A deployment
using another signature/trust profile must select and implement it explicitly.

The harness separately reports Core checks, Binding reference checks and
TSTO integrity. Full TSTO Profile/Policy evaluation and external truth are
`not_checked`, so passing it is **not** a full TSTO-consumer conformance claim.
It uses a local test acceptance store to demonstrate Core idempotency, not
production settlement, distributed storage or payment consumption.

See the [README](../README.md) for the reproduction command and the
[release notes](../releases/binding-02/RELEASE-NOTES.md) for migration and limits.

## References

- JEP Core 0.7: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP Core repository: https://github.com/hjs-spec/jep-core
- TSTO/00: ../SPEC.md
- Binding/01 (historical JEP Core 0.6 binding): ./JEP-TSTO-Binding-01.md
