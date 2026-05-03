# Public Release Checklist

Use this before publishing a customized version of the starter kit.

## Privacy

- [ ] No real personal names.
- [ ] No private local paths.
- [ ] No API keys or tokens.
- [ ] No private preferences that should not be public.
- [ ] No copied private memory from another project.

## Structure

- [ ] README explains what this is, who it is for, and how to start.
- [ ] `AGENTS.md` points to `CLAUDE.md`.
- [ ] `CLAUDE.md` points to memory, skills, and feedback files.
- [ ] `skills/INDEX.md` lists every skill directory.
- [ ] `feedback/update-checklist.md` explains where corrections should be routed.

## Examples

- [ ] `examples/decision-review-task.json` parses as JSON.
- [ ] `python3 scripts/self_review.py self-test` passes.
- [ ] README, skills, and examples use consistent field names: `context`, `constraints`, `plan`.

## Placeholders

- [ ] No unresolved task markers.
- [ ] No unresolved draft markers.
- [ ] No lowercase placeholder filler.
- [ ] No placeholder author names.
- [ ] No broken relative links.

## Scope

- [ ] README says v0.1 does not solve long-term memory cleanup.
- [ ] README does not promise support for every agent tool.
- [ ] README does not imply this is a full agent framework.
