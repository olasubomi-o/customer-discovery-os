---
name: red-team
description: Use when the founder feels the idea is validating and before they trust any conclusion or decision memo: "am I fooling myself", "poke holes in this", "play devil's advocate", "challenge my findings", "is this really validated", "disprove my hypothesis". Runs an adversarial, evidence-based review that tries to disprove the hypothesis.
---

# Red Team (adversarial review)

Read `references/guardrails.md` and `references/evidence-ladder.md` first. If your AI only agrees with you, you are probably using it badly.

## Independence protocol (this is what makes it adversarial instead of theatrical)
1. In Claude Code, delegate to the `red-team` agent with the Agent tool so it runs in a fresh context. Tell it only: the hypothesis (copied from `discovery/context.md`) and the path to `discovery/`. Do NOT summarize your own conclusions or the synthesis for it.
2. Anywhere else, do it yourself in this order: (a) read `context.md`, `interviews/`, `extractions/` and `ledger.csv` first; (b) write down what the evidence supports BEFORE opening `synthesis/` or any decision memo; (c) only then compare against the existing synthesis and note where it goes beyond the evidence.
3. Check the raw transcripts, not only the extractions, for at least the interviews the synthesis relies on most. Extractions can inherit the extractor's bias.

## The review
Act as an adversarial researcher. Your job is NOT to help prove the hypothesis. Your job is to try to disprove it. Identify:
1 evidence that contradicts the hypothesis; 2 alternative explanations for the behavior observed; 3 cases where politeness may have been interpreted as interest; 4 cases where stated preference conflicts with actual behavior; 5 evidence that the problem may not be severe enough; 6 evidence that the customer may not pay; 7 evidence that another customer segment may be more attractive; 8 interview questions that may have biased responses; 9 missing evidence that prevents a conclusion; 10 what would have to be true for the hypothesis to be wrong.

Also check the process: who got interviewed and how they were recruited (selection bias, friendly sources, only people who replied), sample size per segment, whether any claim marked Emerging or Strong in the ledger fails the ladder rules, and whether any quote is used beyond what it says.

Then make the strongest possible evidence-based argument AGAINST pursuing this idea. Afterwards make the strongest evidence-based argument FOR continuing. Do not declare a winner. Tell the founder what evidence is needed next. Every claim cites interview IDs or ledger rows. Do not invent counter-evidence that is not in the material; if you found none for a point, say "none found" and say where you looked.

## Output
Write `discovery/redteam/redteam-<date>.md` with the sections: `## Evidence that contradicts`, `## Alternative explanations`, `## Interpretation risks` (politeness vs interest, stated vs actual), `## Process and sample risks`, `## Case against`, `## Case for`, `## Evidence needed next`. No "Winner" or "Verdict" line.

Then run `python3 scripts/ddos.py check`. Tell the founder the two or three findings most likely to change a decision, and hand off to experiment-designer.
