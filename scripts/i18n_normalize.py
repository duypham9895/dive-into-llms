#!/usr/bin/env python3
"""Normalise Markdown so MkDocs (Python-Markdown) renders the same block structure
that markdown-it-py (CommonMark, used by the validator) parses.

Upstream READMEs are written for GitHub's renderer. Python-Markdown needs 4 spaces per
list level and a blank line before a list, so 8 of the 12 READMEs lose list items or
code blocks when built as-is. These rules fix that without touching any content:

  1. A list that starts after a non-list line gets a blank line before it.
  2. List nesting is re-indented to 4 spaces per level; each item's indented
     continuation lines (code bodies included) move with it.
  3. A fence opened on a bullet line ("  - ```sh") loses its bullet; the fence becomes
     content of the parent item, at the parent's content indent.
  4. A fence that closes inside a list is followed by a blank line, so the next
     unindented block is not swallowed into the last item.
  5. A block that CommonMark lets interrupt a list (fence, heading, blockquote, HTML,
     table) and that sits left of the item's content gets a blank line before it;
     Python-Markdown would otherwise read it as lazy text of the last item.
  6. A closing fence is aligned with its opening fence. CommonMark accepts a closer
     indented up to 3 columns; pymdownx.superfences does not, and then swallows the
     rest of the page into one code block (ch3 opens at column 0, closes at 2).

Code inside fences is never edited apart from the uniform indent shift of rules 2-3.
Both the source and the translation go through the same function, so the validator
compares like with like.

Usage: i18n_normalize.py FILE [FILE ...]   (writes the result to stdout)
       i18n_normalize.py --in-place FILE ...
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ITEM = re.compile(r"^( *)([-*+]|\d{1,9}[.)])( +)(.*)$")
THEMATIC_BREAK = re.compile(r"^ {0,3}([-*_])( *\1){2,} *$")
FENCE_OPEN = re.compile(r"^( *)(`{3,}|~{3,})(.*)$")
INTERRUPTING_BLOCK = re.compile(r"^ {0,3}(#{1,6}(\s|$)|>|<[A-Za-z!/]|\|)")
TAB = 4


@dataclass(frozen=True)
class Item:
    marker_col: int   # column of the list marker in the source
    content_col: int  # column where the item's content starts in the source
    level: int        # nesting level, 0 = top

    @property
    def new_content_col(self) -> int:
        """Where Python-Markdown expects this item's content: 4 columns per level."""
        return TAB * (self.level + 1)

    @property
    def shift(self) -> int:
        """Columns to add to this item's paragraph-continuation lines."""
        return self.new_content_col - self.content_col


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _shift(line: str, delta: int) -> str:
    if not line.strip() or delta == 0:
        return line
    if delta > 0:
        return " " * delta + line
    return line[min(-delta, _indent(line)):]


def _closes(line: str, char: str, length: int) -> bool:
    m = FENCE_OPEN.match(line)
    return bool(m) and m.group(2)[0] == char and len(m.group(2)) >= length and not m.group(3).strip()


def normalize(text: str) -> str:
    """Return text with rules 1-4 applied. normalize(normalize(x)) == normalize(x)."""
    out: list[str] = []
    stack: list[Item] = []
    # While inside a fence: (char, length, body shift, column of the emitted opener)
    fence: tuple[str, int, int, int] | None = None
    prev = "blank"  # blank | item | text
    block_delta = 0  # shift applied to the first line of the current block
    pending_blank = False  # rule 4: a fence closed inside a list

    for raw in text.split("\n"):
        line = raw.expandtabs(TAB)

        if fence is not None:
            char, length, delta, opener_col = fence
            if _closes(line, char, length):
                out.append(" " * opener_col + line.strip())  # rule 6
                fence = None
                pending_blank = bool(stack)
                prev = "text"
            else:
                out.append(_shift(line, delta))
            continue

        if not line.strip():
            out.append("")
            prev = "blank"
            pending_blank = False
            continue

        if pending_blank:  # rule 4
            out.append("")
            prev = "blank"
            pending_blank = False

        indent = _indent(line)
        item = None if THEMATIC_BREAK.match(line) else ITEM.match(line)

        if item:
            marker_col = len(item.group(1))
            marker = item.group(2)
            content_col = marker_col + len(marker) + min(len(item.group(3)), 4)
            rest = item.group(4)
            while stack and marker_col < stack[-1].content_col:
                stack.pop()
            level = len(stack)

            fopen = FENCE_OPEN.match(rest)
            if fopen:  # rule 3: drop the bullet, keep the fence under the parent item
                new_col = TAB * level
                if prev != "blank":
                    out.append("")
                out.append(" " * new_col + rest)
                fence = (fopen.group(2)[0], len(fopen.group(2)), new_col - content_col, new_col)
                prev = "text"
                continue

            if prev == "text" and not stack:  # rule 1
                out.append("")
            stack.append(Item(marker_col, content_col, level))
            out.append(" " * (TAB * level) + marker + " " + rest)  # rule 2
            prev = "item"
            continue

        fopen = FENCE_OPEN.match(line)
        interrupts = fopen is not None or INTERRUPTING_BLOCK.match(line) is not None
        if stack and prev != "blank" and interrupts and indent < stack[-1].content_col:
            out.append("")  # rule 5
            prev = "blank"
        if stack and prev == "blank":
            while stack and indent < stack[-1].content_col:
                stack.pop()

        owner = next((e for e in reversed(stack) if indent >= e.content_col), None)
        starts_block = fopen is not None or prev in ("blank", "item")
        if owner is None:
            delta = 0  # outside any list, or a lazy continuation line
        elif not starts_block:
            delta = block_delta  # continuation keeps its block's alignment
        elif fopen is not None or indent - owner.content_col < TAB:
            # A new block inside the item sits exactly at the item's content column.
            # Extra indent would read as indented code in CommonMark (4+ columns past
            # the 2-column content of "- ") while Python-Markdown would keep a fence.
            delta = owner.new_content_col - indent
        else:
            delta = owner.shift  # an indented code block stays one
        if starts_block:
            block_delta = delta
        out.append(_shift(line, delta))

        if fopen:
            fence = (fopen.group(2)[0], len(fopen.group(2)), delta, _indent(out[-1]))
        prev = "text"

    return "\n".join(out)


def main(argv: list[str]) -> int:
    in_place = "--in-place" in argv
    files = [a for a in argv if a != "--in-place"]
    if not files:
        print(__doc__, file=sys.stderr)
        return 2
    for name in files:
        path = Path(name)
        result = normalize(path.read_text(encoding="utf-8"))
        if in_place:
            path.write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
