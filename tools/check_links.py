"""Check repository-relative Markdown file links; external links are research evidence."""

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
for path in ROOT.rglob("*.md"):
    if any(
        part in {".git", ".venv", ".mypy_cache", ".ruff_cache", "build", "dist"}
        for part in path.relative_to(ROOT).parts
    ):
        continue
    for match in re.finditer(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", path.read_text()):
        target = match.group(1).strip("<>")
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        filename = unquote(target.split("#", 1)[0])
        if not (path.parent / filename).exists():
            errors.append(f"{path.relative_to(ROOT)}: missing {target}")
if errors:
    raise SystemExit("\n".join(errors))
print("Repository Markdown file links passed (external links and anchors not checked).")
