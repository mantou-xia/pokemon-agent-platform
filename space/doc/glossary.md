# Glossary

## Agent Workspace

The persistent workspace under `space/` used to provide runtime context, planning, memory, and recovery for AI agents.

## Bootstrap Loader

The startup document that tells an agent what to read next. In this repository, that file is `space/README.md`.

## Current Plan

The single active primary-task plan stored in `space/users/mantou-xia/plan/current-plan.md`.

## Plan History

Snapshot records of previous primary-task plans stored in `space/users/mantou-xia/plan/history/`.

## Todo State

Execution status files under `space/users/mantou-xia/todolist/`, including `todo.md`, `doing.md`, `done.md`, and `blocked.md`.

## Research

Temporary investigation notes that are not yet stable enough to promote into project-wide documents.

## Dify Runtime

The AI runtime layer responsible for workflow, agent execution, RAG, tool calling, and model routing.

## Agent Operating System

The role played by `/space`: long-term memory, planning, task state, architecture context, and recovery.

## Structured Pokemon Data

Deterministic data sources used for exact Pokemon rules and calculations that should not rely on RAG alone.
