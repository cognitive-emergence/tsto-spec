# Conformity Summary 1.0

A Summary is a VC Data Model 2.0 credential with the fixed credential context
first and the local, immutable context second. The subject identifies the
result by URI. The issuer is the origin's root did:web identifier. `validFrom`
and proof creation use canonical UTC timestamps. `credentialStatus` points to
a Conformity Status endpoint; offline verification does not query it.

The proof uses DataIntegrityProof, eddsa-jcs-2022 and assertionMethod. The proof
retains its context. The original signature verifies directly with a compatible
Data Integrity implementation; a verifier needs no JSON-LD expansion for the
JCS signature. The context's bytes are nevertheless fixed for consumers that
do expand JSON-LD.

Public claims are a jointly authorized selected projection, not a complete
history. Buyer confirmation is not independent verification. Original private
records are not included. Company mandate, external signatures and payment
remain explicitly unverified. A historical signature does not prove that the
summary is still published or that its referenced status is current.
