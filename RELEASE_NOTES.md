# v0.1.0 (beta)

Customer Discovery OS turns the Customer Discovery Prompt Playbook into 13 skills, 2 agents and a shared evidence folder, with a checker that rejects dishonest evidence.

## Included
- 13 skills: discovery-guide, discovery-start, interview-prep, participant-outreach, interview-analysis, pattern-synthesis, market-scan, survey-lab, b2b-discovery, red-team, experiment-designer, decision-memo, voice-of-customer.
- Agents: red-team, discovery-copilot. Commands: /discover, /discovery-checklist.
- `ddos.py` checker: verbatim quote verification, evidence-ladder rules for the ledger, experiment thresholds set before the run, one folder per hypothesis.
- Install paths: Claude Code plugin, skill zips for Claude.ai, ChatGPT Project fallback.

## Known limits
- Automatic checking after every write works in Claude Code only. Elsewhere the skills instruct the model to run the check.
- The checker cannot judge counts, attribution or reasoning quality, and a ledger row can still be marked Strong when most interviews contradict it.
- The red-team agent matched plain Claude in our planted-flaw tests; its value is structure and independence, not a higher catch rate.
- ChatGPT behavior and live web research in market-scan are not yet field-tested.
