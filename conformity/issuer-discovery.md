# Issuer discovery 1.0

The HTTPS origin exposes `/.well-known/conformity-issuer.json` and
`/.well-known/did.json`. The origin maps to `did:web:<host>`; a nondefault port
uses percent-encoded colon in the DID. User information, paths, query and
fragments do not form part of an issuer origin.

Both documents expose exactly the same identifiers, public-key bytes, key
status and validity metadata. Ed25519 Multikey public values use multicodec
0xed followed by the raw 32-byte public key, encoded as base58btc multibase.
Active and retained historical keys remain assertion methods; revoked keys do
not. Key retirement prevents new issuance but does not by itself invalidate a
signature made within the key's validity interval. Rotation updates both
documents in the same release.

Discovery is a lookup convention, not permission to trust a key. A verifier's
independently supplied issuer policy controls acceptance. Embedded keys and a
successful HTTPS fetch never create that trust. No verification function makes
a network request, selects a system clock, or fetches a context.
