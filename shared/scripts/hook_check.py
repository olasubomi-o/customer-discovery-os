#!/usr/bin/env python3
"""PostToolUse hook for Claude Code: validate discovery/ files right after the model writes them.

Reads the hook JSON from stdin. If the written file lives under a discovery/ folder,
runs `ddos.py check --file` and, on errors, prints them to stderr and exits 2 so
Claude Code feeds them back to the model for correction. Silent otherwise.
"""
import json
import subprocess
import sys
from pathlib import Path

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = (data.get("tool_input") or {}).get("file_path") or ""
p = Path(path)
parts = p.parts
if "discovery" not in parts:
    sys.exit(0)
root = Path(*parts[: parts.index("discovery") + 1])
here = Path(__file__).resolve().parent
r = subprocess.run(
    [sys.executable, str(here / "ddos.py"), "--dir", str(root), "check", "--file", str(p)],
    capture_output=True, text=True,
)
if r.returncode == 2:
    sys.stderr.write(
        "Customer Discovery OS standards check FAILED for " + p.name + ". Fix every ERROR below, then re-save:\n"
        + r.stdout
    )
    sys.exit(2)
sys.exit(0)
