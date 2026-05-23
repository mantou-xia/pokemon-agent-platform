# Done

- 2026-05-20: 引入 Dify 上游代码（`dify/`），完成 Docker Compose 启动，12 个容器全部运行，`http://localhost` 访问正常，Dify 处于可用状态。
- 2026-05-20: 构建宝可梦数据层与工具：services/pokemon-data（40 只宝可梦、18 属性、120 条克制关系、19 条进化链）+ plugins/pokemon-tools（4 个 API 工具，端口 8100）
- 2026-05-20: 建立根级 `docs/` 人类文档层，补齐 Phase 1 总结、Phase 2 规划与阶段快照映射，并同步更新 `space` 架构/决策说明

- 2026-05-22: **Phase 2 完成 — pokemon-tools 接入 Dify Agent**
  - Dify 容器内部连通性验证通过（host.docker.internal:8100）
  - pokemon-tools 全部 8 个工具已通过 OpenAPI 导入"Pokemon助手"Agent 应用并启用
  - 创建 Dify API Key（`app-MxbH9j4SG861NENYrNf1hRsJ`）
  - 完成 Dify Console API 认证流程文档化（Base64 密码编码）
  - 更新启动清单（Dify 容器自动启动 + nginx 502 修复 + PostgreSQL 端口暴露）
  - 沉淀完整执行流 memory（phase-02-execution-flow.md）
  - 切换模型至 DeepSeek API（deepseek-chat），Agent 工具调用链路验证通过
  - 测试脚本整理到 `test/` 目录
