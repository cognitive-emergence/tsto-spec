# Conformity 1 conformance suite

Published 2026-11-22 with [Conformity 1.2](../../1.2/README.md). Informative test material, not a normative text.

Language-neutral test vectors for verifiers of Conformity 1.0, 1.1 and 1.2 records: complete Packages, partial
SD-JWT presentations, Status statements and Summaries. The 95 cases cover valid records, every rejection rule the
suite names, ACTIVE/RETIRED/REVOKED key windows, tampered disclosures, records issued by the ProofTask runtime, and
the Conformity 1.2 additions (delegation scope `VERIFY`, the three newly registered reasons, each record validated
under its own version).

- `suite.json`: the case list. Each case names its `artifact`, `trust` and `options` files and its `expected`
  report members and exit status. `profiles.prooftask` overrides `expected` for the ProofTask reference verifier.
- `cases/<id>/`: the input files.
- `run.py`: runs any verifier command against the suite (Python 3.9 or later, standard library only).
- `SHA256SUMS.txt`: the digest of every file in this directory as published.

Suite identifier (the `suite` member of `suite.json`):
`https://github.com/cognitive-emergence/tsto-spec/tree/main/conformity/conformance/conformity-1`.

Licensing: code files here (`run.py`) are licensed under the Apache License 2.0 (SPDX `Apache-2.0`, stated in each
file). The vectors, `suite.json` and this text are covered by the repository licence, CC BY 4.0, like the
specification texts.

## Run it

Your verifier is a command that takes three file paths, `ARTIFACT TRUST OPTIONS.json`, prints one JSON verification
report on standard output, and exits 0 for `VERIFIED_WITH_LIMITATIONS` and `PARTIAL_DISCLOSURE`, 1 for `INVALID`
and 3 for `INDETERMINATE`.

```sh
python3 conformity/conformance/conformity-1/run.py -- your-verifier
python3 conformity/conformance/conformity-1/run.py --only package-1.2-delegated-evaluation,record-1.1-verify-delegation -- your-verifier
python3 conformity/conformance/conformity-1/run.py --profile prooftask -- node verify-conformity.mjs
```

The last line runs the JavaScript reference verifier, which you can download from
<https://prooftask.com/developers/verify-conformity.mjs> (Node.js 24, no network).

The runner compares `status`, `closure`, `disclosures`, `issuer`, `limitations`, `currentStatus`, `currentState`
and the exit status exactly, and `reasons` and `ignoredFiles` as sets. A member the case does not expect must be
absent.

## What to read

- The normative verification procedure: [Conformity Verification 1.2](../../1.2/conformity-verification-1.2.md).
  A report for an invalid artifact carries exactly one reason, the first rule that failed in that procedure's order.
- The implementer guide, with the verifier contract and how to read the results:
  <https://prooftask.com/developers/conformity-verifier.md>.

## Scope and provenance

`expected` is the result of a neutral verifier: no product-specific extension handlers and no product source policy.
A ProofTask record read this way reports `JEP_AUXILIARY_NOT_INTERPRETED`; the ProofTask profile replays those
workflow events instead and names retired ProofTask formats `RETIRED_FORMAT`.

Not covered: anchoring evidence (`evidence/` in a Package, package supplement 1.2), the rule for keys revoked after
signing that depends on it, party-signature anchors and ProofTask participant keys.

Every vector was produced by real issuance code, never written by hand. Each rejection case changes exactly one thing
in an issued artifact; where that needs a new issuer signature it is re-signed with the suite's own key, as an issuer
that made the mistake would. Every expectation was checked against the reference verifier, and an independent
verifier written only from the specification passes the whole suite. Salts and identifiers are random, so a later
regeneration changes bytes but not the case list or the expected results. The keys are synthetic test keys derived
from published seeds: never trust them for anything else. All names and addresses are fictitious.
