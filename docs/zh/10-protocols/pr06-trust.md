---
id: pr06-trust
slug: zh/10-protocols/pr06-trust
order: 1106
section: protocols
status: planned
title: "Agent Identity、Authentication and Trust"
description: "协议互通不等于可信。系统必须区分用户、Client、Remote Agent、Server 和下游 API 的身份与权限。"
updated_at: 2026-08-24
---

# PR06：Agent Identity、Authentication and Trust

> 版本说明：本文以 MCP 2026-07-28 与 A2A 1.0 的稳定架构概念为基准。协议字段可能演进，生产实现必须固定版本并运行 conformance tests。

## 它解决什么问题

协议互通不等于可信。系统必须区分用户、Client、Remote Agent、Server 和下游 API 的身份与权限。

## 核心定义

Authentication 证明主体，Authorization 决定允许动作，Trust 决定在什么证据和责任下接受声明或结果；三者不可混为“已连接”。

## 工作原理

令牌绑定资源/受众，凭据按 issuer 隔离，最小 scope、短期有效、可撤销；Server 调下游 API 使用独立 token，禁止转发收到的 token。

## 架构视图

~~~text
Architecture View
User grant -> Client credential(audience-bound) -> Server
Server -> separate downstream credential -> API
~~~

~~~text
Product View
User intent -> trusted client/host -> external capability -> status/artifact
                 | consent/auth        | failure / revoke / SLA
~~~

## 最小可运行实践

运行 examples/protocols/protocol_boundaries.py 的 trust 场景。实验模拟能力发现、MCP 风格工具调用、A2A 风格远程 Task、Artifact、认证受众检查和 sync/stream/async 状态，不依赖网络或 SDK。

## 正常场景

Client 只获得搜索 scope，Server 验证 audience；需要写入时触发 step-up 而非静默扩大。

## 失败与恢复场景

Server 将用户 token 传给下游造成 confused deputy；架构上分离 token 并验证 audience。

## 什么时候使用

任何远程 MCP/A2A 集成都必须处理，企业场景还需供应方审查与审计。

## 什么时候不要使用

不要把 Agent Card、TLS 或 API key 单独当完整信任模型。

## Trade-offs

强身份和细 scope 增加授权摩擦，却降低跨服务令牌滥用与影响半径。

## 产品视角

### 用户与业务问题

用户知道授权给谁、允许什么、多久有效，并能撤销。

### 产品价值

让外部 Agent 能在可承担责任的边界内进入产品。

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

协议 SDK 帮助实现流程，但应用仍负责主体映射、策略、密钥存储与供应商治理。

## Related Patterns

Permission Boundary、Approval、Data Governance、Zero Trust。

## 检查清单

- 协议连接的是 Tool/Resource 还是独立 Agent？
- 版本与 capability 是否显式协商？
- 身份、授权主体和 token audience 是否正确？
- Task、Message 和 Artifact 是否分开？
- 超时、取消、流式与异步如何呈现？

## 延伸练习与参考资料

测试错误 audience、过期 token、scope 不足和 token passthrough 四种失败。

- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [A2A 1.0 Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A 1.0 changes](https://a2a-protocol.org/latest/whats-new-v1/)
