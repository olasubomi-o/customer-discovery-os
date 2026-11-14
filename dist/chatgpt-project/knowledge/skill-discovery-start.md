---
name: discovery-start
description: Use when the founder has a startup idea or hypothesis and no ranked assumptions yet, e.g. "I have an idea", "what must be true for this to work", "what should I validate first", "plan my first two weeks of discovery". Turns the idea into ranked testable assumptions and a 14-day plan, before any interviews exist.
---

# Discovery Start

Read `references/guardrails.md` and `references/ledger-schema.md` first. Key lesson: start with uncertainty, not a list of questions. Founders ask "what questions should I ask customers?" too early. First ask "what must be true for this business to work?"

## Setup
1. Ask which hypothesis this is (a short name, for example "invoice chasing for agencies"). Run `python3 scripts/ddos.py list` to see existing ones. If `discovery/` does not exist, run `python3 scripts/ddos.py init --hypothesis "<short name>"`. If it exists and belongs to a different idea, do not reuse it: create a separate project folder for the new idea and run init there. One folder holds exactly one hypothesis.
2. Read `discovery/context.md`. Ask only for what is still a template placeholder: the idea, the target customer, the proposed solution, and the real decision this research should inform (build, narrow, pivot, stop). Write the answers back.

## Step 1: Turn the idea into testable assumptions
Act as a rigorous customer discovery advisor. Do NOT evaluate whether the startup is a good idea yet. Deconstruct it into assumptions that must be true, across: 1 Customer, 2 Problem, 3 Frequency, 4 Severity, 5 Existing alternatives, 6 Willingness to change behavior, 7 Willingness to pay, 8 Buyer vs user, 9 Distribution and acquisition, 10 Trust or adoption barriers, 11 Technical feasibility, 12 Business viability.

For each assumption give: the assumption; why it matters; what evidence currently supports it (usually none, say so); what evidence would disprove it; risk level (Critical / High / Medium / Low); and the best method to test it (interview, survey, prototype, landing page, concierge test, pre-sale, usage experiment, other).

Rank from riskiest to least risky, then name the TOP 3 to test before building anything. Rule of thumb: the riskiest assumption is the one that, if wrong, kills the business. Test that first, not the one that is easiest to test.

Save to `discovery/assumptions.md`. Add each assumption to `ledger.csv` as a row with status `Unknown`, `evidence_type` `opinion`, `ladder_rung` 1, `customers_count` 0, `source_ids` blank, `evidence_for` "none yet", and `next_test` filled in. Use ids A-01, A-02 and so on.

## Step 2: 14-day discovery plan (when the founder wants an execution plan)
Design a rigorous study. Include: 1 primary research objective; 2 secondary objectives; 3 who exactly to interview; 4 who NOT to interview; 5 suggested sample size for initial qualitative interviews; 6 where to find participants; 7 outreach strategy; 8 interview structure; 9 key research questions; 10 evidence to collect; 11 signals that would strengthen the hypothesis; 12 signals that would weaken it; 13 what to avoid doing during interviews; 14 decisions the founder should be able to make afterwards.

Do not optimize for proving the idea right. Optimize for reducing uncertainty. Discovery needs a decision objective, not an activity objective: "interview 10 people" is an activity; "determine whether finance managers feel this problem often enough to justify testing a paid solution" is a learning objective.

Typical range: patterns often appear between 10 and 20 interviews with the right audience. Keep going until new conversations mostly confirm what you already heard.

## Finish
Run `python3 scripts/ddos.py check`. Fix errors. Hand off: interview-prep for the guide, participant-outreach for recruiting, market-scan for a secondary-evidence head start.
