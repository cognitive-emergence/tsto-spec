# JEP-TSTO Binding/02

## Binding JEP Core 0.7 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 02 (not a formal standard)**  
**Release date: 2026-09-26**  
**Initiator: Cognitive Emergence**  
**License: Creative Commons Attribution 4.0 International (CC BY 4.0)**  
**Language status: This English text is normative.**

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

All five members are REQUIRED.

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

The marker MUST be signed as part of the JEP unsigned event payload.

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
event identity.

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

Binding/02 does not duplicate the target Event Identity inside `what`.

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

`INDETERMINATE` MUST NOT be collapsed into failure.

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
9. for V, verify the selected Verification Policy and evidence needed for
   the declared scope;
10. return or retain the independent JEP and TSTO results without
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

## References

- JEP Core 0.7: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP Core repository: https://github.com/hjs-spec/jep-core
- TSTO/00: ../SPEC.md
- Binding/01 (historical JEP Core 0.6 binding): ./JEP-TSTO-Binding-01.md
