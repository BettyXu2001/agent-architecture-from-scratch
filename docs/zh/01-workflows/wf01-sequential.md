---
id: wf01-sequential
order: 201
section: workflows
status: planned
title: "Sequential / Prompt Chaining"
description: "一次调用同时研究、起草、校验和润色，提示词会承担过多目标，任何局部错误也难以定位。Sequential 把稳定任务拆成有顺序、有契约的阶段。"
updated_at: 2026-08-24
---

# WF01：Sequential / Prompt Chaining

## 它解决什么问题

一次调用同时研究、起草、校验和润色，提示词会承担过多目标，任何局部错误也难以定位。Sequential 把稳定任务拆成有顺序、有契约的阶段。

## 核心定义

Sequential 是代码驱动的线性 Workflow：前一步的结构化输出成为后一步输入。它不是 Agent，因为下一步在运行前已经确定。

## 工作原理

先定义每步的单一职责与 schema，再设置验证门。步骤成功后提交状态；失败时停在边界，而不是携带错误继续生成。

## 架构视图

~~~text
Architecture View
Request -> Outline -> Draft -> Fact Check -> Polish -> Result
State:   s0 ------> s1 -----> s2 ---------> s3
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 sequential 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

内容生产先生成大纲，再写草稿、检查必需事实、最后润色。每步输出都通过最低校验，Trace 能准确解释质量变化。

## 失败与恢复场景

若大纲缺少必需主题，Workflow 在第一道门停止并返回可修改大纲；不让后续写作放大缺陷。恢复时只重跑大纲及其下游。

## 什么时候使用

任务天然有阶段、依赖稳定、每步可独立验证，且中间成果对用户或运营有价值时使用。

## 什么时候不要使用

步骤高度耦合、路径依赖中间探索，或单次调用已经足够时不要强拆链条。

## Trade-offs

拆分提高可控性与可定位性，却增加调用、延迟和中间契约维护。过细拆分会丢失整体语境。

## 产品视角

### 用户与业务问题

适合报告、营销内容、数据处理等可向用户解释为明确阶段的任务。

### 产品价值

通过局部重试、阶段校验和中间预览减少整单重做。

### 用户体验

用户看到业务阶段、等待原因和可操作错误，不需要看到内部 Prompt 或 Agent 名称。只有真实可测的步骤才展示进度。

### 自主性边界

Workflow 中模型只在步骤内部生成或判断；分支、预算、副作用和最终提交仍由代码及权限规则控制。

### 数据与权限

每一步只接收完成该步骤所需字段；中间结果采用结构化契约，敏感原文不因方便而自动传给全部步骤。

### 失败与降级

支持从失败步骤重试、跳过可选步骤、使用规则或缓存降级，并保留已通过校验的中间结果。

### 产品指标

衡量端到端成功率、各步骤失败率、P50/P95 完成时间、重试率、用户修正率和单成功任务成本。

## 框架中的对应实现

任何语言函数调用即可实现；LangGraph、Google ADK SequentialAgent、CrewAI Flow 都能表达，但不需要为简单链条引入重型框架。

## Related Patterns

后续可与 Routing、Evaluator、Fallback 组合；路径开始动态变化时比较 ReAct。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

增加一道引用完整性校验，并观察它放在写作前后对成本和返工的影响。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
