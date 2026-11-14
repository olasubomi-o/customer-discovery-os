#!/usr/bin/env python3
"""Copy shared/references and shared/scripts/ddos.py into every skill folder.

Skills must be self-contained to work when uploaded one at a time (Claude.ai, ChatGPT).
`shared/` is the single source of truth. Run this after editing anything in shared/.
"""
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
shared_refs = root / "shared" / "references"
shared_script = root / "shared" / "scripts" / "ddos.py"
changed = 0
for skill in sorted((root / "skills").iterdir()):
    if not (skill / "SKILL.md").exists():
        continue
    (skill / "references").mkdir(exist_ok=True)
    (skill / "scripts").mkdir(exist_ok=True)
    for f in shared_refs.glob("*.md"):
        dst = skill / "references" / f.name
        if not dst.exists() or dst.read_bytes() != f.read_bytes():
            shutil.copyfile(f, dst)
            changed += 1
    dst = skill / "scripts" / "ddos.py"
    if not dst.exists() or dst.read_bytes() != shared_script.read_bytes():
        shutil.copyfile(shared_script, dst)
        changed += 1
print(f"sync complete, {changed} file(s) updated")
sys.exit(0)
