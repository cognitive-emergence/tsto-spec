# JEP-TSTO Binding/02

## Binding JEP Core 0.7 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 02 (not a formal standard)**  
**Release date: 2026-09-26**  
**Initiator: Cognitive Emergence**  
**License: Creative Commons Attribution 4.0 International (CC BY 4.0)**

---

## Abstract

This document defines how JEP Core 0.7 Judgment, Delegation, Termination,
and Verification statements bind to immutable TSTO/00 Target State
Transition Objects.

Binding/02 preserves the TSTO object model and updates only the JEP side
of the binding for JEP Core 0.7: stable Event Identity `(who,id)`,
typed event references, optional exact-artifact hash pins, independent
validation checks, and profile-scoped freshness.

This Binding does not modify JEP Core or TSTO Core. It does not establish
substantive truth, authorization, legality, liability, settlement, or
external effect.

## 1. Dependencies

A conforming implementation MUST independently support:

- JEP Core 0.7, `draft-wang-jep-judgment-event-protocol-07`; and
- TSTO/00.

Binding/01 remains an immutable historical binding for JEP Core 0.6.
Binding/02 MUST NOT reinterpret or rewrite Binding/01 signed events.

## 2. Layering

| Layer | Responsibility |
| --- | --- |
| TSTO/00 | Immutable target-state transition object and verification policy |
| JEP Core 0.7 | Signed J/D/T/V statement, Event Identity, artifact hash, Core validation |
| Binding/02 | Placement and semantics of TSTO references in JEP events |
| JEP Profile | Actor/key binding, freshness, audience, algorithm and trust policy |
| TSTO Profile | Domain state projection, evidence mapping and predicates |
| Chain / settlement / legal layer | Causality, cascade, payment, liability and remedies |

A JEP-valid event establishes protocol-observable properties of a signed
statement. It does not by itself establish the substantive correctness
or authority of that statement.

## 3. TSTO Reference

Binding/02 retains the Binding/01 `TSTORef` shape:

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

All members are REQUIRED. A resolver MUST resolve the pair `id + digest`
and reject an identity conflict.

TSTO digest encoding and JEP Event Hash encoding remain distinct domains.

## 4. Binding Marker

Every Binding/02 event MUST contain:

```json
"ext": {
  "jep-tsto.binding": {
    "id": "https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-02.schema.json"
  }
}
```

The marker identifies Binding/02. It MUST NOT be placed in `ext_crit`.
Binding-aware consumers MUST require it. Generic JEP acceptance is not
Binding/02 conformance.

## 5. Carrier Rules

| Verb | `ref` | Minimum `what` |
| --- | --- | --- |
| J | typed TSTO reference | `claim=tsto_judgment`, `decision` |
| D | typed TSTO reference | `claim=tsto_delegation`, `delegatee`, `scope` |
| T | typed `jep:event` Event Identity, optional artifact hash | `claim=tsto_termination`, `subject`, `termination_scope` |
| V | typed TSTO reference | `claim=tsto_verification`, `verification_scope`, `result`, policy/evidence |

The complete `ref`, `what`, marker, and other Core members are covered
by the JEP signature.

## 6. Judgment

A J event MUST use:

```json
"ref": {
  "type": "TargetStateTransition",
  "value": { "...": "TSTORef" }
}
```

`what` MUST contain:

- `claim = "tsto_judgment"`;
- `decision`, one of `propose`, `accept`, `reject`, `reassess`;
- OPTIONAL `reason` and `context`.

The event records the actor's judgment statement. It does not itself
establish truth, authorization, or legal effect.

## 7. Delegation

A D event MUST use the same typed TSTO reference carrier.

`what` MUST contain:

- `claim = "tsto_delegation"`;
- non-empty `delegatee`;
- non-empty `scope`;
- OPTIONAL constraints, expiry, context, or termination conditions.

The D event records a scoped delegation statement. Whether the actor had
authority to delegate is external to JEP Core and this Binding.

## 8. Termination

A T event MUST identify its semantic target by JEP Event Identity:

```json
"ref": {
  "type": "jep:event",
  "value": {
    "who": "did:example:actor",
    "id": "urn:uuid:..."
  },
  "hash": "sha256:..."
}
```

The `hash` member is OPTIONAL. When present, it pins one exact signed
artifact representing the target event. It MUST NOT be treated as the
semantic Event Identity.

`what` MUST contain:

- `claim = "tsto_termination"`;
- `subject`, the affected `TSTORef`;
- `termination_scope`, one of `delegation`, `authority`,
  `future_reliance`;
- OPTIONAL `reason`.

Binding/02 does not duplicate the target Event Identity inside `what`.
The target is carried by `ref`.

Termination records a statement about future reliance. It does not
delete history, retroactively invalidate the target, or define cascade
semantics. Cascade and authorization consequences require a chain,
mandate, or domain profile.

## 9. Verification

A V event MUST use a typed TSTO reference and MUST contain:

- `claim = "tsto_verification"`;
- non-empty `verification_scope`;
- `result`, one of `SATISFIED`, `NOT_SATISFIED`,
  `INDETERMINATE`;
- immutable `policy_ref`;
- non-empty immutable `evidence` array;
- OPTIONAL `observed_at` and `reason`.

The event MUST NOT imply verification beyond its declared scope.
`INDETERMINATE` is a result and MUST NOT be silently mapped to failure.

A V event records a scoped evaluation result. Correctness of that result
still depends on the TSTO policy, evidence, and applicable trust model.

## 10. Event Identity and Artifact Identity

Binding/02 distinguishes:

- JEP Event Identity: `(who,id)`;
- JEP Event Hash: exact full signed artifact digest;
- TSTO identity: TSTO `id`;
- TSTO integrity digest: TSTO `integrity.value`.

These identifiers MUST NOT be substituted for each other.

Semantic JEP event relationships use Event Identity. Exact archival or
artifact commitments MAY additionally use Event Hash.

## 11. Validation Procedure

A conforming consumer MUST:

1. parse JSON with duplicate-member rejection;
2. explicitly select JEP Core 0.7 and Binding/02;
3. validate the JEP Core 0.7 event shape and verb minimums;
4. verify the JEP signature under the selected signature/trust profile;
5. perform required JEP Core and profile checks;
6. validate Binding/02 marker, `ref`, and `what`;
7. resolve TSTO by `id + digest`;
8. validate TSTO/00 and the applicable TSTO Profile;
9. for T, resolve the target by Event Identity and verify the optional
   artifact hash if present;
10. for V, apply the selected TSTO Verification Policy and retain the
    scoped result and evidence.

A failed 0.7/02 validation MUST NOT trigger heuristic fallback to
JEP Core 0.6 or Binding/01.

## 12. Replay and Freshness

Binding/02 does not add a mandatory nonce.

If a deployment requires challenge freshness, nonce uniqueness, trusted
time, ordering, transaction identifiers, counters, or single-use
authority, those requirements MUST be declared by the applicable JEP
Profile or application protocol.

Stable Event Identity and idempotent acceptance do not by themselves
prove current liveness or single-use authority.

## 13. Conformance Roles

An implementation MAY claim one or more roles:

- **Producer**: constructs Binding/02 J/D/T/V events;
- **Resolver**: resolves JEP and TSTO identities and artifact pins;
- **Verifier**: applies JEP checks plus TSTO verification policy;
- **Auditor**: reproduces validation from retained immutable artifacts.

Passing the supplementary JSON Schema alone is not a complete
conformance claim.

## 14. Historical Compatibility

Binding/00 and Binding/01 remain immutable.

Consumers supporting multiple revisions MUST select the decoder
explicitly from known artifact context or binding marker. They MUST NOT:

1. attempt Binding/02;
2. observe failure;
3. silently retry Binding/01 or Binding/00.

Signed historical bytes, signatures, hashes, receipts, and TSTO objects
MUST NOT be rewritten.

## 15. Security and Privacy

Implementations must consider actor/key substitution, target
substitution, Event Identity conflict, artifact-hash mismatch, mutable
evidence, stale data, correlation through stable identifiers, and
over-broad verification scope.

Sensitive evidence SHOULD remain behind access-controlled resolvers when
possible. Digest references do not automatically make sensitive content
safe to disclose.

## 16. Non-goals

This Binding does not define workflow execution, marketplace behavior,
pricing, settlement, payment readiness, legal liability, remedies,
arbitration, or automatic enforcement.

## References

- JEP Core 0.7: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP Core repository: https://github.com/hjs-spec/jep-core
- TSTO/00: ../SPEC.md
- Binding/01: ./JEP-TSTO-Binding-01.md
