# Docs Layer

`docs/` 是仓库中的人类可读文档层，用于沉淀阶段汇报、阶段目标和阶段快照。

它和 `space/` 的职责不同：

- `docs/` 面向人类读者，提供阶段性阅读入口
- `space/` 面向 Agent 运行时，保存计划、待办、历史和恢复上下文

如果需要了解项目当前阶段进展，先从这里开始；如果需要恢复 Agent 执行状态，仍应从 `space/README.md` 开始。

## 目录说明

- `reports/`：阶段总结、阶段性汇报
- `plans/`：下一阶段目标、实施重点、交付标准
- `snapshots/`：阶段快照与 `space` 事实来源映射

## 阅读顺序

1. 读 [Phase 1 阶段总结](./reports/phase-01-pokemon-data-and-tools.md)
2. 再读 [Phase 2 阶段规划](./plans/phase-02-dify-tool-integration.md)
3. 如需追溯事实来源，进入 [Phase 1 阶段快照](./snapshots/phase-01-pokemon-data-and-tools.md)

## 维护原则

- `docs/` 只做总结、规划和索引，不复制 `space/` 中的完整运行时正文
- 阶段汇报与阶段规划分开存放，不混写
- 每个阶段都应在 `snapshots/` 下有对应快照，映射到 `space` 中的计划和完成记录
- 运行时事实以 `space/` 和实现目录为准，`docs/` 不作为执行真相源
