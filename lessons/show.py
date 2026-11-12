#!/usr/bin/env python3
"""Print the cleaned solution source for one or more problems (authoring aid).

    python lessons/show.py two-sum 3sum
    python lessons/show.py --category trees
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lessons.build import clean_solution  # noqa: E402


def main() -> int:
    catalog = json.loads((ROOT / "content" / "catalog.json").read_text(encoding="utf8"))
    args = sys.argv[1:]
    if args[:1] == ["--category"]:
        slugs = [p["slug"] for p in catalog["problems"] if p["category"] == args[1]]
    else:
        slugs = args
    entries = {p["slug"]: p for p in catalog["problems"]}
    for slug in slugs:
        entry = entries[slug]
        code = clean_solution((ROOT / entry["pythonPath"]).read_text(encoding="utf8"))
        print(f"\n######## {slug}  (#{entry['leetcodeNumber']} {entry['difficulty']})")
        for i, line in enumerate(code.split("\n"), 1):
            print(f"{i:3d}| {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
