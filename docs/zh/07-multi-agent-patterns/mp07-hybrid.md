---
id: mp07-hybrid
order: 807
section: multi-agent-patterns
status: planned
title: "Hybrid Multi-Agent Patterns"
description: "真实产品常同时需要入口路由、后台专业计算、直接 Handoff 和质量评价，单一 Pattern 无法覆盖。"
updated_at: 2026-08-24
---

# MP07：Hybrid Multi-Agent Patterns

## 它解决什么问题

真实产品常同时需要入口路由、后台专业计算、直接 Handoff 和质量评价，单一 Pattern 无法覆盖。

## 核心定义

Hybrid 通过清晰边界组合模式：例如 Router 选领域，Specialist 作为 Handoff Owner，再调用后台 Agents as Tools，最终通过 Evaluator。

## 工作原理

为每层指定 control owner、answer owner、context boundary、budget 和 terminal state；避免两个模式同时争夺同一控制权。

## 架构视图

~~~text
Architecture View
Router -> Handoff Specialist -> Agents-as-tools -> Evaluator -> User
~~~

~~~text
Product View
User -> triage -> responsible specialist -> background checks -> verified result
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 hybrid 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

客服 Triage 转退款 Specialist；它调用政策与风险 Agent 作后台检查，合成后直接回复。

## 失败与恢复场景

Manager 与 Handoff Specialist 都认为自己拥有最终答案时产生双回复；通过 active_agent 和 final_owner 状态消除歧义。

## 什么时候使用

不同阶段确有不同控制需求，且团队能测试组合状态时使用。

## 什么时候不要使用

不要为了覆盖 pattern 清单堆叠；简单 Supervisor 能解决就保持简单。

## Trade-offs

最贴合真实需求，也带来最大状态空间和调试成本。

## 产品视角

### 用户与业务问题

在统一体验下获得恰当的专业交互和后台协作。

### 产品价值

分别优化路由、交互、专业质量和验证，而不是让单一角色承担全部。

### 用户体验

用户只看到与任务有关的阶段和负责人变化，内部子调用保持折叠。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

可用图/状态机组合 SDK 的 agents-as-tools 与 handoffs；先画控制图再写 API。

## Related Patterns

Workflow Composition、Graph Orchestration、Reliability、Evaluation。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

给组合图每条边标注 current owner，找出任何双重所有权。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
