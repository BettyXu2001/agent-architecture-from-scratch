---
id: pr02-a2a
order: 1102
section: protocols
status: planned
title: "A2A Architecture：Client Agent and Remote Agent"
description: "独立团队或厂商的 Agent 需要在不暴露内部工具、Memory 和实现的情况下协作。"
updated_at: 2026-08-24
---

# PR02：A2A Architecture：Client Agent and Remote Agent

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

独立团队或厂商的 Agent 需要在不暴露内部工具、Memory 和实现的情况下协作。

## 核心定义

A2A 连接代表用户的 Client Agent 与作为黑盒系统的 Remote Agent。远程方通过 Agent Card 描述接口与技能，通过 Message 或有生命周期的 Task 返回 Artifact。

## 工作原理

Client 发现并验证 Agent Card，选择兼容接口和认证，发送 Message；Remote Agent 可直接回 Message，或创建 Task 并更新状态/Artifact。

## 架构视图

~~~text
Architecture View
User -> Client Agent ==A2A==> Remote Agent System
             card/auth/task/messages/artifacts
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 a2a 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

采购 Agent 委派翻译给外部 Agent，轮询 Task 并接收带 MIME 类型的文件 Artifact。

## 失败与恢复场景

远程 Agent 声称完成但 Artifact 不符合契约时，Client 标记 validation_failed，不把状态 completed 等同产品成功。

## 什么时候使用

能力由独立 Agent 系统拥有，需要长任务、多轮或结构化产物互操作时使用。

## 什么时候不要使用

本地工具调用用 MCP/API 更直接；不要为普通函数制造远程 Agent。

## Trade-offs

组织解耦与黑盒自治换来网络、SLA、身份、版本和结果验证成本。

## 产品视角

### 用户与业务问题

产品可接入外部专业服务而保持统一入口。

### 产品价值

缩短跨团队 Agent 集成并支持远程长任务。

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

使用官方 A2A SDK/协议绑定；内部 Remote Agent 可由任意框架实现。

## Related Patterns

Agent Card、Task Lifecycle、Distributed Runtime、Trust。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

让 Remote Agent 返回 Task 而非即时 Message，并验证客户端恢复轮询。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
