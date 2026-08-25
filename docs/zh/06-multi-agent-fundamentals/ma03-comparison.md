---
id: ma03-comparison
slug: zh/06-multi-agent-fundamentals/ma03-comparison
order: 703
section: multi-agent-fundamentals
status: planned
title: "Single Agent vs Modular Single Agent vs Multi-Agent"
description: "工具函数、Prompt 模块和独立 Agent 常被混为一谈，导致系统宣称 Multi-Agent 却没有真实决策边界。"
updated_at: 2026-08-24
---

# MA03：Single Agent vs Modular Single Agent vs Multi-Agent

## 它解决什么问题

工具函数、Prompt 模块和独立 Agent 常被混为一谈，导致系统宣称 Multi-Agent 却没有真实决策边界。

## 核心定义

Single Agent 只有一个决策上下文；Modular Single Agent 仍由一个主体控制，只把能力封装成模块；Multi-Agent 存在多个独立角色或上下文，并通过协议协作。

## 工作原理

比较 decision owner、context owner、tool scope、state owner、final answer owner 和 failure isolation 六项，而不是数类或函数。

## 架构视图

~~~text
Architecture View
Single: one context -> many tools
Modular: one controller -> bounded modules
Multi: multiple contexts/decisions -> coordination
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 comparison 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

客服入口由一个 Agent 决策，退款计算是确定性模块，法律分析才由隔离 Specialist 完成。

## 失败与恢复场景

把每个函数包装成 Agent 后，调用与摘要增加但没有新边界；恢复为模块并保留一个 Controller。

## 什么时候使用

在设计评审和框架迁移时用统一维度比较。

## 什么时候不要使用

不要仅因多个模型调用就称 Multi-Agent，也不要因同一进程就否认独立 Agent。

## Trade-offs

模块化单 Agent通常是中间最优点；Multi-Agent 才提供强隔离与自治，也承担更高协调成本。

## 产品视角

### 用户与业务问题

保持统一体验，同时只在确有价值处引入 Specialist。

### 产品价值

避免过度架构，并让复杂度升级路径可测。

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

Agent.as_tool 可能是真 Specialist，也可能只是昂贵函数；应检查其上下文和决策权。

## Related Patterns

Why Multi-Agent、Agents as Tools、Handoff。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

给现有组件填写六维边界表并重新命名。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
