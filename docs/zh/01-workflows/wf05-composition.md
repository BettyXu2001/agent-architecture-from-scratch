---
id: wf05-composition
slug: zh/01-workflows/wf05-composition
order: 205
section: workflows
status: planned
title: "Workflow Composition：Branch、Join、Loop 与 Fallback"
description: "真实产品不是单一 pattern，而是线性步骤、条件分支、并行汇合、有界循环与降级的组合。缺少组合语义会让错误路径成为隐式代码。"
updated_at: 2026-08-24
---

# WF05：Workflow Composition：Branch、Join、Loop 与 Fallback

## 它解决什么问题

真实产品不是单一 pattern，而是线性步骤、条件分支、并行汇合、有界循环与降级的组合。缺少组合语义会让错误路径成为隐式代码。

## 核心定义

Composition 用少量控制原语构成完整 Workflow：Branch 选择路径，Join 定义汇合，Loop 定义重复与终止，Fallback 定义主路径失败后的替代结果。

## 工作原理

每个节点声明输入输出、超时和幂等性；边声明触发条件；Join 声明完成策略；Loop 声明预算；Fallback 声明降级质量和用户提示。

## 架构视图

~~~text
Architecture View
Request -> branch -> parallel tasks -> join -> evaluate
             |                              |
             +-> fallback <---- bounded loop+
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 composition 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

内容请求按类型分支，并行事实与合规检查，评价不通过最多修订两轮；搜索不可用时使用缓存并标注时效。

## 失败与恢复场景

若无界循环、Join 永久等待或 Fallback 隐藏关键缺失，系统会假装运行或返回误导结果。用 deadline、部分失败状态和显式降级标签恢复。

## 什么时候使用

当多个基础 Workflow pattern 已被需求证明需要，并且状态转换可以清晰列出时使用。

## 什么时候不要使用

MVP 只有两三步时不要提前画复杂图；无法定义节点契约时，图只会掩盖耦合。

## Trade-offs

组合原语提高表达力和恢复能力，却扩大状态空间。统一编排便于观察，但也可能形成中央瓶颈。

## 产品视角

### 用户与业务问题

解决复杂任务需要稳定承诺：什么时候完成、何时重试、缺失什么以及还能得到什么。

### 产品价值

减少整单失败，支持部分结果、局部重跑和一致进度。

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

DAG、状态机和图框架都能表达；选择依据是是否需要循环、持久化、事件和人工等待，而不是节点数量。

## Related Patterns

下一模块将比较图、状态机和事件驱动；进入模型动态选边时转向 Agent orchestration。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

为每条边增加失败语义，确认不存在只有 happy path 的节点。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
