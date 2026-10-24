# Conformity 1.0 Amendment 1: reliance limitations

Status: additive amendment to Conformity Record 1.0, Package 1.0 and
Verification Report 1.0. It does not change any published 1.0 schema, context,
vector or reason identifier. Records issued before this amendment remain valid
and verify exactly as before.

## Purpose

A Record states what was judged, not that the judged facts are true. Before this
amendment the limits of reliance (no independent verification, no payment
verification, declared authority, no financial reliance) could only be carried
in an issuer's private extensions. A neutral verifier that did not understand
those extensions either rejected the Record or reported fewer limits than the
issuer intended. This amendment moves those limits into the neutral layer.

## The `org.humanjudgment.limitations` extension

- Location: the Record's top-level `extensions` object (path `/`).
- Value: a non-empty array of unique codes from `conformity-limitations.json`,
  sorted in ascending code-point order.
- It MUST be listed in the top-level `critical` array. A verifier conforming to
  this amendment supports it; a verifier that does not cannot rely on the Record.
- It MUST NOT be concealed. The SD-JWT encoding keeps its value visible in every
  presentation, including partial presentations, so that hiding content can
  never hide a limitation. A critical declaration whose value is not visible
  fails with `LIMITATIONS_CONCEALED`; an invalid value fails with
  `INVALID_LIMITATIONS`.
- An issuer declares every limitation that applies. When uncertain, it declares
  the limitation. A missing code is not a positive assurance unless the issuer's
  published profile says so.

## Verifier behaviour

A conforming verifier appends the declared codes, in their declared order, to
the report `reasons` of a full Package verification and of a partial
presentation verification, immediately after `ACTOR_ATTRIBUTION_RECORDER_ASSERTION`.
The report status remains `VERIFIED_WITH_LIMITATIONS` or `PARTIAL_DISCLOSURE`.

A Record without the extension is reported exactly as before this amendment.
Its absence means only that the issuer made no neutral declaration; a relying
party must not infer that no limitation applies.

## Issuer extensions

Issuer-specific (`com.*`, `net.*` and similar) extensions SHOULD be noncritical.
A critical private extension makes every independent verifier reject the Record,
including partial presentations, because critical names are always visible.
Semantics that change reliance belong in this neutral extension instead.

## Codes

| Code | Meaning |
|---|---|
| FINANCIAL_RELIANCE_NOT_ESTABLISHED | Not represented as a basis for payment, financing or other financial reliance |
| INDEPENDENT_VERIFICATION_NOT_PERFORMED | No third party independently verified every agreed criterion |
| LEGAL_LIABILITY_NOT_ASSERTED | Does not determine liability, enforceability or contract consequences |
| ORGANIZATION_AUTHORITY_NOT_INDEPENDENTLY_VERIFIED | At least one actor's authority is declared or attested only |
| ORIGINAL_FILES_NOT_RETAINED_BY_ISSUER | The issuer keeps fingerprints, not originals |
| PAYMENT_NOT_VERIFIED | Payment or settlement is not verified |
| RECORDED_PARTY_STATEMENTS_ONLY | Facts are party statements, not issuer observations |

The code list is closed for this amendment. A later amendment may add codes;
it never renames or reuses one.
