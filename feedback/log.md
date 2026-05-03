# Feedback Log

> Record meaningful corrections, failures, and decisions here. The value is not the log itself; the value is routing each lesson back into rules, memory, or skills.

## Active Patches

Use this section for corrections that are still easy to repeat and have not yet been absorbed into rules, memory, or skills.

| Date | Patch | Owner File | Status |
|---|---|---|---|
| YYYY-MM-DD | Example patch | `CLAUDE.md` | Active |

Remove an active patch after it has become a rule, checkpoint, memory update, or tool constraint.

## Entry Types

| Type | Meaning |
|---|---|
| `fix-logic` | wrong logic, missing data, inconsistent fields |
| `fix-process` | skipped steps, one-option thinking, poor workflow |
| `fix-env` | dependency, permission, path, or tool issue |
| `privacy` | secret or personal data risk |
| `decision` | directional choice that should not be forgotten |
| `learning` | useful insight that may guide future behavior |

## Entry Template

```markdown
### YYYY-MM-DD

- Type:
- Context:
- Problem:
- Correction:
- Lesson:
- Updated:
```

`Updated:` is required. If nothing should be updated, write `Updated: none (reason: ...)`.

## Entries

### YYYY-MM-DD

- Type: learning
- Context: Initial starter-kit setup.
- Problem: Prompt-only systems do not preserve corrections across sessions.
- Correction: Add a feedback loop that routes lessons into rules, memory, or skills.
- Lesson: A personal agent needs a growth loop, not only a rule file.
- Updated: `README.md`, `CLAUDE.md`, `feedback/update-checklist.md`

