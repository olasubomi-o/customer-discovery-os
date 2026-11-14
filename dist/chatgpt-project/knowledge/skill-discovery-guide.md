---
name: discovery-guide
description: Use when the founder is unsure where they are in customer discovery or what to do next, asks "where do I start", "what's next", "what stage am I in", or wants the whole process explained. Also use for a checklist or overview of what to do before, during and after customer research calls. Reads the discovery folder status and routes to the right skill. Does not do the analysis itself.
---

# Discovery Guide (the router)

Read `references/guardrails.md` first.

## Steps
1. Run `python3 scripts/ddos.py status`. It prints counts and a STAGE line. If there is no `discovery/` folder, the stage is "not started".
2. Tell the founder in two sentences where they are and which skill comes next. Name the skill and say why.
3. If they want something else, route by need:

| Founder says | Skill |
|---|---|
| I have an idea, what must be true | discovery-start |
| Write or fix my interview questions, probes | interview-prep |
| How do I get people to talk to me | participant-outreach |
| Here is a transcript | interview-analysis |
| What patterns, segments, personas, jobs across interviews | pattern-synthesis |
| Am I fooling myself, challenge this | red-team |
| Survey | survey-lab |
| What should I test next, A/B test | experiment-designer |
| Decide, update the ledger, where do we stand on evidence | decision-memo |
| Turn customer language into messaging | voice-of-customer |
| Selling to companies, partnerships | b2b-discovery |
| Competitors, alternatives, what people say online | market-scan |

4. The loop to keep in view: assumptions -> interviews -> extraction -> synthesis -> red-team -> experiment -> decision -> next round. If interviews are not changing what the founder does next, something in the loop broke. Say so.

## Before / during / after checklist (offer when asked)
Before: assumptions ranked by risk. Guide built on the context-to-buying-behavior arc. Every question checked for hypothetical language.
During: asked about the last specific time, not "would you". Talked under 20% of the time. No pitch before the end. Asked for a referral.
After: synthesis once 5+ transcripts exist. Red-team before trusting patterns. Scored on the evidence ladder. Ledger updated. Decision memo written. Next experiment designed with thresholds set in advance.

The output of customer discovery is a better decision, not a folder full of notes.
