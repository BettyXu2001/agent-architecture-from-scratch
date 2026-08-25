---
id: ma01-why
slug: zh/06-multi-agent-fundamentals/ma01-why
order: 701
section: multi-agent-fundamentals
status: planned
title: "Why Multi-Agent?"
description: "单 Agent 在工具过多、上下文过长、专业目标冲突或独立子任务较多时会成为瓶颈，但拆 Agent 本身并不创造价值。"
updated_at: 2026-08-24
---

# MA01：Why Multi-Agent?

## 它解决什么问题

单 Agent 在工具过多、上下文过长、专业目标冲突或独立子任务较多时会成为瓶颈，但拆 Agent 本身并不创造价值。

## 核心定义

Multi-Agent System 包含多个拥有独立角色、上下文或局部决策能力的 Agent，并需要额外的委派、通信、协调、终止与结果归属机制。

## 工作原理

先定位单 Agent 的实证瓶颈，再选择专业化、隔离、并行或组织边界中的一种主要拆分理由；定义通信契约与统一验收。

## 架构视图

~~~text
Architecture View
Goal -> Coordinator -> [Specialist A | Specialist B] -> Synthesis
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 why 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

研究任务中财务和政策资料互不依赖、上下文差异大，两个 Specialist 并行产出带来源 Artifact，由 Manager 合成。

## 失败与恢复场景

只是把同一提示词复制三份时，结果重复且互相矛盾；恢复方法是合并回单 Agent或重定义真正不同的职责。

## 什么时候使用

专业化显著提高质量、上下文隔离降低干扰、并行缩短长任务，或团队/信任边界必须分开时使用。

## 什么时候不要使用

单 Agent 加模块、工具路由或 Workflow 已足够时不要拆。

## Trade-offs

获得隔离、专业化和并行，同时付出通信、合成、延迟、调用数和级联错误。

## 产品视角

### 用户与业务问题

解决复杂目标需要多种专业工作，但用户不应承担手工协调。

### 产品价值

以相同用户操作获得更完整、更快或更可信的结果。

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

Agents-as-tools、Supervisor、Handoff 和 Team 都可实现；模式选择取决于控制权，不取决于框架是否称其为 multi-agent。

## Related Patterns

Single vs Modular、Supervisor、Parallel Specialists、Context Isolation。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

列出单 Agent 的失败样本，并为每个拟新增 Agent 写一条可证伪收益假设。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
