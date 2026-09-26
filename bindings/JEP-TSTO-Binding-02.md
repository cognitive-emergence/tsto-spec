# JEP-TSTO Binding/02

## Binding JEP Core 0.7 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 02**  
**Release date: 2026-09-26**  
**Initiator: Cognitive Emergence**  
**Language status: This English text is normative.**

---

## Abstract

This document defines a JEP Core 0.7 binding for immutable TSTO/00 Target
State Transition Objects. It preserves JEP Event Identity `(who,id)`,
separates exact signed-artifact hashes from logical event identity, uses
the JEP Core 0.7 minimum J/D/T/V shapes, and keeps TSTO verification policy,
external truth, authorization, legal effect, and settlement outside JEP Core.

Binding/01 remains an immutable JEP Core 0.6 binding. Binding/02 does not
rewrite or relabel Binding/01 events.

## 1. Dependencies

A Binding/02 implementation MUST independently conform to:

- JEP Core 0.7, `draft-wang-jep-judgment-event-protocol-07`; and
- TSTO/00.

The supplementary Binding/02 JSON Schema does not replace JEP signature,
trust-profile, reference-resolution, or TSTO semantic validation.

## 2. Layering

| Layer | Responsibility |
| --- | --- |
| JEP Core 0.7 | Signed event statement, Event Identity, exact-artifact hash, Core verb semantics, validation-result model |
| TSTO/00 | Immutable target-state transition object and verification-policy reference |
| Binding/02 | Placement and semantics of immutable TSTO references inside JEP events |
| JEP trust/profile layer | Actor/key binding, algorithm policy, audience, freshness, challenge, acceptance-domain rules |
| Chain/mandate layer | Delegation-path interpretation, termination cascade, authorization consequences |
| TSTO Profile | State projection, evidence mapping, predicates, domain types |
| External systems | Legal effect, settlement, remedies, payment, execution |

A Core-valid JEP event records a signed statement. It does not by itself
establish substantive truth, authority, legality, causality, policy outcome,
or external effect.

## 3. TSTO Reference

Binding/02 uses:

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

All five members are REQUIRED.

- `id` is the TSTO identifier.
- `digest` equals the TSTO content digest.
- Resolution MUST use both `id` and `digest`.
- A mutable URL alone is not a conforming TSTO binding.

TSTO digests and JEP Event Hashes are different digest domains and MUST NOT
be compared as if they identify the same bytes.

## 4. Binding Marker

Every new Binding/02 event MUST include:

```json
"ext": {
  "jep-tsto.binding": {
    "id": "https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-02.schema.json"
  }
}
```

The marker is signed as part of the JEP unsigned event. It identifies this
binding version. A consumer MUST select Binding/02 explicitly and MUST NOT
retry Binding/01 after a Binding/02 validation failure.

## 5. Verb Mapping

| Verb | `ref` | Required `what` minimum |
| --- | --- | --- |
| J | TSTO typed reference | Binding judgment claim |
| D | TSTO typed reference | `delegatee`, `scope` plus binding claim |
| T | JEP event reference by Event Identity, optional exact-artifact hash | `termination_scope`, affected TSTO subject |
| V | TSTO typed reference | `verification_scope`, `result`, policy/evidence binding |

Binding/02 MUST NOT redefine the JEP Core minimum requirements.

## 6. Judgment (J)

`ref` MUST identify the TSTO object.

`what` MUST contain:

- `claim: "tsto_judgment"`;
- `decision`: one of `propose`, `accept`, `reject`, `reassess`;
- OPTIONAL `reason`;
- OPTIONAL `context`.

A J event records the actor's judgment statement. It does not prove the
judged proposition or external authority.

## 7. Delegation (D)

`ref` MUST identify the TSTO object.

`what` MUST contain the JEP Core 0.7 minimum:

- `delegatee`;
- `scope`;

and Binding/02 additionally requires:

- `claim: "tsto_delegation"`.

Optional constraints, expiry, termination conditions, and domain metadata MAY
be added without changing the Core meaning.

Binding/02 does not determine whether the delegator had external authority.

## 8. Termination (T)

A T event MUST identify the terminated JEP event using a typed JEP event
reference:

```json
{
  "type": "jep:event",
  "value": {
    "who": "did:example:delegator",
    "id": "urn:uuid:..."
  },
  "hash": "sha256:..."
}
```

The `hash` member is OPTIONAL and pins one exact signed artifact. The
`value` member is the logical target through JEP Event Identity.

`what` MUST contain:

- `claim: "tsto_termination"`;
- `termination_scope`;
- `subject`: the affected TSTORef;
- OPTIONAL `reason`.

Binding/02 does not require a duplicate target inside `what`.

A T event records a termination declaration. It does not delete history,
retroactively invalidate the target event, or independently establish
downstream cascade or authorization consequences.

## 9. Verification (V)

`ref` MUST identify the TSTO object.

`what` MUST contain:

- `claim: "tsto_verification"`;
- `verification_scope`, a non-empty array;
- `result`, exactly one of `SATISFIED`, `NOT_SATISFIED`,
  `INDETERMINATE`;
- `policy_ref`, the immutable Verification Policy identifier and digest;
- `evidence`, a non-empty array of immutable evidence references;
- OPTIONAL `observed_at`;
- OPTIONAL `reason`.

The three-valued mapping is exact. `INDETERMINATE` MUST NOT be silently
converted into failure.

A V event records the result of evaluating the referenced TSTO under the
declared verification scope. Its correctness still depends on the evidence,
TSTO Verification Policy, and applicable trust/profile rules.

## 10. Event Identity and Artifact Pinning

Binding/02 follows JEP Core 0.7:

- logical JEP event identity is `(who,id)`;
- Event Hash identifies an exact signed artifact;
- re-signing identical unsigned event content MAY change Event Hash without
  changing Event Identity;
- a Binding implementation MUST NOT use Event Hash as the stable event
  identity.

When exact-byte provenance matters, a reference MAY carry both Event Identity
and an Event Hash pin.

## 11. Replay, Freshness, and Acceptance

Binding/02 adds no mandatory nonce.

Duplicate delivery and acceptance follow JEP Core 0.7 idempotent acceptance.
A profile MAY add nonce, challenge, timestamp, counter, reservation, ledger,
or other freshness/single-use mechanisms.

TSTO transaction or settlement systems MUST NOT treat JEP Event Identity
deduplication as proof that an external economic authority was consumed only
once unless the applicable profile defines that property.

## 12. Validation Procedure

A Binding/02 consumer MUST:

1. parse JSON and reject duplicate members;
2. select JEP Core 0.7 and Binding/02 explicitly;
3. validate the JEP Core 0.7 minimum shape;
4. verify the JEP signature under the selected signature/trust profile;
5. process critical extensions;
6. validate the Binding/02 marker and verb-specific carrier;
7. resolve TSTO by `id + digest`;
8. validate TSTO/00 and its content digest;
9. for T, resolve the target by JEP Event Identity and validate an optional
   exact-artifact hash pin;
10. for V, apply the declared TSTO Verification Policy to the retained
    evidence and preserve the three-valued result;
11. report JEP Core checks separately from TSTO/domain-policy conclusions.

Failure of a Binding/02 check MUST NOT trigger heuristic fallback to an older
binding.

## 13. Historical Compatibility

Binding/00 and Binding/01 remain immutable.

Historical signed bytes, signatures, hashes, and receipts MUST NOT be
rewritten. A migration creates a new JEP Core 0.7 event with a new Event
Identity; it does not transform an old signed event in place.

Consumers supporting multiple generations MUST select the decoder from
explicit artifact context or signed binding metadata.

## 14. Security and Privacy

Implementations MUST consider actor/key substitution, reference
substitution, stale evidence, digest confusion, malicious resolvers,
overbroad verification scope, incomplete logs, identifier correlation,
unauthorized disclosure, and profile downgrade.

Private evidence SHOULD remain behind access-controlled resolvers when
possible. A digest does not by itself make sensitive information safe to
publish.

## 15. Non-goals

This Binding does not define task execution, marketplaces, pricing, payment,
settlement, legal authority, liability, remedies, arbitration, or automatic
workflow consequences.

## References

- JEP Core 0.7: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP Core repository: https://github.com/hjs-spec/jep-core
- TSTO/00: ../SPEC.md
- Binding/01: ./JEP-TSTO-Binding-01.md
