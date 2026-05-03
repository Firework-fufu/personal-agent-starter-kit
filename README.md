# Personal Agent Starter Kit

[中文说明](./README.zh-CN.md)

A minimal growth system for personal AI agents: rules, memory, skills, feedback loops, and self-review workflows.

This starter kit is for developers who already use tools like Claude Code, Codex, OpenAI-compatible model APIs, or other coding agents, but want something more durable than a pile of prompts.

The core idea:

```text
rules      -> tell the agent how to behave
memory     -> preserve long-term context
skills     -> turn repeated workflows into reusable SOPs
feedback   -> turn mistakes and corrections into system updates
self-review -> pressure-test important plans before acting
```

Without a feedback loop, an agent only follows today's prompt. With a feedback loop, it can gradually become a better fit for your work.

Important: this is not automatic training. The system improves only when you manually record a correction and route it into files the agent will load next time.

## Who This Is For

Use this starter kit if you:

- use coding agents regularly;
- keep repeating the same instructions across projects;
- want rules, memory, and workflows to be versioned as files;
- want a lightweight way to record mistakes and update the system;
- are comfortable editing Markdown and running a small Python script.

This is not for complete non-technical users yet. It is also not an agent framework, vector database, installer, or full memory product.

## How It Works

The starter kit is built around one loop:

```text
1. The agent works on a task.
2. It makes a mistake, misses context, or repeats a bad pattern.
3. You record the issue in feedback/log.md.
4. You classify what needs to change.
5. You update rules, memory, or skills.
6. The next run behaves differently.
```

That loop is the difference between a prompt collection and a personal agent growth system.

### A Tiny Example

Before:

```text
The agent writes code that calls a third-party API endpoint that does not exist.
```

Record it in `feedback/log.md`:

```markdown
### YYYY-MM-DD

- Type: fix-logic
- Context: The agent wrote an API integration.
- Problem: It invented an endpoint name instead of checking the real API.
- Correction: Do not invent API endpoints, function names, package methods, or database fields.
- Lesson: When an external interface is uncertain, inspect docs, types, schema, or examples first.
- Updated: `CLAUDE.md`
```

Then update `CLAUDE.md`:

```markdown
- Do not invent API endpoints, function names, package methods, or database fields. If unsure, inspect the source first.
```

After:

```text
Next time, when the agent is unsure about an API, it should inspect real documentation or source code before writing the call.
```

This is not automatic training. It is a lightweight maintenance discipline: record the correction, route it to the right file, and make the next run better.

The important part is the routing step. A note in `feedback/log.md` is only a record. It changes future behavior only after you update a file your agent actually loads, such as `CLAUDE.md`, `memory/user.md`, `memory/env.md`, or a `SKILL.md`.

## Repository Structure

```text
personal-agent-starter-kit/
├── README.md
├── AGENTS.md                     <- short entry point for agent tools
├── CLAUDE.md                     <- main behavior rules loaded by the agent
├── CHECKLIST.md                  <- public release checks
├── .config/
│   └── openai-compatible.env.example <- optional model API config example
├── memory/
│   ├── user.md                   <- write who you are, goals, collaboration preferences
│   ├── env.md                    <- write OS, tools, versions, local constraints
│   └── decisions.md              <- record durable decisions; can stay mostly empty on day one
├── skills/
│   ├── INDEX.md                  <- skill list and trigger map
│   ├── skill-lifecycle/
│   │   └── SKILL.md              <- create/update reusable workflows
│   └── self-review/
│       └── SKILL.md              <- pressure-test important plans
├── feedback/
│   ├── log.md                    <- record mistakes, corrections, lessons
│   └── update-checklist.md       <- decide where each lesson should be routed
├── scripts/
│   └── self_review.py            <- offline self-test and optional model review
└── examples/
    ├── decision-review-task.json <- sample review input
    └── decision-review-output.md <- sample final judgment format
```

## Quick Start

1. Copy this directory into a project where you use an AI coding agent.
2. Run the offline self-test before editing anything:

```bash
python3 scripts/self_review.py self-test
```

On Windows, use `python` if `python3` is not available.

Expected result: the command prints JSON with keys like `env_default`, `challenge_input_preview`, `coverage_input_preview`, and `review`. If it exits without an error, the offline script path is healthy.

This command does not call a model API and does not verify that your agent tool has loaded the rules.

How to read the self-test output:

| Field | Meaning |
|---|---|
| `env_default` | The default env file path the script will use for real model review |
| `challenge_input_preview` | A sample prompt that would be sent to the challenger role |
| `coverage_input_preview` | A sample prompt that would be sent to the coverage checker role |
| `review` | A fake offline review result used only to prove the script structure works |

3. Edit `memory/user.md` and `memory/env.md` with your own context.
4. Read `CLAUDE.md` and remove anything that does not match your workflow.
5. Optional: configure any OpenAI-compatible model API for real review calls:

```bash
cp .config/openai-compatible.env.example ~/.config/personal-agent.env
```

Then set `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` in `~/.config/personal-agent.env`.

You only need this optional config when you want `skills/self-review/SKILL.md` to run a real model review. Without it, the offline `self-test` still works.

### Where Should This Directory Live?

For the first trial, keep `personal-agent-starter-kit/` as a separate directory inside your project.

```text
your-project/
├── package.json / pyproject.toml / ...
└── personal-agent-starter-kit/
```

Once you decide to use it as your real project memory system, merge the important entry files into your project root:

- If your project does not have `AGENTS.md` or `CLAUDE.md`, copy them to the root.
- If your project already has rule files, merge the relevant sections manually.
- Keep `memory/`, `skills/`, and `feedback/` together so links and paths stay clear.

Merge principle:

- Keep your existing project-specific rules.
- Add the starter kit sections that define memory, skills, feedback, and error handling.
- Remove any generic rule that conflicts with your project.
- Do not overwrite an existing rule file without reading both files.

After merging, the project usually looks like this:

```text
your-project/
├── AGENTS.md
├── CLAUDE.md
├── memory/
├── skills/
├── feedback/
├── scripts/
└── examples/
```

### How Do Agent Tools Load These Files?

Different agent tools have different rule-file conventions. This starter kit uses a conservative pattern:

- `AGENTS.md` is a short entry point.
- `CLAUDE.md` is the main behavior file.
- `AGENTS.md` tells the agent to read `CLAUDE.md`.

Why keep both files? Because agent tools do not all look for the same rule file. `AGENTS.md` is the portable pointer. `CLAUDE.md` is the main rule body. If your tool reads `AGENTS.md`, it gets routed to `CLAUDE.md`; if your tool reads `CLAUDE.md` directly, the rule body is still there.

The default `AGENTS.md` is intentionally tiny:

```markdown
# Agent Entry Point

Read and follow the instructions in `./CLAUDE.md`.
```

If your tool has its own rule file name, merge the relevant parts of `CLAUDE.md` into that file. If your tool can be instructed manually, start a new session by telling it: "Read `AGENTS.md` and follow the linked `CLAUDE.md` instructions."

### How To Check If It Works

After copying or merging the files, start a fresh agent session and ask:

```text
Read the project agent rules. What are the main rules, memory files, skills, and feedback files you should use?
```

A good answer should mention:

- `CLAUDE.md` as the main rule file;
- `memory/user.md` and `memory/env.md`;
- `skills/INDEX.md`;
- `feedback/log.md` and `feedback/update-checklist.md`.

The `self-test` command only checks that the review script can run offline. It does not prove that your agent tool has loaded the rules.

If the answer does not mention these files, check whether your agent tool supports `AGENTS.md` automatically. If not, manually tell it to read `AGENTS.md`, or merge the relevant parts of `CLAUDE.md` into the rule file your tool actually loads.

## First Customization Pass

Start small. Do not try to design a perfect personal agent on day one.

Edit only these sections first:

- `memory/user.md`: who you are, what you are trying to do, how the agent should collaborate with you;
- `memory/env.md`: your operating system, tools, languages, and common local constraints;
- `CLAUDE.md`: the always-loaded rules your agent should follow;
- `feedback/log.md`: the place where future corrections will be recorded.

When you add a correction to `feedback/log.md`, open `feedback/update-checklist.md` immediately. It helps you decide whether the lesson belongs in `CLAUDE.md`, `memory/user.md`, `memory/env.md`, `skills/<skill>/SKILL.md`, or `skills/INDEX.md`.

The checklist is intentionally simple. It asks:

```text
What type of lesson is this?
Which file should absorb it?
Was that file updated?
Does the log entry say exactly what was updated?
```

Example: if the agent invented an API endpoint, the lesson belongs in `CLAUDE.md`. If it misunderstood your collaboration preference, it belongs in `memory/user.md`. If it missed a workflow step, it belongs in a `SKILL.md`.

## Built-In Skills

This starter kit includes two minimal skills.

| Skill | Use It When | Output |
|---|---|---|
| `skill-lifecycle` | You want to create or update a reusable workflow | A new or revised `SKILL.md` plus index and feedback updates |
| `self-review` | A decision is important enough to pressure-test | Challenge notes, coverage notes, and a final decision table |

The point is not to ship many skills. The point is to show the lifecycle:

```text
repeated workflow -> create skill
skill fails or drifts -> update skill
update has a reason -> record feedback
```

## What v0.1 Deliberately Does Not Solve

- Long-term memory cleanup and migration.
- Multi-agent orchestration.
- A full plugin system.
- Vector search or RAG storage.
- Support for every agent tool.
- A web UI or installer.
- Public sharing of private personal memory.

## Publication Gate

Before making your customized version public, run through `CHECKLIST.md`.

At minimum:

- no real names, private paths, API keys, or private preferences;
- no unresolved placeholders;
- example JSON parses;
- `python3 scripts/self_review.py self-test` passes;
- README, skills, and examples use consistent field names.
