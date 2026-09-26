# TSTO/00 and JEP-TSTO Binding/01


## Current Binding/01 publication

**Experimental Binding Draft 01. English is normative; Chinese is informative. This is not a formal standard.** TSTO remains 00 and JEP wire version remains `1`.

- [Binding/01 English specification](bindings/JEP-TSTO-Binding-01.md)
- [Binding/01 中文译文](bindings/JEP-TSTO-Binding-01.zh-CN.md)
- [English PDF](docs/JEP-TSTO-Binding-01-EN.pdf) / [中文 PDF](docs/JEP-TSTO-Binding-01-ZH-CN.pdf)
- [Binding/01 Schema](schemas/jep-tsto-binding-01.schema.json)
- [Signed J/D/T/V and hostile vectors](examples/binding-01/vectors.json)
- [Release notes and validation evidence](releases/binding-01/RELEASE-NOTES.md)

Binding/01 corrects the original Binding/00 carrier incompatibilities with the published JEP event Schema. It uses typed J/D/V references, array-valued D constraints, explicit T target equality, and a signed version marker. Historical 00 artifacts below are retained unchanged; their examples do not pass the current joint JEP Schema path.

```sh
python -m pip install -r scripts/requirements-binding-01.txt
python scripts/check-binding-01.py
```

The command checks joint schemas, JCS, signatures and exact references under synthetic test trust. It does not evaluate external evidence truth or full domain policy.

## Original TSTO/00 publication (retained)

**Target State Transition Object Specification**  
**可验证目标状态迁移对象规范**

TSTO/00 defines an immutable, addressable, and verifiable object for expressing **what state change counts as completion**. It intentionally leaves responsibility, execution, pricing, settlement, and disputes to external layers.

TSTO/00 用不可变、可寻址、可验证的对象表达**什么变化才算完成**，并把责任、执行、价格、结算和争议留给外层系统。

This release also includes the independent **JEP-TSTO Binding/00**, which defines how JEP-Core 0.6 Judgment, Delegation, Termination, and Verification event claims bind to a TSTO without modifying either Core.

## Status

- Version: `TSTO/00`
- Binding: `JEP-TSTO Binding/00`
- Maturity: Experimental Draft 00
- Release date: 2026-08-03
- Initiator: Cognitive Emergence（认知涌现）
- License: CC BY 4.0
- Formal standard: No

The English texts are normative. The Chinese texts are informative translations. This release is suitable for implementation experiments, controlled pilots, and public review; it MUST NOT be presented as an industry consensus or formal standard.

## Repository contents

```text
.
├── README.md
├── SPEC.md
├── SPEC.zh-CN.md
├── bindings/
│   ├── JEP-TSTO-Binding-00.md
│   └── JEP-TSTO-Binding-00.zh-CN.md
├── schemas/
│   ├── tsto-00.schema.json
│   └── jep-tsto-binding-00.schema.json
├── examples/
│   ├── tsto/valid/
│   ├── tsto/invalid/
│   └── jep/
├── docs/
│   ├── TSTO-00-EN.pdf
│   ├── TSTO-00-ZH-CN.pdf
│   ├── JEP-TSTO-Binding-00-EN.pdf
│   └── JEP-TSTO-Binding-00-ZH-CN.pdf
├── LICENSE.md
├── CITATION.cff
├── .zenodo.json
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── RELEASE_CHECKLIST.md
└── SHA256SUMS.txt
```

## Core boundary

TSTO/00 defines the Subject, evidence-backed Baseline, machine-evaluable Target, time boundaries, Constraints, immutable Profile and Verification Policy references, and content integrity. It has no mutable status and does not contain a responsible party, workflow, price, or payment instruction.

JEP-Core records signed event claims. JEP-TSTO Binding/00 specifies how those claims reference a TSTO. A valid event signature does not prove external truth, authorization validity, legal liability, or the correctness of a domain result.

## Validation

The Schemas use JSON Schema Draft 2020-12. Schema validation is structural only; semantic validation remains required.

Example commands using Ajv CLI:

```sh
npx --yes --package ajv-cli@5 --package ajv-formats@2 \
  ajv validate --spec=draft2020 --strict=false -c ajv-formats \
  -s schemas/tsto-00.schema.json \
  -d examples/tsto/valid/ar-invoice-settlement.example.json

npx --yes --package ajv-cli@5 --package ajv-formats@2 \
  ajv validate --spec=draft2020 --strict=false -c ajv-formats \
  -s schemas/jep-tsto-binding-00.schema.json \
  -d 'examples/jep/*.json'
```

The valid TSTO example includes a correctly calculated `integrity.value`; its referenced Profile, Evidence, and Policy digests are format-valid illustrative values. The invalid TSTO example intentionally omits Baseline evidence and MUST fail. JEP examples bind the valid TSTO digest, but their signatures are explicitly marked unsigned and are not cryptographic test vectors.

## Release and citation

Suggested Git tag: `tsto-00`. Citation metadata is in `CITATION.cff`; Zenodo metadata is in `.zenodo.json`. A DOI should be added only after Zenodo assigns it, without changing the protocol semantics.

## Feedback

Use repository Issues for implementation reports, interoperability findings, Profile proposals, and editorial corrections. Use GitHub's private security advisory feature for sensitive reports.


## JEP Core 0.7 binding

The current JEP Core binding work is:

- [JEP-TSTO Binding/02](bindings/JEP-TSTO-Binding-02.md) — JEP Core 0.7
- [Binding/02 schema](schemas/jep-tsto-binding-02.schema.json)

Binding/01 remains the immutable historical binding for JEP Core 0.6.
Binding/02 uses JEP Event Identity `(who,id)` for semantic event targets;
an Event Hash may additionally pin one exact signed artifact.
