# JEP-TSTO Binding/02

First executable experimental publication for **TSTO/00 + JEP Core 0.7**. English is normative. This is not a formal standard or a production domain-policy engine.

## Interoperability decisions

- One signed marker: `ext["jep-tsto.binding"] = {"version":"02","spec":"JEP-TSTO-Binding/02"}`.
- J/D/V use `ref.type = "tsto:target-state-transition"` around the exact five-member TSTO reference.
- T uses `jep:event` with target `(who,id)`, optional exact-artifact hash and a matching TSTO subject. It has no duplicate `what.target`.
- V retains separate scope/result, immutable policy/evidence references and all three TSTO outcomes.
- JEP acceptance is idempotent by Event Identity and unsigned payload. Binding checks precede application acceptance; duplicate delivery does not invalidate a signature.

Two open implementation proposals (#5 and #6) used incompatible markers/carriers. This publication completes the format already recorded on main at `f44a8f2267024424a042700bc31690663585c349`; those proposals are superseded. No unpublished candidate is silently accepted under the released marker.

## Reproduce

Follow the commands in [README](../../README.md). Dependencies are in `scripts/requirements-binding-02.txt`. The upstream Core schema and validator are pinned by commit and SHA-256 in `tests/upstream/jep-core-0.7.json`; the harness refuses mismatched copies. The Core validator is reused from its checkout, not forked into this repository.

The checked-in [report](validation-report.json) covers 10 signed valid events, 30 hostile signed/tampered cases, 6 invalid JSON inputs, 4 rejected historical events and 3 TSTO integrity/semantic failures. Additional assertions cover a re-signed target with/without an artifact pin, duplicate delivery, identity conflict and preservation of acceptance state after rejection.

The external Profile, Policy and Evidence references are illustrative. The harness checks policy-reference equality, not policy execution or real evidence truth. Unresolved termination targets remain indeterminate; `INDETERMINATE` verification claims remain distinct from failure. Test keys MUST NOT be trusted in production.

## Migration and preservation

Binding/00 and Binding/01 retain their original specifications, schemas, translations, PDFs, examples, signatures and checksums. Binding/01's published joint-schema fix remains the historical resolution of the Binding/00 carrier problem reported in Issue #2.

Select each decoder from explicit known context and its signed marker. A failure must not trigger fallback. Migration creates a new Core 0.7 event identity and signature; it does not rewrite or re-sign the old event in place. Core wire `"1"` alone does not select a binding. Existing products such as Prooftask require their own explicit migration and deployment; this release does not claim they are upgraded.

The release ZIP contains the specification, schemas, pinned-source metadata, fixtures, harness, report and license. `SHA256SUMS.txt` verifies the listed source files inside that ZIP. The release workflow preserves an existing tag/release and never overwrites its assets. New normative changes after this publication require a new revision.
