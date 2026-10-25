# Conformity Record 1.0

The decoded Record conforms to conformity-record.schema.json. Its `schema` is
the absolute identifier, not an application alias. `identity.issuer` is an HTTPS
origin; `identity.resultId` is an absolute URI. A profile is an opaque uppercase
identifier or an absolute URI. Profiles all use the same closure algorithm;
none selects a different interpretation of closure.

## Specification and judgments

Each criterion has a unique id, title, requirement, evidence requirement,
determinability, extensions and critical list. Determinability is MACHINE,
MEASURED or HUMAN. Determinability describes the kind of judgment, not its truth.
Each decision covers every agreed criterion exactly once. MET maps to CONFORM;
NEEDS_CHANGES and NOT_MET map to NONCONFORM; UNDETERMINED maps to INDETERMINATE.
Unknown verdicts are errors. An ACCEPT decision requires all MET verdicts.

Parties are FIRST_PARTY, SECOND_PARTY or THIRD_PARTY. A V may only be attributed
to a third party. Party J and independent V are distinct. An issuer's assertion
of an actor does not independently prove the actor's company mandate.

The specification's digest covers its canonical JSON excluding only its own
`reference.digest`. Deliveries and decisions refer to that immutable digest.
A later submission references the previous delivery and the decision it answers.
An evaluation must name the exact delivery and evidence-manifest digest it used.

## One closure machine

Both parties explicitly agree before delivery. A delivery enters SUBMITTED.
ACCEPT enters CONFORM; REJECT enters NONCONFORM; REQUEST_CHANGES enters
CHANGES_REQUESTED; REQUEST_EVIDENCE enters AWAITING_EVIDENCE. A revised delivery
may follow either request. Silence never creates a party action.

Every object is covered by the ordered event history, with matching identity,
timestamp and event digest. Missing stages, a mixed specification, a missing
criterion or a stale delivery cannot establish closure. Unknown unnamespaced
events are errors. Unknown namespaced events make interpretation INDETERMINATE;
a later known event cannot restore certainty about the intervening history.

Delegated actors retain a principal and an action-scoped validity interval.
Expired or wrong-scope grants do not authorize a decision. Verification of
supporting authority evidence remains distinct from structural checks.

## Extension processing

Extension keys use reverse-domain names. Every `critical` entry exists in its
local extensions object. An unknown critical entry fails verification. An
unknown noncritical entry remains covered by the signature and cannot override
a native field. The names `org.humanjudgment.condition`,
`org.humanjudgment.judgment-window`, `org.humanjudgment.upstream`,
`org.humanjudgment.accreditation`, `org.humanjudgment.party-signature` and
`org.humanjudgment.time-anchor` are reserved. Reservation does not imply a
supported handler, accreditation check or time-anchor verification.

The signed JWT's always-visible `criticalManifest` repeats the paths and names
of all critical extensions, including extensions inside concealed criteria.
Unknown critical names fail even a partial verification. In a complete
presentation the verifier compares this manifest with the reconstructed Record
and runs each handler on its disclosed value. Other extension values are
separately concealed; no nested commitments are inserted into a criterion that
is already concealed as one array element.

`_sd`, `_sd_alg` and `...` are reserved for the SD-JWT encoding and cannot be
introduced as business-data property names. Language tags follow RFC 5646 well-formed syntax, including grandfathered and
private-use forms. Repeated variants and repeated extension singletons are
rejected. Registry membership is not inferred; null means that no original
language was recorded. The schema bounds stored tags to 100 characters.

## SD-JWT encoding

RFC 9901 is the signature transport. The issuer-signed JWT uses EdDSA and
`_sd_alg: sha-256`. The schema, identity, profile, object references, state,
acceptance terms, issuance and critical-extension declarations stay visible.
Criterion definitions and criterion judgments are individually disclosed array
elements. Names, external identifiers and free-text judgment notes are separately
disclosable. Salts contain at least 128 bits of cryptographic randomness.

Array disclosures use `[salt,value]`; object disclosures use `[salt,name,value]`.
Disclosure hashes use the RFC-required unpadded base64url encoding. A signed
count records the complete number of commitments. This profile has no decoys or
nested disclosure commitments. A verifier reports disclosed and total counts.
A FULL verification requires every disclosure. A partial presentation retains
the same JWT signature but cannot establish full closure or undisclosed claims.

Full presentations reject unreferenced, duplicate or tampered disclosures and
unresolved commitments. For partial presentations, a verifier cannot determine
whether an unresolved digest was an undisclosed claim or a prohibited decoy.

## Visible evidence and issuer identity

The signed JWT always retains `commitments.tsto`, `commitments.jepEvents` and
`commitments.attachmentManifest`, each binding a path, media type and SHA-256.
Only digests are retained in a partial presentation; TSTO and JEP content is
excluded. The unsigned full Package supplies that content for verification.
See conformity-package.md for the two verification levels.

The canonical issuer is an HTTPS origin in Records, Status and Reports. The
Summary uses the corresponding derived did:web identifier. A correspondence
failure is `ISSUER_IDENTIFIER_MISMATCH`.

A partial verifier validates the visible Record structure, even though it cannot
recompute concealed object digests or establish closure. It cannot conceal or
omit identity, state, history, object references or evidence commitments. Nested
disclosure commitments are forbidden in this profile.

The native TSTO profile is `https://humanjudgment.org/profiles/conformity/1.0`.
Its subject identifier equals the Record result identifier. Its target claims
contain one `eq` claim per criterion, in order, whose JSON Pointer path is
`/criteria/<escaped-id>` and whose value is the exact criterion object. The
verification parameters also commit the specification digest. Original signed
JEP identifiers, timestamps, actors and object digests must match the history.

The JWT NumericDate preserves the millisecond precision of `issuance.issuedAt`;
rounding down must not move a record across a key validity boundary.

## Technical evaluations and explicit acceptance

A decision with `purpose: EVALUATION` is an independently attributed V with
`action: EVALUATE`. It covers a nonempty, unique subset of declared MACHINE or
MEASURED criteria. Its history kind is EVALUATION. It must reference the current
submitted delivery and never changes the acceptance state or current acceptance
decision identifier. This enables technical evidence without fabricating a
party judgment. Its original V result and policy reference must match the
recorded criterion outcomes and TSTO verification policy.

All acceptance decisions (purpose omitted or ACCEPTANCE) still cover every
agreed criterion exactly once. Their judge follows the acceptance terms. Under
BE, only the explicit second-party J can close the result. Technical evidence,
even when conforming, cannot stand in for that J.
