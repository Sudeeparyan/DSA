"""Lesson declarations.

A lesson file calls ``lesson("two-sum", ...)`` once per problem.  Everything a
learner sees comes from that call plus the solution source in ``solutions/``.
"""

from __future__ import annotations

import textwrap

from . import fmt
from .core import MISSING, LessonError, Note
from .prelude import normalize

LESSONS: dict[str, "Lesson"] = {}


class Lesson:
    def __init__(
        self,
        slug: str,
        *,
        statement: str,
        idea: list[str],
        time: tuple[str, str],
        space: tuple[str, str],
        views: list,
        notes: list,
        args: str | None = None,
        expected=MISSING,
        why: str = "",
        ops: list[str] | None = None,
        code: str | None = None,
        pre: str | None = None,
        cls: str | None = None,
        method: str | None = None,
        result: str | None = None,
        unordered: int = 0,
        tests: list | tuple = (),
        pattern: str | None = None,
        intro: str | None = None,
        outro: str | None = None,
        max_steps: int = 120,
        allow_unused: bool = False,
        show_input: str | None = None,
        show_output: str | None = None,
        init: dict | None = None,
        final: dict | None = None,
    ):
        if slug in LESSONS:
            raise LessonError(f"duplicate lesson {slug!r}")
        if (args is None) == (ops is None):
            raise LessonError(f"{slug}: give exactly one of args= or ops=")
        if expected is MISSING:
            raise LessonError(f"{slug}: expected= is required")
        self.slug = slug
        self.statement = " ".join(statement.split())
        self.idea = [" ".join(i.split()) for i in idea]
        self.time = time
        self.space = space
        self.views = views
        self.notes = notes
        self.args = args
        self.expected = expected
        self.why = " ".join(why.split())
        self.ops = ops
        self.code = textwrap.dedent(code).strip("\n") if code else None
        self.pre = textwrap.dedent(pre) if pre else None
        self.cls = cls
        self.method = method
        self.result = result
        self.unordered = unordered
        self.tests = list(tests)
        self.pattern = pattern
        self.intro = intro
        self.outro = outro
        self.max_steps = max_steps
        self.allow_unused = allow_unused
        self.show_input = show_input
        self.show_output = show_output
        self.init = init
        self.final = final  # marks for the closing step, e.g. {"nums.good": "[0, 3]"}
        # filled in by the builder
        self.input_text = ""
        self.output_text = ""
        ids = [v.id for v in views]
        if len(ids) != len(set(ids)):
            raise LessonError(f"{slug}: duplicate view ids {ids}")
        LESSONS[slug] = self

    @property
    def is_design(self) -> bool:
        return self.ops is not None

    def build_notes(self) -> list[Note]:
        out = []
        for item in self.notes:
            if len(item) == 2:
                out.append(Note(item[0], item[1]))
            elif len(item) == 3:
                out.append(Note(item[0], item[1], item[2]))
            else:
                raise LessonError(f"{self.slug}: bad note {item!r}")
        return out

    # captions for the automatic first and last steps -----------------------

    def intro_text(self):
        if self.intro:
            return self.intro
        if len(self.input_text) > 64 or "\n" in self.input_text:
            text = (
                "Our example input is drawn on the stage. "
                "Each step runs one highlighted line of the code."
            )
        else:
            text = (
                f"Our example: **`{self.input_text}`**. "
                "Each step runs one highlighted line of the code."
            )
        return lambda env: text

    def final_value(self, env):
        if self.result:
            scope = dict(env._d)
            return eval(self.result, scope)  # noqa: S307 - trusted lesson source
        return env._ret

    def outro_text(self):
        if self.outro:
            return self.outro
        why = f" {self.why}" if self.why else ""
        if self.is_design:
            return lambda env: f"All the calls are done.{why}"
        return lambda env: (
            f"Done — the answer is **`{fmt.leet(normalize(self.final_value(env)))}`**.{why}"
        )


def lesson(slug: str, **kwargs) -> Lesson:
    return Lesson(slug, **kwargs)
