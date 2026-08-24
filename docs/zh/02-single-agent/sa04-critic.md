---
id: sa04-critic
order: 304
section: single-agent
status: planned
title: "Critic and Revision"
description: "生成者容易重复自己的盲点。独立 Critic 用不同指令、上下文或模型评价候选，再由 Reviser 定向修改。"
updated_at: 2026-08-24
---

# SA04：Critic and Revision

## 它解决什么问题

生成者容易重复自己的盲点。独立 Critic 用不同指令、上下文或模型评价候选，再由 Reviser 定向修改。

## 核心定义

Critic 只负责依据 rubric 找缺口，不直接拥有最终答案；Reviser 根据候选、证据和反馈修改；Controller 决定接受、重试或停止。

## 工作原理

Critic 输出 issue、severity、evidence 与 suggested_fix。Controller 过滤不可验证反馈，优先处理高严重度问题，并以版本号保存候选。

## 架构视图

~~~text
Architecture View
Generator -> Candidate -> Critic -> Controller -> accept
                ^                       |
                +------ Reviser <-------+
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 critic 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

Critic 指出一条结论缺少来源，Reviser 补充引用，Controller 的确定性引用检查通过。

## 失败与恢复场景

Critic 与 Reviser在同一观点上争执时，以预算、严重度和无改进阈值停止，返回 unresolved issues。

## 什么时候使用

质量门槛较高、评价可分工、可接受额外模型调用时使用。

## 什么时候不要使用

低价值短文本、评价标准模糊或 Critic 无独立信息时，简单校验更合适。

## Trade-offs

角色分离降低部分偏差，却增加上下文传递、延迟与“谁判断 Critic”问题。

## 产品视角

### 用户与业务问题

适合用户需要审阅依据和已知缺口，而非只拿到看似完整的结果。

### 产品价值

把修订从随机重写变成问题驱动，并可向运营解释失败原因。

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

可用 agents-as-tools、普通函数节点或 evaluator loop；是否是多个 Agent 取决于上下文和控制边界。

## Related Patterns

与 Reflection、Evaluator–Optimizer、Multi-Agent Evaluator 相邻。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

让 Critic 输出严重度，并验证低严重度问题不会耗尽全部预算。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
