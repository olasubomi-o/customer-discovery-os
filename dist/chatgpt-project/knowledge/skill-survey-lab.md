---
name: survey-lab
description: Use when the founder wants to quantify what interviews found with a survey: design a survey from interview findings, audit an existing survey for bias before publishing, or analyze closed survey results. Only for research surveys about customer problems, not satisfaction or marketing surveys. Triggers include "write a survey", "review my survey", "analyze these survey responses".
---

# Survey Lab

Read `references/guardrails.md` first. Interviews discover the pattern. Surveys measure the pattern. Run interviews first; do not use a survey to discover why. If the founder has no interview findings yet, say so and offer interview-prep.

Read `discovery/synthesis/` and `ledger.csv` for the findings and hypotheses.

## A. Design a survey from findings
Create a survey designed to VALIDATE or CHALLENGE the qualitative findings. Ask for: survey goals and target respondent if missing. Requirements: under 5 minutes; no leading language; no double-barreled questions; avoid unnecessary open-ended questions; ask about real behavior where possible; mutually exclusive response options; include "Other" where appropriate; include segmentation questions; do not overuse Likert scales; do not ask respondents to predict hypothetical future behavior.
For every question give: the question; response type; response options; why it matters; what decision the answer could influence. Then list any survey questions that could create misleading conclusions. Measure frequency, behavior and spending, not just satisfaction. Segment respondents instead of aggregating into one bucket.
Checklist: short; no leading; no double-barreled; real behavior; mutually exclusive options; segmented; frequency, behavior, spending; open-ended sparingly.

## B. Audit an existing survey
Act as a survey methodology expert. Evaluate every question for: leading wording, ambiguity, double-barreled construction, loaded assumptions, social desirability bias, overlapping answer options, missing answer options, scale inconsistency, recall difficulty, hypothetical bias, question order effects, unnecessary questions. Table: original question | issue | severity | why it matters | improved question. Then the biggest threats to validity. Finally: which questions to remove, which to rewrite, which to keep, and what important question is missing.

## C. Analyze results
Inputs: research objective, original hypotheses, dataset (upload or paste). If you can run code, compute the counts in code; do not estimate figures in prose. Analyze: overall response patterns; distribution of key answers; differences by segment; strongest pain indicators; frequency of the problem; severity; current solution; existing spend; purchase authority; behavioral vs attitudinal signals; significant contradictions; unexpected findings; outliers worth investigating; areas where sample size is too small; potential sampling bias. Do not mistake correlation for causation. Do not claim statistical significance unless the analysis genuinely supports it; state the sample size next to every percentage. Finish each original hypothesis with SUPPORTED, NOT SUPPORTED or INCONCLUSIVE, then recommend which findings need follow-up interviews.

## Finish
Save to `discovery/synthesis/survey-<date>.md`. Survey results are stated behavior from a sample, so in the ledger use evidence_type `mixed` or `opinion` unless respondents reported verifiable behavior or spend. Run `python3 scripts/ddos.py check`. Hand off: experiment-designer or decision-memo.
