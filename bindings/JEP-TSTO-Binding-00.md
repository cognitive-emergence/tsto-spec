# JEP-TSTO Binding/00

## Binding JEP-Core 0.6 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 00 (not a formal standard)**  
**Release date: 2026-08-03**  
**Initiator: Cognitive Emergence**  
**License: Creative Commons Attribution 4.0 International (CC BY 4.0)**  
**Language status: This English text is normative. The Chinese text is an informative translation.**

---

## Abstract

This document defines how Judgment Event Protocol (JEP-Core 0.6) Judgment, Delegation, Termination, and Verification event claims bind to an immutable TSTO/00 Target State Transition Object. It specifies carrier rules, signature coverage, distinct digest encodings, three-valued verification mapping, validation order, and example payloads.

This Binding does not modify JEP-Core or TSTO Core. It does not prove external truth, establish authorization, allocate legal liability, execute work, or settle funds.

## 1. Status and Normative Language

This is an experimental interoperability Binding for prototypes and controlled pilots. It is not an IETF work item, an industry consensus, or a formal standard.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are interpreted under BCP 14 when they appear in all capitals.

## 2. Dependencies

An implementation of this Binding MUST independently conform to:

- JEP-Core 0.6, `draft-wang-jep-judgment-event-protocol-06`; and
- TSTO/00, Experimental Draft 00 dated 2026-08-03.

The structural Schema shipped with this Binding is supplementary. It does not replace validation under either dependency.

## 3. Layering Model

| Layer | Responsibility |
| --- | --- |
| TSTO/00 | Immutable statement of the subject, evidenced baseline, target, time boundaries, constraints, and preselected Verification Policy. |
| JEP-Core 0.6 | Signed event claim made by an identified actor at a time, using verb J, D, T, or V. |
| This Binding | Exact placement and semantics of a TSTO reference inside each JEP event. |
| JEP Profile / Trust Profile | Actor, signing-key, credential, authorization-context, archival, or other JEP interoperability rules. |
| TSTO Profile | Domain State Projection, paths, types, evidence mapping, and predicate restrictions. |
| Settlement or legal layer | Payment, liability, remedies, enforceability, and dispute outcomes. |

A valid JEP signature establishes who signed the event content under the applicable trust rules. It does not by itself prove an external fact, authorization, legal liability, or the correctness of a TSTO verification result.

## 4. TSTO Reference

The Binding uses the following `TSTORef` object:

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

All five members are REQUIRED. Additional members are forbidden in Binding/00.

- `id` MUST be the TSTO `id`.
- `digest` MUST equal the TSTO `integrity.value` and therefore use `sha-256:<base64url-no-padding>`.
- A Resolver MUST resolve and validate by the pair `id + digest`; it MUST reject an identity conflict.
- A mutable URL alone is not a TSTO binding.

## 5. Digest Domains

This Binding preserves two different digest domains:

| Object | Encoding |
| --- | --- |
| TSTO content | `sha-256:` followed by 43 unpadded Base64URL characters. |
| JEP event hash | `sha256:` followed by 64 lowercase hexadecimal characters. |

Implementations MUST NOT directly compare these strings, convert one into the other without retrieving and hashing the correct underlying object, or label a TSTO digest as a JEP event hash.

## 6. JEP Carrier Rules

The JEP event MUST retain the top-level members and signature semantics defined by JEP-Core 0.6. This Binding uses `ref` and `what` as follows:

| Verb | `ref` | `what` |
| --- | --- | --- |
| J | `TSTORef` | A `tsto_judgment` claim. |
| D | `TSTORef` | A `tsto_delegation` claim. |
| T | JEP event hash of the terminated delegation or authority event | A `tsto_termination` claim containing the affected `TSTORef` as `subject`. |
| V | `TSTORef` | A `tsto_verification` claim, including scope, Policy, evidence, and three-valued result. |

The complete unsigned JEP event, including `ref` and `what`, MUST be covered by the JEP signature according to JEP-Core. Consequently, both TSTO `id` and `digest` are signed. A detached reference or application database join outside signature coverage is non-conforming.

## 7. Judgment Event (`verb = J`)

`ref` MUST be a `TSTORef`. `what` MUST be an object with:

- `claim` exactly `tsto_judgment`;
- `decision` exactly one of `propose`, `accept`, `reject`, or `reassess`; and
- OPTIONAL `reason` and `context` members.

An `accept` event records the signer's acceptance claim. It does not by itself create legal enforceability, prove authorization, or make the signer an executor.

## 8. Delegation Event (`verb = D`)

`ref` MUST be a `TSTORef`. `what` MUST contain:

- `claim` exactly `tsto_delegation`;
- `delegatee`, a non-empty identifier interpreted by the applicable JEP Profile;
- `scope`, a non-empty array of delegated capabilities or decision contexts;
- OPTIONAL `constraints` object;
- OPTIONAL RFC 3339 `expiry`; and
- OPTIONAL `termination_conditions` array.

The JEP actor in `who` is the declarant of the delegation claim. The Binding does not establish that the actor had external authority to delegate. A JEP Profile or external legal/organizational system MUST supply that determination.

## 9. Termination Event (`verb = T`)

`ref` MUST be the JEP event hash of the terminated Delegation or authority event, using JEP's `sha256:<lowercase-hex>` form. `what` MUST contain:

- `claim` exactly `tsto_termination`;
- `subject`, a `TSTORef` for the affected target object;
- `termination_scope`, exactly one of `delegation`, `authority`, or `future_reliance`; and
- OPTIONAL `reason`.

Termination affects the referenced authority relationship or future reliance. It MUST NOT delete, mutate, or retroactively invalidate the TSTO. Historical events remain available for audit.

## 10. Verification Event (`verb = V`)

`ref` MUST be a `TSTORef`. `what` MUST contain:

- `claim` exactly `tsto_verification`;
- `verification_scope`, a non-empty array containing one or more of `external_evidence`, `factual_claim`, and `policy_compliance`;
- `result`, exactly one of `SATISFIED`, `NOT_SATISFIED`, or `INDETERMINATE`;
- `policy_ref`, the immutable `id + digest` of the same Verification Policy referenced by the TSTO;
- `evidence`, a non-empty array of immutable evidence references; and
- OPTIONAL `observed_at` and `reason`.

The event MUST declare `verification_scope` as required by JEP-Core. A verifier MUST NOT claim a broader scope than it actually evaluated.

The result mapping is exact and lossless:

| TSTO result | JEP-TSTO `result` |
| --- | --- |
| `SATISFIED` | `SATISFIED` |
| `NOT_SATISFIED` | `NOT_SATISFIED` |
| `INDETERMINATE` | `INDETERMINATE` |

`INDETERMINATE` MUST NOT be mapped to failure. A Verification event records the actor's signed verification claim and its scope; its correctness still depends on evidence, Policy execution, and the applicable trust model.

## 11. Verification Policy and Trust Separation

The following objects MUST remain distinct:

1. the TSTO `verification.policy`, selected before outcome evaluation and governing domain facts;
2. the JEP Verification event, created after an evaluation and recording a signed claim;
3. the JEP Profile or Trust Profile, governing event actor, key, credential, and other event-level trust requirements; and
4. the TSTO Profile, governing the domain State Projection, path types, evidence mapping, and predicates.

A matching signature is not a substitute for applying the TSTO Verification Policy. A successful TSTO evaluation is not a substitute for verifying the JEP signature and actor trust.

## 12. Resolution and Validation Procedure

A conforming consumer MUST perform at least the following steps in order:

1. parse JSON while rejecting duplicate member names;
2. validate the event under JEP-Core 0.6, including required members, verb rules, nonce, audience and critical-extension processing where applicable;
3. verify the JEP signature and applicable JEP Profile or Trust Profile;
4. validate the Binding-specific `ref` and `what` shapes for the event verb;
5. obtain the `TSTORef` from `ref`, or from `what.subject` for a Termination event;
6. resolve the TSTO using both `id` and `digest`;
7. validate the TSTO/00 Schema, semantic constraints, and RFC 8785 content digest;
8. confirm that any `policy_ref` matches the TSTO's `verification.policy` by both `id` and digest;
9. for Verification, validate evidence references, declared scope, time rules, and exact three-valued result under the Policy; and
10. retain the event and resolution evidence required by the applicable retention policy.

Failure in steps 2 through 8 MUST cause rejection of the event as conforming to this Binding. Inability to establish a domain result under step 9 normally produces `INDETERMINATE`; it MUST NOT be silently changed to `NOT_SATISFIED`.

## 13. Conformance

An implementation claiming `JEP-TSTO Binding/00` conformance MUST state one or more roles:

| Role | Minimum behavior |
| --- | --- |
| Producer | Constructs a valid JEP event and signs `ref` and `what` within the JEP signature coverage. |
| Resolver | Resolves a TSTO by `id + digest`, validates both protocols, and detects conflicts. |
| Verifier | Applies the TSTO Policy and emits a correctly scoped V event with exact three-valued mapping. |
| Auditor | Replays validation using retained events, objects, Profiles, Policies, evidence references, and trust material. |

The implementation MUST identify the JEP Profile and TSTO Profile used. Passing the supplementary JSON Schema alone is not a conformance claim.

## 14. Security and Privacy

Implementations MUST consider reference substitution, replay, stale Baselines, actor/key substitution, compromised resolvers, digest confusion, mutable evidence locations, overbroad Verification scope, unauthorized disclosure, correlation through stable identifiers, malicious JSON depth or size, Policy withdrawal, and state reversal.

Private evidence MAY remain behind access-controlled resolvers. Events SHOULD expose only the minimum claims and references needed by the audience. A digest does not make personal or confidential material safe to publish if the input space is guessable.

## 15. Versioning and Extensions

This Binding is identified as `JEP-TSTO Binding/00`. A future incompatible change requires a new Binding version. Extensions MUST use JEP's extension mechanism and critical-extension processing rules; they MUST NOT add ambiguous unprotected fields or alter TSTO Core.

## 16. Non-goals

This Binding does not define execution receipts, task orchestration, marketplaces, pricing, settlement, legal authority, liability, remedies, arbitration, or automatic payment. Those systems may rely on conforming events but require separate specifications and policies.

## 17. Examples and Schema

The release includes:

- `schemas/jep-tsto-binding-00.schema.json`, a supplementary structural Schema;
- `examples/jep/J-accept-tsto.example.json`;
- `examples/jep/D-delegate-tsto.example.json`;
- `examples/jep/T-terminate-delegation.example.json`; and
- `examples/jep/V-verify-tsto.example.json`.

Example `sig` values are explicitly marked unsigned and are not cryptographic vectors. Production events MUST carry valid JEP signatures.

## References

- [Judgment Event Protocol, JEP-Core 0.6](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/)
- [JEP Profiles and Interoperability](https://datatracker.ietf.org/doc/draft-wang-jep-profiles/)
- [JEP Conformance and Test Suite](https://datatracker.ietf.org/doc/draft-wang-jep-conformance/)
- [TSTO/00 Target State Transition Object Specification](../SPEC.md)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)
