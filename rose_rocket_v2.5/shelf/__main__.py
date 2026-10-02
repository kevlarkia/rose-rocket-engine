"""Print the operator slate for America/Los_Angeles. Does not send."""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shelf.tools import day_slate, publication_today  # noqa: E402


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    day = date.fromisoformat(raw) if raw else publication_today()
    print(json.dumps(day_slate(day), indent=2))


if __name__ == "__main__":
    main()
