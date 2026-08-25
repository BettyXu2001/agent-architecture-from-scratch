---
id: mp03-router-parallel
slug: zh/07-multi-agent-patterns/mp03-router-parallel
order: 803
section: multi-agent-patterns
status: planned
title: "Router and Parallel Specialists"
description: "请求可能涉及一到多个独立领域；串行 Supervisor 会增加等待，单选 Router 又可能漏掉多意图。"
updated_at: 2026-08-24
---

# MP03：Router and Parallel Specialists

## 它解决什么问题

请求可能涉及一到多个独立领域；串行 Supervisor 会增加等待，单选 Router 又可能漏掉多意图。

## 核心定义

Router 输出一个或多个 Specialist 目标；独立目标并行执行，Join 根据 all、quorum 或 best-effort 合成。

## 工作原理

使用多标签路由和置信度；去重目标、限制 fan-out；每支返回统一 Result Packet，聚合器保留失败。

## 架构视图

~~~text
Architecture View
Request -> multi-label Router -> [A | B | C] -> Join -> Finalizer
~~~

~~~text
Product View
User -> request -> selected checks in parallel -> combined result with gaps
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 router-parallel 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

用户同时询问退款和账户安全，两个 Specialist 并行回复，Finalizer 合成。

## 失败与恢复场景

Router 为模糊请求选中全部角色导致调用爆炸；用阈值、最大分支和澄清控制。

## 什么时候使用

子任务独立、可在输入时识别、并行能降低等待时使用。

## 什么时候不要使用

角色强依赖或下一角色必须基于前一结果动态选择时用 Supervisor。

## Trade-offs

低墙钟时间但高瞬时资源；路由漏选和多选都会影响结果。

## 产品视角

### 用户与业务问题

一个请求包含多个问题时无需用户逐个提交。

### 产品价值

在扩大专业覆盖的同时缩短等待。

### 用户体验

显示并行检查维度和完成/缺失状态，合成后仍是一份结果。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

结构化分类+asyncio 即可；图框架 fan-out/fan-in 或 Google ParallelAgent 可承载。

## Related Patterns

Routing、Parallelization、Supervisor、Join。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

加入多意图与低置信度输入，避免默认 fan-out 到所有 Agent。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
