#!/usr/bin/env python3
"""Customer Discovery OS helper (stdlib only).

Commands:
  init    --hypothesis NAME            create the shared discovery/ folder for ONE hypothesis
  list    [--root .]                   list every hypothesis folder under a workspace
  ingest  FILE [--segment S] [--consent yes|no|unknown] [--date D] [--redact "Name,Company"]
                                       normalise a transcript into interviews/I-NNN.md
  check   [--dir discovery] [--file F] verify the folder against the OS standards
  status  [--dir discovery]            say which stage the founder is in and what is next

`check` exits 2 when it finds ERRORs (so a hook can feed the message back to
the model) and 0 otherwise. WARNs never block.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

LEDGER_COLS = [
    "id", "assumption", "category", "evidence_for", "evidence_against",
    "source_ids", "date", "customers_count", "evidence_type", "ladder_rung",
    "status", "next_test", "decision_affected",
]
STATUSES = {"Unknown", "Weak", "Emerging", "Strong", "Invalidated"}
EVIDENCE_TYPES = {"opinion", "behavioral", "transactional", "commitment", "secondary", "mixed"}
STRONG_TYPES = {"behavioral", "transactional", "commitment"}
PAY_CATEGORIES = {"willingness_to_pay", "pricing", "willingness-to-pay"}
DECISIONS = {"proceed", "narrow", "pivot", "investigate further", "stop"}

EXTRACTION_HEADINGS = [
    "Facts", "Inferences", "Hypotheses", "Exact customer language",
    "What this interview does NOT prove",
]
MEMO_HEADINGS = [
    "Original belief", "What we tested", "What we observed",
    "Strongest supporting evidence", "Strongest contradictory evidence",
    "What appears validated", "What appears invalidated",
    "What remains unknown", "Next experiment", "Decision",
]
REDTEAM_HEADINGS = [
    "Evidence that contradicts", "Alternative explanations",
    "Case against", "Case for", "Evidence needed next",
]
EXPERIMENT_FIELDS = [
    "Hypothesis", "Riskiest assumption", "Success threshold",
    "Failure threshold", "Thresholds-set", "Decision if success", "Decision if failure",
]
MARKET_EXEMPT_SECTIONS = ("limits", "method", "questions", "next", "what online")
QUOTE_DIRS_SKIP = {"interviews", "market"}

ID_I = re.compile(r"\bI-\d{3}\b")
ID_M = re.compile(r"\bM-\d{3}\b")


# ---------------------------------------------------------------- helpers
def norm(s: str) -> str:
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[\s]+", " ", s.lower()).strip()
    return re.sub(r"[.,;:!?]+$", "", s)


def quote_in_source(quote: str, source_text: str) -> bool:
    """Every segment of the quote (split on ... or [...]) must appear verbatim, in order."""
    src = norm(source_text)
    # normalise punctuation noise inside the source too
    parts = [p for p in re.split(r"\s*(?:\[\.\.\.\]|\.\.\.|…)\s*", quote) if p.strip()]
    pos = 0
    for p in parts:
        n = norm(p)
        i = src.find(n, pos)
        if i < 0:
            return False
        pos = i + len(n)
    return True


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def headings(text: str):
    return [re.sub(r"^#+\s*", "", ln).strip() for ln in text.splitlines() if re.match(r"^#+\s", ln)]


def has_heading(text: str, name: str) -> bool:
    n = name.lower()
    return any(h.lower().startswith(n) for h in headings(text))


def section(text: str, name: str) -> str:
    lines, out, on = text.splitlines(), [], False
    for ln in lines:
        if re.match(r"^#+\s", ln):
            h = re.sub(r"^#+\s*", "", ln).strip().lower()
            on = h.startswith(name.lower())
            continue
        if on:
            out.append(ln)
    return "\n".join(out).strip()


def field(text: str, name: str):
    m = re.search(rf"^\s*[-*]?\s*\**{re.escape(name)}\**\s*:\s*(.*)$", text, re.I | re.M)
    return m.group(1).strip() if m else None


class Report:
    def __init__(self):
        self.items = []

    def err(self, where, msg):
        self.items.append(("ERROR", where, msg))

    def warn(self, where, msg):
        self.items.append(("WARN", where, msg))

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]

    def print(self):
        for lvl, where, msg in self.items:
            print(f"{lvl} {where}: {msg}")
        print(f"-- {len(self.errors)} error(s), {len(self.items) - len(self.errors)} warning(s)")


# ---------------------------------------------------------------- checks
def ids_available(root: Path):
    have = set()
    for sub, pat in (("interviews", "I-*.md"), ("market", "M-*.md")):
        d = root / sub
        if d.is_dir():
            have |= {f.stem for f in d.glob(pat)}
    return have


def check_interview(f: Path, rep: Report):
    t = read(f)
    head = t.split("\n---", 1)[0]
    iid = field(head, "ID")
    if iid != f.stem:
        rep.err(f.name, f"header ID '{iid}' does not match filename '{f.stem}'")
    consent = (field(head, "Consent") or "").lower()
    if consent not in {"yes", "no", "unknown"}:
        rep.err(f.name, "header needs 'Consent: yes|no|unknown' (recording/notes consent)")
    elif consent != "yes":
        rep.warn(f.name, f"Consent is '{consent}'. Confirm you may store and analyze this material.")
    if not field(head, "Date"):
        rep.warn(f.name, "header has no Date")


def check_quotes(f: Path, root: Path, rep: Report):
    """Every blockquote is a verified customer quote: > "text" [I-001]."""
    t = read(f)
    for n, ln in enumerate(t.splitlines(), 1):
        if not ln.lstrip().startswith(">"):
            continue
        m = re.match(r'^\s*>\s*["“](.+?)["”]\s*\[(I-\d{3})\]\s*$', ln)
        if not m:
            rep.err(f"{f.relative_to(root)}:{n}",
                    'blockquotes are reserved for verbatim customer quotes in the form > "quote" [I-001]')
            continue
        quote, iid = m.group(1), m.group(2)
        src = root / "interviews" / f"{iid}.md"
        if not src.exists():
            rep.err(f"{f.relative_to(root)}:{n}", f"quote cites {iid} but interviews/{iid}.md does not exist")
            continue
        body = read(src).split("\n---", 1)[-1]
        if not quote_in_source(quote, body):
            rep.err(f"{f.relative_to(root)}:{n}",
                    f'quote not found verbatim in {iid}: "{quote[:70]}". Paraphrase it (no quote marks) or fix the quote.')


def check_extraction(f: Path, root: Path, rep: Report):
    t = read(f)
    iid = field(t, "Interview")
    if not iid or not ID_I.fullmatch(iid):
        rep.err(f.name, "needs a header line 'Interview: I-001'")
    elif f.stem != iid:
        rep.err(f.name, f"filename should be {iid}.md")
    elif not (root / "interviews" / f"{iid}.md").exists():
        rep.err(f.name, f"interviews/{iid}.md does not exist")
    for h in EXTRACTION_HEADINGS:
        if not has_heading(t, h):
            rep.err(f.name, f"missing section '## {h}'")
    facts = section(t, "Facts")
    for ln in facts.splitlines():
        s = ln.strip()
        if s.startswith(("- ", "* ")) and not ID_I.search(s) and "not established" not in s.lower():
            rep.err(f.name, f"Fact without [I-xxx] source tag or 'Not established': {s[:70]}")
    if not section(t, "What this interview does NOT prove").strip():
        rep.err(f.name, "'What this interview does NOT prove' is empty")


def check_market(f: Path, root: Path, rep: Report):
    t = read(f)
    if not re.search(r"^\s*ID\s*:\s*M-\d{3}", t, re.M) or field(t, "ID") != f.stem:
        rep.err(f.name, "needs header 'ID: M-001' matching the filename")
    if (field(t, "Type") or "").lower() != "secondary":
        rep.err(f.name, "needs 'Type: secondary' (online research is never primary evidence)")
    if not field(t, "Date"):
        rep.err(f.name, "needs 'Date:' (when the sources were accessed)")
    cur = ""
    for n, ln in enumerate(t.splitlines(), 1):
        if re.match(r"^#+\s", ln):
            cur = re.sub(r"^#+\s*", "", ln).strip().lower()
            continue
        if ln.lstrip().startswith(">"):
            rep.err(f"{f.name}:{n}", "no block quotes in market scans; paraphrase")
        for q in re.findall(r'"([^"]{1,600})"', ln):
            if len(q.split()) >= 15:
                rep.err(f"{f.name}:{n}", "quoted span is 15+ words; paraphrase instead")
        s = ln.strip()
        is_claim = s.startswith(("- ", "* ")) or (s.startswith("|") and not re.match(r"^\|[\s:-]+\|", s) and not s.lower().startswith("| competitor") and "---" not in s)
        if is_claim and not cur.startswith(MARKET_EXEMPT_SECTIONS):
            if "http" not in s and "(unverified)" not in s.lower() and not s.lower().startswith("| name"):
                if not re.match(r"^\|\s*(competitor|alternative|theme|source)\b", s, re.I):
                    rep.err(f"{f.name}:{n}", "finding without a source URL (add the URL or mark '(unverified)')")


def check_experiment(f: Path, root: Path, rep: Report, ledger_ids):
    t = read(f)
    for fld in EXPERIMENT_FIELDS:
        v = field(t, fld)
        if v is None or not v or v.startswith("["):
            rep.err(f.name, f"missing or empty field '{fld}:'")
    for fld in ("Success threshold", "Failure threshold"):
        v = field(t, fld) or ""
        if v and not re.search(r"\d", v):
            rep.warn(f.name, f"'{fld}' has no number. A threshold you cannot measure is not a threshold.")
    set_d, run_d = field(t, "Thresholds-set"), field(t, "Run-date")
    try:
        if run_d and not set_d:
            rep.err(f.name, "Run-date present but Thresholds-set missing. Thresholds must be set before the run.")
        elif run_d and set_d and dt.date.fromisoformat(set_d) > dt.date.fromisoformat(run_d):
            rep.err(f.name, "Thresholds-set is after Run-date. Pre-commit thresholds before you run the test.")
    except ValueError:
        rep.err(f.name, "Thresholds-set / Run-date must be ISO dates (YYYY-MM-DD)")
    aid = field(t, "Assumption-ID")
    if ledger_ids is not None and (not aid or aid not in ledger_ids):
        rep.warn(f.name, "Assumption-ID missing or not found in ledger.csv")


def check_memo(f: Path, root: Path, rep: Report, ledger_rows):
    t = read(f)
    for h in MEMO_HEADINGS:
        if not has_heading(t, h):
            rep.err(f.name, f"missing section '## {h}'")
    dec = (field(t, "Decision") or "").strip().lower().rstrip(".")
    if dec not in DECISIONS:
        rep.err(f.name, "needs 'Decision: Proceed | Narrow | Pivot | Investigate further | Stop'")
    if (field(t, "Confidence") or "").lower() not in {"low", "medium", "high"}:
        rep.err(f.name, "needs 'Confidence: Low | Medium | High'")
    if has_heading(t, "What remains unknown") and not section(t, "What remains unknown"):
        rep.err(f.name, "'What remains unknown' is empty. Every decision has unknowns.")
    n = field(t, "Interviews-represented")
    try:
        n = int(n)
    except (TypeError, ValueError):
        rep.err(f.name, "needs 'Interviews-represented: <number>'")
        n = None
    if n is not None and n < 5 and dec in {"proceed", "pivot", "stop"}:
        rep.warn(f.name, f"Decision '{dec}' rests on {n} interview(s). Consider 'Investigate further'.")
    if dec == "proceed" and ledger_rows is not None:
        if not any((r.get("ladder_rung", "").isdigit() and int(r["ladder_rung"]) >= 6) for r in ledger_rows):
            rep.warn(f.name, "Proceed with no ledger evidence at rung 6+ (existing spend, commitment or payment).")


def check_redteam(f: Path, rep: Report):
    t = read(f)
    for h in REDTEAM_HEADINGS:
        if not has_heading(t, h):
            rep.err(f.name, f"missing section '## {h}'")
    if re.search(r"^\s*(winner|verdict)\s*:", t, re.I | re.M):
        rep.err(f.name, "red-team output must not declare a winner or verdict")


def load_ledger(root: Path, rep: Report):
    p = root / "ledger.csv"
    if not p.exists():
        return None
    with p.open(newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        missing = [c for c in LEDGER_COLS if c not in (rd.fieldnames or [])]
        if missing:
            rep.err("ledger.csv", f"missing columns: {', '.join(missing)}")
            return None
        return list(rd)


def check_ledger(rows, root: Path, rep: Report):
    have = ids_available(root)
    seen = set()
    for i, r in enumerate(rows, 2):
        where = f"ledger.csv:{i}"
        rid = (r["id"] or "").strip()
        if not rid or rid in seen:
            rep.err(where, "empty or duplicate id")
        seen.add(rid)
        status = (r["status"] or "").strip()
        etype = (r["evidence_type"] or "").strip().lower()
        if status not in STATUSES:
            rep.err(where, f"status '{status}' not in {sorted(STATUSES)}")
            continue
        if etype not in EVIDENCE_TYPES:
            rep.err(where, f"evidence_type '{etype}' not in {sorted(EVIDENCE_TYPES)}")
        try:
            rung = int(r["ladder_rung"])
            assert 1 <= rung <= 8
        except Exception:
            rep.err(where, "ladder_rung must be an integer 1-8 (see evidence ladder)")
            rung = 0
        srcs = set(ID_I.findall(r["source_ids"] or "")) | set(ID_M.findall(r["source_ids"] or ""))
        i_src = {s for s in srcs if s.startswith("I-")}
        m_src = {s for s in srcs if s.startswith("M-")}
        for s in srcs:
            if s not in have:
                rep.err(where, f"source {s} has no file in interviews/ or market/")
        try:
            cc = int(r["customers_count"])
            if cc > len(i_src):
                rep.warn(where, f"customers_count {cc} exceeds distinct interview sources ({len(i_src)})")
        except ValueError:
            rep.err(where, "customers_count must be an integer")
        against = (r["evidence_against"] or "").strip()
        cat = (r["category"] or "").strip().lower()
        if status in {"Strong", "Emerging", "Invalidated"} and not against:
            rep.err(where, "evidence_against is empty. Search for disproof, then write what you found or 'none found after searching: <what you searched>'.")
        if status == "Strong":
            if len(i_src) < 5:
                rep.err(where, f"Strong needs 5+ distinct interviews (has {len(i_src)}). Use Emerging.")
            if rung < 5:
                rep.err(where, f"Strong needs ladder rung 5+ (cost, existing spend, commitment, payment); has {rung}.")
            if cat in PAY_CATEGORIES and rung < 6:
                rep.err(where, "Strong willingness-to-pay needs rung 6+ (existing spend, commitment or payment).")
            if etype not in STRONG_TYPES:
                rep.err(where, f"Strong cannot rest on evidence_type '{etype}'. Opinions and secondary research cannot make an assumption Strong.")
        if status == "Emerging":
            if len(srcs) < 2 or rung < 3:
                rep.err(where, "Emerging needs 2+ sources and ladder rung 3+. Use Weak.")
        if m_src and not i_src:
            if rung > 4:
                rep.err(where, "online-only evidence cannot exceed ladder rung 4")
            if status == "Strong":
                rep.err(where, "online-only evidence can never be Strong")
        if status != "Invalidated":
            if not (r["next_test"] or "").strip():
                rep.err(where, "next_test is empty. Every open assumption needs the cheapest next test.")
            if not (r["decision_affected"] or "").strip():
                rep.warn(where, "decision_affected is empty. Evidence that changes no decision is trivia.")


HYP_LINE = re.compile(r"^\s*(?:Hypothesis|Hypothesis-ID):\s*(\S+)\s*$", re.I | re.M)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def read_hypothesis(root: Path):
    f = root / "hypothesis.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return {"id": None, "name": None}


def check_hypothesis(f: Path, root: Path, hyp, rep: Report):
    """Every file that declares a hypothesis id must match this folder's id."""
    if not hyp or not hyp.get("id"):
        return
    head = "\n".join(read(f).splitlines()[:15])
    ids = set(HYP_LINE.findall(head))
    for other in ids:
        if other != hyp["id"]:
            rep.err(f.name, f"belongs to hypothesis '{other}' but this folder is '{hyp['id']}'. Wrong folder or pasted from another project. Move it or fix the header.")
    if not ids and f.parent.name == "interviews":
        rep.warn(f.name, f"no 'Hypothesis: {hyp['id']}' header. Re-ingest or add it so the interview is tied to this hypothesis.")


def run_check(root: Path, only: Path | None = None) -> Report:
    rep = Report()
    if not root.is_dir():
        rep.err(str(root), "discovery folder not found. Run: ddos.py init")
        return rep
    hyp = read_hypothesis(root)
    if hyp is None:
        rep.warn("hypothesis.json", "this folder has no hypothesis id. Run: ddos.py init --hypothesis \"short name\" so contexts from different ideas cannot mix.")
    elif not hyp.get("id"):
        rep.err("hypothesis.json", "unreadable or missing 'id'. Re-run: ddos.py init --hypothesis \"short name\"")
    rows = load_ledger(root, rep) if (only is None or only.name == "ledger.csv") else None
    ledger_rows_all = load_ledger(root, Report())
    ledger_ids = {r["id"] for r in ledger_rows_all} if ledger_rows_all else None

    def want(p: Path):
        return only is None or only.resolve() == p.resolve()

    for f in sorted((root / "interviews").glob("I-*.md")) if (root / "interviews").is_dir() else []:
        if want(f):
            check_interview(f, rep)
    for f in sorted((root / "extractions").glob("*.md")) if (root / "extractions").is_dir() else []:
        if want(f):
            check_extraction(f, root, rep)
    for f in sorted((root / "market").glob("M-*.md")) if (root / "market").is_dir() else []:
        if want(f):
            check_market(f, root, rep)
    for f in sorted((root / "experiments").glob("*.md")) if (root / "experiments").is_dir() else []:
        if want(f):
            check_experiment(f, root, rep, ledger_ids)
    for f in sorted((root / "decisions").glob("memo-*.md")) if (root / "decisions").is_dir() else []:
        if want(f):
            check_memo(f, root, rep, ledger_rows_all)
    for f in sorted((root / "redteam").glob("*.md")) if (root / "redteam").is_dir() else []:
        if want(f):
            check_redteam(f, rep)
    for f in sorted(root.rglob("*.md")):
        if want(f):
            check_hypothesis(f, root, hyp, rep)
    for f in sorted(root.rglob("*.md")):
        parts = f.relative_to(root).parts
        if parts[0] in QUOTE_DIRS_SKIP or f.name in {"context.md", "README.md"} or len(parts) == 1 and False:
            continue
        if want(f):
            check_quotes(f, root, rep)
    if rows is not None and want(root / "ledger.csv"):
        check_ledger(rows, root, rep)
    return rep


# ---------------------------------------------------------------- commands
CONTEXT_TEMPLATE = """# Discovery context

## Startup
[one or two sentences]

## Target customer
[who exactly, behaviorally]

## Current hypothesis
[the belief you are testing]

## Decision this research should inform
[the real decision, e.g. build / narrow / pivot / stop]
"""


def cmd_init(a):
    root = Path(a.dir)
    existing = read_hypothesis(root)
    if a.hypothesis:
        hid = slugify(a.hypothesis)
        if not hid:
            sys.exit("init: --hypothesis needs a name with letters or digits")
        if existing and existing.get("id") and existing["id"] != hid:
            sys.exit(f"init: this folder already belongs to hypothesis '{existing['id']}'. Use a different folder for '{hid}' (one folder per hypothesis).")
    elif existing and existing.get("id"):
        hid = existing["id"]
        a.hypothesis = existing.get("name") or hid
    else:
        sys.exit('init: pass --hypothesis "short name of the idea you are testing". One discovery folder holds exactly one hypothesis.')
    for sub in ("interviews", "extractions", "synthesis", "market", "redteam", "experiments", "decisions", "voc"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    root.mkdir(parents=True, exist_ok=True)
    (root / "hypothesis.json").write_text(json.dumps({"id": hid, "name": a.hypothesis}, indent=2) + "\n", encoding="utf-8")
    if not (root / "context.md").exists():
        (root / "context.md").write_text(f"Hypothesis-ID: {hid}\n\n" + CONTEXT_TEMPLATE, encoding="utf-8")
    if not (root / "ledger.csv").exists():
        with (root / "ledger.csv").open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(LEDGER_COLS)
    gi = root / ".gitignore"
    if not gi.exists():
        gi.write_text("# Interview material can contain personal data. Keep it out of public repos.\ninterviews/\nextractions/\nsynthesis/\nvoc/\nledger.csv\n", encoding="utf-8")
    print(f"initialised {root}/ for hypothesis '{hid}' (interviews/, extractions/, synthesis/, voc/ and ledger.csv are git-ignored by default)")


EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s.-]?\d{3,4}[\s.-]?\d{3,4}(?!\w)")


def cmd_ingest(a):
    root = Path(a.dir)
    (root / "interviews").mkdir(parents=True, exist_ok=True)
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    counts = {"email": 0, "phone": 0, "custom": 0}
    text, counts["email"] = EMAIL.subn("[EMAIL]", text)
    text, counts["phone"] = PHONE.subn(lambda m: "[PHONE]" if sum(c.isdigit() for c in m.group(0)) >= 10 else m.group(0), text)
    for term in [t.strip() for t in (a.redact or "").split(",") if t.strip()]:
        text, n = re.subn(r"(?<!\w)" + re.escape(term) + r"(?!\w)", "[REDACTED]", text, flags=re.I)
        counts["custom"] += n
    nums = [int(m.group(1)) for f in (root / "interviews").glob("I-*.md") if (m := re.match(r"I-(\d{3})", f.stem))]
    iid = f"I-{(max(nums) + 1 if nums else 1):03d}"
    head = (
        f"ID: {iid}\n{('Hypothesis: ' + _hid + chr(10)) if (_hid := (read_hypothesis(root) or {}).get('id')) else ''}Date: {a.date or dt.date.today().isoformat()}\nConsent: {a.consent}\n"
        f"Segment: {a.segment or 'unspecified'}\nSource: {Path(a.file).name}\n"
        "Redaction: regex for emails and phones plus the names you passed. Names are NOT auto-detected.\n"
    )
    (root / "interviews" / f"{iid}.md").write_text(head + "\n---\n" + text.strip() + "\n", encoding="utf-8")
    print(f"{iid} written. redacted: {counts}. Consent={a.consent}. Review the file for names you did not pass to --redact.")


def cmd_check(a):
    only = Path(a.file) if a.file else None
    root = Path(a.dir)
    if only is not None:
        try:
            only.resolve().relative_to(root.resolve())
        except ValueError:
            sys.exit(0)  # not a discovery file
    rep = run_check(root, only)
    rep.print()
    sys.exit(2 if rep.errors else 0)


def cmd_status(a):
    root = Path(a.dir)
    if not root.is_dir():
        print("STAGE: not started. Next skill: discovery-start (run: ddos.py init).")
        return
    hyp = read_hypothesis(root)
    print("HYPOTHESIS:", f"{hyp['id']} (folder: {root})" if hyp and hyp.get("id") else f"not set (folder: {root}). Run: ddos.py init --hypothesis \"short name\"")
    n = lambda d, pat="*.md": len(list((root / d).glob(pat))) if (root / d).is_dir() else 0
    ctx = (root / "context.md").read_text(encoding="utf-8") if (root / "context.md").exists() else ""
    ledger = load_ledger(root, Report()) or []
    ni, ne, nm, ns, nr, nx, nd = n("interviews", "I-*.md"), n("extractions"), n("market", "M-*.md"), n("synthesis"), n("redteam"), n("experiments"), n("decisions", "memo-*.md")
    print(f"interviews={ni} extractions={ne} market_scans={nm} synthesis={ns} redteam={nr} experiments={nx} memos={nd} ledger_rows={len(ledger)}")
    if "[one or two sentences]" in ctx or not ctx:
        stage = "SET UP: context.md is still a template. Next skill: discovery-start."
    elif not (root / "assumptions.md").exists():
        stage = "ASSUMPTIONS: no assumptions.md. Next skill: discovery-start."
    elif ni == 0:
        stage = "PREPARE: no interviews yet. Next skills: interview-prep, participant-outreach, market-scan."
    elif ni > ne:
        stage = f"EXTRACT: {ni - ne} interview(s) not extracted. Next skill: interview-analysis."
    elif ne < 5 and ns == 0:
        stage = f"INTERVIEW: {ne} of 5+ interviews extracted. Keep interviewing (interview-prep, participant-outreach), then run pattern-synthesis."
    elif ne >= 5 and ns == 0:
        stage = "SYNTHESIZE: 5+ extractions, no synthesis. Next skill: pattern-synthesis."
    elif ns and nr == 0:
        stage = "CHALLENGE: synthesis exists, never red-teamed. Next skill: red-team."
    elif nx == 0:
        stage = "TEST: no experiments designed. Next skill: experiment-designer."
    elif nd == 0:
        stage = "DECIDE: no decision memo. Next skill: decision-memo."
    else:
        stage = "ITERATE: loop continues. Update ledger after each new interview; re-run red-team before the next memo."
    print("STAGE:", stage)


def cmd_list(a):
    base = Path(a.root)
    found = sorted(base.rglob("hypothesis.json"))
    if not found:
        print(f"no hypotheses found under {base}. Start one with: ddos.py --dir <folder>/discovery init --hypothesis \"name\"")
        return
    for f in found:
        h = read_hypothesis(f.parent) or {}
        print(f"{h.get('id')}\t{h.get('name')}\t{f.parent}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="discovery")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--hypothesis")
    p = sub.add_parser("list")
    p.add_argument("--root", default=".")
    p = sub.add_parser("ingest")
    p.add_argument("file")
    p.add_argument("--segment")
    p.add_argument("--consent", choices=["yes", "no", "unknown"], default="unknown")
    p.add_argument("--date")
    p.add_argument("--redact")
    p = sub.add_parser("check")
    p.add_argument("--file")
    sub.add_parser("status")
    a = ap.parse_args()
    {"init": cmd_init, "ingest": cmd_ingest, "check": cmd_check, "status": cmd_status, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    main()
