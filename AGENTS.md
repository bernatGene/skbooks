# AGENTS.md

This repository is a side project for a local book library/scanner.

## Project summary

Currently work in progress

## Dev Workflow

- Avoid reinventing the wheel:
  - the pattern/component/function/helper you are writing might already exist or be
    implemented. Always re-use patterns, helpers and components when possible.
- Happy Path Only: Do not push on your own if you hit a wall; if the original plan has
  an issue that you just found out, instead of circumventing with spaghetti: PAUSE; let's
  discuss the issue, let's go back to the plan.

## Git Workflow

- Always work on the current branch
- Never switch branches unless explicitly requested
- Only commit if explicitly ask to
  - Commit and push to the current branch; do not create or switch to other branches

## Code Style

**General**

- Keep it simple
- Very minimal comments, in general NONE unless it's something that needs an "why?"
  explanation. - Always prefer short-circuit logic over nested ifs

## Principles

- Prefer simple, obvious changes over clever or machine-specific workarounds.
- Be cautious with new dependencies, pinned versions, absolute paths, local assumptions, or setup steps that are not documented.
