---
id: pr01-mcp
slug: zh/10-protocols/pr01-mcp
order: 1101
section: protocols
status: planned
title: "MCP Architecture：Host、Client、Server"
description: "AI 应用需要以统一方式发现和调用外部工具、资源与提示，同时让应用保留上下文、同意和安全控制。"
updated_at: 2026-08-24
---

# PR01：MCP Architecture：Host、Client、Server

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

AI 应用需要以统一方式发现和调用外部工具、资源与提示，同时让应用保留上下文、同意和安全控制。

## 核心定义

MCP 是 Agent/Application 与能力提供方之间的协议。Host 代表产品和用户，管理连接与策略；Client 负责协议通信；Server 暴露聚焦能力。它不是 Multi-Agent 拓扑。

## 工作原理

在 2026-07-28 版本中核心协议无会话握手，每个请求携带版本与客户端元数据，可用 server/discover 获取能力；应用状态用显式 handle 管理。工具调用仍由 Host 决定。

## 架构视图

~~~text
Architecture View
User -> Host -> MCP Client -> MCP Server -> Tool/Resource
            policy/context isolation
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 mcp 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

Host 发现搜索 Server 的 tool schema，只传查询并将结果作为不可信内容返回 Agent。

## 失败与恢复场景

Server 返回工具说明诱导调用另一高风险工具时，Host 不把 Server 内容视为策略，并重新做本地授权。

## 什么时候使用

需要跨应用/语言复用标准化 Tool、Resource 或 Prompt 能力时使用。

## 什么时候不要使用

同一代码库简单函数无需协议；不要用 MCP 替代业务授权或 Agent 编排。

## Trade-offs

互操作与生态复用换来版本、发现、授权和远程故障治理。

## 产品视角

### 用户与业务问题

用户可以安全连接外部能力，而产品保留统一同意和控制。

### 产品价值

降低每个集成单独开发协议的成本。

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

使用官方 SDK 实现线协议；Agent 框架只消费 MCP 能力，仍需自身编排。

## Related Patterns

Tool Boundary、Capability Discovery、Authorization、MCP Tasks extension。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

把一个本地搜索函数包装成能力描述，并证明 Server 看不到完整对话。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
