# JEP-TSTO Binding/01

## 将 JEP-Core 0.6 事件绑定到 TSTO/00 对象

**状态：实验性绑定草案 01，非正式标准**  
**发布日期：2026-09-12**  
**发起方：Cognitive Emergence（认知涌现）**  
**许可：CC BY 4.0**  
**语言地位：英文为规范性文本；中文为资料性译文。如有差异，以英文为准。**

## 摘要

本绑定规定 JEP 的判断（J）、委托（D）、终止（T）和验证（V）事件如何引用不可变的 TSTO/00 目标状态迁移对象，包括载体、签名覆盖、摘要域、三值结果、校验流程和历史兼容。它不修改两个 Core，不证明外部事实，不建立授权，不分配法律责任，也不执行工作或结算资金。

## 1. 状态与规范性用语

本稿用于实现实验、受控试点和公开审阅，不代表 IETF 工作项目、行业共识或正式标准。英文大写 MUST、MUST NOT、REQUIRED、SHOULD、SHOULD NOT、MAY、OPTIONAL 按 BCP 14 解释。中文分别使用“必须”“不得”“应”“不应”“可以”等表达。

## 2. 依赖

实现必须分别满足 JEP-Core 0.6（draft-wang-jep-judgment-event-protocol-06）与 TSTO/00（2026-08-03 实验草案）。随附 Schema 是补充结构校验，不能替代两项依赖及其语义要求。第 17 节明确本次支持的校验路径及范围。

## 3. 分层

| 层 | 职责 |
| --- | --- |
| TSTO/00 | 不可变的对象、证据基线、目标、时间边界、约束和预选验证政策。 |
| JEP-Core | 某个主体在某个时间签署的 J/D/T/V 事件声明。 |
| 本绑定 | TSTO 引用在事件中的准确位置与含义。 |
| JEP / 信任 Profile | 主体、签名密钥、凭证、授权上下文与归档规则。 |
| TSTO Profile | 领域状态投影、路径类型、证据映射与谓词限制。 |
| 结算与法律层 | 付款、责任、救济、可执行性与争议结果。 |

签名有效只能在适用信任规则下证明签署行为，不能单独证明外部事实、授权、法律责任或验证结果正确。

## 4. TSTORef

引用必须恰好包含五个成员，禁止附加成员：

```json
{
  "kind": "external_object",
  "type": "TargetStateTransition",
  "spec": "TSTO/00",
  "id": "urn:uuid:01987654-3210-7abc-8def-0123456789ab",
  "digest": "sha-256:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
}
```

上例摘要仅示意格式。id 必须等于 TSTO 的 id，digest 必须等于其 integrity.value。解析器必须按 id 与 digest 的组合解析并验证，身份冲突必须拒绝；可变 URL 本身不构成绑定。此五成员对象完整保留在第 6 节的外层载体内。

## 5. 两个摘要域

| 对象 | 编码 |
| --- | --- |
| TSTO 内容 | sha-256: 加 43 位无填充 Base64URL。 |
| JEP 完整签名事件 | sha256: 加 64 位小写十六进制。 |

不得直接比较两种字符串，不得把 TSTO 摘要重新标记为 JEP 事件哈希。只有取得正确的原对象并按其规则重新计算，才能产生对应域的摘要。

## 6. 载体与版本标识

保留 JEP 的顶层字段及签名语义。J/D/V 的 ref 必须恰好包含 type 和 value：type 为 TargetStateTransition，value 为完整 TSTORef。T 的 ref 为被终止事件的 JEP 哈希；what.target 必须与它完全相等，what.subject 为受影响的完整 TSTORef。

每个 01 事件必须签署以下非关键扩展：

```json
"ext": {
  "jep-tsto.binding": {
    "id": "https://raw.githubusercontent.com/cognitive-emergence/tsto-spec/main/schemas/jep-tsto-binding-01.schema.json"
  }
}
```

标识对象必须恰好包含 id。消费者必须使用固定版本的本地 Schema，不得根据任意标识 URL 自动抓取或执行内容。该扩展不得列入 ext_crit。理解本绑定的消费者必须校验它；通用 JEP 消费者忽略该非关键扩展后接受事件，不代表通过本绑定。

同一事件不得同时出现历史 prooftask.binding 标识。未实现的关键扩展必须拒绝。整个去掉 sig 的事件，包括 ref、what、ext、存在时的 ext_crit，必须处于 JEP 签名覆盖内。TSTO 的 id 与 digest 因此同时受签名保护；签名外的数据库关联不符合本绑定。

## 7. 判断 J

使用第 6 节的 typed ref。what 必须包含 claim=tsto_judgment，decision 必须为 propose、accept、reject、reassess 之一；可选 reason、context。accept 记录签署者的接受声明，不自行产生法律效力、证明授权或使签署者成为执行方。

## 8. 委托 D

使用第 6 节的 typed ref。what 必须包含 claim=tsto_delegation、非空 delegatee、非空且不重复的 scope 字符串数组；可选 constraints 对象数组、RFC 3339 expiry、termination_conditions 字符串数组。

constraints 中的对象按合取解释，即所有约束同时适用；空数组不增加限制。who 是委托声明人，其实际是否有权委托必须由适用 Profile 或外部法律、组织系统判断。

## 9. 终止 T

ref 必须使用被终止委托或授权事件的 sha256 哈希。what 必须包含 claim=tsto_termination、与 ref 逐字节相等的 target、受影响 TSTORef 的 subject，以及 delegation、authority、future_reliance 之一的 termination_scope；reason 可选。

消费者必须比较 target 与 ref，并按该哈希解析完整签名目标事件。delegation 范围必须指向 D 事件。目标若是 TSTO 绑定事件，其 TSTORef 必须与 subject 相同；其他 authority 或 future_reliance 目标必须由明确支持的 Profile 证明对应同一受影响对象。无法解析或发生冲突必须拒绝。

终止影响授权关系或未来依赖，不得删除、修改或追溯性废除 TSTO。历史事件必须保留用于审计。

## 10. 验证 V

使用第 6 节的 typed ref。what 必须包含 claim=tsto_verification、非空且不重复的 verification_scope、result、policy_ref、非空 evidence 数组；observed_at、reason 可选。

verification_scope 取自 external_evidence、factual_claim、policy_compliance，不得声称超出实际检查的范围。policy_ref 必须以 id 和 digest 匹配 TSTO 预选验证政策。evidence 是不可变证据引用，具体字段按 Schema 和 TSTO/00 解释。

三值映射保持原样：SATISFIED、NOT_SATISFIED、INDETERMINATE。不得把 INDETERMINATE 转为失败。V 记录签署者的验证声明；结果正确性仍取决于证据、政策执行及信任模型。

## 11. 政策与信任分离

必须区分：事先选定的 TSTO verification.policy、事后记录声明的 JEP V 事件、决定事件主体与密钥可信性的 JEP 信任 Profile，以及决定领域状态投影与谓词的 TSTO Profile。签名不能替代政策执行，TSTO 评估成功也不能替代签名及主体信任验证。

## 12. 解析与校验次序

1. 解析 JSON，拒绝重复成员名。
2. 按签名中的标识选定版本，不允许失败后回退；应用声明的 JEP 校验路径，包括字段、动词、nonce、受众与关键扩展。
3. 验证 JEP 签名及适用信任 Profile。
4. 按动词校验本绑定的 ref 与 what。
5. 从 ref.value（J/D/V）或 what.subject（T）取得完整 TSTORef；对 T 检查目标相等与目标事件解析。
6. 按 id 与 digest 共同解析 TSTO。
7. 校验 TSTO Schema、语义约束及 RFC 8785 内容摘要。
8. 存在 policy_ref 时，核对政策 id 和 digest。
9. 对 V 按政策验证证据、范围、时间与三值结果。
10. 按留存政策保存事件及解析证据。

第 2 至 8 步失败必须拒绝其符合性；第 9 步无法确定领域结果时，通常依适用政策产生 INDETERMINATE，不得悄然变成 NOT_SATISFIED。

## 13. 符合性角色

| 角色 | 最低行为 |
| --- | --- |
| Producer | 构造有效事件，签名覆盖引用、声明和版本标识。 |
| Resolver | 按 id 与 digest 解析对象，校验两协议并识别冲突。 |
| Verifier | 执行 TSTO 政策，发出范围正确且保持三值的 V。 |
| Auditor | 使用留存对象、事件、政策、证据和信任材料重放校验。 |

符合性声明必须列明角色及所用 JEP、TSTO Profile。仅通过 Schema 不构成完整符合性。

## 14. 安全与隐私

实现必须考虑引用替换、重放、过期基线、主体或密钥替换、恶意解析器、摘要混淆、可变证据位置、验证范围夸大、未经授权披露、稳定标识关联、恶意 JSON 深度与体积、政策撤回和状态逆转。私有证据可通过访问控制解析；事件应最小化披露。低熵或可猜测内容即使只发布摘要也可能泄漏。

## 15. 版本与历史兼容

本稿版本为 Binding/01；TSTO 仍为 TSTO/00，JEP wire version 仍为 "1"。不兼容修订必须采用新标识及显式解码器支持。

已发布 00 文本、Schema、示例和 PDF 保持不可变。00 的裸 TSTORef、D 对象约束、T 缺少 target 与此次固定的 JEP Schema 存在冲突。明确命名的历史兼容路径仍可验证旧签名，但不能声称旧记录通过当前联合 Schema。

历史候选版使用 prooftask.binding 下的 urn:prooftask:jep-tsto-binding:01-candidate:1。其载体与 01 对齐，但身份不同，不得重新标记为正式 01。

支持历史的消费者必须逐事件选用：明确启用的无标识且载体精确匹配的 00 历史路径、精确候选标识的 candidate.1 路径、精确正式标识的 01 路径。未知标识、双标识、无标识 typed wrapper、有标识旧载体、TSTORef 附加字段都必须拒绝。新版校验失败不得尝试旧版回退。

新增事件必须使用正式标识，包括追加到旧历史的事件。不得修改或重新签署旧字节、签名、哈希、已签发凭证。迁移只能在签署前构造新事件；将旧 D 对象约束转成单元素数组也仅限构造新事件。混合历史须保存每个原事件哈希，并报告其版本。

## 16. 非目标

本绑定不定义执行凭证、编排、市场、定价、结算、法律授权、责任、救济、仲裁或自动付款。依赖这些事件的外部系统需要独立规范与政策。

## 17. 发布材料与校验范围

本次包含正式 01 Schema、固定到 JEP eef317711e0177a64a301bceb1cb6dfd32bf4fc9 的 Schema、副本来源说明、中英文文本、签名合成 J/D/T/V 向量、公开测试密钥、预期哈希、敌对向量、JCS 向量与联合校验程序。

支持的路径对同一个签名事件同时应用两个 Schema，再分别检查签名和语义。JEP 当前 Schema 是其较宽 Core 文本及最小符合性示例的一个实现子集；01 使用该子集。JEP Python seed 单独运行不能替代联合路径，也不执行 TSTO 或外部授权判断。

分别声明两个密码测试 Profile：JOSE alg 严格为 Ed25519 的上游基线，以及 alg 严格为 EdDSA、使用 Ed25519 密钥的 Prooftask recorder 兼容路径。必须显式选择算法；不在所选 Profile 中的算法必须拒绝，改标签会改变签名字节。测试密钥不得用于生产。EdDSA 测试通过不代表上游仅支持 Ed25519 标签的 seed 会接受它。

测试使用合成固定信任，仅覆盖密码与引用完整性；不建立真实主体权限、外部证据真实性、完整 TSTO 政策结果、生产时效与重放保护、结算或真实客户验证。这些仍须由适用角色和部署 Profile 完成。结构无效事件直接拒绝；领域事实缺失只能按相应政策产生 INDETERMINATE。

## 参考

- [英文规范](JEP-TSTO-Binding-01.md)
- [TSTO/00](../SPEC.md)
- [JEP-Core 草案](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
