---
id: mp04-handoff
order: 804
section: multi-agent-patterns
status: planned
title: "Handoff"
description: "某些 Specialist 需要直接与用户连续交流；Manager 代传每句话会损失细节、增加延迟和上下文。"
updated_at: 2026-08-24
---

# MP04：Handoff

## 它解决什么问题

某些 Specialist 需要直接与用户连续交流；Manager 代传每句话会损失细节、增加延迟和上下文。

## 核心定义

Handoff 是活动 Agent、指令和对话所有权的显式转移。转移后 Specialist 直接处理当前会话，直到完成或交回。

## 工作原理

Triage 选择目标并生成 handoff packet；Runtime 记录 from/to/reason/context_scope；接收者确认能力并成为 active_agent。

## 架构视图

~~~text
Architecture View
User <-> Triage --handoff--> Specialist <-> User
                     <--return----
~~~

~~~text
Product View
User -> triage -> visible transfer -> specialist conversation -> resolved/returned
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 handoff 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

退款问题转给退款 Specialist，用户可继续补充订单信息而无需经 Triage 中转。

## 失败与恢复场景

两个 Agent 相互 Handoff 形成 ping-pong；使用 visited_agents、handoff budget 和 owner escalation 停止。

## 什么时候使用

专业角色需要多轮直接交互、语气/工具差异显著时使用。

## 什么时候不要使用

用户需要统一答案、子任务只是后台计算或转移会破坏体验时用 agents-as-tools。

## Trade-offs

上下文更专注、对话更直接，但所有权变化与跨角色连续性更难。

## 产品视角

### 用户与业务问题

用户能快速进入真正解决问题的专业服务。

### 产品价值

减少中间转述和重复澄清。

### 用户体验

明确告诉用户已转到哪个能力、为何转、已携带哪些信息，并允许返回。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

OpenAI Agents SDK handoffs、LangChain handoffs、AutoGen Swarm 的交接均可实现。

## Related Patterns

Router、Agents as Tools、Human Handoff。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

模拟接收者拒绝任务与双向 ping-pong，验证可恢复。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
