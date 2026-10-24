## 2026-10-24 — Conformity 1.0 and Amendment 1

- Published the Conformity 1.0 specification set (Record, Package, Summary, Status, Verification Report, canonical JSON, issuer discovery, Accepterms 2027, reason catalog and test vectors) under `conformity/`, byte-identical to the reference implementation.
- Added Amendment 1: issuer-declared reliance limitations in an always-visible, critical `org.humanjudgment.limitations` extension, with its closed code list and vectors. Earlier records verify unchanged.
- Recommended that issuer-private extensions be noncritical so independent verifiers are not forced to reject records.
- No change to TSTO/00, any Binding, published releases, signatures or harnesses.

## 2026-09-26 — Current implementation follow-up

- Separate original Binding/02 release reproduction from current Core/SDK/API interoperability checks.
- Link the current gate covering signature/hash preservation across client serializers, including large JCS numbers and explicit empty members.
- Allow the repository README, changelog and CI entry point to evolve while retaining the original release manifest and every frozen normative/test artifact byte-for-byte.
- No Binding revision, new release, signature rewrite or change to the published harness/report.

## 2026-09-26 — JEP-TSTO Binding/02

- Completed the first executable Binding/02 publication for JEP Core 0.7.
- Unified the main-branch marker/carrier; superseded conflicting unpublished PRs #5 and #6.
- Added the supplementary Schema, pinned upstream validator checks, signed/hostile fixtures, CI and immutable release bundle.
- Made target identity/hash/subject checks, policy-reference equality and acceptance ordering explicit.
- Reduced the README to current entry points, reproduction and the version matrix.
- Semantic JEP event targets now use Event Identity `(who,id)`; Event Hash is optional exact-artifact pinning.
- Removed any Binding-level assumption that Core requires nonce-based replay handling.
- Aligned D/T/V with JEP Core 0.7 verb-specific `what` requirements.
- Preserved Binding/01 unchanged for historical JEP Core 0.6 verification.

# Binding/01

- Publish independent Experimental Binding Draft 01; TSTO/00 and JEP-Core meanings remain unchanged.
- Align typed references, delegation arrays, termination target equality and a signed version identifier with the pinned JEP Schema.
- Add English/Chinese text, PDFs, signed and hostile vectors, joint validation and historical migration rules.
- Preserve all original 00 normative artifacts and vectors.

# Changelog

## TSTO/00 — 2026-08-03

Initial complete experimental publication.

- Defined the immutable TSTO Core object and TSTO-Predicate/00.
- Defined Evidence Reference and three-valued verification semantics.
- Defined Profile, Verification Policy, RFC 8785 canonicalization, and SHA-256 integrity requirements.
- Defined external Binding boundaries and signature-coverage requirements.
- Published the independent JEP-TSTO Binding/00 for JEP-Core 0.6.
- Added structural Schemas and J/D/T/V examples.
- Added normative English texts, informative Chinese translations, and bilingual PDFs.
- Adopted CC BY 4.0 publication licensing.

