# Conformity Verification Report 1.0

The single reason catalog includes inherited source-verification codes without
renaming or combining distinct meanings. Retaining a source code does not make a
legacy source a native Record, select a different closure algorithm, or establish
that an external fact was verified. In particular, source-specific limitations
about original files, payment, publication permission and organization authority
remain distinct. A reason list is bounded; unregistered arbitrary exception text
is never copied into a report. Unknown namespaced transitions are explicitly
reported as UNKNOWN_NAMESPACED_TRANSITION and cannot establish closure.

The report is a verifier output, not another signed portable artifact. Its issuer
identifier, if established, uses the canonical HTTPS origin. did:web is derived
only for VC Summary interoperability; a mismatch is `ISSUER_IDENTIFIER_MISMATCH`.

| Reason | Meaning |
|---|---|
| PARTIAL_DISCLOSURE | Some content is omitted; the report includes disclosed/total counts |
| JEP_ORIGIN_EVIDENCE_NOT_INCLUDED | The partial presentation has no original JEP/TSTO evidence |
| PARTIAL_PRESENTATION_LEAKS_COMMITTED_CONTENT | A supposed partial presentation includes JEP or TSTO content and is rejected |
| PACKAGE_CONTENT_MISMATCH | A committed file is absent, replaced or inconsistent with its signed commitment |
| UNCOMMITTED_FILE | Extra material is not authenticated and is excluded from conclusions |
| ISSUER_IDENTIFIER_MISMATCH | The canonical origin and presented issuer form do not correspond |
| STATUS_EXPIRED | An authentic observation is outside its validity interval; current status remains unknown |
| STATUS_NOT_YET_VALID | The observation is in the verifier’s future; current status remains unknown |
| STATUS_RECORD_BINDING_MISMATCH | The supplied Status refers to another result or head |
| STATUS_SIGNATURE_BINDING_MISMATCH | Presented Status fields differ from the signed observation |
| NESTED_DISCLOSURE_FORBIDDEN | The Record violates the flat native disclosure profile |
| ACTOR_ATTRIBUTION_RECORDER_ASSERTION | Actor attribution is signed by the recorder, not a party-held signature |

Full Package verification checks original event signatures and material binding;
partial presentation verification does not. Neither signature validity nor full
structural closure proves factual quality, current publication status, company
mandate or payment. This initial reason inventory must be extended with every
legacy-verifier meaning before export convergence is complete.

`org.humanjudgment.party-signature` remains reserved and is not emitted or
implemented. A future separately authorized addition may support party-held
signatures; it cannot be inferred from a recorder signature or a passkey login.

The issuer member is omitted when authenticity has not been established. An
invalid artifact must not present an unverified claimed issuer as an established
identity. Summary and Status reports never claim full Record closure. Current
status is independently NOT_CHECKED, FRESH or UNKNOWN; an expired or future
Status has a null current state. All artifact kinds use this one report schema.

Core reason identifiers are enumerated in `conformity-reasons.json`.
`PUBLIC_SUMMARY_NOT_FULL_RECORD` identifies a deliberately limited public view;
`STATUS_BINDING_AND_CLOCK_REQUIRED` rejects a current-state check without an
independent expected head and clock. TSTO subject/target or JEP identity and V
policy/result mismatches are failures even if every signature is valid.
