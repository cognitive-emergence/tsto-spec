# Conformity 1.2

Published 2026-11-22. The immutable [1.0 baseline](../1.0/README.md) and the
[1.1 limitations supplement](../1.1/README.md) remain available and unchanged.

Conformity 1.2 adds new identifiers at new paths. It changes no earlier file, no
earlier identifier and no earlier verdict. TSTO/00, JEP Core and the JEP-TSTO
bindings are unchanged.

| Document | Identifier | Content |
|---|---|---|
| [Record 1.2](conformity-record-1.2.md) · [Schema](conformity-record-1.2.schema.json) | `https://humanjudgment.org/ns/conformity-record/1.2` | Record 1.1 plus the delegation scope `VERIFY` for delegated technical evaluations |
| [Verification 1.2](conformity-verification-1.2.md) · [Report Schema](conformity-verification-1.2.schema.json) | `https://humanjudgment.org/ns/conformity-verification/1.2` | Report 1.2, the normative verification procedure, and the reason catalog |
| [Reason catalog 1.2](conformity-reasons-1.2.json) | `https://humanjudgment.org/ns/conformity-verification/1.2#reasons` | The current catalog: registers `ACCEPTANCE_NOT_CONFORM`, `UNKNOWN_UNNAMESPACED_EVENT` and `JEP_ORIGIN_EVIDENCE_NOT_INCLUDED` |
| [Package supplement 1.2](conformity-package-1.2.md) · [Evidence index Schema](conformity-anchors.schema.json) | `https://humanjudgment.org/ns/conformity-anchors/1.0` (evidence index) | Anchoring evidence in a Package (RFC 3161, OpenTimestamps, Bitcoin headers) and keys revoked after signing |

The [Conformity 1 conformance suite](../conformance/conformity-1/README.md)
contains signed vectors for Records 1.0, 1.1 and 1.2 and a runner for any
verifier command.

## Compatibility

- A verifier validates each record against the schema of the version it
  declares. A Record 1.1 that uses scope `VERIFY` stays invalid.
- Records 1.0 and 1.1 keep their verdicts and their report identifiers; only
  Record 1.2 is reported with Report 1.2. For two rules that earlier verifiers
  reported as `INVALID_CONFORMITY_INPUT` the reason is now the registered code;
  the verdict stays `INVALID`.
- An issuer that never records a delegated evaluation may keep issuing Record
  1.1. Never re-sign or rewrite an existing record to migrate it.

## File names

The files keep the names under which an issuer serves them (for example
`https://prooftask.com/.well-known/humanjudgment/conformity-record-1.2.md`), so
each can be compared byte for byte with [SHA256SUMS.txt](SHA256SUMS.txt). In
these texts, `conformity-record-1.1.md` and `conformity-package-1.1.md` name the
1.1 texts published here as [1.1/conformity-record.md](../1.1/conformity-record.md)
and [1.1/conformity-package.md](../1.1/conformity-package.md), and
`conformity-package.md` the 1.0 text in [1.0](../1.0/conformity-package.md).

The reason catalog and report schema of 1.1 published here on 2026-10-25 predate
later pre-release edits by the issuer: product-specific codes were removed and
the anchoring, revoked-key and `RETIRED_FORMAT` codes and the `INDETERMINATE`
status were added. The 1.2 catalog and Report 1.2 schema are the current state;
use them for reports.

The vectors contain synthetic data and public test keys only. These are
experimental specifications, not a claim of formal standards-body approval.
