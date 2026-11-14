---
name: interview-analysis
description: Use when the founder has one interview transcript or set of call notes to process: "here is my transcript", "summarize this call", "what did this person say", "extract the evidence", "analyze this interview". Ingests and redacts the transcript, extracts a structured fact / inference / hypothesis record, scores it on the evidence ladder, and updates the ledger. Only for customer research interviews that have already happened, not sales calls or demos. Use interview-prep for questions to ask beforehand and pattern-synthesis for patterns across many interviews.
---

# Interview Analysis (one interview at a time)

Read `references/guardrails.md`, `references/evidence-ladder.md` and `references/ledger-schema.md` first. Read `discovery/context.md` for the hypothesis.

## Step 1: Intake (always first)
1. If the transcript is pasted, save it to a temporary text file.
2. Ask, only if unknown: Did the participant consent to recording or note storage (yes / no / unknown)? What segment or role are they? Which names (person, company, colleagues) should be redacted?
3. Run `python3 scripts/ddos.py ingest <file> --segment "<segment>" --consent <yes|no|unknown> --redact "Name,Company"`. It assigns the next interview ID, redacts emails and phone numbers plus the names you list, and writes `discovery/interviews/I-NNN.md`.
4. Open the ingested file and look for names or details the redaction missed. Tell the founder what you found. Regex cannot detect every name.
5. If consent is `no`, say you will analyze but the founder must decide whether to keep the file. If consent is `unknown`, tell the founder once that consent must be confirmed, mark the interview as provisional in the extraction, and do not quote it in anything shared outside the founder's team until confirmed. The checker will keep warning until the header is changed to yes or no.
6. Run scripts from the workspace root with the full path to this skill's `scripts/ddos.py`; the default `--dir` is `discovery` in the current folder.

## Step 2: Extract (do not summarize generically)
Use ONLY evidence directly supported by the interview. Write `discovery/extractions/I-NNN.md` with the header line `Interview: I-NNN` and these sections. Every bullet under Facts ends with the tag `[I-NNN]`. If the interview contains no evidence for something, write `Not established`.

Facts, one labelled bullet each: participant context; primary jobs or tasks; most recent problem occurrence; trigger; current workflow; pain points; frequency; severity; consequences; current workaround; existing tools or products; money currently spent; time currently spent; buying authority; people involved in the decision; objections or barriers; desired outcome.
Then sections: `## Inferences` (your reading of the facts, labelled as such), `## Hypotheses` (things worth testing), `## Exact customer language` (only verbatim quotes, in the form `> "quote" [I-NNN]`; the checker verifies them against the transcript, so copy exact words), `## Evidence supporting the hypothesis`, `## Evidence contradicting the hypothesis`, `## Open questions`, `## Follow-up research needed`.

Why fact / inference / hypothesis matters: "The customer mentioned spreadsheets" is not "Customers hate spreadsheets."

## Step 3: Analyze without hallucinating (add these sections to the same file)
Rules: use only information in the transcript; do not invent motivations; do not assume silence means agreement; separate evidence from interpretation; quote exact phrases when revealing; flag contradictions; flag where the founder may have asked leading questions; flag claims needing validation from other customers.
Sections: `## Pain points`, `## Jobs to be done`, `## Workarounds`, `## Existing alternatives`, `## Behavioral evidence`, `## Buying signals`, `## Weak or ambiguous signals`, `## Contradictions`, `## Leading questions I asked`, `## Ladder scoring` (table: signal heard | ladder rung 1-8 | frequency/severity/urgency notes), `## Questions for the next interview`.
Finish the file with `## What this interview does NOT prove` (required, never empty). One interview can generate hypotheses. It rarely validates a market.

## Step 4: Update the ledger
For each assumption this interview touches, add or update the row in `discovery/ledger.csv`: add the interview to `source_ids`, update `customers_count`, set `ladder_rung` to the highest rung of the supporting evidence, fill `evidence_against` (including "none found after searching: ..."), and set `status` by the rules in `evidence-ladder.md`. One interview alone can make an assumption `Weak`, not `Emerging` or `Strong`.

## Finish
Run `python3 scripts/ddos.py check`. Fix every ERROR (most common: a quote that is not verbatim, a fact without a source tag). Then tell the founder: the three most important things this interview did and did not establish, and the next skill (pattern-synthesis after 5 extractions, otherwise interview-prep for the next call).
