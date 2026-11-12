#!/usr/bin/env python3
"""Check every solution against an independent brute-force reference.

    python lessons/verify.py                 all 150 problems
    python lessons/verify.py two-sum 3sum    only these
    python lessons/verify.py --cases 500     more random inputs per problem

``lessons/build.py`` proves each solution on a handful of hand-written tests.
This goes further: for every problem it generates many random inputs, runs the
exact code the lesson shows, and compares the answer with a slow but obviously
correct reference (or lets a judge decide when several answers are right).
"""

from __future__ import annotations

import argparse
import importlib
import json
import pkgutil
import random
import sys
import threading
import time
import traceback
import _thread
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lessons import build  # noqa: E402
from lessons.checks.kit import CHECKS, Ok  # noqa: E402
from lessons.engine import fmt  # noqa: E402
from lessons.engine.core import SOLUTION_FILE, CodeInfo  # noqa: E402
from lessons.engine.prelude import normalize  # noqa: E402
from lessons.engine.spec import LESSONS  # noqa: E402

TIME_LIMIT = 10.0  # seconds for one call; a correct solution needs milliseconds


def load_checks() -> None:
    import lessons.checks as checks

    for mod in sorted(pkgutil.iter_modules(checks.__path__), key=lambda m: m.name):
        if mod.name != "kit":
            importlib.import_module(f"lessons.checks.{mod.name}")


def solve(lesson, info, code_obj, call):
    """Run the lesson's solution once and return its (normalised) answer."""
    timer = threading.Timer(TIME_LIMIT, _thread.interrupt_main)
    timer.start()
    try:
        if isinstance(call, list):
            _, got, _ = build.run_design(lesson, code_obj, call)
        else:
            _, got, _ = build.run_function(lesson, info, code_obj, call)
    except KeyboardInterrupt:
        raise TimeoutError(f"no answer after {TIME_LIMIT:.0f} s (endless loop?)") from None
    finally:
        timer.cancel()
    return normalize(got)


def verdict(got, expected) -> str | None:
    """None when the answer is right, otherwise what is wrong."""
    if isinstance(expected, Ok):
        try:
            result = expected.judge(got)
        except Exception as exc:  # e.g. None where a list was expected
            return f"the answer has the wrong shape ({type(exc).__name__}: {exc})"
        if result is True or result is None:
            return None
        return result if isinstance(result, str) else (expected.note or "the judge rejected the answer")
    if build.same(got, expected, 0):
        return None
    return f"expected {fmt.leet(normalize(expected))}"


def verify(slug: str, entry: dict, cases: int | None, seed: str) -> tuple[int, list[str]]:
    lesson = LESSONS[slug]
    make, default_cases = CHECKS[slug]
    code = lesson.code or build.clean_solution((ROOT / entry["pythonPath"]).read_text(encoding="utf8"))
    info = CodeInfo(code)
    code_obj = compile(code, SOLUTION_FILE, "exec")
    failures: list[str] = []
    total = cases or default_cases
    for i in range(total):
        rng = random.Random(f"{seed}:{slug}:{i}")
        call, expected = make(rng)
        shown = " ; ".join(call) if isinstance(call, list) else call
        try:
            got = solve(lesson, info, code_obj, call)
        except Exception as exc:  # the solution crashed or hung
            failures.append(f"input {shown}\n       raised {type(exc).__name__}: {exc}")
        else:
            problem = verdict(got, expected)
            if problem:
                failures.append(f"input {shown}\n       got {fmt.leet(got)} - {problem}")
        if len(failures) >= 3:
            break
    return total, failures


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("slugs", nargs="*", help="only check these problems")
    parser.add_argument("--cases", type=int, default=None, help="random inputs per problem (default: per check)")
    parser.add_argument("--seed", default="neetcode", help="change it to draw different random inputs")
    parser.add_argument("--quiet", action="store_true")
    opts = parser.parse_args()

    catalog = json.loads(build.CATALOG.read_text(encoding="utf8"))
    entries = {p["slug"]: p for p in catalog["problems"]}
    build.load_specs()
    load_checks()

    unknown = [s for s in CHECKS if s not in entries]
    if unknown:
        print(f"checks for unknown problems: {unknown}")
        return 1
    wanted = opts.slugs or [p["slug"] for p in catalog["problems"]]
    missing = [s for s in wanted if s not in CHECKS]

    started = time.time()
    failed = 0
    ran = 0
    for slug in wanted:
        if slug not in CHECKS:
            continue
        try:
            total, failures = verify(slug, entries[slug], opts.cases, opts.seed)
        except Exception:
            print(f"FAIL {slug}: the check itself crashed\n{traceback.format_exc()}")
            failed += 1
            continue
        ran += total
        if failures:
            failed += 1
            print(f"FAIL {slug}")
            for text in failures:
                print(f"     {text[:1200]}")
        elif not opts.quiet:
            print(f"ok   {slug:58s} {total:4d} random inputs")

    print(f"\n{len(wanted) - len(missing) - failed}/{len(wanted)} solutions agree with their reference "
          f"on {ran} random inputs ({time.time() - started:.0f} s)")
    if missing:
        print(f"no check yet ({len(missing)}): {', '.join(missing[:20])}{' ...' if len(missing) > 20 else ''}")
    return 1 if failed or missing else 0


if __name__ == "__main__":
    sys.exit(main())
