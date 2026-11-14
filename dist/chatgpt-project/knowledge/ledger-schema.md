# The `discovery/` folder (shared memory for all skills)

```
discovery/
  context.md        startup, target customer, hypothesis, the decision this informs
  assumptions.md    ranked assumptions (from discovery-start)
  interviews/       I-001.md ...  normalized transcripts (from ddos.py ingest)
  extractions/      I-001.md ...  one structured extraction per interview
  synthesis/        cross-interview analysis, segments, personas, JTBD
  market/           M-001.md ...  web research (secondary evidence)
  redteam/          adversarial reviews
  experiments/      exp-*.md
  decisions/        memo-*.md
  voc/              voice-of-customer library and messaging
  ledger.csv        the Evidence Ledger
```

Every skill: read `context.md` first. Ask the user only for what is missing. Write results back. Run the check.

## interviews/I-001.md
```
ID: I-001
Date: 2026-11-14
Consent: yes
Segment: finance managers, 50-200 staff
Source: granola-export.txt
---
<transcript text>
```
Create it with `python3 scripts/ddos.py ingest FILE --segment "..." --consent yes --redact "Name,Company"`. Names are not auto-detected; pass them to `--redact`.

## extractions/I-001.md
Required header line `Interview: I-001`, and these sections (add more as the skill says):
```
Interview: I-001
## Facts          every bullet ends with its source tag [I-001], or says "Not established"
## Inferences
## Hypotheses
## Exact customer language     only verbatim quotes:  > "text" [I-001]
## What this interview does NOT prove
```
Blockquote lines (`>`) are reserved for verbatim customer quotes. The checker verifies each one against the transcript.

## ledger.csv columns
`id, assumption, category, evidence_for, evidence_against, source_ids, date, customers_count, evidence_type, ladder_rung, status, next_test, decision_affected`

- `id`: A-01, A-02 ...
- `category`: customer, problem, frequency, severity, alternatives, behavior_change, willingness_to_pay, buyer_vs_user, distribution, trust, feasibility, viability
- `source_ids`: semicolon separated, I-001;I-004;M-002
- `evidence_type`: opinion | behavioral | transactional | commitment | secondary | mixed
- `ladder_rung`: highest rung of the supporting evidence (1-8)
- `status`: Unknown | Weak | Emerging | Strong | Invalidated
- `evidence_against`: required for Emerging, Strong, Invalidated. Write what you found, or `none found after searching: <what you searched>`.
- `next_test`: required unless Invalidated.

## experiments/exp-NN.md
```
Assumption-ID: A-03
Hypothesis: ...
Riskiest assumption: ...
Experiment: ...
Target participant: ...
What we measure: ...
Success threshold: at least 12 of 40 visitors join the waitlist
Failure threshold: fewer than 4 of 40
Thresholds-set: 2026-11-14
Run-date: (fill in only when you run it; must be on or after Thresholds-set)
Estimated effort: ...
Strength of evidence if it works: ...
Decision if success: ...
Decision if failure: ...
```

## decisions/memo-YYYY-MM.md
Header lines `Decision:`, `Confidence:`, `Interviews-represented:` plus the ten `##` sections from the decision-memo skill. Decision is one of Proceed, Narrow, Pivot, Investigate further, Stop.

## market/M-001.md
Header `ID: M-001`, `Type: secondary`, `Date:` (access date), `Scope:`. Every finding carries a URL or is marked `(unverified)`. No block quotes. Quote at most one short span (under 15 words) per source, otherwise paraphrase.

## redteam/*.md
Sections: Evidence that contradicts, Alternative explanations, Case against, Case for, Evidence needed next. No winner or verdict line.
