---
id: sa01-react
order: 301
section: single-agent
status: planned
title: "ReAct Architecture"
description: "开放任务的下一步依赖工具返回，无法在运行前写成完整路径。ReAct 让模型在行动与观察之间迭代更新决策。"
updated_at: 2026-08-24
---

# SA01：ReAct Architecture

## 它解决什么问题

开放任务的下一步依赖工具返回，无法在运行前写成完整路径。ReAct 让模型在行动与观察之间迭代更新决策。

## 核心定义

ReAct 是 Reasoning 与 Acting 交错的架构：模型基于目标和当前观察选择一个外部 Action，Runtime 执行后返回 Observation，循环直到完成或停止。产品实现不需要暴露私有推理。

## 工作原理

输入由目标、可用动作、压缩轨迹和预算组成；输出是结构化 Action 或 Final。Runtime 校验 schema、权限与预算，再执行工具并清洗 Observation。

## 架构视图

~~~text
Architecture View
Goal -> Decide -> Action -> Runtime -> Observation
          ^                            |
          +--------- bounded loop -----+
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 react 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

研究 Agent 先搜索主题，观察资料不足后读取一条来源，证据满足后生成结论并停止。

## 失败与恢复场景

模型重复相同搜索时，Runtime 通过 action fingerprint 检测无进展并停止，返回当前证据和建议澄清，而不是继续烧预算。

## 什么时候使用

路径依赖中间观察、工具结果可验证、任务允许多步延迟且错误可恢复时使用。

## 什么时候不要使用

固定路径、强实时、不可逆高风险操作或无法判断进展的任务不要直接采用自由 ReAct。

## Trade-offs

ReAct 提高长尾适应性，却增加调用、轨迹状态和方差。更丰富 Observation 有助判断，也可能造成上下文污染。

## 产品视角

### 用户与业务问题

解决用户不愿自己反复搜索、查看再追问的探索型任务。

### 产品价值

系统可以基于新证据继续工作，减少用户手工拆解步骤。

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

OpenAI Agents SDK Runner、LangGraph 循环图及多数 Agent Runtime 都能承载；关键是决策与执行边界，不是 API。

## Related Patterns

前置 Workflow vs Agent；后续 Reason–Act–Observe、Termination、Planning。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

增加重复 Action 检测，并比较停止与自动改写查询两种恢复策略。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
