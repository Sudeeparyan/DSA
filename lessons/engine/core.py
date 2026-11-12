"""The recorder: runs a real solution under `sys.settrace` and turns the
execution into teaching steps.

How a step is produced
----------------------
A lesson attaches *notes* to lines of the solution (matched by their text).
While the solution runs we watch every line:

* a note's ``post`` text is emitted right after its line finishes, so the
  picture already shows the line's effect;
* ``yes`` / ``no`` texts are chosen by whether an ``if`` / ``while`` / ``for``
  line entered its body;
* ``pre`` is emitted just before the line runs (handy before a recursive call);
* a note on a ``def`` line fires each time that function is called, and its
  ``ret`` text fires when the call returns.

Every step stores the caption plus a snapshot of each view (array, tree, ...).
Because the snapshots come from the live Python objects, the animation cannot
drift from what the code really does.
"""

from __future__ import annotations

import ast
import copy
import math
import sys
from collections import deque

from . import fmt
from .prelude import REG, list_vals, tree_vals

SOLUTION_FILE = "<solution>"
MISSING = object()
TONES = {"cur", "alt", "good", "bad", "seen", "dim", "win", "mark"}


class LessonError(Exception):
    """A lesson spec is wrong (bad anchor, broken caption, wrong answer...)."""


class NS:
    """Attribute access over a dict, e.g. ``was.count`` inside captions."""

    def __init__(self, data: dict):
        object.__setattr__(self, "_d", data)

    def __getattr__(self, name):
        try:
            return self._d[name]
        except KeyError:
            raise AttributeError(name) from None

    def __getitem__(self, name):
        return self._d[name]

    def __contains__(self, name):
        return name in self._d


# --------------------------------------------------------------------------
# Static analysis of the solution source
# --------------------------------------------------------------------------


class CodeInfo:
    def __init__(self, code: str):
        self.source = code
        self.lines = code.split("\n")
        tree = ast.parse(code)
        self.stmt_start: dict[int, int] = {}
        self.body: dict[int, tuple[int, int]] = {}
        self.oneliner: set[int] = set()
        self.defs: dict[int, str] = {}
        self.for_vars: dict[int, list[str]] = {}
        self.classes: list[str] = []
        self.methods: dict[str, list[str]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.classes.append(node.name)
                self.methods[node.name] = [
                    n.name for n in node.body if isinstance(n, ast.FunctionDef)
                ]
            if not isinstance(node, ast.stmt):
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.defs[node.lineno] = node.name
            body = getattr(node, "body", None)
            if isinstance(body, list) and body and isinstance(body[0], ast.stmt):
                first = body[0].lineno
                if first == node.lineno:
                    self.oneliner.add(node.lineno)
                    self.stmt_start[node.lineno] = node.lineno
                else:
                    for ln in range(node.lineno, first):
                        self.stmt_start[ln] = node.lineno
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    self.body[node.lineno] = (first, body[-1].end_lineno or first)
                if isinstance(node, ast.For):
                    self.for_vars[node.lineno] = [
                        n.id for n in ast.walk(node.target) if isinstance(n, ast.Name)
                    ]
            else:
                for ln in range(node.lineno, (node.end_lineno or node.lineno) + 1):
                    self.stmt_start[ln] = node.lineno
        # ast.walk is breadth-first, so nested simple statements were written
        # last and win over the compound header that contains them.
        self.classes.sort(key=lambda name: self._class_line(tree, name))

    @staticmethod
    def _class_line(tree, name) -> int:
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == name:
                return node.lineno
        return 10**9

    def stmt(self, line: int) -> int:
        return self.stmt_start.get(line, line)

    def find(self, anchor: str) -> int:
        """Line number (1-based) of the statement whose text matches `anchor`."""
        nth = None
        text = anchor
        if "@" in anchor:
            head, _, tail = anchor.rpartition("@")
            if tail.isdigit():
                text, nth = head, int(tail)
        hits = [i + 1 for i, ln in enumerate(self.lines) if ln.strip().startswith(text)]
        if not hits:
            hits = [
                i + 1
                for i, ln in enumerate(self.lines)
                if text in ln and not ln.strip().startswith("#")
            ]
        if not hits:
            raise LessonError(f"anchor not found in code: {anchor!r}")
        if nth is None:
            if len(hits) > 1:
                raise LessonError(
                    f"anchor {anchor!r} matches lines {hits}; make it longer or add @N"
                )
            nth = 1
        if nth > len(hits):
            raise LessonError(f"anchor {anchor!r} has only {len(hits)} matches")
        return self.stmt(hits[nth - 1])


# --------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------

_NOTE_KEYS = {
    "post", "pre", "yes", "no", "ret", "when", "first",
    "marks", "yes_marks", "no_marks", "pre_marks", "ret_marks", "save",
}


def parse_marks(marks) -> dict[str, list[tuple[str, object]]]:
    """{"nums.good": expr} -> {"nums": [("good", expr)]}"""
    out: dict[str, list[tuple[str, object]]] = {}
    for key, expr in (marks or {}).items():
        view_id, _, tone = key.rpartition(".")
        if not view_id:
            raise LessonError(f"mark key must look like 'view.tone': {key!r}")
        out.setdefault(view_id, []).append((tone, expr))
    return out


class Note:
    def __init__(self, anchor: str, spec, marks=None):
        self.anchor = anchor
        self.post = self.pre = self.yes = self.no = self.ret = None
        self.when = None
        self.first = None
        self.save = None
        self.marks = self.yes_marks = self.no_marks = self.pre_marks = self.ret_marks = None
        self.line = 0
        self.fired = 0
        if isinstance(spec, dict):
            unknown = set(spec) - _NOTE_KEYS
            if unknown:
                raise LessonError(f"note {anchor!r}: unknown keys {sorted(unknown)}")
            for key, value in spec.items():
                setattr(self, key, value)
        else:
            self.post = spec
        if marks is not None:
            self.marks = marks
        for key in ("marks", "yes_marks", "no_marks", "pre_marks", "ret_marks"):
            setattr(self, key, parse_marks(getattr(self, key)))


# --------------------------------------------------------------------------
# Caption templates:  "text {expression} more text"
# --------------------------------------------------------------------------


def _caption_str(value) -> str:
    if isinstance(value, float) and math.isinf(value):
        return "∞" if value > 0 else "-∞"
    return str(value)


def _split_field(field: str) -> tuple[str, str | None, str]:
    """Split an f-string field into (expression, conversion, format spec)."""
    depth = 0
    quote = None
    i = 0
    n = len(field)
    while i < n:
        ch = field[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0 and ch == "!" and i + 1 < n and field[i + 1] in "rsa" and (
            i + 2 == n or field[i + 2] == ":"
        ):
            return field[:i], field[i + 1], field[i + 3 :] if i + 2 < n else ""
        elif depth == 0 and ch == ":":
            return field[:i], None, field[i + 1 :]
        i += 1
    return field, None, ""


def render_template(template: str, env: dict, where: str) -> str:
    out: list[str] = []
    i = 0
    n = len(template)
    while i < n:
        ch = template[i]
        if ch == "{":
            if i + 1 < n and template[i + 1] == "{":
                out.append("{")
                i += 2
                continue
            depth = 1
            quote = None
            j = i + 1
            while j < n:
                c = template[j]
                if quote:
                    if c == "\\":
                        j += 1
                    elif c == quote:
                        quote = None
                elif c in "\"'":
                    quote = c
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if depth != 0:
                raise LessonError(f"{where}: unbalanced '{{' in caption {template!r}")
            expr, conv, spec = _split_field(template[i + 1 : j])
            try:
                value = eval(expr, env)  # noqa: S307 - trusted lesson source
            except Exception as exc:  # pragma: no cover - reported to the author
                raise LessonError(
                    f"{where}: caption expression {{{expr}}} failed: {exc!r}"
                ) from exc
            if conv == "r":
                value = repr(value)
            elif conv == "s":
                value = str(value)
            out.append(format(value, spec) if spec else _caption_str(value))
            i = j + 1
        elif ch == "}":
            if i + 1 < n and template[i + 1] == "}":
                out.append("}")
                i += 2
                continue
            raise LessonError(f"{where}: single '}}' in caption {template!r}")
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def safe_copy(value, depth: int = 0):
    """Copy plain data so `was.x` shows the value before a line ran."""
    if isinstance(value, (int, float, str, bool, type(None), bytes, frozenset)):
        return value
    if depth > 4:
        return value
    if isinstance(value, list):
        return [safe_copy(v, depth + 1) for v in value]
    if isinstance(value, tuple):
        return tuple(safe_copy(v, depth + 1) for v in value)
    if isinstance(value, deque):
        return deque(safe_copy(v, depth + 1) for v in value)
    if isinstance(value, set):
        return set(value)
    if isinstance(value, dict):
        try:
            clone = copy.copy(value)
            for key in list(clone.keys()):
                clone[key] = safe_copy(clone[key], depth + 1)
            return clone
        except Exception:
            return value
    return value


def _nv(node) -> str:
    """'node 3' / 'None' - how captions name a list or tree node."""
    return "None" if node is None else f"node {fmt.cell(getattr(node, 'val', node))}"


def _chain(head) -> list:
    """Every linked-list node reachable from `head`."""
    out, seen = [], set()
    while head is not None and id(head) not in seen:
        seen.add(id(head))
        out.append(head)
        head = getattr(head, "next", None)
    return out


def _subtree(root) -> list:
    """Every tree node in the subtree rooted at `root`."""
    out, todo = [], [root]
    while todo:
        node = todo.pop()
        if node is None:
            continue
        out.append(node)
        todo.append(getattr(node, "right", None))
        todo.append(getattr(node, "left", None))
    return out


def _span(first, last) -> list:
    """Linked-list nodes from `first` up to and including `last`."""
    out = []
    for node in _chain(first):
        out.append(node)
        if node is last:
            return out
    return out if last is None else []


HELPERS = {
    "nv": _nv,
    "chain": _chain,
    "span": _span,
    "nodes": lambda: list(REG.lists),
    "subtree": _subtree,
    "show": fmt.show,
    "cell": fmt.cell,
    "plural": fmt.plural,
    "ordinal": fmt.ordinal,
    "binary": fmt.bits,
    "lv": list_vals,
    "tv": tree_vals,
    "inf": math.inf,
}


# --------------------------------------------------------------------------
# Recorder
# --------------------------------------------------------------------------


class FrameInfo:
    __slots__ = ("frame", "name", "pending", "call", "loops", "ended")

    def __init__(self, frame, name, call):
        self.frame = frame
        self.name = name
        self.pending = None
        self.call = call
        self.loops: dict[int, int] = {}  # for-line -> index of the current iteration
        self.ended: set[int] = set()  # for-lines whose loop has run out


class Call:
    """One traced function call (used for call stacks and recursion trees)."""

    __slots__ = ("id", "fn", "parent", "args", "ret", "done", "depth", "data")

    def __init__(self, id_, fn, parent, args, depth):
        self.id = id_
        self.fn = fn
        self.parent = parent
        self.args = args
        self.ret = None
        self.done = False
        self.depth = depth
        self.data: dict = {}


class Ctx:
    """What a view sees while it draws one step."""

    def __init__(self, rec: "Recorder", env: dict, marks: dict):
        self.rec = rec
        self.env = env
        self.marks = marks  # view id -> [(tone, expr)]

    def ev(self, expr, default=None):
        if expr is None:
            return default
        try:
            if callable(expr):
                return expr(NS(self.env))
            return eval(expr, self.env)  # noqa: S307 - trusted lesson source
        except Exception:
            return default

    def fmt(self, template: str, default: str = "") -> str:
        try:
            return render_template(template, self.env, "view")
        except LessonError:
            return default

    @staticmethod
    def uid(obj) -> int:
        return REG.uid(obj)

    def extra(self, view_id: str) -> list:
        return self.marks.get(view_id, [])


class Recorder:
    def __init__(self, lesson, info: CodeInfo, ns: dict, max_steps: int = 120):
        self.lesson = lesson
        self.code = info
        self.ns = ns
        self.max_steps = max_steps
        self.frames: list[FrameInfo] = []
        self.calls: list[Call] = []
        self.steps: list[dict] = []
        self.base_scope: dict = {}
        self.result = None
        self.ops: list[dict] = []  # design lessons: [{call, ret, state}]
        self.op_index = -1
        self.saved: dict = {}  # values remembered by `init=` / note `save=`
        self.args: dict = {}  # copy of the original arguments
        self._ret_captioned = False
        self._final_marks: dict | None = None
        self._anchor_lines: dict[str, int] = {}
        for name, expr in (lesson.init or {}).items():
            try:  # constants work now; anything using the arguments waits for the call
                self.saved[name] = eval(expr, {**ns, **HELPERS})  # noqa: S307 - trusted
            except Exception:
                pass
        self.views = list(lesson.views)
        for view in self.views:
            view.reset()
        self.notes: dict[int, Note] = {}
        self.def_notes: dict[int, Note] = {}
        for note in lesson.build_notes():
            line = info.find(note.anchor)
            note.line = line
            target = self.def_notes if line in info.defs else self.notes
            if line in target:
                raise LessonError(f"two notes on line {line}: {note.anchor!r}")
            if (note.yes is not None or note.no is not None) and (
                line not in info.body or line in info.oneliner
            ):
                raise LessonError(
                    f"note {note.anchor!r}: yes/no needs a multi-line if/while/for"
                )
            target[line] = note

    # -- tracing ----------------------------------------------------------

    def start(self) -> None:
        sys.settrace(self._global_trace)

    @staticmethod
    def stop() -> None:
        sys.settrace(None)

    def _global_trace(self, frame, event, arg):
        if event != "call":
            return None
        code = frame.f_code
        if code.co_filename != SOLUTION_FILE or code.co_name.startswith("<"):
            return None
        self._on_call(frame)
        return self._local_trace

    def _local_trace(self, frame, event, arg):
        if event == "line":
            self._on_line(frame)
        elif event == "return":
            self._on_return(frame, arg)
        return self._local_trace

    def _on_call(self, frame) -> None:
        code = frame.f_code
        parent = self.frames[-1].call if self.frames else None
        call = Call(len(self.calls), code.co_name, parent, dict(frame.f_locals), len(self.frames))
        self.calls.append(call)
        self.frames.append(FrameInfo(frame, code.co_name, call))
        if self.views:
            ctx = Ctx(self, self._env(), {})
            for view in self.views:
                view.on_call(ctx, call)
        line = code.co_firstlineno
        if len(self.frames) == 1 and not self.lesson.is_design:
            self.args = {k: safe_copy(v) for k, v in frame.f_locals.items() if k != "self"}
            for name, expr in (self.lesson.init or {}).items():
                self.saved.pop(name, None)
                self.saved[name] = eval(expr, self._env())  # noqa: S307 - trusted
            self._emit(line, self.lesson.intro_text(), where="intro")
        note = self.def_notes.get(line)
        if note is not None and (note.post or note.pre):
            self._emit(line, note.post or note.pre, note, marks=note.pre_marks or note.marks)

    def _on_line(self, frame) -> None:
        info = self.frames[-1]
        if info.frame is not frame:
            return
        line = self.code.stmt(frame.f_lineno)
        prev = info.pending[0] if info.pending is not None else None
        if prev == line and (line not in self.code.body or frame.f_lineno != line):
            return  # another physical line of the same statement
        if line in self.code.for_vars:
            first, last = self.code.body[line]
            if prev is None or not first <= prev <= last:
                info.loops[line] = -1  # the loop is starting afresh, not looping back
                info.ended.discard(line)
        self._finish(info, line)
        note = self.notes.get(line)
        info.pending = (line, self._snapshot() if note is not None else None)
        if note is not None and note.pre:
            self._emit(line, note.pre, note, marks=note.pre_marks or note.marks)

    def _finish(self, info: FrameInfo, next_line, ret=MISSING) -> None:
        pending = info.pending
        if pending is None:
            return
        info.pending = None
        line, before = pending
        took = False
        if line in self.code.body:
            first, last = self.code.body[line]
            took = next_line is not None and first <= next_line <= last
            if line in self.code.for_vars:
                # i_<var> counts iterations; once the loop is exhausted it stays
                # one past the end, so "everything is processed" remains visible
                info.loops[line] = info.loops.get(line, -1) + 1
                if not took:
                    info.ended.add(line)
        note = self.notes.get(line)
        if note is None:
            return
        if note.save:
            env = self._env(before, ret)
            for name, expr in note.save.items():
                self.saved[name] = eval(expr, env)  # noqa: S307 - trusted lesson source
            if not (note.post or note.yes or note.no):
                note.fired += 1  # a note that only remembers a value still did its job
        template, marks = note.post, note.marks
        if note.yes is not None or note.no is not None:
            template = note.yes if took else note.no
            marks = (note.yes_marks if took else note.no_marks) or note.marks
        if template:
            if ret is not MISSING and len(self.frames) == 1:
                self._ret_captioned = True
                self._final_marks = marks  # keep the answer highlighted on the last step
            self._emit(line, template, note, before=before, ret=ret, marks=marks)

    def _on_return(self, frame, arg) -> None:
        info = self.frames[-1]
        if info.frame is not frame:
            return
        last_line = self.code.stmt(frame.f_lineno)
        self._finish(info, None, ret=arg)
        call = info.call
        call.ret = arg
        call.done = True
        if self.views:
            ctx = Ctx(self, self._env(ret=arg), {})
            for view in self.views:
                view.on_return(ctx, call)
        note = self.def_notes.get(frame.f_code.co_firstlineno)
        if note is not None and note.ret:
            self._emit(last_line, note.ret, note, ret=arg, marks=note.ret_marks or note.marks)
        if len(self.frames) == 1 and not self.lesson.is_design:
            self.result = arg
            marks = parse_marks(self.lesson.final) if self.lesson.final else self._final_marks
            self._emit(last_line, self.lesson.outro_text(), ret=arg, where="outro",
                       final=True, marks=marks)
        self.frames.pop()

    # -- design lessons (a list of method calls) ---------------------------

    def begin_op(self, label: str, obj) -> None:
        self.op_index += 1
        if self.op_index < len(self.ops):
            self.ops[self.op_index]["state"] = "cur"
        else:
            self.ops.append({"call": label, "state": "cur"})
        self.base_scope = {"self": obj} if obj is not None else {}
        self._ret_captioned = False
        self._emit(0, "Call **`{_op}`**.", where="op")

    def end_op(self, obj, result) -> None:
        op = self.ops[self.op_index]
        op["state"] = "done"
        self.base_scope = {"self": obj} if obj is not None else {}
        if result is not None:
            op["ret"] = fmt.show(result)
            if not self._ret_captioned:
                self._emit(0, "**`{_op}`** returns **`{show(_ret)}`**.", ret=result, where="op")
            elif self.steps:
                # the lesson already explained this return: just refresh its op list
                for view in self.steps[-1]["views"]:
                    if view.get("t") == "ops":
                        view["items"] = [dict(o) for o in self.ops]

    def finish_design(self, obj, outputs) -> None:
        self.base_scope = {"self": obj} if obj is not None else {}
        self.result = outputs
        self._emit(0, self.lesson.outro_text(), ret=outputs, where="outro", final=True)

    # -- emitting ---------------------------------------------------------

    def _scope(self) -> dict:
        scope = dict(self.base_scope)
        for info in self.frames:
            scope.update(info.frame.f_locals)
            # `for x in xs` has no index variable, so expose one as `i_x`
            for line, index in info.loops.items():
                for name in self.code.for_vars.get(line, ()):
                    scope["i_" + name] = index
        return scope

    def _snapshot(self) -> dict:
        return {k: safe_copy(v) for k, v in self._scope().items()}

    def _env(self, before=None, ret=MISSING) -> dict:
        env = dict(self.ns)
        env.update(HELPERS)
        env.update(self._scope())
        env["was"] = NS(before if before is not None else {})
        env["_ret"] = None if ret is MISSING else ret
        env["_depth"] = len(self.frames)
        env["_op"] = self.ops[self.op_index]["call"] if 0 <= self.op_index < len(self.ops) else ""
        env["_result"] = self.result
        env["_args"] = self.args
        env["_done"] = self._done
        env["at"] = self._loop_at
        env["upto"] = self._loop_upto
        env.update(self.saved)
        return env

    def _loop_state(self, anchor: str):
        line = self._anchor_lines.get(anchor)
        if line is None:
            line = self._anchor_lines[anchor] = self.code.find(anchor)
            if line not in self.code.for_vars:
                raise LessonError(f"at()/upto(): {anchor!r} is not a for loop")
        for info in reversed(self.frames):
            if line in info.loops:
                return info.loops[line], line in info.ended
        return None, False

    def _loop_at(self, anchor: str):
        """Index of the item a `for` loop is on right now (None before / after it)."""
        index, ended = self._loop_state(anchor)
        return None if ended or index is None or index < 0 else index

    def _loop_upto(self, anchor: str) -> int:
        """How many items of a `for` loop are already behind us."""
        index, _ = self._loop_state(anchor)
        return 0 if index is None or index < 0 else index

    def _done(self, fn: str, arg: str) -> list:
        """Argument `arg` of every finished call of `fn` (e.g. nodes fully processed)."""
        return [c.args.get(arg) for c in self.calls if c.fn == fn and c.done]

    def _emit(self, line, template, note=None, before=None, ret=MISSING,
              marks=None, where=None, final=False) -> None:
        where = where or (f"note {note.anchor!r}" if note else "step")
        env = self._env(before, ret)
        if note is not None and note.when is not None:
            try:
                if callable(note.when):
                    ok = note.when(NS(env))
                else:
                    ok = eval(note.when, env)  # noqa: S307
            except Exception as exc:
                raise LessonError(f"{where}: when= failed: {exc!r}") from exc
            if not ok:
                return
        if isinstance(template, (list, tuple)):
            # [(condition, text), ...]: the first condition that holds picks the text
            chosen = None
            for cond, candidate in template:
                try:
                    ok = cond is None or cond is True or bool(eval(cond, env))  # noqa: S307
                except Exception as exc:
                    raise LessonError(f"{where}: condition {cond!r} failed: {exc!r}") from exc
                if ok:
                    chosen = candidate
                    break
            if chosen is None:
                return
            template = chosen
        if callable(template):
            text = template(NS(env))
        else:
            text = render_template(template, env, where)
        if not text or not text.strip():
            return
        if note is not None:
            note.fired += 1
            if note.first is not None and note.fired > note.first:
                return
        ctx = Ctx(self, env, marks or {})
        views = []
        for view in self.views:
            data = view.render(ctx)
            if data is not None:
                views.append(data)
        if self.lesson.is_design:
            views.append({"t": "ops", "id": "ops", "items": [dict(op) for op in self.ops]})
        step = {"line": int(line), "text": " ".join(text.split()), "views": views}
        if final:
            step["final"] = True
        self.steps.append(step)
        if len(self.steps) > self.max_steps:
            raise LessonError(
                f"more than {self.max_steps} steps - use a smaller example or fewer notes"
            )

    def unused_notes(self) -> list[str]:
        notes = list(self.notes.values()) + list(self.def_notes.values())
        return [n.anchor for n in notes if n.fired == 0]
