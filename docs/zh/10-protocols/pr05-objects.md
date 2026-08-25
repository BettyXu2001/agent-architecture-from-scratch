---
id: pr05-objects
slug: zh/10-protocols/pr05-objects
order: 1105
section: protocols
status: planned
title: "Task、Message、Part and Artifact"
description: "自然语言消息、长任务状态和最终文件混在一起时，客户端无法可靠追踪、恢复和交付。"
updated_at: 2026-08-24
---

# PR05：Task、Message、Part and Artifact

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

自然语言消息、长任务状态和最终文件混在一起时，客户端无法可靠追踪、恢复和交付。

## 核心定义

Message 是一轮交流；Part 是文本、原始字节、URL 或结构化数据的内容单元；Task 是有 ID 与状态的工作；Artifact 是任务产生的可交付成果。

## 工作原理

即时请求可返回 Message；复杂请求创建 Task。状态更新不替代 Artifact，Artifact 以 ID、name、mediaType 和 Parts 表达并接受业务验证。

## 架构视图

~~~text
Architecture View
Message -> Task lifecycle -> status updates + Artifacts(parts)
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 objects 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

远程分析返回 running 更新，最终 Task completed 且附 JSON 数据与 PDF 两个 Artifact。

## 失败与恢复场景

completed 但缺必需 Artifact 时，客户端产品状态为 failed_validation，并请求补交或转人工。

## 什么时候使用

远程 Agent 处理多轮、长任务或多模态成果时使用。

## 什么时候不要使用

短文本即时回答无需强制创建 Task，但仍需 Message ID。

## Trade-offs

结构化生命周期支持恢复，代价是状态映射、存储和校验。

## 产品视角

### 用户与业务问题

用户能区分聊天说明、处理中状态和真正交付物。

### 产品价值

支持后台执行、可靠下载与部分成果。

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

遵循 A2A 1.0 schema；内部框架消息需显式映射，不能直接透传。

## Related Patterns

Message vs State vs Artifact、Progress Ledger、Artifact Workspace。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

构造 completed-without-artifact 并让产品层拒绝成功。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
