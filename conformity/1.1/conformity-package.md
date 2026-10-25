# Conformity Package 1.0

## Unsigned carrier and signed commitments

A Package is an unsigned file manifest conforming to
conformity-package.schema.json. Each file has a relative path, media type and
SHA-256 over its exact bytes. JSON delivery uses unpadded base64url `data` with
`encoding: base64url`. Paths are unique and cannot contain empty, parent or
current-directory segments, backslashes or absolute-path prefixes.

`record.sd-jwt` contains the original issuer-signed SD-JWT and all disclosures.
There is no outer Package JWS. Inside the signed JWT, `commitments` is always
visible and includes the TSTO file commitment, the complete ordered list of JEP
file commitments, and the attachment-manifest commitment. Each commitment binds
the path, media type and exact-byte SHA-256. The signed attachment manifest in
turn commits the attachment files. The full TSTO and JEP bytes are preserved.

Verification authenticates the SD-JWT first, using independently trusted issuer
keys. It then checks every committed file, including the attachment manifest
and each attachment. A missing file, replacement or media/digest mismatch yields
`PACKAGE_CONTENT_MISMATCH`. An extra file not reached from these signed
commitments is reported as `UNCOMMITTED_FILE` and excluded from conclusions.
An uncommitted extra file cannot supply evidence or replace a committed file.

Full verification also checks TSTO integrity, its specification binding, JEP
references and original detached signatures, actor attribution, ordered history
and complete criterion coverage. Actor attribution remains a recorder assertion.

## Partial presentation

A partial presentation is only the same original issuer-signed JWT and chosen
RFC 9901 disclosures. It is not a new artifact format and is not an unsigned
Package with some files removed. It never includes TSTO or JEP event content.
The visible signed file commitments remain unchanged, allowing a recipient to
compare with a later full Package.

The verifier reports `PARTIAL_DISCLOSURE`, disclosed/total counts, and
`JEP_ORIGIN_EVIDENCE_NOT_INCLUDED`. It may establish that the issuer signed the
disclosed claims; it cannot establish full closure or independent evidence of
who initiated the original JEP judgments. If TSTO or JEP material is included,
it rejects with `PARTIAL_PRESENTATION_LEAKS_COMMITTED_CONTENT`.

A future TSTO that references criteria only by digest would avoid this plaintext
disclosure boundary. Such a change requires approval by the TSTO specification
owner and is outside this version. TSTO/00 is not modified here.

## Neutral supplementary-event handling

For supplemented records with signed limitations, a neutral reader MAY authenticate
unbound supplementary JEP events without a product source policy. It MUST report
JEP_AUXILIARY_NOT_INTERPRETED, verify each event signature and TSTO reference, and
MUST NOT use these events to change neutral acceptance state or establish product
workflow validity. Bound neutral objects cannot be skipped through this path.
Product readers continue replaying every source operation with their source policy.
