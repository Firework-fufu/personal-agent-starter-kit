# Feedback Update Checklist

> Use this immediately after writing a feedback log entry. A lesson that does not update the system is easy to forget.

## Route The Lesson

| Lesson Type | Update Target |
|---|---|
| Behavior rule | `CLAUDE.md` |
| User preference | `memory/user.md` |
| Environment/tool issue | `memory/env.md` |
| Reusable workflow | `skills/<skill>/SKILL.md` |
| Skill trigger or path | `skills/INDEX.md` |
| Directional decision | `memory/decisions.md` |
| Public release risk | `CHECKLIST.md` |

## Checklist

- [ ] What type of lesson is this?
- [ ] Which file should absorb it?
- [ ] Was that file updated?
- [ ] Does the update match the log entry?
- [ ] Did the log entry include an `Updated:` line?
- [ ] If it is still easy to repeat, did it go into `feedback/log.md` Active Patches?
- [ ] If it is fully absorbed, should an old Active Patch be removed?

## Good Pattern

```markdown
- Problem: The agent guessed a database field.
- Lesson: Inspect real schema before writing database code.
- Updated: `CLAUDE.md`, `memory/env.md`
```

## Bad Pattern

```markdown
- Lesson: Be more careful next time.
- Updated:
```

This does not change future behavior.

