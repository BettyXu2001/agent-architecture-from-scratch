---
id: ma06-economics
slug: zh/06-multi-agent-fundamentals/ma06-economics
order: 706
section: multi-agent-fundamentals
status: planned
title: "Context、Cost and Failure Radius"
description: "Multi-Agent 可能节省单个上下文，却增加重复前缀、通信和合成；一个错误委派还会沿链级联。"
updated_at: 2026-08-24
---

# MA06：Context、Cost and Failure Radius

## 它解决什么问题

Multi-Agent 可能节省单个上下文，却增加重复前缀、通信和合成；一个错误委派还会沿链级联。

## 核心定义

Context Budget 衡量各 Agent 实际可见信息；Cost 包含模型、工具、协调和等待；Failure Radius 是单个错误影响的任务、数据与副作用范围。

## 工作原理

为每个角色记录 input/output token、调用、延迟、共享数据和下游依赖；设置并发、深度、重试和委派预算。

## 架构视图

~~~text
Architecture View
Agent metrics -> coordinator budget -> bounded delegation graph -> outcome
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 economics 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

两个独立 Specialist 并行，各看少量相关资料，总墙钟时间下降且合成一次。

## 失败与恢复场景

Supervisor 反复委派相同任务，子 Agent 又递归委派，调用爆炸；使用 task fingerprint、depth 和 global budget 终止。

## 什么时候使用

在采用和运营 Multi-Agent 时持续做总成本与影响半径评估。

## 什么时候不要使用

不要只看单 Agent token，也不要以并行墙钟时间掩盖总资源。

## Trade-offs

隔离减少单上下文噪声，却产生重复背景；冗余提高韧性，也可能放大同源错误。

## 产品视角

### 用户与业务问题

复杂系统仍需给用户可预测等待、成本和失败承诺。

### 产品价值

确保额外 Agent 真正换来成功率或时间收益。

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

Tracing 能收集调用树，但产品指标和全局预算必须由应用定义。

## Related Patterns

Scheduling、Reliability、Evaluation、Hierarchical Depth。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

为同一任务比较总 Token、墙钟时间和失败下游数量，而非只比答案。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
