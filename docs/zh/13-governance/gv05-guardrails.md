---
id: GV05
slug: zh/13-governance/gv05-guardrails
order: 1405
section: governance
status: complete
title: "Guardrails and Policy Layer"
description: "Prompt 规则会被上下文干扰，且无法单独承担组织政策与副作用控制。"
updated_at: 2026-08-24
lang: zh
module: human-governance
prerequisites: [OR04, SA05]
concepts: [human-in-the-loop, governance, policy]
example: examples/governance/governance_runtime.py
last_reviewed: 2026-08-24
---

# GV05：Guardrails and Policy Layer

## 它解决什么问题

Prompt 规则会被上下文干扰，且无法单独承担组织政策与副作用控制。

## 核心定义

Guardrails 检查输入、输出或工具提议；Policy Layer 是模型外、可版本化的业务与安全决策点。

## 工作原理

治理决策输入包含 identity、action、resource、risk、reversibility、confidence 和 current policy version；输出为 allow、deny、needs_approval、needs_human 或 redact，并写入 Audit Event。

## 架构视图

~~~text
Architecture View
Input guard -> Agent -> action/output guard -> policy -> execute/release
~~~

~~~text
Product View
User sets autonomy -> preview/control -> task progress -> result/redress
                         | approve/edit/reject | take over
~~~

## 最小可运行实践

运行 examples/governance/governance_runtime.py。实验实现风险分级、Action Hash 审批、参数变更失效、人工升级包、版本化 Policy 与最小审计，并主动触发越权和过期批准。

## 正常场景

适用于敏感内容、合规和工具行动。

## 失败与恢复场景

并行 guard 在阻断前工具已执行时造成副作用；高风险检查使用 blocking 模式。

## 什么时候使用

所有能影响外部世界、处理敏感数据、涉及责任判断或需要用户控制的 Agent 产品都要选择性使用。

## 什么时候不要使用

不要让人工批准普通低风险读取；不要用确认弹窗转移产品责任，也不要把 Guardrail 误当模型准确性保证。

## Trade-offs

更多控制提高安全与信任，却增加摩擦和等待；更少日志保护隐私，却降低追责。按风险分层，而非所有动作一刀切。

## 产品视角

### 用户与业务问题

治理的目标是让用户获得有意义的控制、清晰责任与出错后的补救，而不是合规文字堆叠。

### 产品价值

敏感内容、合规和工具行动。使高价值自动化能够在可接受风险下上线。

### 用户体验

审批展示具体动作、对象、影响和可撤销性；人工接管不要求重述；用户可设置默认自主等级并随时暂停。

### 自主性边界

低风险只读可自动，高风险或不可逆动作需 step-up；边界由产品政策和权限系统决定，不由模型自评。

### 数据与权限

数据按目的和最小化使用；用户可查看、撤销和删除；跨 Agent/供应商共享必须记录责任与保留。

### 失败与降级

策略服务不可用时 fail closed 于高风险动作；低风险任务可降级只读/草稿；提供申诉、纠正和人工渠道。

### 产品指标

观察审批接受/拒绝/编辑率、误阻断、非预期行动、人工等待、接管解决率、审计完整率和治理事件。

## 框架中的对应实现

SDK approvals/guardrails 是控制点，真正授权、审计和数据治理仍由产品服务、身份系统和目标 API 强制。

## Related Patterns

Approval、Handoff、Tool Boundary、Policy-as-code、Audit Trace、Data Provenance。

## 检查清单

- 用户是否理解正在批准什么？
- 批准是否绑定不可变动作？
- 权限是否在执行端再次检查？
- 人工接管是否携带完整但最小上下文？
- 审计是否可用且不过度收集？

## 延伸练习与参考资料

对读取、起草、发送、支付、删除五类动作设计不同控制等级并测试参数篡改。

- [OpenAI Agents SDK：Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)
- [OpenAI Agents SDK：Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Anthropic：Trustworthy agents](https://www.anthropic.com/research/trustworthy-agents)
