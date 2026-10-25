# Record and Report 1.1 — limitations supplement

Published 2026-10-25. The immutable [1.0 baseline](../1.0/README.md) remains available.

Record 1.1 and Verification Report 1.1 use distinct schema identifiers and paths. Package, Summary, Status, Accepterms, canonicalization, TSTO/00 and JEP bindings are unchanged. New Record 1.1 issuance requires a visible signed limitations array; absence is invalid, unknown or duplicate codes are rejected. Every declared limitation is preserved in verification output.

- [Record](conformity-record.md) · [Schema](conformity-record.schema.json)
- [Package verification supplement](conformity-package.md)
- [Report Schema](conformity-verification.schema.json) · [Reason catalog](conformity-reasons.json)
- [Synthetic signed vector, public test trust and expected report](vectors/conformity-limitations.json)

The vector contains synthetic data and public test keys only. It establishes no business transaction. It has passed neutral offline verification and malformed/missing-limitations tests in the reference implementation. The W3C official test suite has not been run; that is not claimed.

Private extensions may be noncritical only when dropping them does not change neutral specification, decisions, state or limitations. Product source validation remains distinct from neutral verification; uninterpreted supplementary events must be reported. Never rewrite or re-sign an existing 1.0 record to migrate it.
