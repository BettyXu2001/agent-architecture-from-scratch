---
id: P01
title: 从 AI 功能到 Agent 产品
lang: zh
status: draft
audience: [product-manager, ai-application-builder]
prerequisites: []
concepts: [ai-feature, workflow, agent, autonomy]
example: examples/product-decisions/agent_product_classifier.py
last_reviewed: 2026-08-24
---

# P01：从 AI 功能到 Agent 产品

很多团队拿到 AI 需求后，第一个问题是：“应该用单 Agent 还是 Multi-Agent？”

这个问题通常问早了。更应该先问的是：

> 用户需要的是一次生成、一条稳定流程，还是一个能根据环境动态决定下一步的执行者？

这三种形态都能做出好产品，但它们的成本、可控性和用户体验完全不同。本章建立整套课程最重要的产品判断：**不要把所有 AI 功能都做成 Agent，也不要因为任务复杂就直接使用 Multi-Agent。**

## 用户场景

假设团队收到四个需求：

1. 用户粘贴会议记录，产品生成摘要。
2. 系统读取发票、校验字段，再写入 ERP。
3. 用户给出研究主题，产品自主搜索、比较来源并生成报告。
4. 事故发生后，系统同时调查代码变更、历史事故和服务指标，再合成处置建议。

它们都可以被称为“AI 应用”，但更合适的基础架构分别是：

| 需求 | 优先形态 | 原因 |
|---|---|---|
| 会议摘要 | 普通 AI 功能 | 一次输入对应一次输出 |
| 发票处理 | Workflow | 步骤稳定，业务规则明确 |
| 研究助手 | Single Agent | 下一步取决于搜索结果和证据质量 |
| 事故调查 | Multi-Agent 候选 | 多个独立专业方向可能并行工作 |

这里的“优先形态”不是最终技术选型，而是最小可行起点。团队应该先验证它能否解决问题，再决定是否升级复杂度。

## 产品视角

### 用户问题

用户通常并不在意产品背后有几个 Agent。他们关心的是：

- 能不能完成任务；
- 要等多久；
- 结果是否可信；
- 出错后能否修改；
- 产品会不会未经允许采取行动。

因此，Agent 不是一个面向用户的价值主张。“更少操作地完成更长、更动态的任务”才可能是价值主张。

### 产品价值

只有当 Agent 的动态决策能力带来以下一种或多种收益时，它才值得被引入：

- 用户不需要手动指定每一步；
- 系统能根据中间结果改变计划；
- 产品能够跨多个工具完成闭环任务；
- 信息不足时能够主动追问；
- 失败后能够换方法继续，而不是直接结束。

如果步骤可以提前写清楚，Workflow 往往更稳定、更便宜，也更容易解释。

### 用户体验

不同架构对应不同的产品体验：

```text
普通 AI 功能：输入 -> 等待 -> 输出

Workflow：输入 -> 固定步骤进度 -> 输出 / 某一步失败

Agent：目标 -> 计划或下一步 -> 动态执行 -> 追问/确认 -> 结果
```

一旦使用 Agent，产品通常需要增加计划、进度、来源、确认、取消、部分结果和失败恢复等界面状态。Agent 架构不是只增加后端能力，也会增加前端产品责任。

### 自主性边界

“能够动态决定下一步”不等于“可以自动执行所有动作”。可以把自主性拆成四级：

| 等级 | Agent 可以做什么 | 产品例子 |
|---|---|---|
| L0 建议 | 只生成建议，不执行 | 推荐回复草稿 |
| L1 准备 | 准备操作，等待用户确认 | 填好邮件但不发送 |
| L2 有界执行 | 在明确范围内自动行动 | 只读检索、低风险更新 |
| L3 高自主 | 长时间执行并处理异常 | 后台研究、受限自动化 |

产品应该分别定义“决策权限”和“执行权限”，而不是只有一个模糊的 Agent 开关。

### 数据与权限

在需求评审时至少列出：

- Agent 可以读取哪些用户数据；
- 可以调用哪些外部系统；
- 哪些数据会进入模型上下文；
- 哪些信息会被长期保存；
- 哪些动作会产生不可逆副作用。

如果这些问题没有答案，就还不适合提高自主性。

### 失败与降级

每一种架构都需要不同的降级方式：

- AI 功能失败：允许用户重新生成或手动编辑；
- Workflow 失败：指出具体步骤，支持从该步骤重试；
- Agent 失败：返回已完成工作、当前状态和阻塞原因；
- Multi-Agent 失败：标明哪个专业任务失败，避免整个系统静默给出残缺结论。

产品不应该只设计 happy path。Agent 越自主，越需要让用户在失败后重新获得控制权。

### 产品指标

架构是否值得，至少应通过以下指标验证：

| 指标 | 回答的问题 |
|---|---|
| Task Success Rate | 用户目标是否真正完成？ |
| Time to Completed Outcome | 从发起到可用结果需要多久？ |
| User Correction Rate | 用户需要修改多少内容或步骤？ |
| Human Intervention Rate | 多少任务需要人工接管？ |
| Cost per Successful Task | 每个成功任务花费多少？ |
| Unsafe / Unwanted Action Rate | 是否发生越权或非预期操作？ |

不要只比较模型回答质量。一个回答更漂亮但完成率更低、等待更久或更难修正的 Agent，未必是更好的产品。

### 采用判断

适合从 Agent 开始的信号：

- 下一步高度依赖实时观察结果；
- 无法提前枚举完整执行路径；
- 用户愿意用一定等待时间换取任务闭环；
- 成功与失败可以被观察或验证；
- 工具和动作存在清晰权限边界。

不建议使用 Agent 的信号：

- 需求本质是单次生成或抽取；
- 步骤和业务规则非常稳定；
- 错误成本高，但结果又难以验证；
- 产品无法向用户展示进度和恢复方式；
- 团队还没有基本 eval、日志和权限控制。

## 最小架构理论

### 普通 AI 功能

模型完成一次有边界的转换：

```text
input -> model -> output
```

模型不拥有任务控制权，也不决定后续执行路径。

### Workflow

代码拥有控制权，模型只是某些步骤中的能力：

```text
input -> step A -> model -> rule -> step B -> output
```

即使 Workflow 包含多个模型调用，它仍然不一定是 Agent。

### Agent

模型或模型驱动的策略能够根据目标、当前状态和观察结果选择下一步：

```text
goal -> decide -> act -> observe -> update state
          ^                         |
          +-------------------------+
```

OpenAI Agents SDK 的编排文档也区分由代码决定流程和由 LLM 决定流程；两者可以混合使用。[OpenAI Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)

### Multi-Agent

多个具有独立上下文、角色或行动能力的 Agent 共同完成任务。它可能提供专业化、隔离或并行，但也会增加调用、通信和验证成本。复杂任务并不自动意味着需要 Multi-Agent；单 Agent 配合合适的工具和动态上下文可能已经足够。[LangChain multi-agent overview](https://docs.langchain.com/oss/javascript/langchain/multi-agent/index)

## 产品体验流

以研究助手为例：

```text
用户提交研究目标
    -> 产品展示理解结果和范围
    -> Agent 给出计划
    -> 用户确认高成本或敏感步骤
    -> 产品持续展示进度与来源
    -> Agent 发现信息不足时追问
    -> 返回报告和可检查的引用
    -> 用户修正、继续或导出
```

产品层看到的是目标、计划、进度、确认和结果，而不是内部的每一次模型调用。

## 系统执行流

```text
User Goal
    |
    v
Product Policy -----> Permission / Budget
    |
    v
Workflow or Agent Controller
    |           |
    |           +----> Tool / Knowledge
    |                       |
    +<------ Observation ---+
    |
    v
Typed State -> Progress Events -> Product UI
    |
    v
Result / Partial Result / Human Handoff
```

产品策略层位于 Agent 控制器之外。预算、权限和高风险操作不应只依赖模型自行遵守。

## 最小可运行实践

本章提供一个不调用模型的架构建议器：

```bash
python examples/product-decisions/agent_product_classifier.py
```

它根据步骤是否稳定、是否需要动态决策、是否存在多个独立专业任务，以及是否包含高风险动作，给出一个起始架构和产品提醒。

这个工具不是自动替产品团队做决定，而是把需求评审中的隐含判断显式化。

## 正常场景

对于“自主搜索并根据证据调整方向的研究助手”，判断器会建议从 Single Agent 开始，因为执行路径取决于中间观察结果。

对于“读取发票、校验字段、写入 ERP”，判断器会建议 Workflow，因为步骤稳定。写入动作可以增加审批，但没有必要仅因为调用了外部系统就改成 Agent。

## 失败与降级场景

一个常见错误是把固定发票流程实现为高度自主的 Agent：

- 相同输入可能选择不同步骤；
- 很难定位哪一步违反业务规则；
- 重试可能造成重复写入；
- 用户只看到“Agent 失败”，不知道如何恢复。

更好的降级是回到确定性 Workflow，只在无法识别字段时调用模型或请求人工确认。

另一个错误是因为任务涉及多个领域就直接使用 Multi-Agent。如果这些领域不需要独立上下文，也不需要并行执行，一个 Agent 按顺序调用多个工具通常更简单。

## 产品指标与架构对比

选取 20–50 个真实任务，分别运行最简单版本和 Agent 版本：

| 维度 | 基线版本 | Agent 版本 |
|---|---:|---:|
| 任务成功率 | 记录 | 记录 |
| 完成时间 P50 / P95 | 记录 | 记录 |
| 用户操作次数 | 记录 | 记录 |
| 人工接管率 | 记录 | 记录 |
| 单成功任务成本 | 记录 | 记录 |
| 严重失败数 | 记录 | 记录 |

只有当 Agent 在关键用户指标上产生稳定收益，并且收益大于复杂度成本时，才继续升级架构。

## 上线检查清单

- 用户问题是否经过真实场景验证？
- 普通生成或 Workflow 是否已经足够？
- 动态决策具体发生在哪一步？
- 用户能否看到进度并取消任务？
- 高风险操作是否有外部审批边界？
- 失败时能否返回部分结果、重试或转人工？
- 是否有任务成功率和单成功任务成本基线？

## 小结

AI 功能、Workflow、Agent 和 Multi-Agent 不是能力高低排名，而是不同的产品控制方式。

最好的起点通常不是最智能的架构，而是能够验证用户价值、保持可控，并为下一次演进留下空间的最小架构。

下一篇将进一步比较 Chat、Workflow 与 Agent，并给出更具体的产品选择矩阵。

## 延伸练习与参考资料

1. 从你负责的产品中选择三个 AI 需求，为它们填写架构判断表。
2. 找出其中一个被设计成 Agent、但可能可以降级为 Workflow 的需求。
3. 为一个高风险动作分别设计 L0 建议、L1 准备和 L2 有界执行体验。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/javascript/langchain/multi-agent/index)
- [Anthropic：Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents)
