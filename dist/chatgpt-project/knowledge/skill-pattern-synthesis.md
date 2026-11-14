---
name: pattern-synthesis
description: Use when the founder has 5 or more processed interviews and asks what patterns, recurring pain, hidden segments, real vs surface pain, buyer personas or jobs-to-be-done emerge across them. Also use when interview findings conflict with each other or with a survey and the founder asks which to trust or how to reconcile them. Cross-interview analysis only. Not for a single transcript (interview-analysis) and not for attacking conclusions (red-team).
---

# Pattern Synthesis (across interviews)

Read `references/guardrails.md`, `references/evidence-ladder.md` and `references/ledger-schema.md` first. Read `discovery/context.md` for the original hypothesis.

Input: the files in `discovery/extractions/` (not raw transcripts; open a transcript only to confirm a quote). If there are fewer than 5 extractions, say patterns are likely premature and offer to continue anyway with that caveat stated in the output. Run across ALL interviews at once, not one at a time: the patterns only show up in aggregate.

## A. Cross-interview pattern analysis
You are a senior qualitative research analyst. Do NOT simply summarize each interview. Analyze: recurring pain points; frequency of each pain point across participants; severity indicators; common triggers; current solutions and workarounds; existing spending behavior; switching barriers; desired outcomes; jobs to be done; repeated customer language; buyer vs user differences; segment differences; strong behavioral evidence; weak opinion-based evidence; contradictions; outlier insights; evidence supporting the hypothesis; evidence contradicting it; things we still do not know; new hypotheses.

For every major finding: state the finding; show how many interviews support it (a number out of the total); list the supporting interview IDs; include representative quotes (`> "quote" [I-xxx]`, verbatim only); rate evidence strength Weak / Moderate / Strong. Repetition alone is not proof. Distinguish WHAT PEOPLE SAY, WHAT PEOPLE DO, and WHAT PEOPLE PAY FOR.
Finish with: what appears validated, what remains uncertain, what appears invalidated, and the next 3 highest-priority research questions.

## B. Real pain vs surface complaint
For each problem evaluate: frequency, severity, urgency, financial impact, time impact, emotional impact, operational impact, existing workaround, existing spending, consequence of doing nothing, willingness to change behavior, willingness to commit resources. Do not assume a frequently mentioned complaint is automatically valuable.
Table: pain point | frequency | severity | existing behavior | current spend | consequence | evidence strength | what remains unknown. Classify each as Surface complaint, Moderate pain, Strong pain, or Mission-critical pain, and explain the evidence behind every classification. Strong pain combines frequency x severity x urgency.

## C. Hidden segments
Do NOT segment primarily by demographics unless the evidence supports it. Look for behavioral differences: frequency of problem, severity, use case, existing solution, company maturity, customer sophistication, budget, trigger event, workflow, desired outcome, buying process, urgency, switching willingness. For each real segment: description; shared characteristics; primary job to be done; top pain; trigger; current solution; evidence of urgency; evidence of willingness to pay; acquisition channels; what makes the segment different. Do not invent personas. Only create a segment if the interview evidence supports it. Two customers with the same age, city and industry can be different segments because one has urgent pain and the other does not.

## D. Evidence-based buyer persona (only when patterns have emerged)
Use ONLY the research. A persona explains buying behavior; it is not a fictional person. Skip demographics unless they affect buying. Include: who they are; context; responsibilities; jobs to be done; trigger events; pain points in their own words; desired outcomes; existing alternatives and why they fail; buying criteria; main objections; decision process; influencers; budget and spending evidence; where they look for information; customer language; evidence confidence. Separate SUPPORTED BY EVIDENCE, PLAUSIBLE BUT UNVALIDATED, and UNKNOWN. Do not fill gaps with invented detail. Update the persona whenever reality disagrees with it.

## E. Jobs to be done
Customers hire a product to make progress in a specific situation. Find: the situation that triggered the problem; what the customer is trying to accomplish; what they use today and why it is not enough; what would cause them to switch and what prevents it.

## Save and update
Write `discovery/synthesis/synthesis-<date>.md` (and `personas`, `segments` files if produced). Update `ledger.csv`: raise or lower statuses by the rules; keep contradictions in `evidence_against`. Then run `python3 scripts/ddos.py check` and fix errors. Hand off: red-team before anyone trusts these patterns.
