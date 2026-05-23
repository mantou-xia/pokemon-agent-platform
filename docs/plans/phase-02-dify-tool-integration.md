# Phase 2 阶段规划

## 阶段定位

- 阶段名称：`pokemon-tools` 接入 Dify Agent
- 阶段状态：**Completed**
- 前置阶段：Phase 1 已完成 Pokemon 数据层与工具层基础建设

## 阶段目标

下一阶段的目标不是继续扩展数据量或业务边界，而是把现有 `pokemon-tools` 真正接入 Dify，使 Agent 能在运行时稳定调用这些工具。

## 重点工作

- [x] 明确 Dify 中的工具接入方式 — OpenAPI 导入
- [x] 验证 `plugins/pokemon-tools/openapi.yaml` 是否可直接作为导入入口 — 可行
- [x] 确认工具服务、Dify 容器和 PostgreSQL 的运行链路 — 已打通
- [x] 补齐接入操作说明和验证步骤 — 见 execution-flow.md
- [x] 用一个最小问题链路验证 Agent 调用成功 — 通过 DeepSeek API 验证

## 预期交付

- [x] 一套可复现的 Dify 工具接入步骤
- [x] 一次成功的 Agent 工具调用验证记录
- [x] 对外说明当前工具可用范围与限制
- [x] 必要时补齐接入相关的运行文档，而不是扩展到新业务模块

## 暂不纳入本阶段

- `services/api` 的接口设计与实现
- `services/crawler` 到 Dify Knowledge 的采集链路
- 新一轮大规模 Pokemon 数据扩充

## 交付标准

- [x] Dify 中已能识别并接入 `pokemon-tools`
- [x] 至少 1 条 Agent 调用链路能成功返回工具结果
- [x] 接入说明足以让后续执行者复现
- [x] 阶段快照能映射到对应的 `space` 计划与完成记录

## 关联文档

- [Phase 1 阶段总结](../reports/phase-01-pokemon-data-and-tools.md)
- [Phase 2 阶段快照](../snapshots/phase-02-dify-tool-integration.md)
