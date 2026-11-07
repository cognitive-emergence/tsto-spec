# Post-Action Interoperability Validation Plan

## Status

Experimental validation note for TSTO/00. This document does not modify TSTO Core and does not claim that TSTO is an industry standard or uniquely necessary.

## Research question

When an action has already been identified, authorized, and executed, do independent systems still need a reusable semantic object to determine whether an immutable pre-agreed target state was actually satisfied under fixed evidence and verification rules?

TSTO/00 is a candidate answer to that question. The purpose of this plan is to falsify or narrow the hypothesis before making stronger claims.

## Strongest-baseline rule

TSTO MUST be compared against the strongest reasonable composition of existing systems, including as applicable:

- identity and credentials;
- OAuth/OIDC and fine-grained authorization;
- AuthZEN/COAZ-style policy decisions;
- AP2-style mandates and checkout/payment receipts;
- A2A/MCP task and tool lifecycle records;
- UCP-style order expectations and fulfillment events;
- OpenTelemetry-style traces and events;
- in-toto-style attestations and verification summaries;
- SCITT-style signed-statement transparency receipts;
- domain-native workflow, database, order, billing, delivery, and compliance state.

The hypothesis is not supported merely because one of these mechanisms is insufficient by itself.

## Candidate residual semantic

The candidate residual is deliberately narrow:

1. an immutable reference to what terminal state counts as completion;
2. time boundaries and constraints that cannot be silently rewritten after execution;
3. a fixed verification policy defining admissible evidence and conclusion formation;
4. retained evidence references;
5. an independently reproducible three-valued result: `SATISFIED`, `NOT_SATISFIED`, or `INDETERMINATE`.

Identity, authorization, execution, payment, liability, transport, and cryptographic envelope mechanisms remain external.

## Materially different profiles

The narrow-waist hypothesis is not considered structurally plausible until at least three materially different domain Profiles operate without changes to TSTO Core.

Initial validation domains:

- agent commerce: authorized purchase plus post-purchase delivery/constraint outcome;
- regulatory readiness: evidence-backed organizational readiness under a fixed policy;
- software/service terminal state: successful API/task execution compared with authoritative later state.

These domains are intentionally different in actors, evidence sources, state models, and downstream consequences.

## Required hostile vectors

Every profile SHOULD include at least:

- valid authorization + successful execution + `NOT_SATISFIED` outcome;
- operation/task success + contradictory authoritative terminal state;
- executor self-claim where policy requires independent evidence;
- missing evidence -> `INDETERMINATE`;
- conflicting admissible evidence -> `INDETERMINATE`;
- post-hoc target rewrite attempt;
- verification-policy substitution attempt;
- late observation after achievement deadline;
- terminal target true but constraint violated;
- later reversal or rollback;
- baseline-equivalence attack attempting to reproduce the same conclusion without TSTO semantics.

## Kill conditions

The independent semantic-layer hypothesis SHOULD be rejected or narrowed if any of the following is demonstrated:

1. a strong baseline already provides the same cross-domain, pre-agreed, independently recomputable outcome semantics without recreating equivalent target-state and verification-policy semantics;
2. materially different domains require incompatible TSTO Core changes rather than Profile-level specialization;
3. independent conforming verifiers given the same retained inputs repeatedly disagree because Core semantics are underspecified;
4. a derived completion result adds no portable information beyond domain-native receipts;
5. downstream systems must reconstruct the entire original workflow to use the result;
6. coordination cost introduced by the semantic layer exceeds the verification/interpretation cost it removes.

## Evidence gates

Claims should strengthen only after corresponding evidence exists.

### Gate 1 — Cross-domain structural plausibility

At least three materially different Profiles operate with unchanged TSTO Core.

### Gate 2 — Independent deterministic replay

At least two independent verifier implementations given the same TSTO/Profile/Policy/evidence set produce equivalent normalized results.

### Gate 3 — Baseline differentiation

At least two materially different domains demonstrate a meaningful distinction between valid authorization / successful operation / successful transaction and verified target-state satisfaction.

### Gate 4 — Portable downstream utility

The same derived completion result is consumed by at least two downstream classes, such as settlement and audit, without requiring them to reinterpret the original workflow logs.

### Gate 5 — External reproducibility

An external implementer can reproduce the result from public specifications and vectors without private interpretive guidance.

## Integration posture

TSTO should prefer reuse over replacement.

Examples:

- authorization systems can be referenced as upstream context;
- A2A/MCP and domain systems can supply execution evidence;
- UCP can supply commerce-domain state and fulfillment evidence;
- OpenTelemetry can supply observability evidence;
- in-toto/VC-like mechanisms can carry signed evidence or result statements;
- SCITT can provide transparency/retention receipts;
- payment systems can consume, but are not defined by, a completion result.

If an existing public standard already supplies the complete residual semantics more cleanly, TSTO should profile or reuse that standard rather than duplicate it.

## Public claim discipline

Before the evidence gates are passed, use language such as:

- experimental target-state semantics;
- candidate reusable post-action outcome model;
- interoperability hypothesis under test.

Do not describe TSTO as a universal missing layer, an industry consensus, or the only possible solution based solely on internal validation.

## References

- TSTO/00: `../SPEC.md`
- JEP-TSTO Binding/00: `../bindings/JEP-TSTO-Binding-00.md`
- OpenID AuthZEN / COAZ: https://openid.net/getting-cozy-with-coaz-securing-apis-and-ai-agents-with-standardized-authorization/
- AP2: https://ap2-protocol.org/
- UCP: https://ucp.dev/specification/order/
- A2A: https://a2a-protocol.org/specification/
- in-toto Attestation: https://github.com/in-toto/attestation
- SCITT: https://datatracker.ietf.org/wg/scitt/documents/
- NIST AI Agent Standards Initiative: https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative
