# Architecture

## 架构目标

本项目的架构目标不是单纯把大模型接到前端，而是构建一个由 Dify 驱动、由 `/space` 持续供给上下文的长期运行 Agent 平台。

整体上，系统同时满足两类需求：

1. 面向用户的 Pokemon Agent 产品能力
2. 面向长期工程协作的 Agent 运行与开发能力

## 顶层架构

```txt
pokemon-agent-platform/
├── dify/
├── apps/
├── services/
├── plugins/
├── packages/
├── infra/
└── space/
```

可以把整个系统看成三层：

```txt
Experience Layer
  └─ apps/

Business Control Layer
  └─ services/ + plugins/ + packages/

Agent Runtime and Memory Layer
  └─ dify/ + space/
```

## 核心分层说明

### 1. `dify/`: Agent Runtime Layer

`dify/` 是 AI Runtime 底座，主要承担：

- Chatflow
- Workflow
- Agent orchestration
- RAG
- Tool Calling
- Model Routing
- Prompt Runtime
- Knowledge Base

架构原则：

- 以 fork + 自部署为主
- 尽量不修改 Dify 源码
- 只有在必要场景下做少量 patch

它负责“让 Agent 跑起来”，但不负责整个业务系统的最终控制。

### 2. `apps/`: Experience Layer

`apps/web` 是面向最终用户的产品前端。

建议技术栈：

- Next.js
- Tailwind CSS
- shadcn/ui

前端职责包括：

- 聊天 UI
- Battle UI
- Team Builder UI
- 知识库引用展示
- Agent 状态展示

未来可扩展：

- 实时 Agent 面板
- Tool 调用过程展示
- Workflow 可视化

### 3. `services/`: Business Control Layer

`services/` 是业务核心层，不应由 Dify 直接替代。

#### `services/api`

这是业务大脑和统一控制入口，负责：

- 用户系统
- 权限
- 会员
- 积分
- 支付
- 日志
- Conversation 管理
- Space 管理
- Dify API 转发
- Agent Runtime Control

关键架构原则：

```txt
Frontend
↓
services/api
↓
Dify API
```

而不是：

```txt
Frontend
↓
Dify
```

也就是说，Dify 是 AI 能力后端，不是整个产品的业务后端。

#### `services/crawler`

负责外部 Pokemon 知识抓取与知识化处理。

主要来源：

- Bulbapedia
- Pokemon Wiki
- 神奇宝贝百科

处理流程：

```txt
网页
↓
Markdown
↓
清洗
↓
Chunk
↓
Embedding
↓
Dify Knowledge
```

#### `services/pokemon-data`

负责结构化 Pokemon 数据服务。

存在原因：

- RAG 适合解释与检索
- RAG 不适合精确计算

因此以下能力必须结构化：

- 属性克制
- 技能倍率
- 种族值
- 进化链

推荐存储：

- PostgreSQL

核心数据域建议包括：

- `pokemon`
- `moves`
- `abilities`
- `types`
- `evolution_chains`

### 4. `plugins/`: Deterministic Tool Layer

`plugins/` 为 Dify Agent 提供确定性能力。

典型工具包括：

- `get_pokemon_info`
- `get_move_info`
- `get_type_effectiveness`
- `recommend_team`
- `analyze_battle_log`

核心原则：

```txt
RAG 负责解释
Tool 负责计算
```

不要把确定性规则计算交给模型猜测。

### 5. `packages/`: Shared Modules Layer

用于承载 Monorepo 公共模块，例如：

- `ui/`
- `sdk/`
- `types/`
- `utils/`

原则是把跨应用、跨服务复用的能力抽离到这里，而不是在各模块中重复实现。

### 6. `infra/`: Infrastructure Layer

负责部署与运行环境，包括：

- `docker-compose`
- nginx
- deployment scripts
- CI/CD

### 7. `space/`: Agent Memory OS Layer

`space/` 是整个项目最关键的持久化上下文层。

它不是普通文档目录，而是 Agent Workspace。

它提供：

- 长期记忆
- 规划
- 任务状态
- 开发规则
- 架构上下文
- research
- context recovery

它的角色可以定义为：

```txt
Dify = Agent Runtime
/space = Agent Operating System
```

## 关键系统关系

### 用户请求路径

```txt
User
↓
apps/web
↓
services/api
↓
Dify Runtime
↓
RAG / Workflow / Agent / Tools
```

这里 `services/api` 负责产品级控制、鉴权、日志、计费、会话管理与系统边界隔离。

### 知识路径

```txt
External Pokemon Sources
↓
services/crawler
↓
Cleaned Markdown / Chunk / Embedding
↓
Dify Knowledge Base
↓
RAG Retrieval
```

### 精确计算路径

```txt
User Question or Agent Task
↓
Plugin Tool Call
↓
services/pokemon-data
↓
Structured Database / Deterministic Result
↓
Agent Response Assembly
```

### 工程上下文路径

```txt
Task Start
↓
Read space/README.md
↓
Load doc / memory / plan / todo
↓
Generate or update plan
↓
Implement
↓
Test
↓
Record discoveries back into /space
```

这条链路定义了 Agent 的工程运行方式，而不是业务请求方式。

## `/space` 内部架构

`space/` 当前采用如下结构：

```txt
space/
├── README.md
├── doc/
├── shared/
└── users/
```

职责划分如下：

- `README.md`: Agent Runtime Bootstrap
- `doc/`: 稳定项目知识，如概览、架构、规范、决策
- `shared/`: 团队共享长期上下文
- `users/`: 用户或 Agent 个人工作区

其中 `README.md` 是运行时入口，不是普通说明文档。

## Agent 执行架构

当前项目采用的 Agent 软件工程闭环是：

```txt
1. Read Context
2. Load Memory
3. Read Architecture
4. Read Current Plan
5. Read Todo
6. Generate Plan
7. Update Todo
8. Implement
9. Test
10. Record Discoveries
11. Update Memory
```

对应的核心约束是：

- No Plan, No Code
- 多文件修改前先更新当前计划
- 优先小步修改
- 结果需要可追踪、可恢复、可协作

## 架构原则

项目当前应遵守以下架构原则：

1. Dify 负责 AI Runtime，不负责全部业务控制
2. `services/api` 是统一业务控制平面
3. RAG 用于解释、引用与开放知识理解
4. Tool 用于确定性调用与精确结果
5. 结构化数据优先承载可计算事实
6. `/space` 承载长期工程上下文，不允许 Agent 每次从零开始
7. 尽量在不侵入 Dify 源码的前提下完成产品构建

## 当前重点

当前阶段的架构重点不是追求单点功能堆叠，而是建立一套稳定的长期 Agent 工作机制，使业务产品层与 Agent 工程层能够同时演进。
