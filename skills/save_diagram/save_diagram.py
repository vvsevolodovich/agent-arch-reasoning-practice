"""
save_diagram — Architecture Reasoning Agent tool

Saves a Mermaid diagram to output/diagrams/.
The diagram content is read from a file whose path is passed as the second argument.

Usage:
    python skills/save_diagram/save_diagram.py <diagram-name> <content-file>

Example:
    python skills/save_diagram/save_diagram.py proposed-architecture /tmp/diagram.mmd

The script:
  1. Reads Mermaid content from <content-file>.
  2. Does a basic sanity check (must contain 'graph' or 'flowchart' or 'sequenceDiagram').
  3. Writes to output/diagrams/<diagram-name>.mmd.
  4. Prints a JSON result with the saved path and line count.
"""

import json
import re
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output" / "diagrams"
VALID_DIAGRAM_TYPES = ["graph", "flowchart", "sequenceDiagram", "classDiagram", "erDiagram"]


def save_diagram(name: str, content_file: str) -> dict:
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", name).strip("-")
    content_path = Path(content_file)
    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_file}")

    content = content_path.read_text()

    has_valid_type = any(t in content for t in VALID_DIAGRAM_TYPES)
    if not has_valid_type:
        raise ValueError(
            f"Diagram does not appear to be valid Mermaid. "
            f"Expected one of: {VALID_DIAGRAM_TYPES}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mmd"
    out_path.write_text(content)

    return {
        "saved": str(out_path.relative_to(Path(__file__).parent.parent.parent)),
        "name": name,
        "lines": len(content.splitlines()),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_diagram.py <diagram-name> <content-file>", file=sys.stderr)
        sys.exit(1)

    try:
        result = save_diagram(sys.argv[1], sys.argv[2])
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
