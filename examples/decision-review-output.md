# Example Decision Review Output

This is a hand-written example of the final judgment format. Real review output can be generated with `scripts/self_review.py`.

| Challenge | Coverage | Risk Level | Decision |
|---|---|---|---|
| The starter kit may feel too abstract if it only explains concepts. | partially covered | important | Add a concrete mistake-to-update loop in README. |
| Two skills may look too thin for a starter kit. | covered | acceptable | Explain that v0.1 demonstrates lifecycle, not skill volume. |
| Private memory could leak into the public template. | covered | critical | Keep memory files as blank templates and run `CHECKLIST.md`. |

## Final Judgment

Proceed with v0.1 if:

- the README shows the full growth loop;
- all memory files are templates;
- the offline self-test passes;
- public release checklist passes.

