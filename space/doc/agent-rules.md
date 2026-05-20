# Agent Rules

## Purpose

This document defines detailed execution rules for AI agents working in this repository.

`space/README.md` is the bootstrap loader.

This file holds the detailed rules that should not be expanded into the bootstrap layer.

## Execution Rules

Agents MUST:

- prefer small incremental changes
- avoid rewriting large modules without explicit instruction
- avoid deleting user code without explicit request
- keep implementation aligned with current architecture and repository rules
- ensure files referenced by `space/README.md` actually exist before relying on them as runtime inputs
- update plan state before large edits
- update todo state after meaningful progress
- run the narrowest meaningful verification for the change
- record discoveries when they materially improve future recovery or execution

Agents MUST NOT:

- run dangerous shell commands without explicit user request
- bypass environment or sandbox restrictions
- expose secrets
- modify `.env` files unless requested
- remove existing functionality without explicit instruction

## Plan Lifecycle

The `plan/` directory is a stateful workflow.

Effective lifecycle:

```txt
draft -> active -> completed -> archived
```

Repository form:

```txt
current-plan.md -> history/
```

There MUST be only one active `current-plan.md`.

`current-plan.md` always represents the current highest-priority primary task.

It MUST NOT be used as a catch-all task list. Multi-task tracking belongs in `todolist/`.

Agents MUST archive the current plan when:

- the primary task is completed
- the primary task is abandoned
- the implementation direction significantly changes
- a new primary task replaces the current one

Archived plan snapshots MUST be stored in:

- `space/users/mantou-xia/plan/history/`

Archiving MUST use snapshot copy semantics, not move semantics.

That means:

- keep `current-plan.md` as the runtime plan file
- copy its state into `history/` as a dated snapshot
- then replace `current-plan.md` with the new active primary plan

History filenames MUST use:

```txt
YYYY-MM-DD-topic.md
```

Examples:

- `2026-05-19-dify-runtime-architecture.md`
- `2026-05-20-pokemon-rag-pipeline.md`
- `2026-05-21-agent-memory-system.md`

This naming rule exists so future agents can reason over plan timelines.

## Current Plan Format

`current-plan.md` SHOULD stay short and operational.

Recommended sections:

- `# Status`
- `## Task`
- `## Goal`
- `## Scope`
- `## Steps`
- `## Constraints`
- `## Acceptance`

Valid top-level status values are:

- `Active`
- `Blocked`
- `Completed`
- `Abandoned`

If the status is `Blocked`, the plan SHOULD include:

- `## Reason`

## Todo and Record Rules

Task tracking belongs in:

- `space/users/mantou-xia/todolist/todo.md`
- `space/users/mantou-xia/todolist/doing.md`
- `space/users/mantou-xia/todolist/done.md`
- `space/users/mantou-xia/todolist/blocked.md`

Recommended semantics:

- `todo.md`: not started but accepted tasks
- `doing.md`: currently active execution items
- `done.md`: completed task records or checkpoints
- `blocked.md`: blocked items with blocker reason and next dependency

Promotion rules:

- temporary findings -> `space/users/mantou-xia/research/`
- stable project conclusions -> `space/doc/`
- user-specific long-term preferences -> `space/users/mantou-xia/memory/`
- project-wide architectural decisions -> `space/doc/decisions.md`

## Execution Flow

Between "plan written" and "plan archived", every task MUST follow this execution flow:

```txt
1. Write plan to current-plan.md (Status: Active)
2. Decompose plan Steps into individual items in todo.md
3. Pick first item → move it to doing.md
4. Implement
5. Test
6. Item done → move it to done.md
7. If remaining todo items → repeat from step 3
8. All items done → set plan Status to Completed
9. Snapshot current-plan.md into history/ as YYYY-MM-DD-topic.md
10. Reset current-plan.md for next task
```

This ensures every step is traceable: todo shows what's planned, doing shows what's active, done shows what's finished.

Research rules:

- raw investigation notes and incomplete findings belong in `space/users/mantou-xia/research/`
- only stable conclusions should be promoted into `space/doc/` or `space/shared/`

## Recovery Intent

The planning system should allow the next agent run to recover:

- what the previous agent was doing
- why that direction was chosen
- what remains unfinished
- why work paused
- what is currently blocked
