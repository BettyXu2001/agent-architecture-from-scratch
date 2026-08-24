---
id: EV01
title: Trace、Span and Agent Run Model
lang: zh
status: complete
module: evaluation-observability
prerequisites: [RL01]
concepts: [evaluation, observability, trace]
example: examples/evaluation/evaluation_harness.py
last_reviewed: 2026-08-24
---

# EV01：Trace、Span and Agent Run Model

## 它解决什么问题

没有统一运行模型，团队只能看聊天文本，无法定位模型、工具、Handoff、等待和错误的因果关系。

## 核心定义

Run/Trace 表示一次端到端目标；Span 表示有起止和父子关系的操作；Event 表示瞬时事实。它们与业务 Task ID、用户会话分开关联。

## 工作原理

先定义场景和产品成功，再采集最小必要 Trace。Grader 分确定性规则、参考比较、模型评价与人工；每个分数保留版本、证据和置信度。

## 架构视图

~~~text
Architecture View
Trace(root) -> agent/model/tool/handoff/guard spans -> outcome
~~~

~~~text
Product View
Real user goal -> observable run -> measurable outcome -> safe improvement
                    | privacy/control | correction feedback
~~~

## 最小可运行实践

运行 examples/evaluation/evaluation_harness.py。实验记录 Agent/Tool/Handoff Span，使用任务、轨迹和成本 Grader 评价 Golden Set，并对 Multi-Agent 做消融与单成功任务归因。

## 正常场景

适用于调试、性能、成本和审计关联。

## 失败与恢复场景

并发 Span 父子关系错误时，用显式 context propagation 和 task/correlation ID。

## 什么时候使用

从原型开始建立最小 Eval；每次模型、Prompt、工具、数据和架构变更都应跑与风险相称的回归。

## 什么时候不要使用

不要用单一分数替代产品判断；低频高风险行为不能被平均值稀释；Trace 也不能无限收集敏感内容。

## Trade-offs

更全面评价提高信心却增加数据、人工和执行成本；严格 Golden Set 稳定回归但可能抑制多路径创新，需要分层指标。

## 产品视角

### 用户与业务问题

评价的最终对象是用户目标、等待、控制和失败后果，而不是模型在基准上的抽象分数。

### 产品价值

调试、性能、成本和审计关联。让团队能证明架构升级是否值得并阻止回归上线。

### 用户体验

收集用户反馈时说明用途并允许撤回；纠正入口应直接关联失败 Task，而不要求用户写长评语。

### 自主性边界

线上自动优化不能绕过发布门和安全指标；模型 judge 只能建议，关键风险由规则或人确认。

### 数据与权限

Trace 默认最小化和脱敏，输入输出可关闭；Eval 数据集有访问、留存、来源和删除流程。

### 失败与降级

Grader 不稳定时回退确定性子指标或人工抽样；监控异常触发模型/架构回滚、限权或人工。

### 产品指标

核心组合为 Task Success、Time to Outcome、用户修正率、人工介入率、非预期行动率和单成功任务成本。

## 框架中的对应实现

OpenAI Agents SDK 提供 Trace/Span 与 usage；LangSmith 等提供 trajectory eval。工具不替你定义产品成功、隐私和发布阈值。

## Related Patterns

Reliability、Golden Set、Trace、Human Feedback、Architecture Comparison。

## 检查清单

- 最终结果和轨迹是否分别评价？
- Grader 是否有版本与证据？
- 是否覆盖失败、长尾和高风险场景？
- 成本是否按成功任务全摊？
- Trace 是否遵守数据最小化？

## 延伸练习与参考资料

删除一个 Specialist 做消融，比较质量、延迟和成本，判断它是否值得存在。

- [OpenAI Agents SDK：Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK：Usage](https://openai.github.io/openai-agents-python/usage/)
- [LangSmith：Evaluation approaches](https://docs.langchain.com/langsmith/evaluation-approaches)
