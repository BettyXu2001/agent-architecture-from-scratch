---
id: sa06-termination
slug: zh/02-single-agent/sa06-termination
order: 306
section: single-agent
status: planned
title: "Termination、Clarification 与 Budget"
description: "Agent 不知道何时停，就会过早回答、反复搜索或在信息不足时猜测。停止是一等架构能力，不是 Prompt 末尾一句话。"
updated_at: 2026-08-24
---

# SA06：Termination、Clarification 与 Budget

## 它解决什么问题

Agent 不知道何时停，就会过早回答、反复搜索或在信息不足时猜测。停止是一等架构能力，不是 Prompt 末尾一句话。

## 核心定义

Termination 定义完成或不可继续；Clarification 将缺失决策交还用户；Budget 限制步骤、时间、调用、token 或金钱。三者共同规定 Agent 的运行包络。

## 工作原理

每轮检查 success、hard failure、needs_user、no_progress 和 budget。优先级通常是安全阻断→用户取消→完成→澄清→预算→继续。

## 架构视图

~~~text
Architecture View
Observation -> stop policy -> final | clarify | partial | continue
Budget: steps + time + cost; Progress: new evidence / state change
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 termination 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

Agent 缺少报告受众时在执行昂贵搜索前澄清；获得答案后继续，并在证据满足完成条件时停止。

## 失败与恢复场景

同一 Action 连续出现或状态哈希不变，no_progress 触发 partial。预算耗尽时返回完成项与缺口，而不是伪装成功。

## 什么时候使用

任何自主循环都必须使用，并针对产品风险设置多维预算。

## 什么时候不要使用

不要只设置 max_steps；一步昂贵工具也可能超成本。不要把用户追问当失败，也不要让模型自行扩大预算。

## Trade-offs

严格预算控制成本却可能降低长任务成功率；频繁澄清提高准确性却打断体验。可通过默认值、批量澄清和可续跑状态平衡。

## 产品视角

### 用户与业务问题

用户需要知道系统为什么停、需要什么信息，以及继续会花多少时间或资源。

### 产品价值

把不可控等待变成可预期交互，并保留部分成果。

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

Runner 常提供 max turns；生产系统还需外层 deadline、cost meter、cancellation token 和业务完成判定。

## Related Patterns

Planning 的 Progress Ledger、Reliability 的 Loop Detection、HITL。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

同时注入重复 Action、工具超时和预算耗尽，验证停止原因互斥且可解释。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
