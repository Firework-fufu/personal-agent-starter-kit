---
name: "self-review"
description: "Pressure-test important plans using a challenger pass and a coverage pass before the main agent makes a final judgment."
dependencies:
  tools:
    - "python3 or python"
  files:
    - "scripts/self_review.py"
    - "examples/decision-review-task.json"
  env:
    - "~/.config/personal-agent.env"
---

# Self Review

> Use this for important decisions. It is not a normal checklist. It separates plan creation, challenge, coverage checking, and final judgment.

## Triggers

Use this skill when:

- the user asks for a serious review;
- the plan affects project direction, architecture, business strategy, or public release;
- the agent may be too attached to its own proposal;
- the user asks for a red-team or adversarial check.

Do not use it for small edits or routine tasks.

## Input Format

Use a JSON task file:

```json
{
  "context": "What problem are we solving?",
  "constraints": "What must not be violated?",
  "plan": "What proposal should be reviewed?"
}
```

`context` and `plan` are required. `constraints` is optional but strongly recommended.

## Roles

| Role | Job | Not Allowed |
|---|---|---|
| Plan author | Writes the plan in the main conversation | Does not review itself |
| Challenger | Finds risks, edge cases, and failure paths | Does not comfort or propose alternatives |
| Coverage checker | Checks whether the plan already addresses each challenge | Does not rank or fix the plan |
| Final judge | Main agent decides what to change or accept | Does not ignore uncovered risks |

## Steps

### Step 1: Prepare The Plan

- Write the plan clearly enough for another model to review.
- Include rejected options and known risks when available.
- Avoid private context that should not be sent to an API.

Checkpoint: the plan can be understood without reading the current chat.

### Step 2: Write Task JSON

Use `examples/decision-review-task.json` as a template.

Checkpoint: the JSON parses and contains `context`, `constraints`, and `plan`.

### Step 3: Run Offline Self-Test First

```bash
python3 scripts/self_review.py self-test
```

Checkpoint: the command exits successfully.

### Step 4: Run Review

If you configured `~/.config/personal-agent.env`, run:

```bash
python3 scripts/self_review.py review examples/decision-review-task.json --challenge-out tmp/challenge.json --coverage-out tmp/coverage.json --out tmp/review.json
```

On Windows, use `python` if `python3` is not available.

The script uses Python standard library HTTP calls, so it does not require third-party Python packages.

Checkpoint: challenge and coverage files are generated.

### Step 5: Final Judgment

The main agent must summarize results like this:

```markdown
| Challenge | Coverage | Risk Level | Decision |
|---|---|---|---|
| ... | covered/partial/uncovered | critical/important/acceptable | change now / defer / accept |
```

Checkpoint: every important challenge has a decision.

### Step 6: Feedback

If the review changes the plan, record the decision in `memory/decisions.md` or `feedback/log.md`.

Checkpoint: future agents can see why the plan changed.

## Failure Handling

- Missing API key: run `self-test` only, or configure `OPENAI_API_KEY`.
- Missing model: set `OPENAI_MODEL` or pass `--model`.
- Bad JSON: fix the task file before calling the API.
- Challenger proposes solutions: treat as role drift and rerun.
- Coverage checker gives advice: treat as role drift and rerun.
- Many uncovered risks: do not automatically reject the plan; classify risks first.

## Version History

- v1 (2026-05-03): Initial public starter-kit version.
