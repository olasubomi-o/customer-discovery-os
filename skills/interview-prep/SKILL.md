---
name: interview-prep
description: Use when the founder needs interview questions for customers: write an interview guide, check questions for bias or leading language ("mom test"), or generate follow-up probes. Triggers include "write my interview guide", "are these questions leading", "what should I ask", "follow-up questions". Use before the interview happens. Not for analyzing transcripts or for multi-stakeholder B2B buying committees (use b2b-discovery).
---

# Interview Prep

Read `references/guardrails.md` first. Read `discovery/context.md` (hypothesis, target customer, problem area); ask only for what is missing.

Core idea: past behavior is more reliable than predicted behavior. A strong interview should feel like "Tell me what happened," not "Please validate my hypothesis."

## A. Bias-resistant interview guide (30 minutes)
Act as an expert qualitative researcher. Rules: do not pitch the solution; do not ask whether they like the idea; no hypothetical future questions; no leading questions; avoid yes/no; focus on specific past behavior and real experiences; explore current alternatives, frequency and severity, financial / emotional / operational / time consequences, and purchase behavior; use follow-ups to reach root causes.

Structure: 1 warm-up and context; 2 most recent occurrence of the problem; 3 step-by-step current workflow; 4 pain points; 5 consequences; 6 current workarounds; 7 existing products and services used; 8 spending behavior; 9 decision-making process; 10 closing and referral question.

For every major question give: the main question, why you are asking it, and 2 to 3 follow-up probes. Keep it conversational, not a survey.

Arc to follow: Context, Trigger, Current behavior, Pain, Consequence, Alternatives, Buying behavior. Sample prompts: "Tell me a bit about your role and how a typical week looks." "Tell me about the last time this happened." "Walk me through what you did next." "What was the most frustrating part?" "What happens if you do nothing about it?" "What do you currently use to deal with this? What have you already tried?" "Who else is involved in a decision like this? What are you paying for today?"

Practices: focus on stories, not opinions. Let silence sit. Avoid leading language. Probe two or three "why"s past the first answer. Do not pitch before you have listened. Talk under 20% of the time. Record exact words. End by asking for a referral.

Consent reminder (include in every guide): ask permission before recording or taking notes you will store, say what you will do with the notes, and check the local recording-consent rules for the participant's location. This is a reminder, not legal advice.

## B. Question checker (the "Mom Test")
When the founder pastes questions, act as a skeptical research coach. For each question flag: leading language, confirmation bias, hypothetical behavior, asking for compliments, asking the customer to predict the future, double-barreled, too broad, too vague, solution-focused instead of problem-focused, likely to produce socially desirable answers, likely to produce a yes/no. Return a table: original question | problem | why it is dangerous | better version | best follow-up probe. Prioritize questions that uncover real past behavior. If a question is already strong, say why.
Example: replace "Would you use an AI platform that helped you find scholarships?" with "Tell me about the last time you searched for scholarships," then "What did you do?", "What was difficult?", "How much time did you spend?"

Avoid: "Would you use this?", "Do you like this idea?", "Would you pay $20 for this?", "Do you think this feature is useful?"
Use: "Tell me about the last time this happened.", "What happened next?", "How often does this happen?", "What are you currently paying for, if anything?"

## C. Follow-up probes
Ask for the problem and the answers the founder expects. For each possible answer generate 3 to 5 follow-ups that uncover: why it happened, what triggered it, what they did next, how often, what consequences resulted, what workaround they used, how much time or money it cost, why they have not solved it differently, who else is involved, what they value most. Never produce questions that steer toward the founder's solution.
Generic probes worth remembering: "Tell me more about that." "What happened next?" "Why was that difficult?" "How often does that happen?" "What happens if you do not solve it?" "What have you tried?" "What did that cost?"

## Finish
Save the guide to `discovery/synthesis/interview-guide.md` (no `>` blockquotes except verified quotes). Run `python3 scripts/ddos.py check`. Hand off: participant-outreach, then interview-analysis after the first call.
