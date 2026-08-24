---
id: mp01-agents-as-tools
order: 801
section: multi-agent-patterns
status: planned
title: "Subagents / Agents as Tools"
description: "主 Agent 需要专业帮助，但仍需保持用户关系、全局目标和最终答案控制权。"
updated_at: 2026-08-24
---

# MP01：Subagents / Agents as Tools

## 它解决什么问题

主 Agent 需要专业帮助，但仍需保持用户关系、全局目标和最终答案控制权。

## 核心定义

Specialist 被封装成有输入输出契约的可调用能力。Manager 像调用工具一样委派有限子任务，Subagent 不直接接管用户会话。

## 工作原理

Manager 选择 specialist、构造 Context Packet、等待 Result Packet，再决定继续调用、合成或澄清。子 Agent 不能自行扩大委派链。

## 架构视图

~~~text
Architecture View
User -> Manager -> Specialist as tool -> Result Packet -> Manager -> User
~~~

~~~text
Product View
User -> one assistant -> specialist work hidden/optional -> unified result
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 agents-as-tools 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

客服 Manager 调用政策 Agent 检查退款资格，再用统一语气向用户解释。

## 失败与恢复场景

Manager 把完整历史传给法律 Agent造成泄漏；按 tool schema 只传条款与必要事实。

## 什么时候使用

需要专业化或隔离，但希望一个 Agent 始终拥有最终答案时使用。

## 什么时候不要使用

Specialist 应直接与用户多轮交流或所有工作可由普通函数完成时不用。

## Trade-offs

体验一致、合成集中，但 Manager 上下文与调用成本可能成为瓶颈。

## 产品视角

### 用户与业务问题

用户不需要在多个助手间切换即可获得专业结果。

### 产品价值

在保持统一入口下提高局部质量。

### 用户体验

默认只展示“正在检查政策”等业务进度；可选展示 Specialist 来源。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

OpenAI Agents SDK 的 Agent.as_tool、LangChain subagents 都对应此模式。

## Related Patterns

Supervisor、Modular Single、Handoff。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

限制子 Agent 只能返回结构化资格判断，禁止直接写用户回复。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
