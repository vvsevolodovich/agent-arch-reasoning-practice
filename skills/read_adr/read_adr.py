"""
read_adr — Architecture Reasoning Agent tool

Reads a single ADR by ID prefix (e.g. "ADR-001") and returns its full content
as a JSON object with id, filename, and body.

Usage:
    python skills/read_adr/read_adr.py ADR-001
"""

import json
import sys
from pathlib import Path

ADR_DIR = Path(__file__).parent.parent.parent / "data" / "adrs"


def read_adr(adr_id: str) -> dict:
    adr_id = adr_id.strip().upper()
    matches = list(ADR_DIR.glob(f"{adr_id}*.md"))
    if not matches:
        raise FileNotFoundError(f"No ADR found matching '{adr_id}' in {ADR_DIR}")
    path = sorted(matches)[0]
    return {
        "id": adr_id,
        "filename": path.name,
        "body": path.read_text(),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_adr.py <ADR-ID>", file=sys.stderr)
        print("Example: python read_adr.py ADR-001", file=sys.stderr)
        sys.exit(1)

    try:
        result = read_adr(sys.argv[1])
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
