# Conformity Package 1.0, supplements 1.1 and 1.2

This is the complete 1.0 text with the 1.1 and 1.2 supplements appended. The
published conformity-package.md beside it is the byte-locked 1.0 snapshot, and
conformity-package-1.1.md is the 1.1 text; namespace identifiers remain 1.0.
Supplement 1.2 applies to records with schema conformity-record/1.1 only.

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

## Supplement 1.2: anchoring evidence

### Anchored subject

The anchored digest of a record is SHA-256, as lowercase hex, of the ASCII
issuer-signed JWT: the part of `record.sd-jwt` before the first `~`. It binds
every disclosure digest, so it is the same for the full Package and for any
partial presentation, and any recipient recomputes it from the Package alone.

### Package layout

An issuer MAY add anchoring evidence under `evidence/`. The files are not
signed commitments; each authenticates itself against the record:

- `evidence/anchors.json`: an index conforming to
  conformity-anchors.schema.json (`https://humanjudgment.org/ns/conformity-anchors/1.0`)
  naming the anchored subject and the evidence items.
- `evidence/rfc3161/<n>.tst`: a DER RFC 3161 TimeStampToken whose SHA-256
  message imprint is the anchored digest.
- `evidence/ltv/<n>.pem`: optional long-term validation material for a token:
  certificates and CRLs current when the token was obtained.
- `evidence/rfc3161/<n>-r<k>.tst` and `evidence/ltv/<n>-r<k>.pem`: optional
  renewals of token `<n>`, listed in order in its index item (`renewals`). Each
  renewal is an RFC 3161 token whose SHA-256 message imprint is SHA-256 of the
  previous token's DER bytes, obtained before that token's certificates expire.
- Party-signature tokens: an `rfc3161` item MAY name a `target`
  (`{kind: "party-signature", alg: "sha-256", digest}`), the SHA-256 of a signed
  original that a party produced (for example a holder-signed confirmation). Its
  token stamps that digest, not the anchored digest of the record. Such items may
  appear in a Package for a record that is not issued.
- `evidence/ots/<n>.ots`: a detached OpenTimestamps proof for the anchored digest.
- `evidence/bitcoin/<n>.headers`: optional concatenated 80-byte Bitcoin block
  headers starting at the declared `fromHeight`, linking the attested block to a
  checkpoint the verifier holds.

A file under `evidence/` that the index does not name is reported as
`UNCOMMITTED_FILE`. Re-downloading a Package may add or upgrade evidence; the
record and its signature never change.

### Verification

The verifier checks the evidence with trust it holds independently of the
Package: approved RFC 3161 roots and Bitcoin checkpoints are bundled with the
reference verifier, and a relying party may supply its own instead. Nothing in a
Package adds trust.

- Trusted time: the token must carry the anchored digest, a valid CMS signature
  by a signer whose certificate has a critical, timeStamping-only extended key
  usage and whose ESS signing-certificate reference names it, and a chain to an
  approved root through CA certificates with keyCertSign, each certificate valid
  at genTime. A CRL is authentic when signed by the certificate's issuer, which
  must hold cRLSign; CRLs with an unknown critical extension, or in an
  unsupported algorithm, are ignored. A certificate listed by any authentic CRL
  is rejected. Revocation is `CHECKED` only when every chain certificate is
  covered by an authentic, complete CRL (no IssuingDistributionPoint, no delta
  indicator, no critical entry extension) whose thisUpdate is at least 24 hours
  after genTime and before the certificate expires. A CRL current at genTime is
  not enough: the CRLs in a Package are chosen by whoever assembled it, and only
  a later CRL can show that the TSA key was not already compromised. The stamp
  attests a time no later than genTime plus its stated accuracy.

  Residual assumption: a TSA signing key compromised and not revoked by its CA
  within 24 hours can produce a token that passes. Relying parties that need more
  can require a later CRL or a second, independent anchor.
- Bitcoin: headers must contain a held checkpoint. Headers before it are linked
  by hash; headers after it must link, meet their proof-of-work target, and keep
  the target unchanged except at 2016-block boundaries, where it may change by at
  most a factor of four and never exceed the network limit. A header with eleven
  predecessors in the supplied range must carry a time above their median, and an
  attested block after the checkpoint must not be timed before it. The attested block's
  merkle root must equal the OpenTimestamps commitment, with at least six
  confirmations in the supplied headers. This is proof-of-work linkage, not a
  full-node check (`BITCOIN_POW_LINKED_NOT_FULL_NODE`). A proof may hold several
  attestations; one that does not match its block does not cancel another that
  does. Headers linked to a checkpoint the verifier does not hold leave the
  anchor `PENDING` (`BITCOIN_CHECKPOINT_NOT_HELD`), not failed; verifiers keep
  every checkpoint they ever shipped. The headers may start before the checkpoint
  (a checkpoint newer than the attested block), which keeps them short.
- Party-signature tokens are checked like the record's own token, against their
  target digest, and reported in `anchors.signatures` (`digest`, `time` with
  `status`, `genTime`, `latestTime`, `revocation`, `renewals`). They never count
  toward the record's `time`, `earliestIndependentTime`, the revoked-key rule or
  the verdict. A token that does not verify gives
  `SIGNATURE_TIME_ANCHOR_NOT_VERIFIED`. Whether the record refers to a target is
  the issuer profile's check: the ProofTask profile binds a target to a party
  signed original whose SHA-256 equals the target: a holder proof carried in the
  record's history (`binding: RECORD_HISTORY`) or a supplied agreement proof
  (`VERIFIED_AGREEMENT_PROOF`), in both cases only after the party signatures
  verify against independently approved participant keys. A recorded digest
  alone never binds. When the original is in the history but no participant keys
  were supplied, the entry is `ISSUER_ASSERTED`
  (`SIGNATURE_ANCHOR_PARTICIPANT_KEYS_REQUIRED`) and carries no deadline
  evidence. Otherwise `NOT_BOUND` with `SIGNATURE_ANCHOR_NOT_BOUND`, and the entry
  establishes nothing about the record. Only a verified verdict carries
  `anchors.signatures`; an INVALID or INDETERMINATE report has none. A bound
  entry names `role` and `stage`, and, against the agreed signing deadline,
  `deadlineEvidence`: `EXISTED_BY_SIGNING_DEADLINE` only for a verified,
  revocation-checked token whose `latestTime` is at or before the deadline.
- Frozen time policy: an issuer profile may narrow the trusted TSA roots and
  TSA policies to those the record itself froze (ProofTask: the agreement's
  `trustPolicy.time.rootSha256` and `policyOids`). Tokens outside it do not
  count, for the record's own time and for party signatures alike
  (`TRUST_TIME_POLICY_MISMATCH`). A policy can only narrow trust.
- Omitted evidence: an index may state `omitted`, the number of items the issuer
  held but left out of the Package for size; verifiers report
  `ANCHOR_EVIDENCE_OMITTED`.
- Renewals: each renewal token is checked like the original, against the
  previous token's SHA-256, and its genTime must not precede the previous one.
  The report gives `time.renewals` (`status` `VERIFIED` or `FAILED`, `count`,
  `latestGenTime`) for the reported token. A renewal shows the earlier token
  existed at its own genTime, so the evidence stays checkable after the earlier
  TSA certificate expires. It never changes `genTime`,
  `earliestIndependentTime` or the verdict; a renewal that does not verify gives
  `TIME_ANCHOR_RENEWAL_NOT_VERIFIED` and leaves the original token judged on its
  own.

When a Package carries `evidence/`, the report gains an `anchors` block (a Package
without it gives exactly the 1.1 report, and has no independent time): `time` (`NOT_PRESENT`, `VERIFIED` or
`FAILED`), `bitcoin` (`NOT_PRESENT`, `PENDING`, `VERIFIED` or `FAILED`) and
`earliestIndependentTime`: the earliest verified, revocation-checked genTime plus
its stated accuracy, or a verified block time plus two hours, whichever is
earlier. The two hours are a heuristic margin for backdated block timestamps
(consensus only bounds them by the median of the previous eleven blocks), not a
consensus bound. The signer's
declared time never counts. Missing, pending or failed evidence never makes a
record INVALID; it is reported with `ANCHOR_EVIDENCE_NOT_PRESENT`,
`BITCOIN_ANCHOR_PENDING`, `TIME_ANCHOR_NOT_VERIFIED`,
`BITCOIN_ANCHOR_NOT_VERIFIED`, `BITCOIN_CHECKPOINT_NOT_HELD`, `TIME_ANCHOR_REVOCATION_NOT_CHECKED`,
`TIME_ANCHOR_RENEWAL_NOT_VERIFIED`,
`ANCHOR_SUBJECT_MISMATCH` or `ANCHOR_EVIDENCE_INVALID`.

## Supplement 1.2: keys revoked after signing

For an issuer key with status `REVOKED`, `validUntil` is the earliest possible
time the key was exposed. An issuer publishing a REVOKED key MUST state it.

A record or partial presentation whose signature, or whose committed JEP event
signatures, verify only under a REVOKED key is judged as follows. The signature
is always checked cryptographically; a bad signature is INVALID.

- If the earliest independent time is before `validUntil` of every REVOKED key
  used, the record keeps its verdict and the report adds
  `ISSUER_KEY_REVOKED_PRE_EXPOSURE_PROVEN`.
- Otherwise the verdict is `INDETERMINATE` ("cannot determine"), with
  `ISSUER_KEY_REVOKED_TIME_UNPROVEN`, and `HISTORICAL_KEY_VALIDITY_UNKNOWN` when
  a used key states no `validUntil`. A partial presentation carries no evidence,
  so it is always INDETERMINATE under a REVOKED key.

The declared signing time must still not precede the key's `validFrom`.
Summaries and status statements are current statements, not history; under a
REVOKED key they remain INVALID. Records with schema conformity-record/1.0 keep
the 1.0 report and remain INVALID under a REVOKED key, whether the record or
one of its JEP events was signed with it.

A verifier that reports INDETERMINATE builds nothing on the record: no product
view, no timestamp renewal, no evidence packing and no copy comparison. The
reference CLIs exit with status 3 for INDETERMINATE.
