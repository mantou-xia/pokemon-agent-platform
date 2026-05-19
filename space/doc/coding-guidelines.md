# Coding Guidelines

## Purpose

This document defines project-level implementation conventions for agents and human contributors.

Use this file when the task involves code changes, refactors, naming, or file placement decisions.

## General Principles

- Prefer small incremental changes over broad rewrites.
- Keep changes aligned with existing project structure and architecture.
- Do not invent new layers when an existing layer already owns the behavior.
- Preserve user code unless removal is explicitly requested.
- Favor deterministic system behavior over prompt-only behavior when correctness matters.

## Layer Ownership

- `dify/`: upstream runtime base, minimize local source changes
- `apps/`: user-facing application experiences
- `services/`: business control, data flow, and system integrations
- `plugins/`: deterministic tool interfaces for agent capabilities
- `packages/`: shared monorepo modules
- `infra/`: deployment and environment automation

## Implementation Discipline

- Frontend should route through business APIs, not directly depend on Dify as the product backend.
- RAG should explain and retrieve; tools and structured data should handle precise calculation.
- New code should follow the nearest local pattern before introducing a new abstraction.
- Shared logic should move to `packages/` only when reuse is real, not speculative.
- File and symbol naming should be explicit and domain-oriented.

## Change Boundaries

- Architecture changes should update `space/doc/architecture.md` or `space/doc/decisions.md`.
- Rule changes should update `space/doc/agent-rules.md` or this file.
- New long-term workflow conventions should be reflected in `/space`, not left only in chat.

## Verification Expectations

- Run the narrowest meaningful verification for the modified scope.
- If tests are not run, record that fact explicitly in the task result.
- If a change is documentation-only, verify path correctness and routing consistency.
