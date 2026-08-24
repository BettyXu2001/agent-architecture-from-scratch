---
id: sa03-reflection
order: 303
section: single-agent
status: planned
title: "Reflection / Self-Critique"
description: "Agent 完成后可能遗漏约束或未利用已有证据。Reflection 在最终提交前重新检查轨迹与候选结果。"
updated_at: 2026-08-24
---

# SA03：Reflection / Self-Critique

## 它解决什么问题

Agent 完成后可能遗漏约束或未利用已有证据。Reflection 在最终提交前重新检查轨迹与候选结果。

## 核心定义

Reflection 是同一决策主体基于标准审视自己的结果或过程，并生成修订建议。它不天然保证正确，也不等同独立验证。

## 工作原理

将目标、可验证标准、候选和必要证据交给反思步骤；输出结构化缺口与是否修订。限制轮数，并用外部规则验证可验证事实。

## 架构视图

~~~text
Architecture View
Candidate -> Reflect(rubric) -> accept
    ^             |
    +--- revise --+  max N
~~~

~~~text
Product View
User goal -> Agent running -> evidence / checkpoint -> result
              |       |                 |
              |       +-- clarification +-- partial result
              +-- cancel / approve action
~~~

## 最小可运行实践

运行 examples/single-agent/bounded_research_agent.py 的 reflection 场景。示例用确定性 Policy 模拟模型决策，保留 Action、Observation、Budget、Stop 和 Trace，因此无需 API Key 也能验证架构。

## 正常场景

初稿满足事实要求但缺少限制条件，Reflection 指出后修订一次，通过确定性校验。

## 失败与恢复场景

自我批评产生风格性来回修改或编造新事实时，no-improvement 与证据校验停止循环并保留最佳版本。

## 什么时候使用

输出价值高、有明确检查表、一次修订常能提升完整性时使用。

## 什么时候不要使用

事实必须由外部来源验证、延迟极敏感或没有可操作 rubric 时，不要把 Self-Critique 当质量保证。

## Trade-offs

低成本复用同一模型，但共享盲点强；更多轮数可能只增加措辞变化和成本。

## 产品视角

### 用户与业务问题

适合报告、方案和复杂答复提交前的完整性检查。

### 产品价值

减少明显遗漏和用户返工，但必须通过 A/B 或 eval 证明提升。

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

可作为 Agent 内部步骤或 Workflow 节点实现；框架并不改变同源评价偏差。

## Related Patterns

替代/组合 Critic and Revision、Evaluator–Optimizer、Trajectory Eval。

## 检查清单

- 模型拥有哪些决策权？
- Action 与内部推理是否分离？
- Observation 是否经过验证和裁剪？
- 是否有停止、澄清、预算与无进展检测？
- 高风险行动是否由 Runtime 而非 Prompt 控制？

## 延伸练习与参考资料

分别使用开放式“再检查”和五项 rubric，对比反馈可执行性。

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
