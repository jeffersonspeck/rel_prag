"""Export the generated OpenAPI contract for external consumers."""

from __future__ import annotations

import json
from pathlib import Path

from epm.api import app

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "openapi.json"


def main() -> None:
    payload = json.dumps(app.openapi(), ensure_ascii=False, indent=2)
    # Stable LF endings keep the generated contract identical across platforms.
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(payload)
        stream.write("\n")
    print(f"OpenAPI exported to: {OUTPUT}")


if __name__ == "__main__":
    main()
