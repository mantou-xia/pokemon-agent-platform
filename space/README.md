# Agent Workspace

This directory is the runtime bootstrap for AI agents working in this repository.

This file is a bootstrap loader, not a full knowledge base.

Agents MUST read this file first, then load additional context on demand.

## Core Philosophy

- `No Plan, No Code.`
- `space/` is the Agent Workspace, not a generic docs folder.
- `README.md` routes context. Detailed rules belong in `space/doc/` and user workspace files.

## Startup Flow

Every non-trivial task MUST follow this order:

1. Read `space/README.md`
2. Decide what extra context is needed
3. Read only the required context files
4. Update `space/users/mantou-xia/plan/current-plan.md`
5. Update todo state if needed
6. Implement
7. Test
8. Record discoveries

For any multi-file modification, the agent MUST update `space/users/mantou-xia/plan/current-plan.md` before editing implementation files.

## Context Routing

Use this file as a router.

### Always check

- `space/doc/`
- `space/shared/`
- `space/users/mantou-xia/`
- `.cursor/rules/*.mdc` when `.cursor/rules/` exists

If `.cursor/rules/` does not exist, explicitly state that no `.mdc` project rules were available for this run.

### Load by task type

If the task involves project positioning or scope:

- read `space/doc/project-overview.md`

If the task involves system structure, module boundaries, runtime flow, or integration design:

- read `space/doc/architecture.md`

If the task involves coding style, implementation conventions, file organization, or change discipline:

- read `space/doc/coding-guidelines.md`

If the task involves project decisions, rationale, tradeoffs, or architecture history:

- read `space/doc/decisions.md`

If the task involves term definitions or naming interpretation:

- read `space/doc/glossary.md`

If the task involves agent behavior, safety, planning rules, git discipline, testing expectations, or record-keeping:

- read `space/doc/agent-rules.md`

If the task involves current implementation direction or unfinished primary work:

- read `space/users/mantou-xia/plan/current-plan.md`

If the task involves pending execution items:

- read `space/users/mantou-xia/todolist/todo.md`
- read `space/users/mantou-xia/todolist/doing.md`

If the task involves blocked work recovery:

- read `space/users/mantou-xia/todolist/blocked.md`

If the task involves long-term user preferences or recurring constraints:

- read `space/users/mantou-xia/memory/memory.md`

If the task needs shared roadmap or team backlog context:

- read `space/shared/memory/project-memory.md`
- read `space/shared/plan/roadmap.md`
- read `space/shared/todolist/backlog.md`

If the task needs previous investigation notes:

- read `space/users/mantou-xia/research/README.md`

Do not load the whole `space/` tree by default.

## Directory Responsibilities

- `space/doc/`: stable project knowledge and rules
- `space/shared/`: shared long-term team context
- `space/users/mantou-xia/plan/`: current primary plan and plan history
- `space/users/mantou-xia/memory/`: user-specific long-term preferences and constraints
- `space/users/mantou-xia/research/`: temporary investigation notes
- `space/users/mantou-xia/todolist/`: execution tracking for todo, doing, done, blocked

## High-Level Rules

- Only one active `current-plan.md` may exist.
- `current-plan.md` represents the highest-priority primary task only.
- Task lists belong in `todolist/`, not in `current-plan.md`.
- Detailed plan lifecycle, safety rules, and execution rules are defined in `space/doc/agent-rules.md`.

## Runtime Intent

The workspace exists to make AI-assisted software engineering traceable, recoverable, and consistent across long-running tasks and multi-agent collaboration.
