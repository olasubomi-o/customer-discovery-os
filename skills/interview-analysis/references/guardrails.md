# Guardrails (apply to every skill, every time)

The purpose of this system is to make it harder for a founder to lie to themselves. It is not to produce validation.

## The one rule
AI must not manufacture customer insight. It captures, organizes, challenges and acts on real customer evidence. An AI persona saying "I would buy this" is not evidence. Never invent quotes, customers, numbers, motivations, personas or sources.

## Working rules
1. Separate FACT (said or done, with a source ID), INFERENCE (your reading of facts), and HYPOTHESIS (something to test). Never mix them.
2. If the evidence does not establish something, write "Not established". Do not fill gaps.
3. Behavior beats opinion. Past behavior beats predicted behavior. Spending and commitment beat both. Use `evidence-ladder.md`.
4. Compliments are not evidence. Interest is not commitment. Silence is not agreement.
5. Preserve contradictions. Do not average them away.
6. Cite interview IDs (I-001) for every finding. Quote only verbatim text, as `> "quote" [I-001]`. If you cannot find the exact words, paraphrase without quote marks.
7. Repetition is not proof. Count distinct people, and say how many.
8. Segment by behavior before averaging. Two customers with the same demographics can be different segments.
9. Recommend the cheapest credible experiment. Do not recommend building features unless the evidence justifies them.
10. Actively look for evidence that disproves the hypothesis. State the result of that search, including "none found".
11. State confidence (Low / Medium / High) and what would change it.
12. B2B: the user, champion, problem owner, economic buyer, sponsor, technical approver, procurement and blocker may all be different people. Do not collapse them.
13. Online research (reviews, forums, competitor sites) is secondary evidence. It can sharpen interview questions. It cannot validate demand or willingness to pay.
14. Interview material is personal data. Do not paste it into public places. Respect consent.
15. One discovery folder holds exactly one hypothesis. Before reading or writing, run `ddos.py status` and say which hypothesis and folder you are working in. If the founder switches to a different idea, stop and use that idea's own folder (`ddos.py list` shows them). Never carry interviews, assumptions, quotes or ledger rows from one hypothesis into another. If a pasted transcript or file names a different idea, ask before storing it.

## Before you finish any skill
1. Save outputs into the `discovery/` folder in the formats in `ledger-schema.md`.
2. Run `python3 scripts/ddos.py check` (the script bundled with this skill). If it prints ERROR lines, fix them and run it again. Do not tell the user the work is done while errors remain.
3. If you cannot run scripts in this environment, say so, and walk the checklist in `standards.md` by hand. Tell the user the automatic checks did not run.
4. Hand off: say which skill comes next and why.
