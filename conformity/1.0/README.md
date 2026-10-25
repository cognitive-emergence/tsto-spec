# Portable conformity 1.0

This directory defines neutral, independently implementable records. The texts
and schemas are candidates until the complete conformance corpus and independent
interoperability checks have passed. Published bytes are immutable after release.

| Object | Identifier | Purpose |
|---|---|---|
| Conformity Record | `https://humanjudgment.org/ns/conformity-record/1.0` | Agreed criteria, deliveries and attributable judgments |
| Conformity Package | `https://humanjudgment.org/ns/conformity-package/1.0` | Complete private portable record and supporting material |
| Conformity Summary | `https://humanjudgment.org/ns/conformity-summary/1.0` | Public, jointly authorized VC 2.0 projection |
| Conformity Status | `https://humanjudgment.org/ns/conformity-status/1.0` | Signed, short-lived current observation |
| Conformity Verification Report | `https://humanjudgment.org/ns/conformity-verification/1.0` | A verifier's bounded conclusions, not a new credential |
| Canonical JSON | `https://humanjudgment.org/ns/canonical-json/1.0` | Strict JSON input and RFC 8785 serialization |
| Accepterms 2027 | `https://humanjudgment.org/ns/accepterms/2027` | Named acceptance terms |

The three portable artifacts are Package, Summary and Status. A Record is their
semantic substrate. A Verification Report is a verifier output. Neither creates
a fourth issued artifact. A collection of summaries has no separate schema.

An issuer is an HTTPS origin with one corresponding root did:web identifier.
Issuer discovery is not trust. Verifiers receive their own trusted keys and
policies. No verifier needs a live namespace, context, issuer or status endpoint
to validate a historical signature.

Normative dependencies and exact downloaded-source digests are in REFERENCES.md.
No new transport overrides existing JEP or TSTO signature bytes.
