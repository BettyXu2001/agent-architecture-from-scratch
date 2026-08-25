---
id: mp02-supervisor
slug: zh/07-multi-agent-patterns/mp02-supervisor
order: 802
section: multi-agent-patterns
status: planned
title: "Supervisor / Manager"
description: "多个 Specialist 需要统一分解、委派、预算、合成和停止，否则会重复工作或无人负责。"
updated_at: 2026-08-24
---

# MP02：Supervisor / Manager

## 它解决什么问题

多个 Specialist 需要统一分解、委派、预算、合成和停止，否则会重复工作或无人负责。

## 核心定义

Supervisor 是中心控制 Agent：维护目标与全局状态，选择 Worker，并拥有最终结果；Worker 在局部任务内自治。

## 工作原理

每次委派含 task_id、scope、inputs、done 和 budget；Supervisor 检查结果、更新 Ledger、避免重复委派并决定下一项。

## 架构视图

~~~text
Architecture View
User -> Supervisor <-> Workers
            | state/budget | -> Final
~~~

~~~text
Product View
User -> goal -> coordinated milestones -> one accountable final answer
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 supervisor 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

Supervisor 将研究拆给事实、风险和写作 Specialist，依据依赖顺序合成。

## 失败与恢复场景

Supervisor 反复委派同一问题时，task fingerprint 与 completed ledger 拒绝重复。

## 什么时候使用

任务需动态选择多个专业 Worker，且统一控制和答案所有权重要时使用。

## 什么时候不要使用

固定并行分支用 Workflow 更便宜；中心上下文无法承受全部结果时考虑层级或 Artifact。

## Trade-offs

统一责任和治理，却形成中心瓶颈与单点故障。

## 产品视角

### 用户与业务问题

让系统替用户协调多种专业工作。

### 产品价值

提高复杂任务覆盖，同时保持统一目标。

### 用户体验

展示业务里程碑和缺口，不展示 Supervisor 的内部派单闲聊。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

OpenAI manager/agents-as-tools、LangChain supervisor/custom workflow、CrewAI manager 都可表达。

## Related Patterns

Agents as Tools、Hierarchical Supervisor、Task Allocation。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

注入重复委派并证明全局预算与 Ledger 同时阻止它。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
