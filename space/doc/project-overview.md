# Project Overview

## 项目一句话定义

`pokemon-agent-platform` 本质上不是普通的 AI Chat 产品，而是一个基于 Dify Runtime、使用 `/space` 作为 Agent Operating System、面向长期 AI 软件工程与 Pokemon Agent 场景的 AI-Native 开发平台。

在这个模型之外，仓库还包含一个并行的 `docs/` 层，用于面向人类读者输出阶段汇报、阶段规划和阶段快照。

## 核心定位

项目有两个同时存在的层级：

### Level 1: 业务层（Pokemon Agent）

这是最终用户直接感知到的产品层，目标是构建一个 AI Native Pokemon 平台。

主要能力包括：

- 宝可梦百科问答
- 战斗分析
- 属性克制计算
- 队伍推荐
- Wiki RAG 检索与引用
- 多 Agent 协作

### Level 2: Agent Engineering Layer

这是项目更重要的底层能力层，目标是构建一个可长期运行的 AI 软件工程工作流系统。

核心特征包括：

- Agent 有长期记忆
- Agent 有规划能力
- Agent 有上下文恢复能力
- Agent 不必每次从零开始
- Agent 可以沉淀架构知识
- Agent 可以维护长期项目
- Agent 可以支持多人和多 Agent 协作

这一层的关键载体是：

- `/space`

## 核心思想

整个项目由两个互补部分组成：

### Dify 提供 Agent Runtime

Dify 负责：

- LLM Runtime
- Workflow
- Agent
- RAG
- Tool Calling
- Model Routing
- Prompt Runtime
- Knowledge Base

### `/space` 提供 Agent Operating System

`/space` 负责：

- 长期记忆
- 规划
- 任务状态
- 开发规则
- 架构上下文
- Research
- Context Recovery

因此，项目的基本认知模型是：

```txt
Dify = Agent Runtime
/space = Agent Operating System
docs/ = Human Reporting Layer
```

## 项目目标

项目不是只做一个 Pokemon Wiki Chatbot，而是要验证并沉淀一套长期可运行的 AI 原生软件工程工作流。

当前目标可以概括为：

1. 在业务层交付可用的 Pokemon Agent 产品体验
2. 在工程层建立可复用的 Agent 记忆、规划、研究与恢复机制
3. 让 Agent 能在长期项目中持续积累上下文，而不是每轮重新开始

## 仓库整体结构

```txt
pokemon-agent-platform/
├── dify/
├── docs/
├── apps/
├── services/
├── plugins/
├── packages/
├── infra/
└── space/
```

各目录的高层职责如下：

- `dify/`: Dify AI Runtime 底座，尽量保持 fork + 自部署，避免重度改源码
- `apps/`: 面向用户的应用层，尤其是 Web 前端
- `services/`: 业务核心能力与数据处理服务
- `plugins/`: Dify Tool Plugins，为 Agent 提供确定性工具能力
- `packages/`: Monorepo 公共模块
- `infra/`: 部署与基础设施
- `space/`: AI Agent 长期开发工作区
- `docs/`: 面向人的阶段文档层

## `/space` 的意义

`/space` 不是普通文档目录，而是整个项目最重要的 Agent Workspace。

它解决的是：

```txt
Agent 每次都失忆
```

它让 Agent 具备：

1. 长期记忆
2. 任务计划
3. 任务状态追踪
4. 研究记录
5. 架构理解
6. 上下文恢复能力

## Agent 工作方式

当前项目希望 Agent 按以下工作闭环运行：

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

这是项目的 AI Software Engineering Loop，也是 `/space/README.md` 所约束的实际执行模型。

## 技术路线

当前项目的技术路线是：

```txt
Dify
+ RAG
+ Tool Calling
+ Workflow
+ /space Memory System
+ Structured Pokemon Data
+ Custom Frontend
```

设计原则包括：

- RAG 负责解释与引用
- Tool 负责确定性计算
- 结构化数据负责精确事实与规则
- `/space` 负责长期工程上下文

## 核心创新

项目真正的核心创新并不是 Pokemon 问答本身，而是 Agent 持久化上下文系统，即：

```txt
space/
```

通过 `memory`、`plan`、`research`、`todo`、`architecture`、`decisions` 这些结构，项目试图让 Agent 具备接近长期工程协作者的工作能力。

与之配套，`docs/` 负责把这些运行时沉淀转化为人类更容易阅读的阶段汇报与阶段规划，但不替代 `space/` 的执行地位。

## 当前共识

后续所有 Agent 在理解本项目时，应优先采用以下共识：

1. 这是一个 AI-Native Software Engineering Workspace，而不仅是聊天产品
2. `services/api` 是业务控制中心，不应让前端直接依赖 Dify
3. `plugins` 和结构化数据用于补足大模型在精确计算上的不足
4. `/space` 是长期记忆与规划系统，不是装饰性文档目录
5. `No Plan, No Code` 是项目级执行原则
