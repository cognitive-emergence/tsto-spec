# JEP-TSTO Binding/01

## Binding JEP-Core 0.6 Events to TSTO/00 Objects

**Status: Experimental Binding Draft 01 (not a formal standard)**  
**Release date: 2026-09-12**  
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

All five members are REQUIRED. Additional members are forbidden in Binding/01. This exact five-member object is preserved inside the typed JEP carrier described below.

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
| J | `{"type":"TargetStateTransition","value":TSTORef}` | A `tsto_judgment` claim. |
| D | `{"type":"TargetStateTransition","value":TSTORef}` | A `tsto_delegation` claim. |
| T | JEP event hash of the terminated delegation or authority event | A `tsto_termination` claim with `target` equal to `ref` and the affected `TSTORef` as `subject`. |
| V | `{"type":"TargetStateTransition","value":TSTORef}` | A `tsto_verification` claim, including scope, Policy, evidence, and three-valued result. |

Every Binding/01 event MUST include this signed, non-critical extension:

```json
"ext": {
  "jep-tsto.binding": {
    "id": "https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-01.schema.json"
  }
}
```

The marker object MUST contain exactly `id`. It identifies this versioned Schema and this Binding; consumers MUST use a pinned local copy and MUST NOT fetch or execute an arbitrary marker URL. The marker MUST NOT occur in `ext_crit`. Binding-aware consumers MUST require and validate it even though generic JEP consumers may ignore it. Such generic acceptance is not Binding conformance. An event MUST NOT also contain the historical `prooftask.binding` marker. Unknown critical extensions MUST be rejected unless explicitly implemented by the declared profile.

The complete unsigned JEP event, including `ref`, `what`, `ext`, and `ext_crit` when present, MUST be covered by the JEP signature according to JEP-Core. Consequently, both TSTO `id` and `digest` are signed. A detached reference or application database join outside signature coverage is non-conforming.

## 7. Judgment Event (`verb = J`)

`ref` MUST be an object with exactly `type` and `value`: `type` MUST be `TargetStateTransition`, and `value` MUST be the exact `TSTORef`. `what` MUST be an object with:

- `claim` exactly `tsto_judgment`;
- `decision` exactly one of `propose`, `accept`, `reject`, or `reassess`; and
- OPTIONAL `reason` and `context` members.

An `accept` event records the signer's acceptance claim. It does not by itself create legal enforceability, prove authorization, or make the signer an executor.

## 8. Delegation Event (`verb = D`)

`ref` MUST be an object with exactly `type` and `value`: `type` MUST be `TargetStateTransition`, and `value` MUST be the exact `TSTORef`. `what` MUST contain:

- `claim` exactly `tsto_delegation`;
- `delegatee`, a non-empty identifier interpreted by the applicable JEP Profile;
- `scope`, a non-empty array of delegated capabilities or decision contexts;
- OPTIONAL `constraints`, an array of objects interpreted conjunctively; all listed constraints apply, and an empty array adds no restrictions;
- OPTIONAL RFC 3339 `expiry`; and
- OPTIONAL `termination_conditions` array.

The JEP actor in `who` is the declarant of the delegation claim. The Binding does not establish that the actor had external authority to delegate. A JEP Profile or external legal/organizational system MUST supply that determination.

## 9. Termination Event (`verb = T`)

`ref` MUST be the JEP event hash of the terminated Delegation or authority event, using JEP's `sha256:<lowercase-hex>` form. `what` MUST contain:

- `claim` exactly `tsto_termination`;
- `target`, exactly equal to the JEP event hash in `ref`;
- `subject`, a `TSTORef` for the affected target object;
- `termination_scope`, exactly one of `delegation`, `authority`, or `future_reliance`; and
- OPTIONAL `reason`.

A consumer MUST compare `what.target` and `ref` byte-for-byte and resolve that hash to the full signed target event. For `delegation`, the target MUST be D. When the target is a TSTO-bound event, its TSTORef MUST equal `what.subject`; other authority/future-reliance targets require an explicitly supported profile that establishes the same affected object. Missing or conflicting target resolution MUST fail closed.

Termination affects the referenced authority relationship or future reliance. It MUST NOT delete, mutate, or retroactively invalidate the TSTO. Historical events remain available for audit.

## 10. Verification Event (`verb = V`)

`ref` MUST be an object with exactly `type` and `value`: `type` MUST be `TargetStateTransition`, and `value` MUST be the exact `TSTORef`. `what` MUST contain:

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
2. select the version from the signed marker without fallback, and validate the event under the declared JEP-Core 0.6 path, including required members, verb rules, nonce, audience and critical-extension processing where applicable;
3. verify the JEP signature and applicable JEP Profile or Trust Profile;
4. validate the Binding-specific `ref` and `what` shapes for the event verb;
5. obtain the exact `TSTORef` from `ref.value`, or from `what.subject` for T; validate T target equality and target-event resolution as specified in Section 9;
6. resolve the TSTO using both `id` and `digest`;
7. validate the TSTO/00 Schema, semantic constraints, and RFC 8785 content digest;
8. confirm that any `policy_ref` matches the TSTO's `verification.policy` by both `id` and digest;
9. for Verification, validate evidence references, declared scope, time rules, and exact three-valued result under the Policy; and
10. retain the event and resolution evidence required by the applicable retention policy.

Failure in steps 2 through 8 MUST cause rejection of the event as conforming to this Binding. Inability to establish a domain result under step 9 normally produces `INDETERMINATE`; it MUST NOT be silently changed to `NOT_SATISFIED`.

## 13. Conformance

An implementation claiming `JEP-TSTO Binding/01` conformance MUST state one or more roles:

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

## 15. Versioning and Historical Compatibility

This Binding is identified as `JEP-TSTO Binding/01` by the exact signed marker in Section 6. TSTO remains `TSTO/00`; JEP wire version remains `"1"`. Incompatible revisions require a new identifier and explicit decoder support.

The published Binding/00 texts, Schemas, examples, and PDFs remain immutable. Its J/D/V bare TSTORef, object-valued D constraints, and T without `what.target` conflict with the JEP Schema pinned for this release. Historical signature verification under an explicitly named compatibility profile is not a claim that these records satisfy the current joint Schema path.

The historical Prooftask candidate uses `ext["prooftask.binding"].id = "urn:prooftask:jep-tsto-binding:01-candidate:1"`. Its carrier is structurally aligned with 01, but its identity is distinct. Candidate records MUST NOT be relabelled as published Binding/01.

Consumers supporting history MUST select each event's decoder independently: unmarked exact 00 carrier under an explicitly enabled historical profile; exact candidate marker under candidate.1; exact final marker under 01. Unknown markers, both markers together, unmarked typed wrappers, marked legacy carriers, or extra TSTORef members MUST fail closed. A failed final-version check MUST NOT be retried as 00 or candidate. Producers of new Binding/01 events MUST use the final marker, including when appending to an older history.

Signed historical bytes, signatures, hashes, and issued receipts MUST NOT be modified or re-signed. A migration constructs a NEW unsigned event before signing; it does not rewrite history. Mapping a historical D constraint object to a one-element array is allowed only during construction of a new event. Mixed histories MUST retain the original hash for each referenced event and state which version was validated.

## 16. Non-goals

This Binding does not define execution receipts, task orchestration, marketplaces, pricing, settlement, legal authority, liability, remedies, arbitration, or automatic payment. Those systems may rely on conforming events but require separate specifications and policies.

## 17. Release Artifacts and Declared Validation Path

- `schemas/jep-tsto-binding-01.schema.json`: supplementary Draft 2020-12 Schema.
- `tests/upstream/jep-event-0.6.schema.json`: JEP Schema pinned to `hjs-spec/jep-v06@eef317711e0177a64a301bceb1cb6dfd32bf4fc9`.
- `examples/binding-01/`: signed synthetic J/D/T/V vectors, public test key, expected hashes, hostile cases, and canonicalization vector.
- `scripts/check-binding-01.py`: joint structural, RFC 8785, signature, immutable-reference, and termination-resolution checks.
- `releases/binding-01/RELEASE-NOTES.md`: release scope and compatibility evidence.

The supported path applies BOTH Schemas to the SAME signed event, then independent semantic and cryptographic checks. The JEP shipped Schema is an implementation subset of the broader Core prose and minimal conformance seed. Binding/01 deliberately stays within this subset. The Python seed validator alone is not a substitute for the joint path and does not evaluate TSTO semantics or external authority.

Two cryptographic test profiles are declared separately: detached JWS with exact JOSE `alg` `Ed25519` (the upstream JEP baseline), and exact JOSE `alg` `EdDSA` with an Ed25519 key (the Prooftask recorder compatibility profile). Algorithm selection MUST be explicit; changing an algorithm label changes signed bytes. A consumer MUST reject an algorithm outside its selected profile. Public test keys are synthetic and MUST NOT be trusted in production. Passing EdDSA tests does not claim that the upstream Ed25519-only seed accepts them.

The harness tests cryptography and reference integrity under synthetic fixed test trust. It does not establish real actor authority, external evidence truth, full TSTO Policy evaluation, production freshness/replay enforcement, settlement, or real customer validation. These remain required where applicable to the claimed role and deployment profile. A structurally invalid event is rejected, not assigned a TSTO result. An unavailable domain fact can yield `INDETERMINATE` only through the applicable Verification Policy.

## References

- [Judgment Event Protocol, JEP-Core 0.6](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/)
- [JEP Profiles and Interoperability](https://datatracker.ietf.org/doc/draft-wang-jep-profiles/)
- [JEP Conformance and Test Suite](https://datatracker.ietf.org/doc/draft-wang-jep-conformance/)
- [TSTO/00 Target State Transition Object Specification](../SPEC.md)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)
