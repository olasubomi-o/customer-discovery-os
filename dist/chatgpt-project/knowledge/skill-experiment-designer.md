---
name: experiment-designer
description: Use when the founder knows what remains uncertain and asks what to test next or how to test it cheaply: landing page, fake door, concierge MVP, Wizard of Oz, pre-sale, paid pilot, ads, pricing test, or a rigorous A/B test. Designs the smallest credible experiment with success and failure thresholds written down before it runs.
---

# Experiment Designer

Read `references/guardrails.md`, `references/evidence-ladder.md` and `references/ledger-schema.md` first. Read `ledger.csv` for open assumptions. Do not build the full product to test an assumption. Build the smallest, cheapest experiment that produces credible evidence.

## Pick the method
| If you need to test... | Reach for... |
|---|---|
| Whether the problem is real and people talk about it | Customer interviews |
| How common a pattern is across a broader group | A short survey (survey-lab) |
| Whether anyone cares enough to raise a hand | Landing page plus waitlist (smoke test) |
| Whether people would use a feature that "exists" | Fake-door test |
| Whether a manual version of the service has demand | Concierge MVP |
| Whether the workflow makes sense before automating | Wizard-of-Oz test |
| Which message or framing performs better | A/B test on headline, page or pricing |
| Whether people will actually pay | Pre-sales, letters of intent, a paid pilot |

## Design experiments
Inputs: the unresolved assumptions from the ledger (ask the founder which to target, default to the riskiest). Options include: customer interview, survey, landing page, fake door, prototype, concierge MVP, Wizard-of-Oz, pre-sale, letter of intent, paid pilot, manual service, ad test, email campaign, pricing test, usability test.
For each experiment give: 1 hypothesis; 2 riskiest assumption; 3 experiment; 4 target participant; 5 what we measure; 6 success threshold; 7 failure threshold; 8 estimated effort; 9 strength of evidence it would produce (use the ladder: a waitlist signup is rung 1 to 2, a pre-payment is rung 8); 10 the decision we will make afterwards. Prioritize HIGH learning value, LOW cost, LOW build effort. Do not recommend building a full product if a cheaper experiment can answer the question.

Thresholds are numeric and written BEFORE the run. A threshold you cannot measure is not a threshold. Set both: what result means "go", and what result means "stop". Record `Thresholds-set:` with today's date. Only fill `Run-date:` when the experiment actually runs; the checker rejects a run whose thresholds were set after the fact.

## When asked for an A/B test
Help design a rigorous test. Ask for: business question, audience, version A, version B, primary metric. Produce: 1 hypothesis; 2 independent variable; 3 control; 4 treatment; 5 primary metric; 6 guardrail metrics; 7 potential confounding variables; 8 required audience consistency; 9 minimum practical sample considerations; 10 duration considerations; 11 how to interpret A wins, B wins, no meaningful difference; 12 what conclusions we should NOT make. Also flag if an A/B test is NOT the right method and recommend a better one. A/B testing is not automatically the right methodology: a founder with 23 monthly visitors probably needs more direct customer discovery. Do not invent a sample-size number you cannot justify; state the assumptions behind any estimate.

## Save and update
One file per experiment: `discovery/experiments/exp-01.md` using the template in `ledger-schema.md` (`Assumption-ID:` must exist in the ledger). Update the ledger row's `next_test`. Run `python3 scripts/ddos.py check` and fix errors. Hand off: decision-memo after the experiment runs.
