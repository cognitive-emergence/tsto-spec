# Conformity Record 1.2

Published 2026-11-22 as part of Conformity 1.2. Identifier:
`https://humanjudgment.org/ns/conformity-record/1.2`. Schema:
conformity-record-1.2.schema.json.

Record 1.2 is Record 1.1 (`https://humanjudgment.org/ns/conformity-record/1.1`:
the 1.0 text with the limitations supplement) with exactly one change, stated
below. Every other rule of Record 1.1 applies to Record 1.2 unchanged,
including the visible, issuer-signed `limitations` array, the one closure
machine, extension processing, the SD-JWT encoding and the binding to TSTO/00
and JEP events.
Package supplements 1.1 and 1.2 (conformity-package-1.2.md) apply to a Record
1.2 exactly as they apply to a Record 1.1, although supplement 1.2 names only
conformity-record/1.1.

## Delegated technical evaluations: scope VERIFY

An actor's `delegation.scope` is one of `AGREE`, `DELIVER`, `JUDGE` and
`VERIFY`. The scope a delegation must carry follows from the object the actor
records:

| Object | Required scope |
|---|---|
| Agreement | `AGREE` |
| Delivery | `DELIVER` |
| Decision with purpose omitted or `ACCEPTANCE` | `JUDGE` |
| Decision with purpose `EVALUATION` | `VERIFY` |

Record 1.1 already requires an evaluation's delegation to carry the scope for
technical verification, but its schema lists only `AGREE`, `DELIVER` and
`JUDGE`, so a delegated evaluation cannot be expressed in Record 1.1. Record 1.2
adds `VERIFY` to the schema. A delegation with any other scope than the one in
the table is `INVALID_DELEGATION`. A delegation with scope `VERIFY` never
authorizes an acceptance decision, and `JUDGE` never authorizes an evaluation.

## Choosing the version

An issuer that never records a delegated technical evaluation may continue to
issue Record 1.1; nothing else differs. A record that contains a delegation with
scope `VERIFY` MUST be issued as Record 1.2. An issuer never re-signs or
rewrites an issued Record 1.0 or 1.1 as 1.2.

A verifier validates each record against the schema of the version it declares.
A Record 1.1 that contains scope `VERIFY` stays invalid (`INVALID_SCHEMA_SHAPE`)
under every verifier; supporting 1.2 does not change the meaning of 1.0 or 1.1.

## Limitations

The `limitations` of a Record 1.2 are codes from conformity-reasons-1.2.json.
The limitations of a Record 1.0 or 1.1 keep the rule of their own version. A
verifier reports every declared limitation and never treats one as a successful
check.

## Reports

A verifier reports a Record 1.2, its Package and its partial presentations with
Verification Report 1.2 (conformity-verification-1.2.md,
conformity-verification-1.2.schema.json).
