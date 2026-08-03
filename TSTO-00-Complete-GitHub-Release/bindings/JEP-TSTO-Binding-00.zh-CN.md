# JEP-TSTO Binding/00

## JEP-Core 0.6 事件与 TSTO/00 对象绑定规范

**状态：Experimental Binding Draft 00（实验性绑定草案，不是正式标准）**  
**发布日期：2026-08-03**  
**发起方：认知涌现（Cognitive Emergence）**  
**许可：Creative Commons Attribution 4.0 International（CC BY 4.0）**  
**语言地位：本中文文本为信息性翻译；发生歧义时以英文规范文本为准。**

---

## 摘要

本文件定义 JEP-Core 0.6 的 Judgment、Delegation、Termination 和 Verification 事件声明如何绑定不可变的 TSTO/00 目标状态迁移对象。它规定承载位置、签名覆盖、两种摘要编码、三值验证映射、校验顺序和示例。

本 Binding 不修改 JEP-Core 或 TSTO Core，也不证明外部事实、建立授权、分配法律责任、执行任务或结算资金。

## 1. 状态与规范性用语

本文件用于原型和封闭试点，不是 IETF 工作项、行业共识或正式标准。全大写的 **MUST、MUST NOT、REQUIRED、SHOULD、SHOULD NOT、MAY、OPTIONAL** 按 BCP 14 解释。

## 2. 依赖

实现本 Binding 必须分别符合：

- JEP-Core 0.6，即 `draft-wang-jep-judgment-event-protocol-06`；
- 2026-08-03 发布的 TSTO/00 Experimental Draft 00。

随附 Schema 只用于补充结构校验，不能替代对两个基础规范的独立校验。

## 3. 分层

| 层 | 职责 |
| --- | --- |
| TSTO/00 | 不可变地表达 Subject、Baseline、Target、时间、Constraints 与预先指定的 Verification Policy。 |
| JEP-Core 0.6 | 记录某主体在某时间作出的 J、D、T 或 V 签名事件声明。 |
| 本 Binding | 规定每类 JEP 事件怎样准确引用 TSTO。 |
| JEP Profile / Trust Profile | 规定事件主体、密钥、凭证、授权上下文、归档等互操作规则。 |
| TSTO Profile | 规定领域 State Projection、路径、类型、证据和谓词。 |
| 结算或法律层 | 规定付款、责任、救济、效力和争议结果。 |

有效 JEP 签名证明适用信任规则下谁签署了事件内容；它不自行证明外部事实、授权有效、法律责任或 TSTO 验证结论正确。

## 4. TSTO 引用

本 Binding 使用以下 `TSTORef`：

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

五个成员全部 REQUIRED，Binding/00 禁止增加其他成员。`id` 必须等于 TSTO `id`，`digest` 必须等于 TSTO `integrity.value`。Resolver 必须按照 `id + digest` 解析并校验，发现同一 `id` 对应不同摘要时拒绝处理。仅有可变 URL 不构成绑定。

## 5. 摘要域

| 对象 | 编码 |
| --- | --- |
| TSTO 内容 | `sha-256:` 加 43 个无填充 Base64URL 字符。 |
| JEP 事件哈希 | `sha256:` 加 64 个小写十六进制字符。 |

实现不得直接字符串比较两者，不得在未取得并散列正确底层对象时相互转换，也不得把 TSTO 摘要标记为 JEP event hash。

## 6. JEP 承载规则

JEP 事件必须保留 JEP-Core 0.6 的真实顶层字段和签名语义：

| Verb | `ref` | `what` |
| --- | --- | --- |
| J | `TSTORef` | `tsto_judgment` 声明。 |
| D | `TSTORef` | `tsto_delegation` 声明。 |
| T | 被终止的 Delegation 或 authority 事件的 JEP event hash | `tsto_termination` 声明，并在 `subject` 中放入受影响的 `TSTORef`。 |
| V | `TSTORef` | `tsto_verification` 声明，包含 scope、Policy、Evidence 和三值结论。 |

完整未签名 JEP 事件中的 `ref` 与 `what` 必须进入 JEP 签名覆盖范围，因此 TSTO 的 `id` 与 `digest` 同时被签名。签名范围外的数据库关联不符合本规范。

## 7. Judgment（`verb = J`）

`ref` 必须是 `TSTORef`。`what.claim` 必须为 `tsto_judgment`，`decision` 必须为 `propose`、`accept`、`reject` 或 `reassess`；可选 `reason` 和 `context`。

`accept` 只记录签名者作出的接受声明，不自行产生法律可执行性、证明授权或把签名者变成执行者。

## 8. Delegation（`verb = D`）

`ref` 必须是 `TSTORef`。`what` 必须包含 `claim = tsto_delegation`、非空 `delegatee` 和非空 `scope`；可以包含 `constraints`、RFC 3339 `expiry` 与 `termination_conditions`。

`who` 是委托声明的作出者。本 Binding 不证明其拥有外部委托权限，该问题必须由 JEP Profile 或外部法律、组织系统处理。

## 9. Termination（`verb = T`）

`ref` 必须是被终止的 Delegation 或 authority 事件的 JEP event hash，使用 `sha256:<lowercase-hex>`。`what` 必须包含 `claim = tsto_termination`、`subject` 中的 `TSTORef` 和 `termination_scope`；`termination_scope` 只能是 `delegation`、`authority` 或 `future_reliance`。可选 `reason`。

Termination 影响被引用的权限关系或未来依赖，不得删除、修改或追溯性取消 TSTO。历史事件必须保留以供审计。

## 10. Verification（`verb = V`）

`ref` 必须是 `TSTORef`。`what` 必须包含：

- `claim = tsto_verification`；
- 非空 `verification_scope`，元素取自 `external_evidence`、`factual_claim`、`policy_compliance`；
- `result`，只能是 `SATISFIED`、`NOT_SATISFIED` 或 `INDETERMINATE`；
- `policy_ref`，同时绑定 TSTO 所引用 Verification Policy 的 `id + digest`；
- 非空 `evidence` 引用数组；
- 可选 `observed_at` 与 `reason`。

必须按照 JEP-Core 要求明确声明 `verification_scope`，验证者不得声称超出实际验证范围。三值结果按同名值一一对应；`INDETERMINATE` 不得映射为失败。

V 事件记录签名者作出的、有明确范围的验证声明；结论正确性仍依赖 Evidence、Policy 执行和适用信任模型。

## 11. Policy 与信任分离

以下对象必须分离：

1. TSTO `verification.policy`：结果评估前固定的领域事实规则；
2. JEP Verification：评估后生成的签名事件声明；
3. JEP Profile 或 Trust Profile：主体、密钥、凭证等事件级信任规则；
4. TSTO Profile：领域 State Projection、路径、类型、证据与谓词规则。

签名有效不能替代 TSTO Policy 求值；TSTO 求值成功也不能替代 JEP 签名与主体信任校验。

## 12. 解析与校验顺序

符合规范的消费方至少必须依次：

1. 解析 JSON 并拒绝重复成员；
2. 按 JEP-Core 0.6 校验事件，包括 verb、nonce、audience 和 critical extensions；
3. 验证 JEP 签名与适用 JEP/Trust Profile；
4. 按 verb 校验 Binding 的 `ref` 与 `what`；
5. 从 `ref` 取得 `TSTORef`，T 事件则从 `what.subject` 取得；
6. 按 `id + digest` 解析 TSTO；
7. 校验 TSTO/00 Schema、语义约束和 RFC 8785 内容摘要；
8. 验证 `policy_ref` 与 TSTO `verification.policy` 的 `id + digest` 完全一致；
9. 对 V 事件校验证据、scope、时间与 Policy 下三值结果；
10. 按保留策略保存事件与解析证据。

步骤 2 至 8 失败必须拒绝其 Binding 合规性。步骤 9 无法形成领域结论通常应产生 `INDETERMINATE`，不得静默改成 `NOT_SATISFIED`。

## 13. 合规角色

| 角色 | 最低行为 |
| --- | --- |
| Producer | 构造有效 JEP 事件，并使 `ref` 与 `what` 进入签名覆盖。 |
| Resolver | 按 `id + digest` 解析 TSTO，校验双方协议并检测冲突。 |
| Verifier | 执行 TSTO Policy，生成 scope 准确、三值映射无损的 V 事件。 |
| Auditor | 使用保留的事件、对象、Profile、Policy、Evidence 与信任材料重放校验。 |

合规声明必须同时说明使用的 JEP Profile 与 TSTO Profile。仅通过补充 Schema 不构成合规声明。

## 14. 安全与隐私

实现必须处理引用替换、重放、陈旧 Baseline、主体或密钥替换、恶意 Resolver、摘要混淆、可变证据地址、过宽 Verification scope、未授权披露、稳定标识符关联、恶意 JSON 深度或大小、Policy 撤销和状态逆转。

私有证据可保留在受控 Resolver 后。事件应仅向其 audience 暴露必要声明和引用。若输入空间可猜测，摘要并不能使个人或机密数据适合公开。

## 15. 版本与扩展

本 Binding 标识为 `JEP-TSTO Binding/00`。不兼容修改必须发布新版本。扩展必须使用 JEP 扩展和 critical-extension 机制，不得增加含义不明的未保护字段，也不得修改 TSTO Core。

## 16. 非目标

本 Binding 不定义执行回执、任务编排、市场、定价、结算、法律授权、责任、救济、仲裁或自动付款。这些系统可以依赖合规事件，但需要独立规范与 Policy。

## 17. 示例与 Schema

发布包提供补充结构 Schema，以及 J、D、T、V 四类 JSON 示例。示例 `sig` 明确标为未签名，不是加密测试向量；生产事件必须包含有效 JEP 签名。

## 参考资料

- [Judgment Event Protocol, JEP-Core 0.6](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/)
- [JEP Profiles and Interoperability](https://datatracker.ietf.org/doc/draft-wang-jep-profiles/)
- [JEP Conformance and Test Suite](https://datatracker.ietf.org/doc/draft-wang-jep-conformance/)
- [TSTO/00](../SPEC.md)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)
