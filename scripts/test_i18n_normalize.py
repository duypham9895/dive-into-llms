#!/usr/bin/env python3
"""Check i18n_normalize against every upstream source the site translates.

For each of the 12 READMEs and the markdown cells of the 3 unique notebooks:
  - parity:   markdown-it-py (CommonMark) and Python-Markdown (MkDocs' extensions)
              render the same number of <pre>, <li>, <table>, <h1-6>, <img>;
  - kept:     normalising does not change the number of code blocks, tables,
              headings or images CommonMark sees in the source;
  - items:    CommonMark loses exactly one <li> per item that is only a fence opened
              on its bullet line (rule 3 drops that bullet), and no other item;
  - code:     every fenced code block keeps its content (per-line, indent-insensitive);
  - idempotent: normalize(normalize(x)) == normalize(x).
Synthetic cases pin the CommonMark edge rules the corpus does not exercise: the
normalised text must render exactly as the source does under CommonMark.
Blockquote counts are reported, not enforced: Python-Markdown merges two quotes
separated by one blank line into one quote with two paragraphs (ch1); no text is lost.

Run from the repo root: .venv/bin/python scripts/test_i18n_normalize.py
Exit status 0 when every source passes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import markdown
from markdown_it import MarkdownIt
from pymdownx.slugs import slugify

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_normalize import normalize  # noqa: E402

UNIQUE_NOTEBOOKS = (
    "documents/chapter4/sft_math.ipynb",
    "documents/chapter9/GUIagent.ipynb",
    "documents/chapter11/RLHF.ipynb",
)
COMPARED = ("pre", "li", "table", "h[1-6]", "img")
_MIT = MarkdownIt("commonmark").enable("table")


def render_mkdocs(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "md_in_html", "pymdownx.superfences", "pymdownx.arithmatex", "toc"],
        extension_configs={
            "pymdownx.arithmatex": {"generic": True},
            "toc": {"slugify": slugify(case="lower")},
        },
    )


def counts(html: str, tags: tuple[str, ...] = COMPARED) -> tuple[int, ...]:
    return tuple(len(re.findall(rf"<{tag}[\s>]", html)) for tag in tags)


def fence_contents(text: str) -> list[tuple[str, ...]]:
    return [tuple(l.strip() for l in t.content.split("\n")) for t in _MIT.parse(text) if t.type == "fence"]


def fence_bullets(text: str) -> int:
    """Items whose content opens with a fence on the bullet line (rule 3 drops them).
    Counted from the CommonMark parse, independently of the normaliser's own state."""
    tokens = _MIT.parse(text)
    return sum(
        1
        for open_, first in zip(tokens, tokens[1:])
        if open_.type == "list_item_open" and first.type == "fence" and first.map[0] == open_.map[0]
    )


# (name, source, also check Python-Markdown parity). Each must render identically under
# CommonMark before and after normalising.
SYNTHETIC = (
    # 5+ spaces after the marker: the item opens with indented code (content column = marker + 1).
    # Python-Markdown cannot open an item with code, so parity is not expected here.
    ("5+ spaces after marker", "-     indented item text\n    more text at col 4\n", False),
    ("5+ spaces, nested", "- a\n\n  1.      code in item\n     text\n", False),
    # Only a bullet or "1." can interrupt a paragraph.
    ("ordered 2023. after paragraph", "Phần này ra đời năm\n2023. Sau đó được cập nhật\n", True),
    ("ordered 2) after paragraph", "văn bản\n2) không phải mục\n", True),
    ("ordered 1. after paragraph", "văn bản\n1. mục một\n2. mục hai\n", True),
    ("bullet after paragraph", "văn bản\n- mục\n", True),
    ("ordered 2. after heading", "# Tiêu đề\n2. mục\n", True),
    # A backtick fence's info string cannot hold a backtick.
    ("backticks in info string", "```python``` là cú pháp\n- a\n  - b\n", True),
    # Tilde fences may hold backticks (CommonMark); superfences rejects this info string,
    # so only the CommonMark side is pinned.
    ("tilde fence with backticks", "~~~ a`b\ncode\n~~~\n", False),
)


def check_synthetic() -> int:
    failures = 0
    for name, src, parity in SYNTHETIC:
        norm = normalize(src)
        checks = {
            "commonmark-same": _MIT.render(src) == _MIT.render(norm),
            "idempotent": normalize(norm) == norm,
        }
        if parity:
            checks["parity"] = counts(_MIT.render(norm)) == counts(render_mkdocs(norm))
        ok = all(checks.values())
        failures += not ok
        failed = ", ".join(k for k, v in checks.items() if not v)
        print(f"{'ok  ' if ok else 'FAIL'} synthetic: {name}{'  failed: ' + failed if failed else ''}")
    return failures


def sources(root: Path) -> list[tuple[str, str]]:
    readmes = [root / "README.md"] + sorted(
        (root / "documents").glob("chapter*/README.md"),
        key=lambda p: int(re.search(r"\d+", p.parent.name).group()),
    )
    items = [(str(p.relative_to(root)), p.read_text(encoding="utf-8")) for p in readmes]
    for rel in UNIQUE_NOTEBOOKS:
        cells = json.loads((root / rel).read_text(encoding="utf-8"))["cells"]
        text = "\n\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "markdown")
        items.append((rel + " [markdown cells]", text))
    return items


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    failures = 0
    for name, src in sources(root):
        norm = normalize(src)
        src_c, cm, pm = counts(_MIT.render(src)), counts(_MIT.render(norm)), counts(render_mkdocs(norm))
        checks = {
            "parity": cm == pm,
            "kept": tuple(src_c[i] for i in (0, 2, 3, 4)) == tuple(cm[i] for i in (0, 2, 3, 4)),
            "items": src_c[1] - cm[1] == fence_bullets(src),
            "code": fence_contents(src) == fence_contents(norm),
            "idempotent": normalize(norm) == norm,
        }
        quotes = counts(_MIT.render(norm), ("blockquote",))[0], counts(render_mkdocs(norm), ("blockquote",))[0]
        ok = all(checks.values())
        failures += not ok
        failed = ", ".join(k for k, v in checks.items() if not v)
        note = f"  blockquote {quotes[0]}/{quotes[1]} (merged, text kept)" if quotes[0] != quotes[1] else ""
        print(f"{'ok  ' if ok else 'FAIL'} {name:52s} commonmark {cm} mkdocs {pm}{note}{'  failed: ' + failed if failed else ''}")
    failures += check_synthetic()
    print(f"{'all pass' if not failures else f'{failures} failing'} (pre, li, table, h, img)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
