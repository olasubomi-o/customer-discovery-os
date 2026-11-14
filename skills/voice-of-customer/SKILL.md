---
name: voice-of-customer
description: Use when the founder wants customer language turned into positioning and messaging: a voice-of-customer phrase library, value propositions, landing page headlines or pain-focused and outcome-focused messages, all grounded in real interview quotes. Not for general copywriting or rewriting copy that is not based on customer research.
---

# Voice of Customer

Read `references/guardrails.md` first. Source material is `discovery/extractions/` and `discovery/interviews/`. If there are fewer than 3 interviews, say the language library will be thin and label every output as provisional.

## Step 1: Build the library before any marketing language
Extract phrases customers use to describe: their problem, their frustration, their desired outcome, their current workaround, why existing solutions fail, their fears, their priorities, their urgency, their definition of success. Do NOT invent marketing language yet.
Write the library as verbatim quotes only, each as `> "quote" [I-xxx]` (the checker verifies them), grouped by those nine headings. Count how many different interviews use similar language; a phrase one person said is a data point, not a theme.

## Step 2: Messaging, each traceable
Then create: 5 potential value propositions; 5 landing-page headlines; 5 pain-focused messages; 5 outcome-focused messages. For every proposed message explain which customer evidence inspired it, by interview ID. Messages may be written in the founder's words but must reuse the customers' vocabulary. Do not claim features, numbers or results the evidence does not show.

## Why this matters
Customer discovery should improve product, positioning, marketing, sales conversations, pricing and onboarding, not just the product backlog.

## Finish
Save to `discovery/voc/voc-<date>.md`. Messages are hypotheses: add a ledger row or next_test to try them (A/B test or landing page via experiment-designer). Run `python3 scripts/ddos.py check` and fix errors.
