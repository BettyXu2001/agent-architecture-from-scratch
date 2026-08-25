---
id: wf04-evaluator
slug: zh/01-workflows/wf04-evaluator
order: 204
section: workflows
status: planned
title: "Evaluator–Optimizer"
description: "一次生成很难稳定满足可明确检查的质量标准，但让生成器无限自我修改又会循环。Evaluator–Optimizer 把生成和评价分离，并设置有界反馈回路。"
updated_at: 2026-08-24
---

# WF04：Evaluator–Optimizer

## 它解决什么问题

一次生成很难稳定满足可明确检查的质量标准，但让生成器无限自我修改又会循环。Evaluator–Optimizer 把生成和评价分离，并设置有界反馈回路。

## 核心定义

Optimizer 产出或修订候选；Evaluator 根据 rubric 返回 pass/fail、分项分数和可执行反馈。代码根据阈值与预算决定继续或停止。

## 工作原理

评价标准必须先于运行定义。每轮保存候选、反馈和分数；只有反馈具体且仍有预算时重试，达到阈值、无改进或预算耗尽即结束。

## 架构视图

~~~text
Architecture View
Draft -> Evaluate -> pass -> Result
  ^         |
  +-- revise+  (max rounds / no-improvement stop)
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 evaluator 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

报告草稿缺少风险说明，Evaluator 指出具体缺口；第二轮补齐并通过，系统返回最终稿与校验摘要。

## 失败与恢复场景

Evaluator 每轮给出矛盾反馈或分数不再提高时触发 no-improvement，返回最佳候选与未满足项，而不是无限循环。

## 什么时候使用

存在清晰 rubric，迭代能带来可测改进，且额外调用成本可接受时使用。

## 什么时候不要使用

偏好完全主观、评价器与生成器共享同一盲点，或任务只允许极低延迟时不要套循环。

## Trade-offs

分离角色提高质量控制，却增加调用和“评价器正确性”依赖。更严格阈值可能提高质量，也可能导致成本失控。

## 产品视角

### 用户与业务问题

适合用户宁愿多等一点也需要达到明确质量门槛的高价值产出。

### 产品价值

把“再好一点”转化为可验证的通过条件和可解释返工。

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

代码 while 循环已足够；OpenAI 文档给出 agent+evaluator 循环，LangGraph/ADK LoopAgent 可承载带状态的循环。

## Related Patterns

与 Critic and Revision 相邻；Workflow 版本的继续条件由代码掌握。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

加入无改进检测，并比较返回最后候选和最佳候选的差异。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
