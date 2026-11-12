#!/usr/bin/env python3
"""Print a built lesson as plain text: one line per step plus what each view shows.

    python lessons/trace.py two-sum
    python lessons/trace.py two-sum --brief     captions only

Handy for proof-reading a lesson without opening the browser.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _tone(item: dict) -> str:
    return "/" + item["tone"] if item.get("tone") else ""


def describe(view: dict) -> str:
    kind = view["t"]
    head = f"{view['id']}"
    if kind == "array":
        cells = " ".join(c["v"] + _tone(c) for c in view["cells"])
        extra = ""
        if view.get("ptrs"):
            extra += "  ptrs " + ",".join(f"{p['name']}@{p['at']}" for p in view["ptrs"])
        if view.get("ranges"):
            extra += "  ranges " + ",".join(f"{r['from']}..{r['to']}" for r in view["ranges"])
        if view.get("pool"):
            extra += f"  pool {view['pool']}"
        return f"{head}: [{cells}]{extra}"
    if kind == "map":
        ents = ", ".join(e["k"] + (":" + e["v"] if "v" in e else "") + _tone(e) for e in view["entries"])
        return f"{head}: {{{ents}}}"
    if kind == "stack":
        return f"{head} ({view['kind']}): " + " | ".join(i["v"] + _tone(i) for i in view["items"])
    if kind == "vars":
        return "vars: " + ", ".join(f"{i['k']}={i['v']}" + ("*" if i.get("changed") else "") for i in view["items"])
    if kind == "items":
        return f"{head}: " + " ; ".join(i["v"] + _tone(i) for i in view["items"])
    if kind == "list":
        by_id = {n["id"]: n for n in view["nodes"]}
        nodes = " ".join(
            f"{n['v']}→{by_id[n['next']]['v'] if n.get('next') in by_id else '∅'}"
            + (f"~{by_id[n['rand']]['v']}" if n.get("rand") in by_id else "") + _tone(n)
            for n in view["nodes"]
        )
        ptrs = ",".join(f"{p['name']}@{by_id[p['at']]['v'] if p['at'] in by_id else 'None'}" for p in view.get("ptrs", []))
        return f"{head}: {nodes}" + (f"  ptrs {ptrs}" if ptrs else "")
    if kind == "tree":
        by_id = {n["id"]: n for n in view["nodes"]}

        def kids(n):
            if "kids" in n:
                return ",".join(by_id[k]["v"] for k in n["kids"] if k in by_id)
            left = by_id[n["l"]]["v"] if n.get("l") in by_id else "-"
            right = by_id[n["r"]]["v"] if n.get("r") in by_id else "-"
            return f"{left},{right}"

        nodes = " ".join(
            f"{n['v']}({kids(n)})" + _tone(n) + (f"={n['badge']}" if "badge" in n else "") + ("$" if n.get("end") else "")
            for n in view["nodes"]
        )
        ptrs = ",".join(f"{p['name']}@{by_id[p['at']]['v']}" for p in view.get("ptrs", []) if p["at"] in by_id)
        return f"{head}: {nodes}" + (f"  ptrs {ptrs}" if ptrs else "")
    if kind == "graph":
        nodes = " ".join(n["v"] + _tone(n) + (f"={n['badge']}" if "badge" in n else "") for n in view["nodes"])
        arrow = "→" if view.get("directed") else "—"
        edges = " ".join(f"{e['a']}{arrow}{e['b']}" + (f"({e['w']})" if "w" in e else "") + _tone(e) for e in view["edges"])
        return f"{head}: nodes {nodes} | edges {edges}"
    if kind == "grid":
        rows = " / ".join(" ".join((c["v"] or "·") + _tone(c) for c in row) for row in view["cells"])
        ptrs = ",".join(f"{p['name']}@({p['r']},{p['c']})" for p in view.get("ptrs", []))
        return f"{head}: {rows}" + (f"  ptrs {ptrs}" if ptrs else "")
    if kind == "intervals":
        rows = " | ".join(
            row["label"] + ": " + " ".join(f"[{i['a']},{i['b']}]" + _tone(i) for i in row["items"])
            for row in view["rows"]
        )
        return f"{head}: {rows}"
    if kind == "bits":
        return f"{head}: " + " | ".join(f"{r['label']}={r['bits']}({r['v']})" for r in view["rows"])
    if kind == "ops":
        return "ops: " + ", ".join(
            ("▶" if o["state"] == "cur" else "✓" if o["state"] == "done" else "·") + o["call"]
            + (f"→{o['ret']}" if "ret" in o else "")
            for o in view["items"]
        )
    return f"{head}: <{kind}>"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    brief = "--brief" in sys.argv
    for slug in args:
        doc = json.loads((ROOT / "content" / "lessons" / f"{slug}.json").read_text(encoding="utf8"))
        lines = doc["code"].split("\n")
        print(f"\n===== {doc['title']}  [{doc['difficulty']}]  {len(doc['steps'])} steps")
        print(f"Q: {doc['statement']}")
        print(f"example: {doc['example']['input']}  =>  {doc['example']['output']}   ({doc['example']['why']})")
        for i, step in enumerate(doc["steps"]):
            code = lines[step["line"] - 1].strip() if step["line"] else ""
            print(f"{i + 1:3d}. [{step['line']:>2}] {step['text']}")
            if not brief:
                if code:
                    print(f"        code: {code}")
                for view in step["views"]:
                    print(f"        {describe(view)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
