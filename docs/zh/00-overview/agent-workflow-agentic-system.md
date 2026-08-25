---
id: agent-workflow-agentic-system
slug: zh/00-overview/agent-workflow-agentic-system
order: 110
section: overview
status: planned
title: "Agent、Workflow 与 Agentic System"
description: "一个产品接入大模型、知识库和工具后，是不是 Agent？答案取决于谁拥有下一步决策权，而不是组件数量。代码规定“先分类，再查询，最后生成”是 Workflow；模型能根据观察动态决定查询、追问、修改计划或停止，更接..."
updated_at: 2026-08-24
---

# OV02：Agent、Workflow 与 Agentic System

## 它解决什么问题

一个产品接入大模型、知识库和工具后，是不是 Agent？答案取决于**谁拥有下一步决策权**，而不是组件数量。代码规定“先分类，再查询，最后生成”是 Workflow；模型能根据观察动态决定查询、追问、修改计划或停止，更接近 Agent。Agentic System 是包含二者的上位概念。

## 核心定义

| 概念 | 控制权 | 适合的问题 | 主要风险 |
|---|---|---|---|
| LLM Feature | 调用方 | 局部生成、抽取、分类 | 输出错误 |
| Workflow | 代码或规则 | 路径已知、可分解任务 | 分支遗漏、步骤失败 |
| Agent | 模型在边界内动态决策 | 路径未知、需要观察环境 | 误操作、循环、成本漂移 |
| Agentic System | 代码、模型和人共同控制 | 混合确定性与自主性 | 边界不清、难以运营 |

Anthropic 将 Workflow 描述为由预定义代码路径编排模型与工具的系统，将 Agent 描述为由模型动态指导过程和工具使用的系统。这个区分比“有没有工具调用”更有解释力。

## 工作原理

~~~text
Code control  : if / switch / DAG / state transition
Model control : choose_tool / choose_next_step / revise_plan / stop
Human control : approve / edit / cancel / take_over
~~~

真实产品常采用混合控制：代码定义安全边界和关键流程，模型在局部选择行动，人对高风险操作保留否决权。

## 架构视图

~~~text
Architecture View

Workflow: Request -> A -> Router(code) -> B/C -> Result

Agent:    Request -> Model -> Action -> Observation
                     ^                    |
                     +------ decide ------+

Hybrid:   Request -> Policy -> Workflow Shell -> Agent Zone -> Approval
~~~

~~~text
Product View

User -> state goal -> see progress -> approve risky action -> result
                         |                       |
                         +-- cancel / correct ---+
~~~

## 最小可运行实践

运行 examples/overview/architecture_decision.py。示例根据路径可预知性、动态决策、副作用和风险级别，给出 workflow、agent 或 hybrid 建议。它不调用模型，目的是把架构判断变成显式规则。

## 正常场景

合同字段抽取与校验路径稳定，适合 Workflow；研究陌生市场并根据发现继续追查，适合受预算约束的 Agent；起草采购单并提交，需要 Agent 处理信息、Workflow 验证格式、人审批提交，适合 Hybrid。

## 失败与恢复场景

常见错误是把开放式语言输入误认为开放式执行。用户能自由描述需求，不意味着模型必须拥有流程控制权。若任务只有有限分支，应把理解交给模型，把分支和副作用留给代码。

恢复方法是缩小 Agent Zone：将稳定步骤下沉为 Workflow，把模型输出改为结构化决策，并为未知状态设置澄清、失败和人工接管出口。

## 什么时候使用

- Workflow：步骤可枚举、验收清晰、监管要求高。
- Agent：路径依赖中间观察，规则难覆盖，错误可恢复。
- Hybrid：既要动态探索，又包含资金、消息、权限或数据变更。

## 什么时候不要使用

单次生成能解决时不要引入循环；固定流程不要为了“智能感”改为模型路由；无法检测成功、限制预算或撤销副作用时，不要给予高自主性。

## Trade-offs

自主性提高长尾覆盖，却降低确定性；代码控制容易测试，却增加流程维护；人工审批降低风险，却可能形成新队列。目标不是最大化 Agent 程度，而是让每一份自主性对应用户价值。

## 产品视角

### 用户与业务问题

先问“用户目标是否需要系统在运行中做新决定”，再问是否需要 Agent。

### 产品价值

升级应提高长尾任务完成率、减少用户拆步骤的工作，或处理此前无法自动化的任务。

### 用户体验

Workflow 可展示固定阶段；Agent 应展示当前目标、关键行动、可信进度和停止原因，不伪造精确百分比。

### 自主性边界

读取和分析通常可自动进行；发送、购买、删除、授权等不可逆动作默认需要预览或确认。

### 数据与权限

每个工具采用最小权限。动态决策不能绕过产品层身份、策略和审计。

### 失败与降级

Agent 应能降级为有限分支、只读、草稿或人工处理，并保留中间成果。

### 产品指标

观察任务成功率、长尾覆盖、用户修正率、非预期行动率、完成时间和单成功任务成本。

## 框架中的对应实现

OpenAI Agents SDK 区分模型驱动与代码驱动编排；Google ADK 同时提供 LLM Agent 与 Sequential、Parallel、Loop 等 Workflow Agent；LangGraph 用图和显式状态承载混合控制。框架名不是架构答案。

## Related Patterns

前置：Architecture Map。后续：Sequential、Routing、ReAct、Human-in-the-Loop、State Machine。

## 检查清单

- 下一步由代码、模型还是人决定？
- 自主性新增价值能否测量？
- 是否定义预算、停止和澄清？
- 副作用是否有权限与确认？
- 失败时能否降级并保留中间结果？

## 延伸练习与参考资料

为自己的产品标注每个步骤的控制权，并尝试把 Agent Zone 缩小一半。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [Google ADK：Agent types](https://google.github.io/adk-docs/agents/)
