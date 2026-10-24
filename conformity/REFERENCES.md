# Pinned references

Retrieved 2026-10-24. SHA-256 covers the original response bytes of each retrieved resource, without whitespace normalization. Dated Recommendations and RFC 9901 are normative; did:web is a community method specification and is pinned to the retrieved snapshot. Newer editor drafts do not replace these versions.

| Reference | Status | Version URL | SHA-256 |
|---|---|---|---|
| VC Data Model 2.0 | W3C Recommendation, 2025-05-15 | https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/ | `a9196a3d0b6601356c4e127bad24f8c7f2c17f6ed22e41b35755a910104156f8` |
| Data Integrity 1.0 | W3C Recommendation, 2025-05-15 | https://www.w3.org/TR/2025/REC-vc-data-integrity-20250515/ | `ba5c4baf13fe3bab3ebd95ab6650d6fe83720e254b383bb444b4fbbae7bcf4fe` |
| Data Integrity EdDSA Cryptosuites 1.0 | W3C Recommendation, 2025-05-15 | https://www.w3.org/TR/2025/REC-vc-di-eddsa-20250515/ | `d404f372131a0e237d85aa3a6887aa54acadb862714d73e7b001ba789b5716eb` |
| SD-JWT | RFC 9901, Standards Track, November 2025 | https://www.rfc-editor.org/rfc/rfc9901.txt | `fd4cb79184162fa7ef95f4f63abab8ee6d03c9a04c19b8f83758946464b284eb` |
| did:web | W3C Credentials Community Group method specification; not a W3C Recommendation | https://w3c-ccg.github.io/did-method-web/ | `7e48b1ad2d658452bc9ce23b975d243abe095f7696c06671fc332705a1290610` |

## Normative corrections to the implementation brief

RFC 9901 section 4.2.1 uses `[salt, name, value]` for an object member and section 4.2.2 uses `[salt, value]` for an array element. Criteria and criterion judgments use the array form. Hashes inside SD-JWT use unpadded base64url as RFC 9901 requires; other new conformity references use `sha256:` followed by lowercase hexadecimal. Existing nested JEP and TSTO bytes retain their published digest formats.

A complete presentation with an unresolved commitment fails completeness. A partial presentation cannot distinguish an undisclosed legitimate claim from a decoy hash by itself. Accordingly, issuers MUST NOT emit decoys; validators report the signed commitment counts and MUST NOT claim closure completeness for partial presentations.

The EdDSA JCS proof signs SHA-256(canonical proof configuration) concatenated with SHA-256(canonical unsecured document), in that order. Proof context is retained. This is not a raw signature over the credential JSON.
