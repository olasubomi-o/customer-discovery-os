---
name: market-scan
description: Use when the founder wants web research on competitors, alternatives, or what customers say online (reviews, forums, Reddit, app stores, G2, social posts): "who are my competitors", "what are people complaining about", "scan the alternatives", "online customer sentiment". Produces sourced, dated, secondary-evidence scans. Requires a web search or fetch tool.
---

# Market Scan (competitors, alternatives, online sentiment)

Read `references/guardrails.md`, `references/evidence-ladder.md` and `references/ledger-schema.md` first. Read `discovery/context.md` for the target customer and problem area.

## What this is and is not
Online research is SECONDARY evidence. It is quick and it sharpens interview questions. It does not replace customers. People who post online are the extremes, reviews can be paid or manipulated, search results are shaped by SEO and ads, and none of it can show willingness to pay. Say this in every output.

## Hard rules
1. Use only a real web search or fetch tool. If none is available in this environment, say so, do not invent anything, and give the founder a manual checklist (the sources and search phrases below) instead.
2. Never fabricate a URL, a quote, a rating, a price, a company, or a statistic. Every finding carries a URL and is dated with the access date. If you could not verify something, mark it `(unverified)`.
3. Paraphrase. No block quotes. At most one short quoted span (under 15 words) per source. Do not reproduce review text at length.
4. Public content only. Aggregate into themes. Do not name or profile individual private people or usernames. Do not circumvent paywalls, logins or robots restrictions.
5. Count honestly: "7 of 22 reviews I read mention X" beats "many users complain about X". State how many sources you read and where they came from.

## Scan modes (run the ones asked for, default to all three)
A. Competitors and direct alternatives. Who solves this job today? For each: what they claim to do, who they target, pricing as published (with date), strengths and gaps customers point out, and recent changes if visible.
B. Non-software alternatives. Spreadsheets, agencies, interns, internal processes, doing nothing. These are often the real competitor. Evidence usually appears in forum posts and job listings.
C. Online customer sentiment. Where the target customer talks: review sites (G2, Capterra, Trustpilot, app stores), forums and communities, Reddit, public social posts, YouTube comments, support threads. Look for: recurring complaints, workarounds people describe, switching stories, praise that reveals the valued job, price complaints.

## Output file `discovery/market/M-NNN.md`
```
ID: M-001
Type: secondary
Date: <access date>
Scope: <what was scanned and the search phrases used>
## Method          (sources checked, how many items read, limits)
## Competitors     table: competitor | what they offer | target | price (dated) | gap customers cite | source URL
## Alternatives    table: alternative | who uses it | why it persists | source URL
## Sentiment themes   bullets: theme, how many of how many items, source mix, URL
## Limits          what online evidence cannot tell us here
## Questions for interviews    the specific past-behavior questions this research suggests
```

## Ledger
Add or update rows with `source_ids` M-NNN, `evidence_type` secondary, ladder rung 4 or lower, status no higher than Emerging, and fill `evidence_against`. Online evidence alone can never make an assumption Strong. Its best use is to create better questions and to name alternatives to ask interviewees about.

## Finish
Run `python3 scripts/ddos.py check` and fix errors (most common: a finding with no URL, a quote that is too long). Hand off: interview-prep, using the "Questions for interviews" section.
