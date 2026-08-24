---
id: sa05-tools
order: 305
section: single-agent
status: planned
title: "Tool-Using Agent as an Architecture Boundary"
description: "模型能提出行动意图，但不能成为执行权限本身。若工具只是任意函数入口，Prompt 注入和参数错误会直接变成外部副作用。"
updated_at: 2026-08-24
---

# SA05：Tool-Using Agent as an Architecture Boundary

## 它解决什么问题

模型能提出行动意图，但不能成为执行权限本身。若工具只是任意函数入口，Prompt 注入和参数错误会直接变成外部副作用。

## 核心定义

Tool Boundary 将不可信模型决策与可信执行环境分开：Agent 提议 name+arguments，Runtime 负责 schema、身份、策略、确认、执行和结果裁剪。

## 工作原理

调用依次经过 capability allowlist、参数校验、授权、风险分类、幂等、执行、输出清洗和审计。工具错误被编码为 Observation，不泄露凭据或内部堆栈。

## 架构视图

~~~text
Architecture View
Model proposal -> Schema -> Policy -> Approval? -> Executor
                                              -> Sanitized observation
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 tools 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

Agent 提议读取订单，Runtime 验证仅能访问当前用户订单，返回必要字段；Agent 据此回答。

## 失败与恢复场景

网页内容诱导 Agent 发送数据时，外发工具的目标域和字段策略阻断调用，并把可解释错误返回 Agent 与用户。

## 什么时候使用

所有能访问外部数据、代码、计算机或产生副作用的 Agent 都必须有此边界。

## 什么时候不要使用

不要依靠系统提示词替代授权，也不要把数据库客户端或通用 Shell 无限制暴露给模型。

## Trade-offs

边界限制灵活性并增加适配代码，却显著降低影响半径。宽工具少开发但难治理；窄工具安全但数量更多。

## 产品视角

### 用户与业务问题

用户需要明确系统能读什么、做什么，以及哪些动作会先征求同意。

### 产品价值

在保留自动化的同时建立最小权限、预览、撤销和责任记录。

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

SDK 的 function tools、guardrails 和 approvals 提供入口；真正权限仍必须在服务端和目标系统执行。

## Related Patterns

后续 MCP、Human Approval、Idempotency、Action Safety。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

给发送消息工具加入收件人域、敏感字段和重复提交三类拦截。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
