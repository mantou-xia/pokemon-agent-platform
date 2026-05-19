# Decisions

## Purpose

This file records stable project decisions that future agents should treat as default unless superseded.

## Active Decisions

### 2026-05-19: `/space` is the Agent Workspace runtime

- `/space` is not a generic documentation folder.
- `space/README.md` acts as the bootstrap loader and context router.
- Detailed rules belong in specialized documents under `space/doc/` and user workspace files.

### 2026-05-19: README should stay thin

- `space/README.md` should remain a bootstrap/router document.
- Detailed execution rules should live in `space/doc/agent-rules.md`.
- README should route context; it should not become the full project knowledge base.

### 2026-05-19: Plan lifecycle uses snapshot history

- Only one active `current-plan.md` may exist.
- Historical plans are kept as snapshots in `space/users/mantou-xia/plan/history/`.
- Snapshot naming uses `YYYY-MM-DD-topic.md`.
- Archive by copy, not by move.

### 2026-05-19: Task state directory is `todolist/`

- User task state is tracked under `space/users/mantou-xia/todolist/`.
- `todo/` is not a separate active convention for this repository.

## Update Rule

Add a new entry here only when the decision is stable and should guide future work across tasks.
