# Conformity Verification 1.2

Published 2026-11-22 as part of Conformity 1.2. Report identifier:
`https://humanjudgment.org/ns/conformity-verification/1.2`. Schema:
conformity-verification-1.2.schema.json. Reason catalog:
conformity-reasons-1.2.json.

This text adds three things to Verification Report 1.0 and its 1.1 supplement:
Report 1.2, the 1.2 reason catalog, and the verification procedure below. The
procedure writes down rules that the earlier texts left implicit. It does not
change the verdict of any Record, Package, Status or Summary issued under 1.0 or
1.1; for three rules it names a registered reason where earlier verifiers
reported `INVALID_CONFORMITY_INPUT`.

## Report 1.2

A verifier reports a Record 1.2, its Package and its partial presentations with
Report 1.2. A Record 1.1 keeps the identifier of Report 1.1 and a Record 1.0 that
of Report 1.0. Report 1.2 has the members of Report 1.1 plus those a verifier
of package supplement 1.2 adds: the status `INDETERMINATE` and the `anchors`
member. A Report 1.1 produced by a verifier that implements package supplement
1.2 may carry the same two additions; validate those members against the Report
1.2 schema. A report for an INVALID artifact may use any of the three
identifiers; its members are always `schema`, `status`, `closure`
(`NOT_ESTABLISHED`), `disclosures` (0 of 0) and exactly one reason.

## Reason catalog 1.2

conformity-reasons-1.2.json is the catalog of the 1.1 supplement plus three
registrations:

| Reason | Meaning |
|---|---|
| ACCEPTANCE_NOT_CONFORM | An ACCEPT decision contains a criterion verdict other than MET |
| UNKNOWN_UNNAMESPACED_EVENT | A history kind is neither a registered kind nor a namespaced URI |
| JEP_ORIGIN_EVIDENCE_NOT_INCLUDED | The partial presentation has no original JEP/TSTO evidence (required by Report 1.0 and now registered) |

When a rule fails whose code is not in the catalog, the reason is
`INVALID_CONFORMITY_INPUT`. A verifier never copies exception text into a
report.

## Verification order

A report for an INVALID artifact carries exactly one reason: the first rule
that failed. Verifiers check in this order, so that independent
implementations report the same reason.

1. **Input.** Strict UTF-8; then strict JSON (Canonical JSON 1.0) when the text
   starts with `{`: duplicate member names including escaped spellings, lone
   surrogates, non-finite numbers, trailing material and a byte-order mark are
   rejected; depth is at most 64 and the value count at most 100,000. Otherwise
   the trimmed text is a compact SD-JWT presentation. Errors use the parser codes
   `INVALID_UTF8`, `INVALID_JSON`, `DUPLICATE_KEY`, `INVALID_UNICODE`,
   `NON_FINITE_NUMBER` and `LIMIT_EXCEEDED`.
2. **Artifact kind** by `schema`: Package, Summary, Status. An object with
   `presentation` or `sdJwt` is not a format:
   `PARTIAL_PRESENTATION_LEAKS_COMMITTED_CONTENT` when it also carries TSTO or
   JEP content or a `tsto`, `jepEvents` or `files` member, otherwise
   `INVALID_PARTIAL_PRESENTATION`. Anything else is
   `UNSUPPORTED_CONFORMITY_ARTIFACT`.
3. **Package carrier** (Package only): exactly the members `schema` and `files`
   (`INVALID_PACKAGE`); safe, unique paths and a `record.sd-jwt` entry
   (`PACKAGE_CONTENT_MISMATCH`).
4. **Issuer-signed JWT**, then **disclosures**, the **envelope**, the
   **visible Record**, and for a complete Record the **critical manifest** and
   **Record semantics** (sections below).
5. **Committed files**: the record file's media type `application/sd-jwt` and
   digest, then the TSTO, each JEP event, the attachment manifest and each
   attachment (`PACKAGE_CONTENT_MISMATCH`).
6. **Origin evidence**: TSTO, then JEP events.
7. **Revoked keys** decide between `VERIFIED_WITH_LIMITATIONS` and
   `INDETERMINATE` (package supplement 1.2).

## Keys

- The trust input lists keys per issuer origin. The key is the one whose `id`
  equals the JWT header `kid`. Zero or more than one match is
  `UNTRUSTED_ISSUER_KEY`. A key that is not an Ed25519 SubjectPublicKeyInfo is
  `UNSUPPORTED_KEY_TYPE`.
- The signing time is the signed claim, never the verifier's clock: for a
  Record the JWT `iat` (milliseconds kept, as a canonical UTC timestamp), for a
  Status `iat`, for a Summary `proof.created`, and for each JEP event the
  `recordedAt` of its history entry or, for an auxiliary event, its `when`. Each
  event is checked at its own time.
- Validity is half-open: a key is valid when `validFrom <= at < validUntil`
  (both bounds optional). `ACTIVE` and `RETIRED` keys are valid inside their
  window; status never extends it. Otherwise `ISSUER_KEY_NOT_VALID_AT_ISSUANCE`.
- `REVOKED`: for a Status, a Summary and any Record 1.0 the signature is
  `ISSUER_KEY_NOT_VALID_AT_ISSUANCE`. For a Record 1.1 or 1.2 and its partial
  presentations the signature is still verified (and must not precede
  `validFrom`); the use is then weighed as package supplement 1.2 describes.
  Without anchoring evidence the result is `INDETERMINATE` with
  `ISSUER_KEY_REVOKED_TIME_UNPROVEN`, plus `HISTORICAL_KEY_VALIDITY_UNKNOWN` when
  a used key has no `validUntil`. This applies when only the JEP events used the
  revoked key, too.

## Issuer-signed JWT

- Compact JWS with three parts in strict unpadded base64url (a non-canonical
  encoding is `INVALID_BASE64URL`). The presentation is `JWT~disclosure~…~` and
  ends with `~` (`INVALID_SD_JWT`).
- The protected header has only the members `alg`, `kid` and `typ`; `alg` is
  `EdDSA` (not `Ed25519`, which the JEP events use); otherwise
  `UNSUPPORTED_JWT_HEADER`. The payload has a string `iss` and a number `iat`
  for which `iat × 1000` is an integer; otherwise `INVALID_JWT_CLAIMS`. The
  signature is Ed25519 over the ASCII text `header.payload`
  (`INVALID_SIGNATURE`).
- Record: `typ` is `sd-jwt` (`UNSUPPORTED_SD_JWT_TYPE`); `_sd_alg` is `sha-256`
  at the top level only (`UNSUPPORTED_SD_ALGORITHM`).

## Disclosures

- Each disclosure is base64url of the JSON array `[salt, value]` (array
  element) or `[salt, name, value]` (object member). The salt is base64url of at
  least 16 bytes; a name is a string other than `_sd` and `...`. Otherwise
  `INVALID_DISCLOSURE`. A disclosure's digest is the unpadded base64url SHA-256
  of its ASCII text. Two identical disclosures are `DUPLICATE_DISCLOSURE`.
- The payload is walked: an array element `{"...": digest}` (with no other
  member, else `INVALID_ARRAY_DISCLOSURE`) is replaced by an array disclosure;
  an object's `_sd` list adds object disclosures (a name already present is
  `DUPLICATE_CLAIM`). A digest that is not base64url of 32 bytes is
  `INVALID_DISCLOSURE_DIGEST`; one referenced twice is
  `DUPLICATE_DISCLOSURE_DIGEST`; an object disclosure in an array position or
  the reverse is `DISCLOSURE_LOCATION_MISMATCH`. Disclosed values are walked too.
- After the walk, a disclosure that no digest referenced is
  `UNREFERENCED_DISCLOSURE` (a modified disclosure fails this way). Then a
  disclosed value containing `_sd`, `_sd_alg` or `...` is
  `NESTED_DISCLOSURE_FORBIDDEN`. A complete Package with unresolved digests is
  `INCOMPLETE_DISCLOSURE_SET`.
- `disclosures.total` is the number of digests referenced; `disclosed` is the
  number resolved.

## Envelope and visible Record

- `iss` equals `identity.issuer` (`ISSUER_IDENTIFIER_MISMATCH`). `schema` is
  Record 1.0, 1.1 or 1.2; `iat` equals `issuance.issuedAt` in seconds; and
  `disclosureCount` equals `total`. Otherwise `RECORD_ENVELOPE_MISMATCH`.
- `criticalManifest` is a list of `{path, keys}` (`CRITICAL_MANIFEST_INVALID`).
  Every key names an extension the verifier supports, even in a partial
  presentation (`UNSUPPORTED_CRITICAL_EXTENSION`).
- The Record is the resolved payload without `iss`, `iat`, `disclosureCount` and
  `criticalManifest`. It validates against the schema of its own version with
  the concealable members optional: actor and party `name` and `identifiers`,
  decision `note`, and `criteria`, which may be empty (`INVALID_SCHEMA_SHAPE`).
  Schema patterns are ECMAScript patterns: `\d` matches ASCII digits only and
  `$` matches only at the very end.
- Every timestamp is canonical UTC, `YYYY-MM-DDTHH:MM:SS.mmmZ`, naming a real
  calendar instant.
- A complete Record's manifest equals the one recomputed from it: every object
  with a nonempty `critical` list, as a JSON Pointer (`/` for the root), in
  document order with members in canonical (UTF-16) key order
  (`CRITICAL_MANIFEST_INVALID`).

## Record semantics

The Record is checked in document order: limitations (registered in the
catalog of the record's version, unique: `INVALID_RECORD_LIMITATIONS`), identity,
profile, extension slots (reverse-domain names with at least three labels;
`org.humanjudgment.party-signature` is `PARTY_HELD_SIGNATURE_NOT_IMPLEMENTED`; a
critical name the verifier does not support is
`UNSUPPORTED_CRITICAL_EXTENSION`), commitments, the specification digest,
terms, durations, language tag, criteria, parties, agreements, deliveries,
decisions, history, current state.

- Digests are `sha256:` plus lowercase hex of the JCS bytes. The specification
  digest omits only `reference.digest`. A delivery's or decision's digest omits
  `reference.digest` and `eventDigest`.
- Within a decision, the semantic rules come before the digest check: binding,
  verb and party, terms or evaluation rules, the actor and its delegation
  (`INVALID_DELEGATION`; scopes as in Record 1.2), exact criteria, outcome
  mapping, then the action rules: ACCEPT requires every verdict MET
  (`ACCEPTANCE_NOT_CONFORM`), REQUEST_CHANGES a NEEDS_CHANGES or NOT_MET
  verdict, REQUEST_EVIDENCE an UNDETERMINED verdict, REJECT a NOT_MET verdict.
- A history kind other than AGREEMENT, DELIVERY, DECISION and EVALUATION must
  be a namespaced URI (`UNKNOWN_UNNAMESPACED_EVENT`); a namespaced kind makes
  the interpretation `INDETERMINATE` and adds `UNKNOWN_NAMESPACED_TRANSITION`.
- Closure is `COMPLETE` when the history ends in `CONFORM` with both parties'
  agreements; `NOT_COMPLETE` for any other valid Record; `NOT_ESTABLISHED` for
  partial presentations, Status and Summary.

## Origin evidence

- TSTO: `spec` `TSTO/00`, `type` `TargetStateTransition`, a string `id`,
  `integrity.alg` `sha-256` and `integrity.canonicalization` `RFC8785`
  (`TSTO_ORIGIN_EVIDENCE_INVALID`). `integrity.value` is `sha-256:` plus
  unpadded base64url SHA-256 of the JCS of the TSTO without `integrity`, and
  `verification.parameters["org.humanjudgment.specification-digest"]` is the
  specification digest (`TSTO_SPECIFICATION_BINDING_MISMATCH`). Subject and
  target rules are those of the Record text.
- A JEP event is identified by `sha256:` plus hex of the JCS of the whole signed
  event. Each history entry's event exists, is a JEP Core 0.7 event with the
  JEP-TSTO Binding/02 marker referencing this TSTO, and carries the extension
  `org.humanjudgment.record-binding` `{objectId, specificationDigest,
  objectDigest}`. Its `id` equals the history id, `when` equals the recorded
  time in whole seconds (rounded down), and `who` equals the object's actor id;
  otherwise `JEP_ORIGIN_EVIDENCE_INVALID`. `objectDigest` is the delivery's or
  decision's digest, or the specification digest for agreements
  (`JEP_RECORD_BINDING_MISMATCH`). `what.decision` is `propose` for a
  second-party agreement and for a delivery, `accept` for a first-party
  agreement, and for a J decision `accept`, `reject` or `reassess` by action
  (`JEP_JUDGMENT_KIND_MISMATCH`). A V decision maps its outcomes to
  `what.result` and repeats the TSTO verification policy as `what.policy_ref`
  (`JEP_VERIFICATION_BINDING_MISMATCH`).
- In a Record 1.1 or 1.2, committed events without a record binding are
  auxiliary: they are authenticated, take their time from `when`, and are
  reported as `JEP_AUXILIARY_NOT_INTERPRETED`. Every committed event is
  accounted for.
- Each event's `sig` is a detached JWS `header..signature` with header `alg`
  `Ed25519`, `kid` and optional `typ` `JEP`; the signing input is
  `header + "." + base64url(JCS(event without sig))`; the key is the Record
  issuer's key at the event's time (`JEP_SIGNATURE_INVALID`, or a key error from
  "Keys").

## Report contents

- A Package report has `issuer`, `status`, `closure`, `disclosures`,
  `limitations` (Record 1.1 and 1.2 only, in Record order), `reasons`,
  `ignoredFiles` (carrier paths that no commitment reached, in carrier order)
  and `commitments`. Its reasons are `ACTOR_ATTRIBUTION_RECORDER_ASSERTION`, the
  limitation codes, then `UNKNOWN_NAMESPACED_TRANSITION`, `UNCOMMITTED_FILE`,
  `JEP_AUXILIARY_NOT_INTERPRETED` and the revoked-key codes, as they apply.
- A partial presentation report has status `PARTIAL_DISCLOSURE` (or
  `INDETERMINATE`), closure `NOT_ESTABLISHED`, the reasons `PARTIAL_DISCLOSURE`,
  `JEP_ORIGIN_EVIDENCE_NOT_INCLUDED`, `ACTOR_ATTRIBUTION_RECORDER_ASSERTION`, the
  limitations and the revoked-key codes, and no `ignoredFiles`. A presentation
  with every disclosure but no Package is still partial. A disclosed value that
  contains TSTO or JEP content, also as JSON text inside a string, is
  `PARTIAL_PRESENTATION_LEAKS_COMMITTED_CONTENT`.
- Status: `currentStatus` is `FRESH` when `observedAt <= checkedAt <
  expiresAt`; otherwise it is `UNKNOWN` with `currentState` null and
  `STATUS_NOT_YET_VALID` or `STATUS_EXPIRED`. Summary: `currentStatus`
  `NOT_CHECKED` and `PUBLIC_SUMMARY_NOT_FULL_RECORD`.

## Neutral and product verifiers

A neutral verifier installs no product-specific extension handlers and no
product source policy. A record whose committed events include an issuer's
workflow events is then reported with `JEP_AUXILIARY_NOT_INTERPRETED`: the
events are authenticated but not replayed, which is the correct neutral result
(package supplement 1.1). A product verifier that replays those events omits
that reason and may name formats its issuer retired.

## Conformance suite

The Conformity 1 conformance suite (informative) contains signed vectors for
Records 1.0, 1.1 and 1.2 with the expected report members of a neutral verifier.
It does not cover anchoring evidence (package supplement 1.2).
