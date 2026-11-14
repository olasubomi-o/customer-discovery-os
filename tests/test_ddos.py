#!/usr/bin/env python3
"""Enforcement tests: the checker must reject planted violations and accept valid work."""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "shared" / "scripts" / "ddos.py"
HOOK = ROOT / "shared" / "scripts" / "hook_check.py"
spec = importlib.util.spec_from_file_location("ddos", SCRIPT)
ddos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ddos)

TRANSCRIPT = (
    "ID: I-001\nDate: 2026-11-01\nConsent: yes\nSegment: agency owner\nSource: t.txt\n---\n"
    "Interviewer: Tell me about the last time a client paid late.\n"
    "Owner: Last month. I spent about five hours chasing it, and I built a spreadsheet to track who owes me.\n"
    "Owner: We already pay thirty nine dollars a month for reminders but nobody reads them.\n"
)

GOOD_EXTRACTION = """Interview: I-001
## Facts
- Spends about five hours chasing a late invoice [I-001]
- Built a spreadsheet to track debtors [I-001]
- Money spent on reminder tool: Not established
## Inferences
- Time cost is real for this participant
## Hypotheses
- Reminders sent to the wrong inbox fail
## Exact customer language
> "I built a spreadsheet to track who owes me" [I-001]
## What this interview does NOT prove
It does not show the problem is common or that anyone will pay.
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "discovery"
        for s in ("interviews", "extractions", "market", "experiments", "decisions", "redteam", "synthesis"):
            (self.root / s).mkdir(parents=True)
        (self.root / "interviews" / "I-001.md").write_text(TRANSCRIPT)
        self.write_ledger([])

    def tearDown(self):
        self.tmp.cleanup()

    def write_ledger(self, rows):
        with (self.root / "ledger.csv").open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=ddos.LEDGER_COLS)
            w.writeheader()
            for r in rows:
                base = dict(id="A-01", assumption="x", category="problem", evidence_for="e", evidence_against="none found after searching: all transcripts",
                            source_ids="I-001", date="2026-11-01", customers_count="1", evidence_type="behavioral", ladder_rung="4",
                            status="Weak", next_test="interview 5 more", decision_affected="build or not")
                base.update(r)
                w.writerow(base)

    def add_interviews(self, n):
        for i in range(2, n + 1):
            (self.root / "interviews" / f"I-{i:03d}.md").write_text(TRANSCRIPT.replace("I-001", f"I-{i:03d}"))

    def errors(self):
        rep = ddos.run_check(self.root)
        return [m for lvl, w, m in rep.items if lvl == "ERROR"], [m for lvl, w, m in rep.items if lvl == "WARN"]

    def put(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def assertErr(self, frag):
        errs, _ = self.errors()
        self.assertTrue(any(frag in e for e in errs), f"expected error containing {frag!r}, got {errs}")

    def assertClean(self):
        errs, _ = self.errors()
        self.assertEqual(errs, [], errs)


class TestExtractionsAndQuotes(Base):
    def test_good_extraction_passes(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION)
        self.assertClean()

    def test_fabricated_quote_rejected(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION.replace("I built a spreadsheet to track who owes me", "I would pay anything to fix this"))
        self.assertErr("not found verbatim")

    def test_curly_quotes_and_ellipsis_accepted(self):
        t = GOOD_EXTRACTION.replace('> "I built a spreadsheet to track who owes me" [I-001]', '> “I spent about five hours chasing it, and I built a spreadsheet” [I-001]')
        self.put("extractions/I-001.md", t)
        self.assertClean()
        t2 = GOOD_EXTRACTION.replace('> "I built a spreadsheet to track who owes me" [I-001]', '> "I spent about five hours ... a spreadsheet to track who owes me" [I-001]')
        self.put("extractions/I-001.md", t2)
        self.assertClean()

    def test_untagged_blockquote_rejected(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION + "\n> some note without a source\n")
        self.assertErr("reserved for verbatim customer quotes")

    def test_fact_without_source_rejected(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION.replace("- Built a spreadsheet to track debtors [I-001]", "- Customers hate spreadsheets"))
        self.assertErr("Fact without [I-xxx] source tag")

    def test_missing_sections_rejected(self):
        self.put("extractions/I-001.md", "Interview: I-001\n## Facts\n- x [I-001]\n")
        self.assertErr("missing section '## Inferences'")
        self.assertErr("missing section '## What this interview does NOT prove'")

    def test_empty_does_not_prove_rejected(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION.replace("It does not show the problem is common or that anyone will pay.", ""))
        self.assertErr("'What this interview does NOT prove' is empty")

    def test_extraction_for_missing_interview_rejected(self):
        self.put("extractions/I-009.md", GOOD_EXTRACTION.replace("I-001", "I-009"))
        self.assertErr("interviews/I-009.md does not exist")

    def test_quote_pointing_at_wrong_interview_rejected(self):
        (self.root / "interviews" / "I-002.md").write_text(TRANSCRIPT.replace("I-001", "I-002").replace("spreadsheet", "whiteboard"))
        self.put("extractions/I-001.md", GOOD_EXTRACTION.replace('track who owes me" [I-001]', 'track who owes me" [I-002]'))
        self.assertErr("not found verbatim in I-002")

    def test_quotes_checked_in_other_dirs_too(self):
        self.put("voc/voc.md", '> "customers love our tool" [I-001]\n')
        self.assertErr("not found verbatim")


class TestLedger(Base):
    def test_valid_weak_row_passes(self):
        self.write_ledger([{}])
        self.assertClean()

    def test_strong_with_one_interview_rejected(self):
        self.write_ledger([dict(status="Strong", ladder_rung="6")])
        self.assertErr("Strong needs 5+ distinct interviews")

    def test_strong_on_opinion_rejected(self):
        self.add_interviews(5)
        self.write_ledger([dict(status="Strong", ladder_rung="6", evidence_type="opinion", source_ids="I-001;I-002;I-003;I-004;I-005", customers_count="5")])
        self.assertErr("Strong cannot rest on evidence_type 'opinion'")

    def test_strong_low_rung_rejected(self):
        self.add_interviews(5)
        self.write_ledger([dict(status="Strong", ladder_rung="4", source_ids="I-001;I-002;I-003;I-004;I-005", customers_count="5")])
        self.assertErr("Strong needs ladder rung 5+")

    def test_strong_wtp_needs_rung6(self):
        self.add_interviews(5)
        self.write_ledger([dict(status="Strong", ladder_rung="5", category="willingness_to_pay", source_ids="I-001;I-002;I-003;I-004;I-005", customers_count="5")])
        self.assertErr("willingness-to-pay needs rung 6+")

    def test_strong_requires_counter_evidence_search(self):
        self.add_interviews(5)
        self.write_ledger([dict(status="Strong", ladder_rung="6", evidence_against="", source_ids="I-001;I-002;I-003;I-004;I-005", customers_count="5")])
        self.assertErr("evidence_against is empty")

    def test_good_strong_passes(self):
        self.add_interviews(5)
        self.write_ledger([dict(status="Strong", ladder_rung="6", category="problem", source_ids="I-001;I-002;I-003;I-004;I-005", customers_count="5")])
        self.assertClean()

    def test_emerging_needs_two_sources(self):
        self.write_ledger([dict(status="Emerging", ladder_rung="4")])
        self.assertErr("Emerging needs 2+ sources")

    def test_missing_source_file_rejected(self):
        self.write_ledger([dict(source_ids="I-001;I-077")])
        self.assertErr("source I-077 has no file")

    def test_online_only_capped(self):
        self.put("market/M-001.md", "ID: M-001\nType: secondary\nDate: 2026-11-02\n")
        self.write_ledger([dict(source_ids="M-001", ladder_rung="5", evidence_type="secondary", status="Weak")])
        self.assertErr("online-only evidence cannot exceed ladder rung 4")
        self.write_ledger([dict(source_ids="M-001", ladder_rung="3", evidence_type="secondary", status="Strong")])
        self.assertErr("online-only evidence can never be Strong")

    def test_invalidated_requires_evidence_against(self):
        self.write_ledger([dict(status="Invalidated", evidence_against="")])
        self.assertErr("evidence_against is empty")

    def test_open_row_needs_next_test(self):
        self.write_ledger([dict(next_test="")])
        self.assertErr("next_test is empty")

    def test_unknown_row_with_blank_source_ok(self):
        self.write_ledger([dict(status="Unknown", source_ids="", customers_count="0", ladder_rung="1", evidence_type="opinion", evidence_against="")])
        self.assertClean()

    def test_bad_status_and_rung(self):
        self.write_ledger([dict(status="Validated!", ladder_rung="9")])
        self.assertErr("status 'Validated!' not in")


class TestExperiments(Base):
    GOOD = (
        "Assumption-ID: A-01\nHypothesis: agencies will join a waitlist\nRiskiest assumption: demand\nExperiment: landing page\n"
        "Success threshold: at least 12 of 40 visitors join\nFailure threshold: fewer than 4 of 40\nThresholds-set: 2026-11-01\n"
        "Decision if success: build a concierge version\nDecision if failure: drop this segment\n"
    )

    def test_good_passes(self):
        self.write_ledger([{}])
        self.put("experiments/exp-01.md", self.GOOD)
        self.assertClean()

    def test_missing_thresholds_rejected(self):
        self.put("experiments/exp-01.md", self.GOOD.replace("Failure threshold: fewer than 4 of 40\n", ""))
        self.assertErr("missing or empty field 'Failure threshold:'")

    def test_thresholds_after_run_rejected(self):
        self.put("experiments/exp-01.md", self.GOOD + "Run-date: 2026-10-30\n")
        self.assertErr("Thresholds-set is after Run-date")

    def test_run_without_set_rejected(self):
        self.put("experiments/exp-01.md", self.GOOD.replace("Thresholds-set: 2026-11-01\n", "") + "Run-date: 2026-11-05\n")
        self.assertErr("Thresholds-set")

    def test_non_numeric_threshold_warns_only(self):
        self.write_ledger([{}])
        self.put("experiments/exp-01.md", self.GOOD.replace("at least 12 of 40 visitors join", "many people join"))
        errs, warns = self.errors()
        self.assertEqual(errs, [])
        self.assertTrue(any("no number" in w for w in warns))


class TestMemos(Base):
    def memo(self, decision="Investigate further", n="3", conf="Low", drop=None, unknown="Whether anyone pays."):
        secs = ["Original belief", "What we tested", "What we observed", "Strongest supporting evidence", "Strongest contradictory evidence",
                "What changed in our understanding", "What appears validated", "What appears invalidated", "What remains unknown",
                "Updated customer definition", "Next experiment", "Decision"]
        body = f"Decision: {decision}\nConfidence: {conf}\nInterviews-represented: {n}\n"
        for s in secs:
            if s == drop:
                continue
            body += f"\n## {s}\n{unknown if s == 'What remains unknown' else 'text'}\n"
        return body

    def test_good_memo(self):
        self.put("decisions/memo-2026-11.md", self.memo())
        self.assertClean()

    def test_bad_decision_word(self):
        self.put("decisions/memo-2026-11.md", self.memo(decision="Looks great"))
        self.assertErr("needs 'Decision:")

    def test_missing_section(self):
        self.put("decisions/memo-2026-11.md", self.memo(drop="What remains unknown"))
        self.assertErr("missing section '## What remains unknown'")

    def test_empty_unknowns(self):
        self.put("decisions/memo-2026-11.md", self.memo(unknown=""))
        self.assertErr("'What remains unknown' is empty")

    def test_proceed_on_thin_evidence_warns(self):
        self.put("decisions/memo-2026-11.md", self.memo(decision="Proceed", n="2"))
        errs, warns = self.errors()
        self.assertEqual(errs, [])
        self.assertTrue(any("rests on 2 interview" in w for w in warns))
        self.assertTrue(any("rung 6+" in w for w in warns))


class TestMarketAndRedteam(Base):
    GOOD = (
        "ID: M-001\nType: secondary\nDate: 2026-11-02\nScope: invoice chasing tools\n\n## Method\n- read 12 reviews\n\n"
        "## Competitors\n| competitor | offer | source |\n|---|---|---|\n| ChaseBoard | reminders | https://example.com/chaseboard |\n\n"
        "## Sentiment themes\n- 4 of 12 reviews mention emails landing in spam https://example.com/reviews\n\n## Limits\n- reviews skew to extremes\n"
    )

    def test_good_scan(self):
        self.put("market/M-001.md", self.GOOD)
        self.assertClean()

    def test_finding_without_url_rejected(self):
        self.put("market/M-001.md", self.GOOD.replace(" https://example.com/reviews", ""))
        self.assertErr("finding without a source URL")

    def test_unverified_marker_accepted(self):
        self.put("market/M-001.md", self.GOOD.replace(" https://example.com/reviews", " (unverified)"))
        self.assertClean()

    def test_long_quote_rejected(self):
        long = " ".join(["word"] * 16)
        self.put("market/M-001.md", self.GOOD + f'\n## Extra\n- they said "{long}" https://example.com/x\n')
        self.assertErr("15+ words")

    def test_blockquote_rejected(self):
        self.put("market/M-001.md", self.GOOD + "\n> pasted review text\n")
        self.assertErr("no block quotes")

    def test_type_must_be_secondary(self):
        self.put("market/M-001.md", self.GOOD.replace("Type: secondary", "Type: primary"))
        self.assertErr("Type: secondary")

    def test_redteam_verdict_rejected(self):
        body = "".join(f"## {h}\ntext\n" for h in ddos.REDTEAM_HEADINGS)
        self.put("redteam/r.md", body)
        self.assertClean()
        self.put("redteam/r.md", body + "Verdict: keep going\n")
        self.assertErr("must not declare a winner")


class TestCLIAndHook(Base):
    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=cwd)

    def test_init_and_ingest_redaction(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d).returncode, 0)
            self.assertTrue((Path(d) / "discovery" / "ledger.csv").exists())
            src = Path(d) / "t.txt"
            src.write_text("Jane Doe at Acme said email jane@acme.com or call +1 (212) 555-0147. Acme pays late.")
            r = self.run_cli("ingest", str(src), "--consent", "yes", "--redact", "Jane Doe,Acme", cwd=d)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = (Path(d) / "discovery" / "interviews" / "I-001.md").read_text()
            self.assertNotIn("jane@acme.com", out)
            self.assertNotIn("555-0147", out)
            self.assertNotIn("Jane Doe", out)
            self.assertNotIn("Acme", out)
            self.assertIn("Consent: yes", out)
            r2 = self.run_cli("ingest", str(src), "--consent", "unknown", cwd=d)
            self.assertIn("I-002", r2.stdout)
            self.assertEqual(self.run_cli("check", cwd=d).returncode, 0)

    def test_redaction_respects_word_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d)
            src = Path(d) / "t.txt"
            src.write_text("Ana is managing the same account. Sam said Ana's team is the same as Sam's.")
            self.run_cli("ingest", str(src), "--redact", "Ana,Sam", cwd=d)
            out = (Path(d) / "discovery" / "interviews" / "I-001.md").read_text()
            self.assertIn("managing", out)
            self.assertIn("same", out)
            self.assertNotIn("Ana ", out)
            self.assertNotIn("Sam ", out)
            self.assertIn("[REDACTED]'s team", out)

    def test_init_requires_hypothesis(self):
        with tempfile.TemporaryDirectory() as d:
            r = self.run_cli("init", cwd=d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("--hypothesis", r.stderr + r.stdout)
            self.assertFalse((Path(d) / "discovery").exists())

    def test_one_folder_one_hypothesis(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d).returncode, 0)
            self.assertEqual(self.run_cli("init", "--hypothesis", "invoice chasing", cwd=d).returncode, 0)
            r = self.run_cli("init", "--hypothesis", "AI tutor for nurses", cwd=d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("already belongs to hypothesis 'invoice-chasing'", r.stderr + r.stdout)
            self.assertEqual(self.run_cli("init", cwd=d).returncode, 0)  # re-init without flag keeps identity

    def test_ingest_stamps_hypothesis_and_check_passes(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d)
            src = Path(d) / "t.txt"
            src.write_text("P: I chase invoices weekly.")
            self.run_cli("ingest", str(src), "--consent", "yes", cwd=d)
            out = (Path(d) / "discovery" / "interviews" / "I-001.md").read_text()
            self.assertIn("Hypothesis: invoice-chasing", out)
            r = self.run_cli("check", cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertNotIn("hypothesis.json", r.stdout)

    def test_foreign_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d)
            f = Path(d) / "discovery" / "synthesis" / "s.md"
            f.write_text("Hypothesis: ai-tutor-for-nurses\n\n# Synthesis\nnotes\n")
            r = self.run_cli("check", cwd=d)
            self.assertEqual(r.returncode, 2)
            self.assertIn("belongs to hypothesis 'ai-tutor-for-nurses'", r.stdout)
            r2 = self.run_cli("check", "--file", str(f), cwd=d)  # the hook path
            self.assertEqual(r2.returncode, 2)

    def test_foreign_context_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_cli("init", "--hypothesis", "Invoice chasing", cwd=d)
            c = Path(d) / "discovery" / "context.md"
            c.write_text(c.read_text().replace("Hypothesis-ID: invoice-chasing", "Hypothesis-ID: something-else"))
            self.assertEqual(self.run_cli("check", cwd=d).returncode, 2)

    def test_legacy_folder_warns_not_errors(self):
        r = self.run_cli("--dir", str(self.root), "check")
        self.assertEqual(r.returncode, 0)
        self.assertIn("no hypothesis id", r.stdout)

    def test_list_and_status_name_the_hypothesis(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ("Invoice chasing", "AI tutor for nurses"):
                sub = Path(d) / "ideas" / name.split()[0].lower()
                sub.mkdir(parents=True)
                self.assertEqual(self.run_cli("init", "--hypothesis", name, cwd=sub).returncode, 0)
            out = self.run_cli("list", "--root", d).stdout
            self.assertIn("invoice-chasing", out)
            self.assertIn("ai-tutor-for-nurses", out)
            st = self.run_cli("status", cwd=Path(d) / "ideas" / "invoice").stdout
            self.assertIn("HYPOTHESIS: invoice-chasing", st)
            self.assertNotIn("ai-tutor", st)

    def test_check_exit_code_two_on_error(self):
        self.put("extractions/I-001.md", GOOD_EXTRACTION.replace("track who owes me", "invented words"))
        r = self.run_cli("--dir", str(self.root), "check")
        self.assertEqual(r.returncode, 2)
        self.assertIn("not found verbatim", r.stdout)

    def test_hook_blocks_bad_write_and_ignores_others(self):
        bad = self.root / "extractions" / "I-001.md"
        bad.write_text(GOOD_EXTRACTION.replace("track who owes me", "invented words"))
        payload = json.dumps({"tool_input": {"file_path": str(bad)}})
        r = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("standards check FAILED", r.stderr)
        r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"tool_input": {"file_path": "/tmp/other/readme.md"}}), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        good = self.root / "extractions" / "I-001.md"
        good.write_text(GOOD_EXTRACTION)
        r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"tool_input": {"file_path": str(good)}}), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)

    def test_status_progression(self):
        r = self.run_cli("--dir", str(self.root), "status")
        self.assertIn("STAGE: SET UP", r.stdout)
        self.put("context.md", "# c\n## Startup\nInvoice chasing\n")
        self.assertIn("ASSUMPTIONS", self.run_cli("--dir", str(self.root), "status").stdout)
        self.put("assumptions.md", "x")
        self.assertIn("EXTRACT", self.run_cli("--dir", str(self.root), "status").stdout)
        self.put("extractions/I-001.md", GOOD_EXTRACTION)
        self.assertIn("INTERVIEW: 1 of 5+", self.run_cli("--dir", str(self.root), "status").stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
