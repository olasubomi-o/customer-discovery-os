# Founder and PM standards, and how each one is enforced

Honest status: "Enforced" means `ddos.py check` fails when the standard is broken (and in Claude Code a hook runs it automatically after every write to `discovery/`). "Advisory" means it is an instruction the model is asked to follow; nothing mechanical stops a violation. Enforcement catches structural cheating. It cannot judge whether an insight is good.

| # | Standard | Status | Mechanism |
|---|---|---|---|
| 1 | Every quoted customer line exists verbatim in the transcript | Enforced | quote verification against interviews/ |
| 2 | Every finding traces to an interview ID | Enforced | facts need [I-xxx] or "Not established" |
| 3 | Facts, inferences and hypotheses are separated | Enforced (structure) | required sections in extractions |
| 4 | Every interview states what it does not prove | Enforced | required non-empty section |
| 5 | Opinions and online research cannot make anything "Strong" | Enforced | ledger rules (type, rung, 5+ interviews) |
| 6 | Willingness to pay needs spend, commitment or payment | Enforced | ledger rule (rung 6+) |
| 7 | You must search for disproof | Enforced (presence) | evidence_against required, even if "none found after searching: ..." |
| 8 | Every open assumption has a next test | Enforced | next_test required |
| 9 | Experiment thresholds are numeric and set before the run | Enforced (partly) | success/failure thresholds required; dates checked; numbers warned |
| 10 | Decisions use the fixed vocabulary and state unknowns and confidence | Enforced | memo sections and fields |
| 11 | Small samples do not carry big decisions | Warned | memo with fewer than 5 interviews and Proceed/Pivot/Stop |
| 12 | Market research is sourced, short-quoted, dated and secondary | Enforced | URL per finding, quote length, Type: secondary |
| 13 | Red-team output does not declare a winner | Enforced | no winner/verdict line |
| 14 | Consent is recorded per interview | Enforced (presence) | Consent header required; warns if not yes |
| 15 | Quality of the question wording, depth of probing, honesty of the "does not prove" content | Advisory | model instructions only; review it yourself |
| 17 | One folder, one hypothesis; files from another hypothesis are rejected | Enforced (files); Advisory (chat) | hypothesis.json id checked against file headers and context.md. The conversation itself cannot be isolated by a script |
| 16 | The founder actually talks to customers instead of the AI | Advisory | nothing can enforce this |

## Standards checklist (use when scripts cannot run)
- [ ] Context file states the decision this research should inform.
- [ ] Every claim cites an interview ID, or says Not established.
- [ ] Every quote is verbatim from the transcript.
- [ ] Opinion, behavior, spend and commitment are labelled separately.
- [ ] Counter-evidence was searched for and the result written down.
- [ ] Sample size is stated next to every finding.
- [ ] The next test is the cheapest one that could change the decision.
- [ ] Thresholds were written down before the test ran.
- [ ] Nothing in the output was invented to fill a gap.
