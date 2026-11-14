#!/usr/bin/env python3
"""Build distributable bundles into dist/.

dist/skills/<name>.zip      one self-contained Agent Skill per zip (Claude.ai, ChatGPT, Codex, any SKILL.md host)
dist/chatgpt-project/       fallback for ChatGPT plans without native skills: Project instructions + knowledge files
"""
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, str(root / "tools" / "sync_shared.py")], check=True)
dist = root / "dist"
shutil.rmtree(dist, ignore_errors=True)
(dist / "skills").mkdir(parents=True)

for skill in sorted((root / "skills").iterdir()):
    if not (skill / "SKILL.md").exists():
        continue
    with zipfile.ZipFile(dist / "skills" / f"{skill.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, Path(skill.name) / f.relative_to(skill))

proj = dist / "chatgpt-project"
(proj / "knowledge").mkdir(parents=True)
copilot = (root / "agents" / "discovery-copilot.md").read_text()
copilot = re.sub(r"^---.*?---\s*", "", copilot, flags=re.S)
instructions = (
    "# Customer Discovery OS (The Product Builders)\n\n"
    + copilot.strip()
    + "\n\n## Hard rules\n"
    "- Never invent customers, quotes, numbers, sources or motivations. Say \"Not established\" instead.\n"
    "- Quote only verbatim text from transcripts the founder pasted, with an interview ID.\n"
    "- Opinions and online research can never make an assumption Strong. Strong needs 5+ interviews and spend, commitment or payment evidence.\n"
    "- Online research is secondary evidence and must carry URLs and dates.\n"
    "- Before saying a deliverable is done, walk the checklist in knowledge file standards.md and say which items pass.\n\n"
    "## How to work\n"
    "Match the founder's request to one of the playbooks in the knowledge files (skill-*.md) and follow it exactly. "
    "Ask the founder to paste the contents of their ledger.csv and context at the start of a new chat, because this chat may not remember earlier sessions.\n"
    "This Project is for exactly ONE hypothesis. At the start of each chat, state the hypothesis name. If the founder describes or pastes material about a different idea, stop and tell them to use a separate Project for it. Never mix interviews, quotes, assumptions or ledger rows across hypotheses.\n"
)
assert len(instructions) < 8000, f"instructions are {len(instructions)} chars; trim to fit the 8000 character limit"
(proj / "INSTRUCTIONS.md").write_text(instructions)
for skill in sorted((root / "skills").iterdir()):
    if (skill / "SKILL.md").exists():
        shutil.copyfile(skill / "SKILL.md", proj / "knowledge" / f"skill-{skill.name}.md")
for f in (root / "shared" / "references").glob("*.md"):
    shutil.copyfile(f, proj / "knowledge" / f.name)
shutil.copyfile(root / "shared" / "scripts" / "ddos.py", proj / "knowledge" / "ddos.py")
(proj / "README.md").write_text(
    "Fallback for ChatGPT plans without native skills.\n\n"
    "1. Create a Project (or custom GPT). Paste INSTRUCTIONS.md into its instructions.\n"
    "2. Upload everything in knowledge/ as project files.\n"
    "3. If your plan has Code Interpreter or data analysis, ddos.py can run there. If not, the automatic checks DO NOT run. "
    "The assistant is told to walk the standards checklist by hand, which is weaker than the script.\n"
    "4. Chats may not share memory. Paste ledger.csv and context at the start of a session.\n"
    "5. One Project per hypothesis. Do not put two ideas in the same Project or its knowledge files.\n"
)
n = len(list((dist / "skills").glob("*.zip")))
print(f"built {n} skill zips and the ChatGPT project fallback in {dist}")
