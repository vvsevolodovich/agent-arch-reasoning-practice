"""
write_adr — Architecture Reasoning Agent tool

Writes a new ADR Markdown file to output/adrs/.
Content is read from a file whose path is passed as the third argument.

Usage:
    python skills/write_adr/write_adr.py <adr-id> <title> <content-file>

Example:
    python skills/write_adr/write_adr.py ADR-004 "Message Queue Selection" /tmp/adr_draft.md

The script:
  1. Reads the Markdown content from <content-file>.
  2. Validates that required ADR sections are present.
  3. Writes the file to output/adrs/<adr-id>-<slug>.md.
  4. Prints a JSON result with the saved path.
"""

import json
import re
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output" / "adrs"
REQUIRED_SECTIONS = ["Context", "Decision", "Consequences"]


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def write_adr(adr_id: str, title: str, content_file: str) -> dict:
    adr_id = adr_id.strip().upper()
    content_path = Path(content_file)
    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_file}")

    content = content_path.read_text()

    missing = [s for s in REQUIRED_SECTIONS if s not in content]
    if missing:
        raise ValueError(f"ADR is missing required sections: {missing}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{adr_id}-{slugify(title)}.md"
    out_path = OUTPUT_DIR / filename
    out_path.write_text(content)

    return {
        "saved": str(out_path.relative_to(Path(__file__).parent.parent.parent)),
        "adr_id": adr_id,
        "title": title,
        "sections_validated": REQUIRED_SECTIONS,
    }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python write_adr.py <adr-id> <title> <content-file>", file=sys.stderr)
        sys.exit(1)

    try:
        result = write_adr(sys.argv[1], sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
