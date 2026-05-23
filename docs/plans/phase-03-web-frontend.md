# Phase 3 阶段规划

## 阶段定位

- 阶段名称：构建 Web 前端（`apps/web`）
- 阶段状态：Planned
- 前置阶段：Phase 2 已完成 pokemon-tools 接入 Dify Agent

## 阶段目标

在 Phase 2 的基础上，构建一个面向最终用户的 Web 前端应用，
让用户通过界面与 Pokemon Agent 进行对话交互，而不是仅通过 API 调用。

## 架构位置

```txt
User
↓
apps/web (本阶段建设)
↓
Dify Runtime (已就绪)
  ├── Agent Chat (已配置: Pokemon助手)
  └── pokemon-tools (已接入)
```

> 当前架构中 `services/api` 层尚未建设，本阶段前端直接对接 Dify API。
> `services/api` 作为统一的业务控制层将放入后续阶段。

## 重点工作

### 1. 技术选型与项目初始化

- 创建 `apps/web` 目录
- 技术栈：Next.js + Tailwind CSS + shadcn/ui
- 初始化项目脚手架，配置 TypeScript、ESLint

### 2. 聊天界面核心功能

- 消息气泡展示（用户消息 / Agent 回复）
- 消息输入框与发送按钮
- 流式输出渲染（SSE stream）
- 对话历史管理（基于 Dify conversation_id）

### 3. Agent 交互增强

- 显示 Agent 思考过程（tool calling 状态）
- 显示工具调用结果引用
- 加载状态与错误提示

### 4. 接入 Dify API

- 使用已创建的 API Key（`app-MxbH9j4SG861NENYrNf1hRsJ`）
- 实现聊天消息 API 调用
- 实现流式响应解析

## 预期交付

- 一个可运行的 Web 前端应用（`apps/web`）
- 通过浏览器访问后可开始与 Pokemon Agent 对话
- 基础聊天界面包含：输入框、消息列表、流式输出
- 部署文档与启动说明

## 暂不纳入本阶段

- `services/api` 业务控制层
- 用户登录/注册系统
- 宝可梦战斗 UI / Team Builder
- 知识库引用展示
- 响应式移动端适配
- 单元测试与 E2E 测试

## 交付标准

满足以下条件即可认为 Phase 3 完成：

- `apps/web` 可通过 `npm run dev` 启动
- 浏览器访问后可看到聊天界面
- 输入问题后，Agent 能流式返回回答
- Agent 调用工具时，界面上能看到工具调用状态
- 部署/启动说明可复现

## 关联文档

- [Phase 2 阶段快照](../snapshots/phase-02-dify-tool-integration.md)
- [Phase 3 阶段快照](../snapshots/phase-03-web-frontend.md)
