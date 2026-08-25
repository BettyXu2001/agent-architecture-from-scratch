---
id: sa02-loop
slug: zh/02-single-agent/sa02-loop
order: 302
section: single-agent
status: planned
title: "Reason–Act–Observe Loop"
description: "只画一个圆环无法实现可运营 Agent：必须明确每轮读取什么、产出什么、谁执行、状态何时提交。"
updated_at: 2026-08-24
---

# SA02：Reason–Act–Observe Loop

## 它解决什么问题

只画一个圆环无法实现可运营 Agent：必须明确每轮读取什么、产出什么、谁执行、状态何时提交。

## 核心定义

Reason–Act–Observe Loop 是 Agent 的控制周期。Reason 选择结构化意图，Act 由可信 Runtime 执行，Observe 将外部结果转成可供下一轮使用的事实。

## 工作原理

每轮采用 prepare→decide→validate→execute→record→stop-check。工具调用前记录 pending，成功后原子提交结果；副作用用幂等键避免重试重复执行。

## 架构视图

~~~text
Architecture View
State -> prepare context -> decision -> validate -> execute
  ^                                             |
  +-- record observation / error / cost --------+
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 loop 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

工具成功后，Observation 与调用 ID 一起写入轨迹；下一轮只读取必要结果，达到完成条件后产生 Final。

## 失败与恢复场景

工具在“已执行但响应丢失”状态失败时，不直接重试；Runtime 用幂等键查询结果，再决定提交或补偿。

## 什么时候使用

实现任何可调用工具并自主迭代的 Agent 时，用它作为运行契约。

## 什么时候不要使用

不要把自由文本中的“我将调用工具”当作 Action，也不要将全部聊天历史当成可靠 State。

## Trade-offs

显式周期增加工程状态，却换来可恢复和可审计；原子提交与幂等会增加存储复杂度。

## 产品视角

### 用户与业务问题

用户需要可信地知道行动是否真的发生，而不只是模型说自己完成了。

### 产品价值

让取消、重试、恢复和动作历史成为可靠产品能力。

### 用户体验

向用户展示目标、关键行动、证据、等待和停止原因；不要把内部思维文本当成进度，也不要用动画掩盖无界循环。

### 自主性边界

Agent 可以在白名单能力中选择只读行动；写入、发送、购买、删除等动作由 Runtime 校验并按风险触发确认。

### 数据与权限

工具只返回任务所需字段；Context 与 Trace 分开处理，敏感观察不得自动进入后续所有调用或长期 Memory。

### 失败与降级

超时、预算耗尽或连续无进展时返回最佳已有结果、缺口和可继续选项；工具不可用时可转 Workflow、缓存或人工。

### 产品指标

衡量任务成功、有效工具选择率、平均步骤、无进展循环率、澄清解决率、非预期行动率和单成功任务成本。

## 框架中的对应实现

Runner/Graph/State Machine 的命名不同，但都应能定位 decision、tool call、observation 和 terminal state。

## Related Patterns

与 Tool Boundary、Termination、Durable Execution、Trace 直接相连。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

模拟工具已执行但超时，验证不会发生重复副作用。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
