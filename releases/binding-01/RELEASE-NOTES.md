# JEP-TSTO Binding/01

**Experimental Binding Draft 01. Not a formal standard.** English is normative; Chinese is informative. TSTO stays at 00; JEP-Core stays at 0.6 with wire value `1`.

Binding/00's reference and claim carriers did not pass the shipped JEP event Schema. This release corrects that interoperability failure and gives final 01 events an explicit signed version identity.

- J/D/V use a typed wrapper around the unchanged exact five-member TSTORef.
- D constraints are an array of objects interpreted conjunctively.
- T includes `what.target`, equal to its JEP event-hash `ref`; `what.subject` identifies the affected TSTO.
- `ext["jep-tsto.binding"].id` identifies the versioned published Schema. The historical Prooftask candidate retains its separate signed marker.
- English/Chinese specifications and PDFs, the Schema, signed vectors, hostile vectors, canonicalization evidence and a runnable joint validation path are included.

All original Binding/00 and TSTO/00 normative text, Schema, examples and PDFs remain byte-for-byte unchanged. Compatibility decoding does not relabel or rewrite signed history. New events require the new marker; unknown versions and mixed carriers fail closed.

## Verification evidence

- 8 signed J/D/T/V vectors passed both Schemas, RFC 8785, signatures under synthetic actor/key trust, and exact object resolution.
- 15 hostile cases were rejected, including correctly signed wrong references, marker conflicts, digest-domain confusion, wrong T targets and wrong policy references.
- 4 original unsigned 00 examples reproduce the prior JEP Schema incompatibilities.
- 4 `Ed25519` baseline events also passed the unchanged upstream Python seed. The `EdDSA` recorder profile is tested separately and is not claimed to pass that seed.
- The Prooftask migration was locally verified with 188 passing tests, type/syntax checks and its joint-schema gate. Frozen 00 and candidate signatures/hashes and mixed 00/candidate/01 online/standalone proof verification passed. Source merge and production deployment are tracked separately in tsto-spec Issue #3.

Reproduce with `python scripts/check-binding-01.py`; use `--jep-seed PATH` to include the pinned upstream Python seed. Dependencies are in `scripts/requirements-binding-01.txt`. Expected machine-readable results are in `validation-report.json`.

This release tests the declared structural, cryptographic and reference path. It does not establish external evidence truth, real actor authority, complete domain-policy evaluation, production replay protection, legal effect, payment validity, or completion of a real customer transaction.

## Pinned dependencies

- JEP Schema and baseline seed: `hjs-spec/jep-v06@eef317711e0177a64a301bceb1cb6dfd32bf4fc9`.
- Original TSTO/00 and Binding/00: `cognitive-emergence/tsto-spec@c5a0de4f0e00835ee9355c9959d976f501c4f0c1`.
- Prooftask migration base: `cognitive-emergence/prooftask@8f34924030f1c73f4e2e8e5b898e6920e8ae56ab`.

CC BY 4.0 applies to the Binding publication. Public test keys and test seeds MUST NOT be used in production. This publication does not assign a new DOI or claim IETF submission of Binding/01.
