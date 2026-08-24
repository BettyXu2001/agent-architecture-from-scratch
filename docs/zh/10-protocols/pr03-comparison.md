---
id: pr03-comparison
order: 1103
section: protocols
status: planned
title: "MCP vs A2A"
description: "两种协议都涉及 Agent，很容易误选：把独立 Agent 当工具会丢失任务生命周期，把普通工具当 Agent会增加复杂度。"
updated_at: 2026-08-24
---

# PR03：MCP vs A2A

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

两种协议都涉及 Agent，很容易误选：把独立 Agent 当工具会丢失任务生命周期，把普通工具当 Agent会增加复杂度。

## 核心定义

MCP 主要连接 Host/Agent 与 Tool、Resource 等能力；A2A 连接 Client Agent 与独立 Remote Agent System。二者可组合但不互相替代。

## 工作原理

判断远端是否拥有自己的任务决策、身份、状态与 Artifact 生命周期。没有则按工具能力；有且需黑盒协作则按 Agent。

## 架构视图

~~~text
Architecture View
MCP: Agent -> capability
A2A: Client Agent -> remote autonomous system
Combined: Agent -> MCP tools; Agent -> A2A remote agent
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 comparison 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

本地研究 Agent 用 MCP 搜索，又通过 A2A 委派远程法律分析。

## 失败与恢复场景

把付款 API 包成自主 Agent 后责任模糊；恢复为窄 MCP Tool 并保留本地审批。

## 什么时候使用

协议选型和系统边界评审时使用。

## 什么时候不要使用

不要按营销名称或 SDK 支持决定；先确定远端责任与生命周期。

## Trade-offs

工具接口可控且轻，Agent 接口自治且重；组合能力强但信任链更长。

## 产品视角

### 用户与业务问题

用户应知道连接的是可控工具还是独立服务主体。

### 产品价值

选择正确抽象可减少集成和运营歧义。

### 用户体验

用户看到连接主体、请求权限、远程处理状态、产物与责任边界；协议握手、轮询和重试由产品吸收。

### 自主性边界

发现能力不等于允许调用。Host/Client 按用户授权、策略、风险和当前 Task 重新决定；远程 Agent 不能获得本地全部权限。

### 数据与权限

令牌绑定目标受众，禁止 token passthrough；请求最小化并标注主体、目的和保留责任。远程服务视为独立信任域。

### 失败与降级

版本/能力不兼容时协商或拒绝；远程任务超时可取消、查询或返回部分 Artifact；连接撤销后立即停止新调用。

### 产品指标

衡量集成周期、连接成功率、授权放弃率、远程成功率、P95 延迟、取消生效率、SLA 违约和数据边界事件。

## 框架中的对应实现

框架可同时支持 MCP 与 A2A；映射层不能改变语义边界。

## Related Patterns

Tool vs Agent、Remote Ownership、Hybrid Systems。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

为五个外部服务分类并写出为何不是另一种协议。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
