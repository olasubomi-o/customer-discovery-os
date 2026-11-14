---
name: decision-memo
description: Use when the founder must decide whether to proceed, narrow, pivot, investigate further or stop, or wants the evidence ledger updated or summarized: "write the decision memo", "should I keep going", "update the ledger", "where do we stand on the evidence". Turns research into a founder decision memo and keeps the evidence ledger honest. Not for deciding between conflicting data sources (use pattern-synthesis).
---

# Decision Memo and Evidence Ledger

Read `references/guardrails.md`, `references/evidence-ladder.md` and `references/ledger-schema.md` first. The output of customer discovery is a better decision, not a folder full of notes.

## Step 1: Refresh the ledger
Read every row of `discovery/ledger.csv`. For each assumption track: assumption, category, evidence supporting, evidence contradicting, source, date, number of customers represented, evidence type, strength, confidence, status (Unknown / Weak / Emerging / Strong / Invalidated), next test, and decision affected. Never allow an assumption to reach Strong on customer opinions alone. Prioritize behavioral, transactional and commitment evidence. Your understanding changes over time: instead of "We validated this", write "We currently have moderate evidence supporting this assumption, but willingness to pay remains untested."
Run `python3 scripts/ddos.py check`. A ledger that fails the check cannot support a memo; fix it first. Do not relax a status to make the check pass unless the evidence truly supports it.

## Step 2: Write the founder decision memo
Inputs: the original hypothesis, research conducted, evidence (all in `discovery/`). If a red-team review does not exist or predates the newest interviews, say so at the top and recommend red-team before the memo is relied on.
Create `discovery/decisions/memo-<YYYY-MM>.md` with header lines `Decision:`, `Confidence:` (Low / Medium / High), `Interviews-represented:` (a number), then these `##` sections in order: Original belief; What we tested; What we observed; Strongest supporting evidence; Strongest contradictory evidence; What changed in our understanding; What appears validated; What appears invalidated; What remains unknown; Updated customer definition; Updated problem definition; Product implications; Go-to-market implications; Pricing implications; Next experiment; Decision.
Decision is exactly one of: Proceed, Narrow, Pivot, Investigate further, Stop. Add one paragraph of reasoning under `## Decision`.

Rules: do not make the decision simply because customers said they liked the idea. Weight actual behavior, spending, commitment and observed pain more heavily than stated enthusiasm. Cite interview IDs and ledger row ids for every claim. "What remains unknown" is never empty. If the evidence is thin (fewer than 5 interviews, no rung 6+ evidence, one segment only), the honest decision is usually Investigate further, and the memo should say what the cheapest next test is.

## Finish
Run the check again. Report to the founder: the decision, the confidence, the one fact that most drove it, and the one fact that would most change it.
