---
id: pr07-delivery
order: 1107
section: protocols
status: planned
title: "Sync、Streaming and Async Tasks"
description: "Agent 工作从毫秒回答到数小时任务，单一同步请求会超时，纯轮询又让体验迟钝。"
updated_at: 2026-08-24
---

# PR07：Sync、Streaming and Async Tasks

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

Agent 工作从毫秒回答到数小时任务，单一同步请求会超时，纯轮询又让体验迟钝。

## 核心定义

Sync 在一次响应内完成；Streaming 增量传递状态或内容；Async Task 持久化工作并由查询、订阅或推送获得更新。传输方式不改变最终验收。

## 工作原理

按预计时长和断连容忍选择方式；每种都支持 request/task ID、deadline、cancel、resume 和 terminal state。MCP 2026 的 Tasks 是扩展，A2A 原生支持 Task 生命周期。

## 架构视图

~~~text
Architecture View
Sync: request->response
Stream: request->events->terminal
Async: create task->poll/subscribe->artifact
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 delivery 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

短分类同步返回，报告生成创建异步 Task，用户离开后回来仍可查看 Artifact；流式只展示真实阶段。

## 失败与恢复场景

断流被误判失败时，客户端用 task_id 查询最终状态；取消与完成竞争时以版本化终态规则处理。

## 什么时候使用

根据任务时长、进度价值和网络条件选择，允许同一产品混合。

## 什么时候不要使用

不要把 token streaming 当任务进度；不可恢复的长连接不适合小时级工作。

## Trade-offs

Sync 简单，Streaming 响应快，Async 最可恢复但状态和存储最多。

## 产品视角

### 用户与业务问题

用户得到合适等待体验，可离开、取消、回来和领取成果。

### 产品价值

减少超时与流失，支持真正后台 Agent。

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

MCP Tasks extension 与 A2A Task 各有语义，应用需映射到统一产品状态机。

## Related Patterns

Durable Execution、Cancellation、Progress Ledger、Event Delivery。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

模拟流断开后用 Task ID 恢复，并验证不会重复创建任务。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
