# Conformity Status 1.0

A Status is a signed observation, not a permanent assertion that a historical
result is still current. Its canonical issuer is an HTTPS origin. The identity
and `headDigest` bind the exact result and record head being observed.

`observedAt` and `expiresAt` are canonical UTC instants. The validity interval is
half-open and at most 300 elapsed seconds. Verifiers supply their own `checkedAt`
and expected issuer, result identifier and head digest. A future observation or
expired copy retains its signature validity but reports current status UNKNOWN;
it cannot supply a current state. No network is required or implicitly trusted.

`signature` is an EdDSA compact JWS with `typ: conformity-status+jwt`. Its payload
contains every unsigned Status member, plus `iss` equal to `identity.issuer` and
`iat` equal to the exact epoch seconds of `observedAt`, including fractional seconds. The verifier compares
the authenticated payload with the complete presented observation. A different
head, issuer, expiry, state or extension is not an equivalent observation.

Extension and critical-list processing follows the Record rules. Actor
attribution remains a recorder assertion. A fresh Status alone establishes
neither factual quality nor company mandate, payment or publication permission.

For this profile the head digest is the latest recorded JEP event digest. A
consumer obtains the expected head independently from the Package or its own
retained record. It must not use the Status itself to approve its own binding.
