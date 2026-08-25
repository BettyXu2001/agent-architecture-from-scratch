---
id: wf06-comparison
slug: zh/01-workflows/wf06-comparison
order: 206
section: workflows
status: planned
title: "Workflow vs Agent"
description: "Workflow 稳定但覆盖有限，Agent 灵活但不确定。团队需要基于任务证据选择，而不是把 Agent 当作默认升级方向。"
updated_at: 2026-08-24
---

# WF06：Workflow vs Agent

## 它解决什么问题

Workflow 稳定但覆盖有限，Agent 灵活但不确定。团队需要基于任务证据选择，而不是把 Agent 当作默认升级方向。

## 核心定义

核心边界是运行时控制权：Workflow 的合法路径由代码预先约束；Agent 的模型能根据观察生成此前未确定的下一步。混合系统可以把 Agent 放在 Workflow 的局部区域。

## 工作原理

先实现最简单 Workflow 基线，用长尾失败样本证明静态路径不足；再只开放必要决策，并加入预算、工具白名单、状态和评价。

## 架构视图

~~~text
Architecture View
Known paths -> Workflow baseline -> failure set
                               -> bounded Agent zone -> evaluate
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 comparison 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

研究产品先用固定搜索—汇总—校验链覆盖常见任务；当复杂问题需要根据新证据追问时，只把搜索策略开放给 Agent。

## 失败与恢复场景

直接用自由 Agent 替换稳定业务流程，会出现不可复现路径、延迟漂移和副作用风险。恢复时把稳定动作重新收回代码。

## 什么时候使用

路径清晰选择 Workflow；路径依赖观察且有可判定目标选择 Agent；高风险任务采用 Hybrid。

## 什么时候不要使用

不要因自然语言界面、工具调用或多个模型调用就把系统称为 Agent，也不要为营销标签放弃确定性。

## Trade-offs

Workflow 牺牲长尾灵活性换取可预测运营；Agent 以成本和方差换取适应性。Hybrid 增加边界设计，却常是产品最优解。

## 产品视角

### 用户与业务问题

用户真正需要的是任务完成与控制感，不是内部自主性。选择应从失败任务和等待承诺出发。

### 产品价值

用基线对照证明 Agent 是否真正提升成功率，而不是只展示更复杂轨迹。

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

同一框架常能表达两者。OpenAI 明确区分 code orchestration 与 LLM orchestration；LangGraph 的边可由代码或模型决定。

## Related Patterns

前置 OV02 与全部 Workflow patterns；后续 ReAct 展开模型驱动循环。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

对十个真实任务运行 Workflow 基线，仅对失败样本判断是否需要 Agent。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
