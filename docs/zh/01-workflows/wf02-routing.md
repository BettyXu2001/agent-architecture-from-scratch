---
id: wf02-routing
order: 202
section: workflows
status: planned
title: "Routing"
description: "不同请求需要不同能力与政策，却都进入同一提示词，导致上下文臃肿、答案不稳定。Routing 先判断类别，再选择有限分支。"
updated_at: 2026-08-24
---

# WF02：Routing

## 它解决什么问题

不同请求需要不同能力与政策，却都进入同一提示词，导致上下文臃肿、答案不稳定。Routing 先判断类别，再选择有限分支。

## 核心定义

Router 将输入映射到预先注册的目标。分类器可以是规则、传统模型或 LLM，但可选目标与回退路径由代码限定。

## 工作原理

先做输入归一化，再输出结构化 route、confidence 与 reason。Runtime 验证 route 是否允许；低置信度进入澄清或人工队列。

## 架构视图

~~~text
Architecture View
Request -> Classifier -> [support | sales | unsafe | clarify]
                         -> selected bounded workflow
~~~

~~~text
Product View
User goal -> start -> visible stage/progress -> result
                 |             |
                 +-- cancel / retry / fallback
~~~

## 最小可运行实践

运行 examples/workflows/content_pipeline.py，并选择 routing 场景。示例以普通 Python 函数模拟模型步骤，不依赖 API Key；关注输入输出契约、控制路径和失败处理，而不是模型能力。

## 正常场景

用户询问退款时被送入退款政策 Workflow；销售问题进入产品问答。每个分支只加载所需工具和上下文。

## 失败与恢复场景

模型输出未知 route 或置信度低时，不猜测执行；进入 clarify。若高风险请求被错分，独立策略层仍会阻断副作用。

## 什么时候使用

任务类别有限、分支差异显著、专业上下文或权限需要隔离时使用。

## 什么时候不要使用

所有请求都走相同步骤，或类别持续变化且难以定义验收集时不要增加 Router。

## Trade-offs

路由减少上下文和成本，却引入分类错误。细分类提高专业度，但增加样本维护、重叠类别和用户跳转。

## 产品视角

### 用户与业务问题

解决一个入口承接多种任务时的准确性与服务边界问题。

### 产品价值

提高首轮命中率，并将昂贵模型或人工服务只用于真正需要的请求。

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

OpenAI Agents SDK 可用结构化输出后由代码分派；LangGraph 使用条件边；Google ADK 可用自定义 Agent/Workflow 路由。

## Related Patterns

可组合 Parallel Specialists、Handoff；区别是 Routing 不一定转移对话所有权。

## 检查清单

- 控制路径是否显式且可测试？
- 每步输入输出是否结构化？
- 是否定义超时、重试、降级和停止？
- 用户看到的进度是否对应真实状态？
- 新增步骤带来的质量是否覆盖延迟与成本？

## 延伸练习与参考资料

加入低置信度和多意图输入，设计澄清而不是强制二选一。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
