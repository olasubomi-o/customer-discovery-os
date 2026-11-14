---
name: b2b-discovery
description: Use when the founder sells to organizations with several stakeholders, or is building early partnerships without funding: B2B interview questions by role (end user, manager, economic buyer, sponsor, IT or procurement), mapping buyer, user, champion and blockers, or designing partner pilots. Triggers include "selling to companies", "who is the buyer", "enterprise discovery", "early partnerships".
---

# B2B Discovery and Partnerships

Read `references/guardrails.md` and `references/evidence-ladder.md` first. Your user is not your champion, your buyer, or your approver. Sometimes five different people are involved. "The customer" is rarely one person, and selling to the wrong one is a common reason deals stall for reasons that look like "no budget" but are really "wrong person."

## A. B2B interview guide
Inputs: target organization type, target role, problem. Create interview questions that help understand: 1 current workflow; 2 who experiences the problem; 3 who owns the problem; 4 who pays for solving it; 5 who approves purchases; 6 existing vendors; 7 current budget; 8 contracting process; 9 procurement; 10 security and compliance; 11 integration requirements; 12 trigger for purchasing; 13 cost of doing nothing; 14 switching cost; 15 internal politics; 16 time to purchase; 17 pilot requirements; 18 success metrics.
Separate questions for: END USER, MANAGER, ECONOMIC BUYER, EXECUTIVE SPONSOR, PROCUREMENT / IT. Avoid pitching. Past behavior only ("Tell me about the last vendor you bought for this and how that went"), and apply the interview-prep rules and consent reminder.

## B. Map the buying system
From the research in `discovery/extractions/`, identify: end user, champion, problem owner, economic buyer, executive sponsor, technical approver, procurement, legal/security, blocker, influencer. For each stakeholder: what they care about; their pain; their incentives; their objections; their success metric; their role in the purchase; what evidence supports the conclusion (interview IDs). Flag everything that has not actually been validated. A stakeholder you have not spoken to is "Not established", not a guess.

## C. Early partnership discovery (no significant funding)
Inputs: the community or customers served and the partner types. Help find mutually beneficial early partnerships. Do not simply suggest asking organizations for sponsorship. For each partner type: what they care about; what problem you could solve for them; what asset you can offer without significant capital; what they can offer you; the lowest-friction first partnership; a pilot idea; evidence and results to collect; how the relationship could expand; what would make it economically sustainable.
Think in stages: Introduction, Access, Event, Pilot, Measurable outcome, Paid partnership, Strategic partnership. Before asking "Will your institution buy our product?", start with "Can we interview 10 students?", then "Can we host a workshop?", then "Can we run a 30-person pilot?", then "Here are the measured results", then "Would you like to expand this?"

## Finish
Save to `discovery/synthesis/b2b-<date>.md` (use `discovery/synthesis/` for partnership notes too). Update `ledger.csv` (category `buyer_vs_user` or `distribution`). Run `python3 scripts/ddos.py check`. Hand off: interview-analysis per stakeholder interview, experiment-designer for the first pilot.
