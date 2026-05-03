#!/usr/bin/env python
"""Self-review helper for personal agent decisions.

The script separates two review roles:

1. Challenger: finds risks and failure paths in a plan.
2. Coverage checker: checks whether the plan already addresses those risks.

Default env file:
  ~/.config/personal-agent.env

Offline self-test:
  python3 scripts/self_review.py self-test

Real review:
  python3 scripts/self_review.py review examples/decision-review-task.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ENV_FILE = Path.home() / ".config" / "personal-agent.env"
DEFAULT_BASE_URL = "https://api.openai.com/v1"


CHALLENGER_PROMPT = """You are the challenger.

Your only job is to attack the submitted plan.

Find fragile assumptions, missing constraints, edge cases, hidden risks, privacy issues, and likely failure paths.

Do not comfort the user.
Do not propose a replacement plan.
Do not defend the submitted plan.

Output:

## Core Risks
- Risk: plan assumption -> challenge -> possible failure

## Edge Cases
- ...

## Failure Preview
- If this plan fails later, the most likely reason is...

## Facts To Verify
- Assumption -> verification needed
"""


COVERAGE_PROMPT = """You are the coverage checker.

Your only job is to compare the challenger notes against the original plan.

For each challenge, decide whether the plan already covers it.

Allowed labels:
- covered
- partially covered
- uncovered

Do not propose fixes.
Do not rank importance.
Do not defend the plan.

Output a Markdown table:

| # | Challenge | Coverage | Objective Note |
|---|---|---|---|
"""


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_env_file(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    return True


def load_configured_env(explicit_env_file: Path | None) -> Path | None:
    if explicit_env_file:
        return explicit_env_file if load_env_file(explicit_env_file) else None
    return DEFAULT_ENV_FILE if load_env_file(DEFAULT_ENV_FILE) else None


def get_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing API key. Set OPENAI_API_KEY in the environment or in "
            f"{DEFAULT_ENV_FILE}."
        )
    return api_key


def get_model(cli_model: str | None) -> str:
    model = cli_model or os.environ.get("OPENAI_MODEL")
    if not model:
        raise SystemExit("Missing model. Set OPENAI_MODEL in the environment or pass --model.")
    return model


def get_base_url(cli_base_url: str | None) -> str:
    return (
        cli_base_url
        or os.environ.get("OPENAI_BASE_URL")
        or DEFAULT_BASE_URL
    )


def call_model(system_prompt: str, user_content: str, model: str, base_url: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }
    request = urllib.request.Request(
        build_chat_completions_url(base_url),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {get_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"API request failed: HTTP {exc.code}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"API request failed: {exc}") from exc

    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
        raise SystemExit(f"Unexpected API response:\n{formatted}") from exc


def build_chat_completions_url(base_url: str) -> str:
    url = base_url.rstrip("/")
    if url.endswith("/chat/completions"):
        return url
    return f"{url}/chat/completions"


def build_challenge_input(task: dict[str, Any]) -> str:
    context = task.get("context", "")
    constraints = task.get("constraints", "")
    plan = task.get("plan", "")
    if not context or not plan:
        raise SystemExit("Task JSON must include non-empty 'context' and 'plan' fields.")
    return f"Context:\n{context}\n\nConstraints:\n{constraints}\n\nPlan:\n{plan}\n"


def build_coverage_input(task: dict[str, Any], challenge: dict[str, Any]) -> str:
    plan = task.get("plan", "")
    challenge_text = challenge.get("challenge", "")
    if not plan or not challenge_text:
        raise SystemExit("Coverage requires task.plan and challenge.challenge.")
    return f"Plan:\n{plan}\n\nChallenger Notes:\n{challenge_text}\n"


def make_result(role: str, model: str, key: str, content: str) -> dict[str, Any]:
    return {
        "role": role,
        "model": model,
        "created_at": datetime.now(timezone.utc).isoformat(),
        key: content,
    }


def run_challenge(args: argparse.Namespace) -> dict[str, Any]:
    task = read_json(args.task)
    model = get_model(args.model)
    base_url = get_base_url(args.base_url)
    content = call_model(CHALLENGER_PROMPT, build_challenge_input(task), model, base_url)
    result = make_result("challenger", model, "challenge", content)
    if args.out:
        write_json(args.out, result)
    return result


def run_coverage(args: argparse.Namespace) -> dict[str, Any]:
    task = read_json(args.task)
    challenge = read_json(args.challenge)
    model = get_model(args.model)
    base_url = get_base_url(args.base_url)
    content = call_model(COVERAGE_PROMPT, build_coverage_input(task, challenge), model, base_url)
    result = make_result("coverage-checker", model, "coverage", content)
    if args.out:
        write_json(args.out, result)
    return result


def run_review(args: argparse.Namespace) -> dict[str, Any]:
    challenge_args = argparse.Namespace(task=args.task, model=args.model, base_url=args.base_url, out=None)
    challenge = run_challenge(challenge_args)
    if args.challenge_out:
        write_json(args.challenge_out, challenge)

    task = read_json(args.task)
    model = get_model(args.model)
    base_url = get_base_url(args.base_url)
    coverage_text = call_model(COVERAGE_PROMPT, build_coverage_input(task, challenge), model, base_url)
    coverage = make_result("coverage-checker", model, "coverage", coverage_text)
    if args.coverage_out:
        write_json(args.coverage_out, coverage)

    result = {"challenge": challenge, "coverage": coverage}
    if args.out:
        write_json(args.out, result)
    return result


def run_self_test() -> dict[str, Any]:
    task = {
        "context": "We need to decide whether this starter kit is ready for local review.",
        "constraints": "It must be small, private-data-free, and runnable offline.",
        "plan": "Ship a v0.1 template with rules, memory, skills, feedback, and self-review.",
    }
    challenge = make_result(
        "challenger",
        "offline-self-test",
        "challenge",
        "## Core Risks\n- Risk: small template -> may be too abstract -> users may not know what to edit first\n",
    )
    coverage = make_result(
        "coverage-checker",
        "offline-self-test",
        "coverage",
        "| # | Challenge | Coverage | Objective Note |\n|---|---|---|---|\n| 1 | Too abstract | partially covered | Quick start helps, but more examples may be needed. |\n",
    )
    return {
        "env_default": str(DEFAULT_ENV_FILE),
        "challenge_input_preview": build_challenge_input(task),
        "coverage_input_preview": build_coverage_input(task, challenge),
        "review": {"challenge": challenge, "coverage": coverage},
    }


def print_json(data: dict[str, Any]) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Personal agent self-review helper.")
    parser.add_argument("--model", help="Model name. Defaults to OPENAI_MODEL.")
    parser.add_argument("--base-url", help="OpenAI-compatible base URL.")
    parser.add_argument("--env-file", type=Path, help=f"Env file. Defaults to {DEFAULT_ENV_FILE}.")
    sub = parser.add_subparsers(dest="command", required=True)

    challenge = sub.add_parser("challenge", help="Run challenger only.")
    challenge.add_argument("task", type=Path)
    challenge.add_argument("--out", type=Path)

    coverage = sub.add_parser("coverage", help="Run coverage checker only.")
    coverage.add_argument("task", type=Path)
    coverage.add_argument("challenge", type=Path)
    coverage.add_argument("--out", type=Path)

    review = sub.add_parser("review", help="Run challenger and coverage checker.")
    review.add_argument("task", type=Path)
    review.add_argument("--challenge-out", type=Path)
    review.add_argument("--coverage-out", type=Path)
    review.add_argument("--out", type=Path)

    sub.add_parser("self-test", help="Run offline self-test.")

    args = parser.parse_args(argv)
    if args.command == "self-test":
        print_json(run_self_test())
        return 0

    env_path = load_configured_env(args.env_file)
    if not env_path:
        sys.stderr.write(f"No env file loaded. Using process environment only. Default: {DEFAULT_ENV_FILE}\n")

    result = {
        "challenge": run_challenge,
        "coverage": run_coverage,
        "review": run_review,
    }[args.command](args)

    if not getattr(args, "out", None):
        print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
