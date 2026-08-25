---
id: wf03-parallel
slug: zh/01-workflows/wf03-parallel
order: 203
section: workflows
status: planned
title: "Parallelization / Fan-out Fan-in"
description: "多个互不依赖的子任务串行执行会放大等待；单一回答也可能缺少多视角覆盖。Parallelization 同时运行独立工作，再合并结果。"
updated_at: 2026-08-24
---

# WF03：Parallelization / Fan-out Fan-in

## 它解决什么问题

多个互不依赖的子任务串行执行会放大等待；单一回答也可能缺少多视角覆盖。Parallelization 同时运行独立工作，再合并结果。

## 核心定义

Fan-out 将任务拆为独立分支，Fan-in 等待全部或足够结果并聚合。并行是调度方式，不等于 Multi-Agent；分支可以只是函数或模型调用。

## 工作原理

先证明分支没有写冲突，设置并发上限和每支超时。聚合器接受成功结果与失败清单，并明确 all、quorum 或 best-effort 完成条件。

## 架构视图

~~~text
Architecture View
             +-> Research A -+
Request -> fan -+-> Research B -+-> join -> Result
             +-> Research C -+
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 parallel 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

内容任务并行检查事实、受众和合规，聚合器在三项完成后生成修订建议，总等待接近最慢分支而非总和。

## 失败与恢复场景

一个分支超时，best-effort 策略返回其余结果并标注缺口；若该分支是发布必需校验，则整体停在 review_pending。

## 什么时候使用

子任务真正独立、单支耗时高、合并规则明确，或需要多样化候选时使用。

## 什么时候不要使用

分支共享可变资源、强依赖前序结果、并发配额有限或聚合成本超过收益时不要并行。

## Trade-offs

并行降低墙钟时间，却增加瞬时资源、总调用量和部分失败状态。更多候选不必然提高最终质量。

## 产品视角

### 用户与业务问题

适合用户更关心总等待时间，且任务可拆为多个来源、区域或检查维度的场景。

### 产品价值

在相同任务覆盖下缩短完成时间，或在相同时间内增加覆盖。

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

Python asyncio、任务队列即可实现；OpenAI 示例使用并行 agent execution，Google ADK 有 ParallelAgent，图框架可表达 fan-out/fan-in。

## Related Patterns

可与 Router 选择分支、Evaluator 聚合质量、Scheduler 控制并发。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

分别用 all 与 best-effort 完成策略注入超时，比较用户承诺。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
