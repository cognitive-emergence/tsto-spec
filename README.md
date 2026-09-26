# TSTO and JEP interoperability

**TSTO defines what state change counts as completion. JEP records signed statements about it.** The binding connects their immutable references; a signature alone does not prove completion, authority or payment eligibility.

当前接入：**TSTO/00 + JEP Core 0.7 + Binding/02**。先读规范，再运行联合验证。英文为规范文本；这些文件是实验草案，并非正式标准。

| Use | Entry |
| --- | --- |
| Target-state object | [TSTO/00](SPEC.md) · [中文](SPEC.zh-CN.md) |
| Current JEP integration | [Binding/02](bindings/JEP-TSTO-Binding-02.md) · [supplementary Schema](schemas/jep-tsto-binding-02.schema.json) |
| Reproduce interoperability | [Signed examples and hostile vectors](examples/binding-02/vectors.json) · [validation report](releases/binding-02/validation-report.json) |
| Publication and migration | [Binding/02 release notes](releases/binding-02/RELEASE-NOTES.md) |

## Validate

From this repository, with Python 3.12 in a virtual environment:

```sh
python -m pip install -r scripts/requirements-binding-02.txt
git clone https://github.com/hjs-spec/jep-core.git ../jep-core
# For an existing checkout, use a separate worktree instead of changing its branch.
git -C ../jep-core checkout 32e3321f887d52b5a50942d1eb7a42f618b2771d
python scripts/check-binding-02.py --jep-root ../jep-core
```

The harness checks the pinned Core validator and Schema hashes before execution. It tests real baseline signatures with public synthetic keys, joint structure, TSTO integrity, exact references, termination targets and Core idempotent acceptance. Its external Profile/Policy/Evidence references are illustrative: **domain policy and external truth remain `not_checked`**. It is a conformance fixture, not a production verifier or credential store.

## Versions

| Binding | JEP Core | Status |
| --- | --- | --- |
| [02](bindings/JEP-TSTO-Binding-02.md) | 0.7, wire `1` | Current experimental integration; signed `version/spec` marker |
| [01](bindings/JEP-TSTO-Binding-01.md) | 0.6, wire `1` | [Historical publication](releases/binding-01/RELEASE-NOTES.md); separate signed Schema-URL marker |
| [00](bindings/JEP-TSTO-Binding-00.md) | 0.6 | Historical original; carrier incompatibilities reproduced by the 01 harness |

Select the version explicitly. Wire `jep: "1"` does not distinguish these revisions. Do not rewrite old signatures or retry another decoder after validation fails. The competing unpublished 02 proposals in PRs #5 and #6 are superseded by the main-branch `version/spec` marker and `tsto:target-state-transition` carrier.

Original 00/01 specifications, translations, PDFs, schemas and signed fixtures remain unchanged. The root `SHA256SUMS.txt` and `RELEASE_CHECKLIST.md` describe the original 00 publication, not today's repository index. Each later release has its own manifest under `releases/`.

Use [Issues](https://github.com/cognitive-emergence/tsto-spec/issues) for interoperability findings and [private security advisories](https://github.com/cognitive-emergence/tsto-spec/security/advisories) for sensitive reports. [Contribution rules](CONTRIBUTING.md) · [CC BY 4.0](LICENSE.md) · [Citation](CITATION.cff).
