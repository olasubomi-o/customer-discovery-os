#!/usr/bin/env python3
"""Blind skill-routing test.

  router_eval.py prepare OUTDIR SEED     write OUTDIR/task.txt (skill list + shuffled messages)
  router_eval.py score ANSWERS.json      score an agent's answers against router_cases.json

The agent under test sees ONLY skill names + descriptions (what a host loads at startup) and the user
messages. Strict = matches the primary label. Lenient = primary or any acceptable label.
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
import os
CASES = json.loads((HERE / os.environ.get("ROUTER_CASES", "router_cases.json")).read_text())


def skills():
    out = []
    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        t = p.read_text()
        name = re.search(r"^name:\s*(.+)$", t, re.M).group(1).strip()
        desc = re.search(r"^description:\s*(.+)$", t, re.M).group(1).strip()
        out.append((name, desc))
    return out


def prepare(outdir, seed):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(int(seed))
    sk = skills()
    rnd.shuffle(sk)
    msgs = CASES[:]
    rnd.shuffle(msgs)
    lines = ["You are the skill router of an AI assistant. The assistant has these skills. At startup it only sees each skill's name and description.\n"]
    for n, d in sk:
        lines.append(f"SKILL: {n}\nDESCRIPTION: {d}\n")
    lines.append("\nFor each user message below choose the ONE skill the assistant should load, or 'none' if no skill fits (then it just answers normally).")
    lines.append("Decide only from the descriptions. Do not read any other files and do not use tools other than reading this file.")
    lines.append("Write your answer to the answers file named in your instructions as JSON: {\"<id>\": \"<skill-name or none>\", ...} covering every id.\n")
    lines.append("USER MESSAGES:")
    for c in msgs:
        lines.append(f"[{c['id']}] {c['msg']}")
    (out / "task.txt").write_text("\n".join(lines))
    print(out / "task.txt")


def score(path):
    ans = json.loads(Path(path).read_text())
    strict = lenient = 0
    confusion = collections.Counter()
    misses = []
    per_skill = collections.defaultdict(lambda: [0, 0])
    for c in CASES:
        got = str(ans.get(str(c["id"]), "MISSING")).strip().lower()
        prim = c["primary"]
        per_skill[prim][1] += 1
        s = got == prim
        l = s or got in [x.lower() for x in c["ok"]]
        strict += s
        lenient += l
        per_skill[prim][0] += s
        if not s:
            confusion[(prim, got)] += 1
        if not l:
            misses.append((c["id"], prim, got, c["msg"][:80]))
    n = len(CASES)
    print(f"strict accuracy:  {strict}/{n} = {strict / n:.0%}")
    print(f"lenient accuracy: {lenient}/{n} = {lenient / n:.0%}")
    print("per primary label (strict):")
    for k, (a, b) in sorted(per_skill.items()):
        print(f"  {k:22s} {a}/{b}")
    print("confusions (expected -> chosen):")
    for (e, g), cnt in confusion.most_common():
        print(f"  {e} -> {g}: {cnt}")
    print("lenient misses:")
    for m in misses:
        print("  ", m)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(sys.argv[2], sys.argv[3])
    else:
        score(sys.argv[2])
