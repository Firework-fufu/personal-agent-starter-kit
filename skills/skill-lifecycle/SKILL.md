---
name: "skill-lifecycle"
description: "Create and update reusable agent skills: decide if a workflow deserves a skill, draft it, add checkpoints, index it, and route future corrections through feedback."
dependencies:
  files:
    - "skills/INDEX.md"
    - "feedback/log.md"
    - "feedback/update-checklist.md"
---

# Skill Lifecycle

> Use this when a repeated workflow should become a skill, or when an existing skill fails and needs to be updated.

## Triggers

Use this skill when the user says:

- "create a skill"
- "turn this into a skill"
- "update this skill"
- "improve this workflow"
- "the skill missed a step"

## Preflight

- [ ] Is this workflow likely to repeat?
- [ ] Is the output format stable?
- [ ] Does the workflow have steps that an agent might skip?
- [ ] Is there already a similar skill in `skills/INDEX.md`?
- [ ] Are we creating a new skill or updating an existing one?

## Decision: Create Or Update

| Situation | Action |
|---|---|
| New repeated workflow | Create a new skill |
| Existing skill missed a step | Update the existing skill |
| Trigger wording changed | Update the skill and `skills/INDEX.md` |
| Output format changed | Update the skill, examples, and downstream references |
| Workflow is one-off | Do not create a skill; answer directly |

## Create A Skill

### Step 1: Name The Skill

- Use lowercase kebab-case, such as `publish-report`.
- Make the name action-oriented.

Checkpoint: the name is unique in `skills/INDEX.md`.

### Step 2: Define The Contract

Write these five fields before drafting:

- Trigger: when should the agent use it?
- Inputs: what does it need?
- Steps: what does the agent do?
- Output: what is produced?
- Failure modes: what usually goes wrong?

Checkpoint: each field has a concrete answer.

### Step 3: Draft `SKILL.md`

Use this template:

```markdown
---
name: "skill-name"
description: "Trigger + output in one sentence."
dependencies:
  tools: []
  files: []
  skills: []
---

# Skill Title

> One-sentence purpose.

## Triggers

- Use when...

## Preflight

- [ ] Required condition

## Steps

### Step 1: ...

- Action
- Must: non-negotiable rule

Checkpoint: how to know this step is complete.

## Verification

- [ ] Final check

## Failure Handling

- If X fails, do Y.

## Version History

- v1 (YYYY-MM-DD): Initial version.
```

### Step 4: Make It Weak-Model Friendly

Add:

- explicit "Must" rules for non-negotiable behavior;
- checkpoints after important steps;
- at least one common failure mode;
- a final verification section.

Checkpoint: a weaker model can follow the skill without relying on hidden context.

### Step 5: Add It To The Index

Update `skills/INDEX.md` with:

```markdown
| `skill-name` | trigger | output | `skills/skill-name/SKILL.md` |
```

Checkpoint: the new skill can be found from the index.

### Step 6: Record The Reason

Add an entry to `feedback/log.md` explaining why this skill was created.

Checkpoint: the log entry has an `Updated:` line.

## Update A Skill

### Step 1: Diagnose The Failure

Classify the update:

| Type | Symptom | Likely Update |
|---|---|---|
| Rule gap | Agent skipped or misread a step | Add a Must rule or checkpoint |
| Trigger gap | Skill should have been used but was not | Update trigger wording and index |
| Output drift | Output fields changed or became inconsistent | Update format and examples |
| Tool/env issue | The skill assumes a missing tool or wrong path | Update dependencies and env memory |

Checkpoint: the failure type is named before editing.

### Step 2: Read Current State

Read the full current `SKILL.md` before editing.

Checkpoint: you can summarize the current trigger, steps, and version history.

### Step 3: Edit Precisely

- Do not rewrite the whole skill unless the user asks.
- Add the smallest rule, step, or checkpoint that prevents recurrence.
- If triggers changed, update `skills/INDEX.md`.
- If environment assumptions changed, update `memory/env.md`.

Checkpoint: the edit matches the diagnosis.

### Step 4: Append Version History

Add one line:

```markdown
- vN (YYYY-MM-DD): What changed and why.
```

Checkpoint: old version history remains intact.

### Step 5: Route The Feedback

Add an entry to `feedback/log.md`, then use `feedback/update-checklist.md`.

Checkpoint: the log says exactly which files were updated.

## Verification

- [ ] Skill file exists.
- [ ] `skills/INDEX.md` matches trigger and path.
- [ ] Checkpoints exist after important steps.
- [ ] Feedback entry explains why the skill exists or changed.
- [ ] No private user data is included.

## Version History

- v1 (2026-05-03): Initial public starter-kit version combining create and update into one lifecycle skill.

