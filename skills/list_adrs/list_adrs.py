"""
list_adrs — Architecture Reasoning Agent tool

Scans data/adrs/ and returns a JSON list of all ADRs with their ID, title,
date, status, and author (parsed from standard ADR front-matter).
"""

import json
import re
import sys
from pathlib import Path

ADR_DIR = Path(__file__).parent.parent.parent / "data" / "adrs"


def parse_adr_meta(path: Path) -> dict:
    text = path.read_text()
    lines = text.splitlines()

    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            break

    def field(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else ""

    adr_id = path.stem.split("-")[0] + "-" + path.stem.split("-")[1] if "-" in path.stem else path.stem
    return {
        "id": adr_id,
        "filename": path.name,
        "title": title,
        "date": field("Date"),
        "status": field("Status"),
        "author": field("Author"),
    }


def list_adrs() -> list[dict]:
    if not ADR_DIR.exists():
        return []
    adrs = sorted(ADR_DIR.glob("*.md"))
    return [parse_adr_meta(p) for p in adrs]


if __name__ == "__main__":
    result = list_adrs()
    print(json.dumps(result, indent=2))
