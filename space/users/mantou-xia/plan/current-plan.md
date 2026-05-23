# Status

Active

## Task

Phase 3: 构建 Web 前端（`apps/web`）

## Goal

构建一个面向最终用户的 Web 聊天界面，让用户通过浏览器与 Pokemon Agent 对话，支持流式输出和工具调用状态展示。

## Scope

- 初始化 `apps/web` Next.js 项目（Tailwind CSS + shadcn/ui）
- 实现聊天界面（消息气泡、输入框、发送按钮）
- 对接 Dify API（流式响应解析）
- 展示 Agent 工具调用状态
- 对话历史管理

## Steps

1. 环境检查（Node.js/npm）并初始化 Next.js 项目
2. 配置 Tailwind CSS 和 shadcn/ui
3. 实现核心聊天组件（消息列表、输入框）
4. 对接 Dify Chat API（流式 SSE 解析）
5. 实现工具调用状态展示
6. 基础 UI 美化与手势优化
7. 验证端到端流程

## Constraints

- 不实现用户登录/注册（直接使用现有 API Key）
- 不引入 `services/api` 层
- 不考虑移动端适配

## Acceptance

- [ ] `apps/web` 可通过 `npm run dev` 启动
- [ ] 浏览器访问 http://localhost:3000 可见聊天界面
- [ ] 输入问题后 Agent 流式返回回答
- [ ] 工具调用时界面上可见状态
- [ ] 部署/启动说明可复现
