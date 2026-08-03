# TSTO/00

## Target State Transition Object Specification

**Status: Experimental Draft 00 (not a formal standard)**  
**Release date: 2026-08-03**  
**Initiator: Cognitive Emergence**  
**License: Creative Commons Attribution 4.0 International (CC BY 4.0)**  
**Language status: This English text is normative. The Chinese text is an informative translation.**

---

## Abstract

TSTO/00 defines an immutable, addressable, and verifiable Target State Transition Object (TSTO). A TSTO states which subject is expected to change, the evidenced baseline from which the change starts, the target state, the applicable time boundaries and constraints, and the policy under which the result is evaluated.

A TSTO does not assign responsibility, prescribe execution, establish a price, move funds, or resolve disputes. Those functions belong to external protocols, bindings, and products. TSTO is the minimum semantic object for stating **what change counts as completion**.

## 1. Status of This Document

This document is Draft 00 for implementation, experimentation, and public review. It may be used as an interoperability basis for prototypes and controlled pilots, but MUST NOT be represented as an industry consensus or formal standard.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

Draft 00 freezes only:

1. the minimum TSTO Core fields and semantics;
2. the minimum predicate language;
3. content canonicalization and digest calculation;
4. constraints on Profiles and Verification Policies; and
5. generic rules by which external systems reference a TSTO.

It does not freeze industry fields, market mechanisms, responsibility-allocation algorithms, or execution workflows.

## 2. Design Goals

Two independent systems referring to the same target change should be able to determine consistently:

- which subject is expected to change;
- the evidenced initial state;
- the required target state;
- when the transition may start, must be achieved, and must be verified;
- which conditions may not be violated;
- which rules and evidence decide the result; and
- whether both systems refer to identical, untampered content.

## 3. Non-goals

TSTO/00 does not define:

- execution steps, workflow orchestration, or agent instructions;
- an identity system for principals, executors, or verifiers;
- authorization, permissions, liability caps, or termination rights;
- pricing, bidding, escrow, clearing, settlement, or tax handling;
- attribution, revenue sharing, insurance, guarantees, or arbitration;
- a network transport, queue, or API invocation mechanism;
- a general-purpose state-machine language; or
- legal contract validity.

These capabilities may reference a TSTO, but MUST NOT be inserted into TSTO Core.

## 4. Terminology

| Term | Definition |
| --- | --- |
| TSTO | An immutable Target State Transition Object. |
| Subject | The object whose state is observed and expected to change. |
| State Projection | The canonical JSON state view defined by a Profile for predicate evaluation. |
| Baseline | An evidence-backed set of claims about the subject's initial state. |
| Target | A machine-evaluable set of claims about the desired terminal state. |
| Constraint | A condition that must hold during transition or at target verification. |
| Evidence | Addressable material, events, receipts, or snapshots supporting a state claim or verification result. |
| Profile | A versioned specification that maps a domain object to a State Projection and constrains fields, types, evidence, and predicate use. |
| Verification Policy | Immutable rules for evidence admissibility, evaluation, time boundaries, and conclusion formation. |
| Resolver | An implementation that retrieves and validates a TSTO, Profile, Policy, or Evidence. |
| Verifier | An implementation or principal that evaluates a TSTO under its Verification Policy. |
| Binding | An independent specification describing how an external responsibility, execution, verification, or settlement protocol references a TSTO. |

## 5. Core Model and Boundary

TSTO Core has nine semantic parts:

| Part | Question answered |
| --- | --- |
| Protocol metadata | Which version and immutable object is this? |
| Profile | How is this domain object and its fields interpreted? |
| Subject | Which object is expected to change? |
| Baseline | From which observed state does the transition start? |
| Target | Which terminal conditions must hold? |
| Validity | Within which time boundaries does the object apply? |
| Constraints | Which conditions must not be violated? |
| Verification | Which rules decide the result? |
| Integrity | Are all parties seeing identical content? |

A TSTO is a static, immutable statement. It has no mutable `status`. Pending, executing, completed, failed, terminated, disputed, and settled states are derived from external responsibility events, receipts, time, verification, and settlement records. They MUST NOT be written back into an issued TSTO.

## 6. Serialization and Media Type

The normative serialization is UTF-8 JSON.

- `spec` is exactly `TSTO/00`.
- `type` is exactly `TargetStateTransition`.
- The proposed experimental media type is `application/tsto+json`. Until registration, Internet implementations SHOULD also accept `application/json`.
- Transport does not affect semantics.
- Implementations MUST reject duplicate JSON member names.
- Unknown top-level Core members render an object non-conforming to Draft 00.

## 7. TSTO Core Object

### 7.1 Top-level members

| Member | Requirement | Meaning |
| --- | --- | --- |
| `spec` | REQUIRED | Specification identifier; exactly `TSTO/00`. |
| `id` | REQUIRED | Globally unique absolute URI for this immutable object. |
| `type` | REQUIRED | Exactly `TargetStateTransition`. |
| `issued_at` | REQUIRED | RFC 3339 time at which the content became immutable. |
| `profile` | REQUIRED | Immutable `id + digest` reference to the domain Profile. |
| `subject` | REQUIRED | Domain subject identifier, type, and optional source version. |
| `baseline` | REQUIRED | Initial claims, observation time, and evidence references. |
| `target` | REQUIRED | Target claims. |
| `validity` | REQUIRED | Achievement and verification time boundaries. |
| `constraints` | REQUIRED | Zero or more interval or target constraints. |
| `verification` | REQUIRED | Immutable Policy reference and optional parameters. |
| `integrity` | REQUIRED | Canonicalization and digest of the TSTO content. |

The complete normative JSON structure is defined by `schemas/tsto-00.schema.json` in this release. The examples distributed with this specification are informative and are not cryptographic test vectors.

### 7.2 `spec`

The value MUST be exactly `TSTO/00`. Other values MUST NOT be interpreted under vague forward-compatibility assumptions.

### 7.3 `id`

`id` MUST be an absolute URI and globally unique within its issuing namespace. A UUID URN conforming to RFC 9562 is RECOMMENDED. If the same `id` resolves to different content digests, an implementation MUST report an identity conflict and refuse automatic replacement.

### 7.4 `type`

The value MUST be exactly `TargetStateTransition`.

### 7.5 `issued_at`

`issued_at` MUST be an RFC 3339 `date-time` and SHOULD use UTC `Z`. It denotes when the object became immutable, not acceptance, authorization, or execution start.

### 7.6 `profile`

`profile` MUST contain an absolute `id` and a TSTO digest. The Profile MUST define the State Projection, path data types, evidence mapping, permitted predicates, and domain verification requirements. It MUST be versioned and immutable under the same `id + digest`, and MUST NOT change Core semantics.

### 7.7 `subject`

`subject.id` MUST be an absolute URI that uniquely identifies the business object within the Profile's scope. `subject.type` MUST be a non-empty Profile-defined string. `subject.version` MAY bind an ETag, ledger height, snapshot, or source version. Identifiers SHOULD avoid embedding direct personal information.

### 7.8 `baseline`

`baseline.observed_at` MUST be RFC 3339 and MUST NOT be later than `issued_at`. `claims` and `evidence` MUST each contain at least one item. Top-level claims are combined by logical AND. Each claim MUST be supportable by at least one evidence item according to the Profile or Policy. Before delegation or execution, consumers SHOULD re-check freshness and conflicts under the Profile.

### 7.9 `target`

`target.claims` MUST contain at least one predicate. Top-level claims are combined by logical AND and MUST be deterministically evaluable against the Profile's State Projection. A Target states the terminal condition, not the method used to reach it.

### 7.10 `validity`

`not_before` is OPTIONAL and defaults to `issued_at`. `achieve_by` and `verify_by` are REQUIRED. Target evidence MUST have an observation time no later than `achieve_by`, and final verification MUST be formed no later than `verify_by`. `sustain_for`, when present, is an RFC 3339 duration for which target and applicable constraints must continue to hold. Profiles and Policies MUST define sampling and continuity rules.

The ordering MUST be:

`issued_at <= not_before <= achieve_by <= verify_by`

with omitted `not_before` treated as `issued_at`.

### 7.11 `constraints`

`constraints` is REQUIRED and MAY be empty. Each constraint has a unique non-empty `id`, a `scope` of `at_target` or `interval`, and a predicate. `interval` spans `not_before` through the end of `sustain_for` or the target observation time. The applicable Profile or Policy MUST specify evidence sampling sufficient to evaluate interval constraints.

### 7.12 `verification`

`verification.policy` is an immutable `id + digest` reference. `parameters` MAY contain values explicitly permitted by that Policy and MUST NOT silently alter its semantics.

A Policy MUST define:

1. acceptable evidence types and source requirements;
2. freshness, time-source, and clock-skew rules;
3. State Projection construction;
4. Target and Constraint evaluation;
5. verifier qualifications, independence, or authoritative sources where applicable;
6. conflicting evidence, revocation, rollback, and reversal handling; and
7. formation and finality of the three-valued result.

A Policy MUST NOT equate an executor's unverified claim of completion with verified satisfaction unless the Profile explicitly permits and discloses that trust model.

### 7.13 `integrity`

Draft 00 permits only `alg = sha-256` and `canonicalization = RFC8785`. `value` has the form `sha-256:<base64url-no-padding>`.

Digest calculation:

1. copy the complete TSTO;
2. remove the top-level `integrity` member;
3. canonicalize the remainder using RFC 8785;
4. SHA-256 hash the resulting UTF-8 bytes; and
5. encode without-padding Base64URL and prefix `sha-256:`.

Signatures are not Core members. An external signed event, evidence object, or signature envelope SHOULD place both `id` and `integrity.value` within its signature coverage or trusted timestamp proof. No undefined string concatenation is implied.

### 7.14 Drafts and issuance

A product MAY store an incomplete target draft, but it is not a TSTO/00 object. An object is an **Issued TSTO** only after all REQUIRED fields are present, structural and semantic validation passes, Baseline evidence is bound and resolvable or authorized, Profile and Policy versions and digests are fixed, and `integrity.value` is correct. Any post-issuance change creates a new TSTO.

## 8. TSTO-Predicate/00

### 8.1 Paths

`path` uses RFC 6901 JSON Pointer against the Profile-defined State Projection. A path MUST NOT be interpreted directly against a private source schema.

### 8.2 Comparison operators

| `op` | Required members | Meaning |
| --- | --- | --- |
| `eq`, `ne` | `path`, `value` | Strict typed equality or inequality. |
| `lt`, `lte`, `gt`, `gte` | `path`, `value` | Ordered comparison. |
| `in` | `path`, `value` | Observed value is a member of the value array. |
| `contains` | `path`, `value` | Observed array contains an element, or string contains a string. |
| `exists` | `path`, Boolean `value` | Whether the path is expected to exist. |

Profiles MUST constrain operators and value types for each path. Monetary and high-precision values SHOULD use integer minor units. Decimal strings require deterministic comparison rules.

### 8.3 Logical operators

- `{ "op": "all", "args": [<predicate>, ...] }`
- `{ "op": "any", "args": [<predicate>, ...] }`
- `{ "op": "not", "arg": <predicate> }`

`all` and `any` arrays MUST NOT be empty. Predicate evaluation MUST NOT execute code, access a network, or produce side effects. External data must first enter a State Projection or Evidence object.

## 9. Evidence Reference

An Evidence Reference has an absolute URI `id`, a Profile- or Policy-defined `kind`, a TSTO digest, and an RFC 3339 `observed_at`. It MAY include `media_type` and an authorized-resolution `location` URI.

Evidence may remain private. Parties may exchange only references and digests and expose the underlying material through controlled access. Resolvability does not imply authorization to read.

## 10. Three-valued Verification

| Result | Required meaning |
| --- | --- |
| `SATISFIED` | All Target predicates are true, no Constraint is violated, time conditions hold, and required evidence and finality are met. |
| `NOT_SATISFIED` | Sufficient evidence proves a Target false, the time window closes without achievement, or a Constraint is violated. |
| `INDETERMINATE` | Evidence is missing, conflicting, inaccessible, unverifiable, or the Policy cannot reach a determinate result. |

`INDETERMINATE` MUST NOT be coerced to `NOT_SATISFIED` unless the Policy explicitly makes failure to submit specified evidence by a deadline a negative condition. Termination and payment are external state facts, not TSTO verification results.

## 11. Immutability, Revision, and Composition

- An issued TSTO MUST be immutable.
- Changing Subject, Baseline, Target, Validity, Constraints, Profile, or Policy requires a new `id` and digest.
- Relationships such as `supersedes`, `derived_from`, and `part_of` belong to an outer registry or event system.
- A Draft 00 TSTO MUST have exactly one Subject.
- Multi-subject, staged, optional, or composite outcomes SHOULD be decomposed into atomic TSTOs and organized externally.
- Partial completion is not a Core result; independently priced milestones require independent TSTOs.

## 12. External Protocols and Bindings

An external event, task, or transaction referencing a TSTO MUST bind all of `type`, `spec`, `id`, and digest. It MUST NOT modify Core semantics, bind only the `id`, write responsibility or settlement state back into the TSTO, or confuse a preselected Verification Policy with an actual verification event.

If the external protocol signs the reference, both TSTO `id` and digest MUST lie within signature coverage. Signing only an identifier, mutable location, or digest of unspecified encoding does not bind specific TSTO content.

Responsibility, execution, verification, and settlement may use separate Bindings. Implementing one does not require the others. The companion `JEP-TSTO Binding/00` defines one such independent event binding.

## 13. Profile Conformance

A Profile MUST publish:

1. a versioned Profile identifier and content digest;
2. Subject types and identifier rules;
3. a JSON Schema for its State Projection;
4. types, units, and enumerations for paths;
5. deterministic source-to-projection mappings;
6. permitted predicate operators;
7. Baseline evidence and freshness rules;
8. Target evidence and finality rules;
9. privacy, confidential-data, and access-control rules; and
10. at least one valid, one invalid, and one `INDETERMINATE` example.

The narrow waist should be considered stable only after at least three materially different Profiles operate without Core changes. Suggested pilots are `commerce.order-recovery.v1`, `ar.invoice-settlement.v1`, and `freight.claim-paid.v1`.

## 14. Conformance Classes

| Class | Requirements |
| --- | --- |
| TSTO Producer | Pass structural and semantic validation and calculate the correct digest. |
| TSTO Resolver | Resolve by `id + digest`, detect conflicts, and validate the object, Profile, and Policy. |
| TSTO Verifier | Produce a deterministic State Projection, execute the Policy, and output a three-valued result with evidence references. |
| TSTO Binding | Bind `type`, `spec`, `id`, and digest without altering Core semantics. |

An implementation claiming TSTO/00 conformance MUST state its conformance classes and Profiles.

## 15. Security and Privacy Considerations

Implementations must address content substitution, stale baselines, replay, clock divergence, verifier collusion, selective disclosure, identifier leakage, state reversal, resource-exhaustion during resolution and predicate evaluation, and unknown semantics. Unknown Core members or operators and unavailable Profiles or Policies require rejection or `INDETERMINATE`, not guessed interpretation.

A content digest proves content consistency only. It does not prove issuer identity, factual truth, authorization, or legal effect.

## 16. Interoperability and Advancement Criteria

Before Draft 01, this work should demonstrate three domain Profiles without Core changes, two independent interoperable Producer/Resolver implementations, identical digest and predicate outputs for shared vectors, at least one independent end-to-end Binding, cases covering conflict, timeout, termination, rollback and `INDETERMINATE`, and a concrete external interoperability demand.

## 17. Naming Resolution

The publication name is `TSTO/00`; the English expansion is **Target State Transition Object Specification**; the object acronym is **TSTO**; and the JSON type is `TargetStateTransition`.

`TST` alone is avoided because RFC 3161 uses it for `TimeStampToken` and RFC 2756 uses a `TST` operation. The `O` identifies this construct as an object rather than a transport or execution protocol. Naming review does not replace trademark, domain, or standards-registry review.

## 18. Draft 00 Resolutions

| Question | Resolution |
| --- | --- |
| Is the TSTO itself traded? | No. A commitment, responsibility, or service producing the change may be traded; TSTO is the referenced target object. |
| Does TSTO contain execution steps? | No. |
| Does it name a responsible party? | No; an external protocol or Binding does. |
| Does it contain price and settlement? | No. |
| Is an incomplete target draft a TSTO? | No. |
| Is a TSTO mutable? | No; a change creates a new object. |
| Is completion binary? | No; verification is three-valued. |
| Where do domain differences live? | Profiles and Verification Policies. |

# Appendix A: Normative JSON Schema

The normative Draft 2020-12 Schema is distributed as [`schemas/tsto-00.schema.json`](schemas/tsto-00.schema.json). Passing the Schema does not establish semantic conformance; time ordering, digest correctness, Profile constraints, predicate typing, and evidence-policy rules require semantic validation.

# Appendix B: Open Questions

Draft 01 should be informed by implementations addressing discovery, caching, and revocation of Profiles and Policies; minimum sampling for sustained states; multiple verifiers and conflicting results; selective disclosure and confidential computation; non-destructive correction after state reversal; multi-TSTO composition and atomic settlement; and governance of registries and test vectors.

# Appendix C: Relationship to JEP (Informative)

TSTO/00 has no dependency on JEP. JEP-Core 0.6 records signed claims of Judgment, Delegation, Termination, or Verification around a referenced object; it does not itself establish external truth, authorization validity, legal liability, or enforceability. TSTO states what change counts as completion.

TSTO's `verification.policy` is a preselected domain-fact evaluation rule. A JEP Verification is a signed event stating that a verification occurred. A JEP Trust Profile binds event actors and signing keys. These layers MUST remain separate. A TSTO Profile and a JEP Profile are also distinct specifications despite the shared word “Profile.”

TSTO uses `sha-256:<base64url-no-padding>` for TSTO content. JEP-Core 0.6 uses `sha256:<lowercase-hex>` for a JEP event hash. A Binding MUST preserve and label both encodings and MUST NOT compare them as strings or present one as the other.

Complete event shapes, result mappings, signature-coverage rules, and examples are defined in the independent `JEP-TSTO Binding/00` shipped with this release.

# References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339)
- [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986)
- [RFC 6901](https://www.rfc-editor.org/rfc/rfc6901)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)
- [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
- [Judgment Event Protocol, JEP-Core 0.6](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/)
- [JEP Profiles and Interoperability](https://datatracker.ietf.org/doc/draft-wang-jep-profiles/)
- [JEP Conformance and Test Suite](https://datatracker.ietf.org/doc/draft-wang-jep-conformance/)
