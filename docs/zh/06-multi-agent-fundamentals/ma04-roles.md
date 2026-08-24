---
id: ma04-roles
order: 704
section: multi-agent-fundamentals
status: planned
title: "Agent Specialization and Role Boundary"
description: "角色只写成“你是专家”无法建立可靠分工，容易角色漂移、工具越权和重复劳动。"
updated_at: 2026-08-24
---

# MA04：Agent Specialization and Role Boundary

## 它解决什么问题

角色只写成“你是专家”无法建立可靠分工，容易角色漂移、工具越权和重复劳动。

## 核心定义

Role Boundary 由目标、输入契约、可见上下文、工具/权限、输出契约、预算、停止和升级条件共同定义。

## 工作原理

Coordinator 只委派符合 capability 的任务；Specialist 可拒绝越界请求并返回 needs_handoff；结果包含证据和置信度。

## 架构视图

~~~text
Architecture View
Delegation contract -> Specialist(role/context/tools) -> Result contract
~~~

~~~text
Product View
User -> one product goal -> coordinated work -> one accountable result
             | progress/control     | sources / gaps / handoff
~~~

## 最小可运行实践

运行 examples/multi-agent/single_vs_multi.py 的 roles 场景。相同任务分别由 Single Agent、模块化 Single Agent 和多个 Specialist 完成，记录调用数、上下文可见范围、失败影响与最终答案所有者。

## 正常场景

财务 Specialist 只处理数值与来源，不写最终营销文案；Writer 只读取其结构化结论。

## 失败与恢复场景

Specialist 为完成目标调用未授权发布工具时，Runtime 阻断并回报 role_violation。

## 什么时候使用

任务确有稳定专业边界、不同数据权限或不同模型配置时使用。

## 什么时候不要使用

角色高度重叠或每次任务都要重新解释全部背景时，拆分价值低。

## Trade-offs

窄角色提高专注和权限控制，却增加交接损失与覆盖空白。

## 产品视角

### 用户与业务问题

用户得到专业质量，但不必理解内部转派。

### 产品价值

降低工具误选和上下文干扰，提高局部评测能力。

### 用户体验

默认向用户呈现一个连续的产品身份、统一进度与最终结果；只有 Specialist 身份有助于信任或接管时才展示内部角色。

### 自主性边界

每个 Agent 只能在角色、工具和预算范围内行动；跨角色委派、扩大任务范围和高风险副作用由编排与策略层约束。

### 数据与权限

Private Context 默认隔离，共享仅通过结构化结果或 Artifact。角色专业化不能成为复制全部用户数据的理由。

### 失败与降级

单个 Specialist 失败时标注缺口、重试或退回 Manager；必要时合并回 Single Agent、返回部分结果或转人工。

### 产品指标

除任务成功率外，比较调用数、总 Token、墙钟时间、协调开销、用户修正率、部分失败恢复率和单成功任务成本。

## 框架中的对应实现

instructions、tool allowlist 和 handoff description 只是声明，Runtime 权限与契约才是边界。

## Related Patterns

Context Packet、Capability Discovery、Task Allocation。

## 检查清单

- 拆分是否解决了可证明的瓶颈？
- 各 Agent 是否有独立角色、上下文或决策边界？
- 谁拥有最终答案和用户关系？
- 共享信息是否最小且结构化？
- 额外协调成本是否被收益覆盖？

## 延伸练习与参考资料

为一个 Specialist 写拒绝条件和升级包，而不只写人物设定。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
