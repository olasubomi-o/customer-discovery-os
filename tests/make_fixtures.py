#!/usr/bin/env python3
"""Generate synthetic test fixtures. All people, companies and quotes are invented.

Startup used in every test: "InvoiceNudge", automated polite invoice chasing for small agencies.
"""
import csv
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"

LEDGER_COLS = ["id", "assumption", "category", "evidence_for", "evidence_against", "source_ids", "date",
               "customers_count", "evidence_type", "ladder_rung", "status", "next_test", "decision_affected"]

# ------------------------------------------------------------------ executor scenario (raw transcripts)
SCENARIO = {
"t1.txt": """Founder: Thanks for making time. Tell me about the last time a client paid you late.
Priya: That was probably three weeks ago. A retail client, an invoice for about eighteen thousand, due the first of the month, and by the fifteenth nothing.
Founder: What happened next?
Priya: I sent the standard reminder from Xero. Nothing. Then I emailed their accounts payable address, nothing. In the end I called the marketing director I actually work with, and she walked it over to finance. It got paid on day forty-six.
Founder: How often does that happen?
Priya: Every month there are at least two or three. I keep a Google Sheet with every overdue invoice, who I chased, and when. I block out Friday afternoon for it. It is about five hours a week, honestly.
Founder: What was the most frustrating part?
Priya: The Xero reminders go to a generic AP inbox that nobody reads. They are basically useless, but we pay for the plan anyway. And I cannot be too pushy because those clients are also the ones giving us new work.
Founder: What else have you tried?
Priya: We pay our bookkeeper three hundred a month and part of that is meant to be chasing, but she only does the really old ones. I looked at ChaseBoard last year, it was ninety dollars a month and I could not get my boss to sign off because it felt like another tool nobody would use.
Founder: Who decides on something like this?
Priya: Our managing partner, Dan, signs off on anything over fifty a month. I would be the one using it.
Founder: If you had something that fixed the wrong inbox issue, what would happen?
Priya: Send it over when it exists. I would bring it to Dan. Actually, I know two other agency owners who complain about this constantly, I can introduce you.
""",
"t2.txt": """Founder: Thanks for helping, Marcus. So tell me about the last time a client paid you late.
Marcus: Hm. Honestly, I cannot think of a recent one. Most of our clients pay within a couple of weeks. We had one two years ago that took a while.
Founder: Okay. But the idea is software that sends polite reminders automatically. What do you think?
Marcus: Oh that is a great idea. I would totally use something like that. You should absolutely build it, I think a lot of people would love it.
Founder: Would you pay for it?
Marcus: Sure, probably. Depends on the price, but yeah. It sounds really cool.
Founder: How do you handle it when someone does pay late?
Marcus: I just email them. It takes a minute. Honestly it is not really a problem for us.
Founder: Anyone else you know who has this problem?
Marcus: I am sure plenty of people do. Agencies, freelancers. Good luck with it, I am rooting for you!
""",
"t3.txt": """Founder: Tell me about the last time a client paid you late.
Jo: Ugh. Last quarter. A startup client owed me twenty-two hundred and it dragged for two months.
Founder: Walk me through what you did.
Jo: I sent a friendly nudge after a week. Then another. By the third email I was rewriting it for twenty minutes because I did not want to sound desperate. I have a template in my notes app now.
Founder: What was the hardest part?
Jo: The awkwardness. It is not really the time. It is feeling like I am begging for money I earned.
Founder: What would you do if you did not chase?
Jo: Honestly I would just not take that kind of client again. I have started asking for fifty percent upfront with new clients, which fixed most of it.
Founder: What do you spend on tools for this?
Jo: Nothing. I use a free invoicing app. I would not pay more than ten bucks a month for anything, and honestly I would probably just keep my template.
Founder: How often does it happen?
Jo: Maybe three times a year.
""",
"t4.txt": """Founder: Thanks for joining. I am building a tool that automatically chases late invoices. Wouldn't it be great if software handled that for you?
Sam: Yeah, sure, that would be nice.
Founder: Great. Let's back up. Tell me about the last time an invoice was late.
Sam: Two weeks ago. Average on our receivables is forty-seven days against thirty-day terms. I tracked it last quarter because cash got tight. Back in March I delayed payroll by two days because three clients were sitting on about sixty thousand combined.
Founder: What did you do about it?
Sam: I chase them myself, weekly, usually Monday morning, maybe two hours. My account manager also nags her contacts. There is no real system.
Founder: Have you tried tools?
Sam: I looked at two or three. ChaseBoard and another one. They were too expensive for what they did, and honestly they felt like they would make us look like a collections agency.
Founder: What matters most in a solution?
Sam: That it does not damage the relationship. Tone matters. And it has to plug into Xero without me touching it.
Founder: Is it urgent?
Sam: It is urgent when cash is tight. Right now it is fine.
""",
"t5.txt": """Founder: Tell me about how invoicing and collections work at your agency.
Ana: We use QuickBooks. Invoices go out on the first, terms are thirty days, and QuickBooks sends an automatic reminder at day thirty-five.
Founder: What happens when a client is late?
Ana: Honestly, most pay within a week of the due date. It is mostly fine. The real problem is two or three big clients who always go sixty or ninety days. For those I just call their finance contact.
Founder: How much time does that take?
Ana: Not much. An hour or two a month. The bigger issue is when a client disputes something and the invoice gets stuck, and software cannot fix that.
Founder: Would a better reminder tool change anything?
Ana: I doubt it. We have a process. And I am not the one who picks software. Our CFO, Mei, decides, and she is skeptical of adding tools.
Founder: Anything you would change about the current setup?
Ana: Maybe having the reminders sound less robotic. But that is minor.
""",
"t6.txt": """Founder: Tell me about the last time you chased an invoice.
Lee: Let me think. Probably early this month. A client was twenty days over. I sent two emails and they paid.
Founder: How often?
Lee: Not that often, to be honest. A few times a year. Most of our work is retainers with prepayment.
Founder: What did that cost you?
Lee: Barely anything, maybe thirty minutes.
Founder: Do you currently pay for anything related to this?
Lee: Our accountant handles billing. We pay for Xero, that is it.
Founder: Is there anything about this you would want fixed?
Lee: Not really. Everyone says it is a problem, but it is not a big one for us. Though, we are changing our model next quarter to project-based work with milestone invoices. That will create more invoices, and I have some budget set aside for finance tooling. If you have something, send me a demo.
""",
}

# ------------------------------------------------------------------ red-team dossiers
HYP = "Agency owners will pay $90 a month for automated invoice chasing."
CONTEXT = f"""# Discovery context

## Startup
InvoiceNudge: automated, polite invoice chasing for small agencies.

## Target customer
Owners and operations managers at small creative and marketing agencies.

## Current hypothesis
{HYP}

## Decision this research should inform
Whether to build the full product now.
"""


def interview(iid, date, seg, recruited, body):
    return (f"ID: {iid}\nDate: {date}\nConsent: yes\nSegment: {seg}\nSource: recorded call\nRecruited-via: {recruited}\n---\n" + body.strip() + "\n")


FLAWED = {
"I-001": ("18-person agency, ops manager", "cold LinkedIn outreach", """Founder: Tell me about the last time a client paid late.
P: Every Friday I spend about four hours chasing. We keep a sheet. We pay Xero thirty-nine a month for reminders but they go nowhere.
Founder: Would you pay for something better?
P: I would pay for something that works, yes."""),
"I-002": ("solo video producer", "friend of the founder", """Founder: What do you think of the idea?
P: Honestly it is a great idea, I would probably use it. I have not had a late invoice in a year though."""),
"I-003": ("6-person agency owner", "signed up to the idea newsletter", """Founder: Would you pay ninety a month?
P: Yeah I would pay ninety, sure. Last year I looked at ChaseBoard at ninety a month and passed because it was too expensive for what it did."""),
"I-004": ("12-person agency owner", "cold LinkedIn outreach", """Founder: How does late payment affect you?
P: Lateness is not the real problem. It is disputes. When a client disputes a line item the invoice just sits for months and no reminder fixes that."""),
"I-005": ("2-person studio", "introduced by the founder's friend", """Founder: Wouldn't you pay ninety dollars a month to never chase an invoice again?
P: I guess, yeah.
Founder: How often do clients pay late?
P: Late payers are rare for us, one or two a year."""),
"I-006": ("22-person agency owner", "cold LinkedIn outreach", """Founder: Tell me about the last time cash was tight.
P: March. Three clients owed us sixty grand. I chase weekly, two hours. We pay our bookkeeper two hundred a month partly for it.
Founder: What would make you try something?
P: If you can show it works with Xero I will run a pilot."""),
"I-007": ("freelance designer", "signed up to the idea newsletter", """Founder: Don't you think automated reminders would save you a ton of time?
P: Definitely, that sounds really useful.
Founder: Would you pay ninety?
P: Probably, if it works as described. When it happens it takes me five minutes."""),
"I-008": ("partner at a 4-person agency", "friend of the founder", """Founder: What do you think?
P: Love it. Send me a link. I do not really chase invoices, my partner handles billing, but I am sure it is useful."""),
}

FLAWED_SYNTHESIS = """# Validation summary (draft for cofounder)

Result: the hypothesis is validated. 8 of 8 interviewees confirmed the problem and 6 of 8 said they would pay $90 a month. Willingness to pay is validated.

Existing spend is validated: agencies already pay for reminders and for bookkeepers to chase invoices.

All agencies behave the same way. Average pain is about four hours a week.

Representative quotes:
> "Every Friday I spend about four hours chasing" [I-001]
> "I would pay double for this" [I-002]
> "the single biggest pain in our business" [I-006]
> "I would pay for something that works, yes" [I-001]

Recommendation: proceed to build the full product now.
"""

FLAWED_LEDGER = [
    dict(id="A-01", assumption="Agencies have a serious invoice-chasing problem", category="problem", evidence_for="8 of 8 confirmed", evidence_against="none found after searching: all transcripts", source_ids="I-001;I-002;I-003;I-004;I-005;I-006;I-007;I-008", date="2026-11-10", customers_count="8", evidence_type="opinion", ladder_rung="2", status="Strong", next_test="build the MVP", decision_affected="build now"),
    dict(id="A-02", assumption="Agency owners will pay $90 a month", category="willingness_to_pay", evidence_for="6 of 8 said they would pay", evidence_against="none found after searching: all transcripts", source_ids="I-001;I-003;I-005;I-006;I-007;I-008", date="2026-11-10", customers_count="6", evidence_type="opinion", ladder_rung="1", status="Strong", next_test="build the MVP", decision_affected="build now"),
]

GROUND_TRUTH = {
    "F1": "Politeness read as interest: 'sounds great, I'd probably use it' (I-002, I-007, I-008) counted as demand with no behavior",
    "F2": "Stated vs actual: I-003 says he would pay $90 but passed on ChaseBoard at $90 last year as too expensive",
    "F3": "Selection bias: 5 of 8 came from friends, friend introductions or the idea's own newsletter signup",
    "F4": "Leading questions in I-005 and I-007 ('Wouldn't you pay ninety...', 'Don't you think...')",
    "F5": "Segment averaging: only I-001 and I-006 (18 and 22 staff) show real pain; the small/solo ones show little or none",
    "F6": "Existing spend overstated: only I-001 and I-006 show spend; synthesis says 'agencies already pay'",
    "F7": "Contradiction omitted: I-004 says the real problem is disputes, not lateness",
    "F8": "Overclaim: 'validated', Strong in ledger on opinion evidence (rung 1 to 2), n=8, decision to build full product",
    "F9": "Count inflation: '6 of 8 would pay $90' vs at most 1 unhedged yes (I-003, contradicted) and 3 hedged",
    "F10": "Fabricated quotes: 'I would pay double for this' [I-002] and 'the single biggest pain in our business' [I-006] appear in no transcript",
}

CONTROL = {
"I-001": ("20-person agency owner", "cold LinkedIn outreach", """Founder: Tell me about the last time an invoice was late.
P: Two weeks ago. Our average is forty-seven days against thirty-day terms. I tracked it because cash got tight. In March I delayed payroll by two days when three clients owed about sixty thousand.
Founder: What did you do?
P: I chase weekly, two hours on Monday. I looked at ChaseBoard and passed, ninety a month was too much for what it did. I would pilot something at half that if it worked with Xero."""),
"I-002": ("12-person agency ops manager", "cold LinkedIn outreach", """Founder: Walk me through the last late invoice.
P: Retail client, eighteen thousand, paid on day forty-six. I keep a sheet and block Friday afternoons, about five hours a week. We pay Xero thirty-nine a month for reminders that go to an inbox nobody reads, and our bookkeeper gets three hundred a month partly to chase.
Founder: What next?
P: Show me something and I will take it to my managing partner. I can introduce two other owners."""),
"I-003": ("15-person agency finance manager", "referral from I-002", """Founder: How do you handle late payers?
P: About three hours a week. I built a Zap that emails a template at day thirty-five. I also pay forty-nine a month for a small chasing tool but it is clunky and sends the same text to everyone.
Founder: Would you switch?
P: Maybe, but the owner decides on software, not me."""),
"I-004": ("18-person agency finance lead", "cold LinkedIn outreach", """Founder: Tell me about collections.
P: Our days outstanding are fifty-two. We hired a part-time AR clerk at eighteen hundred a month, mostly for chasing. Switching tools means retraining her, so the bar is high.
Founder: Who signs off?
P: Our CFO. She would allow a pilot if it connects to QuickBooks."""),
"I-005": ("solo freelance copywriter", "community forum post", """Founder: Last time a client paid late?
P: Last quarter, twenty-two hundred, two months. It happens maybe three times a year. I have a template in my notes app and I now ask for half upfront. I would not pay more than ten a month."""),
"I-006": ("8-person branding agency owner", "cold LinkedIn outreach", """Founder: How often do you chase invoices?
P: A few times a year. Most of our work is prepaid retainers. It costs me maybe thirty minutes. I pay for nothing related to this and do not want to."""),
}

CONTROL_SYNTHESIS = """# Synthesis (n=6, honest limits first)

Limits: 6 interviews, 5 recruited by cold outreach or a forum post and 1 by referral from I-002. Only 4 interviews are in the segment that shows pain (agencies of 12 to 20 staff). No price test has been run.

## Findings
- Strong behavioral pain in the 12 to 20 staff segment: 4 of 4 describe recurring hours spent chasing or an extra hire (I-001, I-002, I-003, I-004). Evidence is time cost and workarounds (rung 5).
- Existing spend appears in 3 of those 4: Xero reminders plus a bookkeeper (I-002), a small chasing tool (I-003), a part-time AR clerk (I-004). Rung 6.
- Price resistance: I-001 passed on a $90 tool and would pilot at half that price. This contradicts the $90 hypothesis.
- Not in the target segment: the solo freelancer and the 8-person prepaid-retainer agency show little pain (I-005, I-006).
- Buyer is not the user in 3 of 4 (I-002, I-003, I-004): owner, managing partner or CFO signs off.

Representative quotes:
> "about five hours a week" [I-002]
> "I would pilot something at half that if it worked with Xero" [I-001]
> "the owner decides on software, not me" [I-003]

## What this does not prove
That $90 a month works, that the pain exists outside the 12 to 20 staff segment, or that people will pay rather than pilot.

Recommendation: Narrow to agencies of 12 to 20 staff. Investigate further on price before building.
"""

CONTROL_LEDGER = [
    dict(id="A-01", assumption="12 to 20 staff agencies have a recurring, costly invoice-chasing problem", category="problem", evidence_for="4 of 4 in segment report hours per week or a dedicated hire", evidence_against="none found after searching: I-005 and I-006 outside the segment show little pain", source_ids="I-001;I-002;I-003;I-004", date="2026-11-10", customers_count="4", evidence_type="behavioral", ladder_rung="5", status="Emerging", next_test="4 more interviews in segment, then waitlist page", decision_affected="segment to target"),
    dict(id="A-02", assumption="Owners will pay $90 a month", category="willingness_to_pay", evidence_for="3 of 4 already pay for related things", evidence_against="I-001 passed on a $90 tool and would pilot at half price", source_ids="I-001;I-002;I-003;I-004", date="2026-11-10", customers_count="4", evidence_type="transactional", ladder_rung="6", status="Weak", next_test="pricing pre-sale at $45 and $90", decision_affected="pricing"),
    dict(id="A-03", assumption="The user is also the buyer", category="buyer_vs_user", evidence_for="none", evidence_against="3 of 4 say owner, partner or CFO decides", source_ids="I-002;I-003;I-004", date="2026-11-10", customers_count="3", evidence_type="behavioral", ladder_rung="3", status="Emerging", next_test="ask each for a buyer intro", decision_affected="who we sell to"),
]


# ------------------------------------------------------------------ subtle dossier (flaws the checker cannot see)
SUBTLE = {
"I-001": ("14-person agency owner", "cold outreach reply", """Founder: Tell me about the last late invoice.
P: Last week. I chase weekly, about three hours, with a sheet. I would pay for something that works, but not at ninety. Forty is my ceiling, honestly, because I already pay Xero thirty-nine for reminders."""),
"I-002": ("9-person agency owner", "cold outreach reply", """Founder: How do late payments affect you?
P: Back when we had that big retail client, three years ago, I chased constantly. These days we invoice upfront for most work so it hardly comes up."""),
"I-003": ("16-person agency ops lead at Pixel and Pine", "cold outreach reply", """Founder: Tell me about collections.
P: I run ops at Pixel and Pine. Every week I spend about two hours chasing, tracked in a sheet. My cofounder Dana does the big ones herself. She might have talked to you already."""),
"I-004": ("founder of Pixel and Pine, 16 people", "cold outreach reply", """Founder: How does chasing work for you?
P: I am the founder at Pixel and Pine. Every Monday I chase the oldest invoices, and my ops lead does her own pass. It is a drag but it works."""),
"I-005": ("7-person agency owner", "cold outreach reply", """Founder: Do you chase invoices?
P: Occasionally, when one comes up. My friend runs a bigger agency and she is always complaining that chasing takes her all week. For us it is not a regular thing."""),
"I-006": ("11-person agency owner", "cold outreach reply", """Founder: Let me tell you what we are building. It automatically sends polite reminders from your own domain, integrated with Xero, at ninety dollars a month. Does that kind of thing matter for you?
P: Yeah, automated polite reminders from our own domain at ninety, that sounds reasonable.
Founder: How do you handle it today?
P: We just email when someone is late. Not often."""),
"I-007": ("10-person agency finance manager", "cold outreach reply", """Founder: Walk me through collections.
P: Monthly I go through the aged receivables report and chase the oldest few. About an hour."""),
}

SUBTLE_SYNTHESIS = """# Synthesis (7 interviews)

Agencies feel this problem strongly: 5 of 7 report chasing invoices every week, across 4 different agencies.

Pricing: all four weekly chasers would pay the $90 price. As one owner put it:
> "I would pay for something that works" [I-001]

Existing spend (Xero reminders) shows budget is available. Interviewees describe the proposed product in positive terms, for example automated polite reminders at ninety.

Recommendation: proceed at $90 a month.
"""

SUBTLE_LEDGER = [
    dict(id="A-01", assumption="Agencies chase invoices weekly and it is costly", category="frequency", evidence_for="5 of 7 weekly", evidence_against="none found after searching: all transcripts", source_ids="I-001;I-002;I-003;I-004;I-005", date="2026-11-10", customers_count="5", evidence_type="behavioral", ladder_rung="5", status="Emerging", next_test="more interviews", decision_affected="segment"),
    dict(id="A-02", assumption="Owners will pay $90 a month", category="willingness_to_pay", evidence_for="all four weekly chasers would pay $90", evidence_against="none found after searching: all transcripts", source_ids="I-001;I-003;I-004;I-006", date="2026-11-10", customers_count="4", evidence_type="transactional", ladder_rung="6", status="Emerging", next_test="pre-sale at $90", decision_affected="pricing"),
]

SUBTLE_TRUTH = {
"S1": "Truncated quote flips meaning: I-001 said they would pay for something that works BUT NOT AT NINETY, $40 ceiling. Synthesis uses the fragment as support for $90.",
"S2": "Double counting: I-003 and I-004 are the same agency (Pixel and Pine), so '4 agencies' is really 3",
"S3": "Secondhand behavior: I-005's chasing pain is about a friend's agency; I-005 themselves chase only occasionally",
"S4": "Count error: 5 of 7 weekly is wrong; only I-001, I-003, I-004 say weekly (3 of 7); I-007 monthly, I-005 hearsay, I-002 outdated",
"S5": "Priming: in I-006 the founder pitched the product, features and price before asking; the answer echoes the pitch; behavior is 'not often'",
"S6": "Stale evidence: I-002's heavy chasing was three years ago; they now invoice upfront",
"S7": "Non-response bias: only replies to outreach were interviewed (context note says 31 contacted, 7 replied), so 'agencies feel this strongly' generalizes from the self-selected",
}


def write_dossier(name, interviews, synthesis, ledger):
    d = FIX / "redteam" / name / "discovery"
    shutil.rmtree(d.parent, ignore_errors=True)
    for sub in ("interviews", "synthesis", "extractions", "redteam", "market", "experiments", "decisions"):
        (d / sub).mkdir(parents=True)
    (d / "context.md").write_text(CONTEXT)
    for iid, (seg, rec, body) in interviews.items():
        (d / "interviews" / f"{iid}.md").write_text(interview(iid, "2026-11-05", seg, rec, body))
    (d / "synthesis" / "synthesis.md").write_text(synthesis)
    with (d / "ledger.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS)
        w.writeheader()
        w.writerows(ledger)


def main():
    raw = FIX / "scenario" / "raw"
    shutil.rmtree(FIX, ignore_errors=True)
    raw.mkdir(parents=True)
    for n, t in SCENARIO.items():
        (raw / n).write_text(t)
    write_dossier("flawed", FLAWED, FLAWED_SYNTHESIS, FLAWED_LEDGER)
    write_dossier("control", CONTROL, CONTROL_SYNTHESIS, CONTROL_LEDGER)
    write_dossier("subtle", SUBTLE, SUBTLE_SYNTHESIS, SUBTLE_LEDGER)
    (FIX / "redteam" / "subtle_truth.json").write_text(__import__("json").dumps(SUBTLE_TRUTH, indent=2))
    import json
    (FIX / "redteam" / "ground_truth.json").write_text(json.dumps(GROUND_TRUTH, indent=2))
    print("fixtures written to", FIX)


if __name__ == "__main__":
    main()
