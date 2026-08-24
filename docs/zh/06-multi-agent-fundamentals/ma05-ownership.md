---
id: ma05-ownership
order: 705
section: multi-agent-fundamentals
status: planned
title: "Final Answer Ownership"
description: "多个 Agent 都能输出时，用户会收到重复、矛盾或无人负责的答案。必须有唯一可解释的最终答案所有权。"
updated_at: 2026-08-24
---

# MA05：Final Answer Ownership

## 它解决什么问题

多个 Agent 都能输出时，用户会收到重复、矛盾或无人负责的答案。必须有唯一可解释的最终答案所有权。

## 核心定义

Final Answer Owner 负责合成、解决冲突、检查要求、标注缺口并向用户交付；它可以是 Manager、当前 Handoff Specialist 或代码聚合器。

## 工作原理

在运行前声明 owner；各 Worker 只能返回 Result Packet。Owner 使用用户目标与证据合成，不能隐藏失败或无来源结论。

## 架构视图

~~~text
Architecture View
Workers -> result packets -> Final Answer Owner -> User
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 ownership 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

Manager 合成研究与合规结果，明确一项来源缺失，并给用户下一步选择。

## 失败与恢复场景

两个 Specialist 直接回复导致口径冲突；编排器拦截 Worker 输出，只允许 owner 交付。

## 什么时候使用

所有 Multi-Agent 产品都必须明确；Handoff 场景还要说明所有权何时转移。

## 什么时候不要使用

不要用多数投票替代责任归属；票数不保证事实正确。

## Trade-offs

集中所有权保证一致体验，却可能形成合成瓶颈；分散所有权更直接但易割裂。

## 产品视角

### 用户与业务问题

用户始终知道谁在回答、结果是否完整以及缺口由谁处理。

### 产品价值

减少矛盾输出和用户自行合成的负担。

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

Manager pattern 保留所有权；Handoff 将所有权转给 Specialist；Group Chat 需额外 termination 和 finalizer。

## Related Patterns

Supervisor、Handoff、Evaluator、Conflict Resolution。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

注入互相矛盾的 Worker 结果，要求 Owner 保留证据差异而非随意选择。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
