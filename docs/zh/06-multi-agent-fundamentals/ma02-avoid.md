---
id: ma02-avoid
slug: zh/06-multi-agent-fundamentals/ma02-avoid
order: 702
section: multi-agent-fundamentals
status: planned
title: "When Not to Use Multi-Agent"
description: "Multi-Agent 容易在 Demo 中显得聪明，却可能把一个 Prompt 问题放大成分布式协调问题。"
updated_at: 2026-08-24
---

# MA02：When Not to Use Multi-Agent

## 它解决什么问题

Multi-Agent 容易在 Demo 中显得聪明，却可能把一个 Prompt 问题放大成分布式协调问题。

## 核心定义

不使用 Multi-Agent 是一项主动架构决策：当瓶颈可由更好的任务定义、工具、Context、Workflow 或模块化单 Agent 解决时，保持单一决策主体。

## 工作原理

建立 Single Agent 基线，按成功、成本、延迟和失败半径与 Multi-Agent 方案对比；没有显著增益就回退。

## 架构视图

~~~text
Architecture View
Problem -> prompt/context/tool fix? -> modular single? -> only then multi-agent
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 avoid 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

工具过多导致选择错误，通过 Router 只暴露相关工具后成功率恢复，无需新增 Agent。

## 失败与恢复场景

三个 Agent 互相复述并投票，成本三倍却共享同一盲点；删除冗余角色并使用独立确定性校验。

## 什么时候使用

把本章作为每次 Multi-Agent 评审的反方检查。

## 什么时候不要使用

不要把“任务复杂”直接等同“需要多个 Agent”；复杂但紧耦合的任务反而更适合单一上下文。

## Trade-offs

保持简单牺牲少量专业并行，但显著降低状态空间、故障和运营成本。

## 产品视角

### 用户与业务问题

用户需要稳定完成，不需要内部组织图。

### 产品价值

用更低成本和更短等待达到相同结果。

### 用户体验

默认向用户呈现一个连续的产品身份、统一进度与最终结果；只有 Specialist 身份有助于信任或接管时才展示内部角色。

### 自主性边界

每个 Agent 只能在角色、工具和预算范围内行动；跨角色委派、扩大任务范围和高风险副作用由编排与策略层约束。

### 数据与权限

Private Context 默认隔离，共享仅通过结构化结果或 Artifact。角色专业化不能成为复制全部用户数据的理由。

### 失败与降级

单个 Specialist 失败时标注缺口、重试或退回 Manager；必要时合并回 Single Agent、返回部分结果或转人工。

### 产品指标

除任务成功率外，比较调用数、总 Token、墙钟时间、协调开销、用户修正率、部分失败恢复率和单成功任务成本。

## 框架中的对应实现

任何框架都不能消除协调开销；框架示例不是采用证据。

## Related Patterns

Architecture Decision、Workflow vs Agent、Tool Routing。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

尝试用 Context Selection 与工具分组解决一个拟拆分问题。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
