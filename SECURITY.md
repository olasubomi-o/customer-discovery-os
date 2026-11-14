# Security and privacy

## Reporting an issue
Open a private security advisory on the GitHub repository, or email the maintainer through the contact on theproductbuilders.com. Please do not post exploit details publicly before there is a fix.

## What to report
- The helper script (`ddos.py`) or hook writing, reading or deleting files outside the `discovery/` folder.
- A way for interview content to leak into public output or into another hypothesis folder.
- Redaction that exposes personal data it claims to remove.

## What this project does not promise
- Redaction removes emails, phone numbers and names you list. It does not detect names automatically. Review ingested files.
- Interview material is personal data. `interviews/`, `extractions/`, `synthesis/`, `voc/` and `ledger.csv` are git-ignored by default. Keep them out of public repositories.
- The hook and checker are stdlib Python and make no network calls. The `market-scan` skill uses your assistant's own web tools.
