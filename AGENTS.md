# AGENTS.md

Local book library/scanner project, being rebuilt as an offline-first desktop app.
Architecture and product details are still being explored. Add pointers to settled
architecture and development documentation here as they become available.

## Development Process

- Work in small, well-contained steps that can be discussed and verified independently.
- Agree on the current task's scope, approach, and completion criteria before implementing.
  Ask when a consequential decision is unresolved; do not silently choose for the user.
- Stay on the current task. Implement and verify the agreed scope, then discuss the
  outcome. Do not start the next step or adjacent work until the user agrees the current
  task is complete and authorizes moving on.
- If new information undermines the approach, pause and discuss a plan adjustment.
  Do not work around a design problem by adding complexity.
- Prefer simplicity and robustness: straightforward code, explicit behavior, and useful
  failure handling. Avoid speculative abstractions and features.
- Reuse existing patterns, components, and helpers before introducing new ones.
- Verify each change with checks appropriate to its behavior and impact. Report what
  was verified and any unresolved issues; passing checks alone is not user sign-off.

## Plan Files

- `PLAN_*.md` files capture scope, decisions, open questions, progress, and verification
  criteria. They support discussion and handoff; they are not permission to implement
  every listed step.
- Read the plan relevant to the current task before working. Follow an explicitly named
  plan; when asked for the latest plan, use file modification time rather than its name.
- Keep detailed design close to the step being discussed. Plans are a working baseline,
  not immutable specifications; revise them when agreed findings support a better approach.
- Keep the active plan current with agreed decisions, actual progress, verification
  results, and remaining questions. Distinguish proposals from settled decisions.
- Preserve useful experimental findings and samples even when prototype code is discarded.

## Code Style

- Keep changes small, obvious, and consistent with the surrounding code.
- Prefer short-circuit logic over nested conditionals.
- Use comments sparingly, primarily to explain non-obvious reasons.
- Be cautious with new dependencies, version pins, machine-specific paths, and setup
  assumptions. Introduce them deliberately and document what is required.

## Git Workflow

- Stay on the current branch; create or switch branches only when explicitly requested.
- Commit or push only when explicitly requested, using the current branch.
- Preserve changes made by the user or other agents. Do not revert, stash, or clean up
  unrelated work; stage only the files/hunks belonging to the requested commit.
