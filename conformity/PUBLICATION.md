# Conformity 1.0 publication in this repository

Conformity 1.0 is the neutral result-conformity layer that sits above TSTO/00 and JEP Core 0.7:
TSTO states the target, JEP records who judged, and a Conformity Record states which agreed criteria
the parties judged as met, in what order, and with which reliance limitations.

This directory is the interim public source of the Conformity 1.0 specification set until its
identifiers are served from `https://humanjudgment.org/ns/`. The identifiers inside the files are
the canonical ones and do not change when the hosting location changes. Implementations must not
fetch them at verification time.

| Set | Files |
| --- | --- |
| Record, Package, Summary, Status, Verification Report | `conformity-*.md`, `conformity-*.schema.json`, `conformity-summary.context.jsonld` |
| Canonical JSON, issuer discovery, acceptance terms | `canonical-json.*`, `issuer-discovery.md`, `conformity-issuer.schema.json`, `accepterms.*` |
| Reason catalog | `conformity-reasons.json` |
| Amendment 1: reliance limitations | `conformity-amendment-1.md`, `conformity-limitations.json` |
| Test vectors (no private keys) | `vectors/conformity-1.0.json`, `vectors/conformity-supplement-1.json`, `vectors/conformity-amendment-1.json` |

Every file is copied byte-for-byte from the reference implementation's `standards/` directory and
listed in `SHA256SUMS.txt`. Published files are append-only: a correction is a new amendment or a new
version under a new path, never an edit of a published file.

Amendment 1 is additive. Records issued before it verify exactly as before; records issued after it
carry an always-visible, critical `org.humanjudgment.limitations` declaration that every conforming
verifier reports. Issuer-private extensions should be noncritical so that independent verifiers are
never forced to reject a record.

License: CC BY 4.0, as for the rest of this repository.
