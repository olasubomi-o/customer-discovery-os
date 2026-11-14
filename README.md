# Customer Discovery OS

Free tools from [The Product Builders](https://theproductbuilders.com) for founders and product managers who want evidence, not encouragement, before they build.

It turns the 25 prompts, worksheets and checklist of the *Customer Discovery Prompt Playbook* into 13 skills, 2 agents and a shared evidence folder. The skills read from and write to the same `discovery/` folder, so each step builds on the last: assumptions, interviews, extraction, synthesis, red-team, experiments, decision memo.

## What is different about it
- **Shared memory.** One `discovery/` folder holds your context, transcripts, extractions, evidence ledger, experiments and memos.
- **Enforced standards.** A checker (`ddos.py check`) rejects fabricated quotes, findings with no interview ID, "Strong" evidence built on opinions, experiments with thresholds set after the fact, and more. In Claude Code a hook runs it after every write. Elsewhere the skills run it as a required last step.
- **A red-team agent** that tries to disprove your hypothesis from a fresh context.
- **A web research skill** for competitors, alternatives and online sentiment, always labelled secondary evidence with sources and dates.

## Install

**Claude Code**
```
/plugin marketplace add olasubomi-o/customer-discovery-os
/plugin install customer-discovery-os@product-builders
```
Then run `/discover`.

**Claude.ai** (Settings, Capabilities, Skills): upload the zips from `dist/skills/`. Start with `discovery-guide` and `discovery-start`.

**ChatGPT**: ChatGPT supports the same SKILL.md skill format on plans where skills are enabled. Upload the same zips. On plans without skills, use `dist/chatgpt-project/` (instructions plus knowledge files). The fallback is weaker: see below.

## How enforcement really works, by platform
| Platform | Automatic check after each write | Scripts can run | Shared folder persists |
|---|---|---|---|
| Claude Code (plugin) | Yes, hook | Yes | Yes, in your project |
| Claude.ai / ChatGPT skills | No. The skill instructs the model to run the check | Only if code execution is on | Depends on the platform. Test it. |
| ChatGPT Project fallback | No | Only with Code Interpreter | No. Paste `ledger.csv` back each session |

Enforcement catches structural cheating. It cannot judge whether an insight is good, and no tool can make a founder talk to customers. See `shared/references/standards.md` for exactly what is enforced and what is advisory.

## Running several hypotheses
One `discovery/` folder holds exactly one hypothesis. Create it with `ddos.py init --hypothesis "short name"`; this writes `hypothesis.json`, stamps `Hypothesis-ID` in `context.md` and a `Hypothesis:` line on every ingested interview. `ddos.py check` then fails if any file carries a different hypothesis id, which catches a transcript or synthesis pasted into the wrong project. Keep each idea in its own project folder (for example `ideas/invoice-chasing/discovery/`) and run `ddos.py list --root .` to see them all. `status` always prints which hypothesis and folder is active.

What this does not cover: the conversation itself and any account-level AI memory. Use one chat per hypothesis, and on ChatGPT one Project per hypothesis. Older folders without `hypothesis.json` still work and get a warning.

## Privacy
Interview material is personal data. `discovery/interviews/` and `extractions/` are git-ignored by default. Ingest redacts emails, phone numbers and names you list; it does not detect names automatically. Record consent per interview. This is not legal advice.

## Develop
```
python3 tools/build.py          # syncs shared/ into every skill and builds dist/
python3 tests/test_ddos.py      # enforcement tests
claude plugin validate .
```
`shared/` is the single source of truth. Never edit the copies inside `skills/*/references/` or `skills/*/scripts/`.

## License
Apache-2.0. See `LICENSE`, `NOTICE` and `docs/LICENSING.md`.
