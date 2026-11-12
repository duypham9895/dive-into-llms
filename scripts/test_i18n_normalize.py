#!/usr/bin/env python3
"""Check i18n_normalize against every upstream source the site translates.

For each of the 12 READMEs and the markdown cells of the 3 unique notebooks:
  - parity:   markdown-it-py (CommonMark) and Python-Markdown (MkDocs' extensions)
              render the same number of <pre>, <li>, <table>, <h1-6>, <img>;
  - kept:     normalising does not change the number of code blocks, tables,
              headings or images CommonMark sees in the source;
  - code:     every fenced code block keeps its content (per-line, indent-insensitive);
  - idempotent: normalize(normalize(x)) == normalize(x).
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
            "code": fence_contents(src) == fence_contents(norm),
            "idempotent": normalize(norm) == norm,
        }
        quotes = counts(_MIT.render(norm), ("blockquote",))[0], counts(render_mkdocs(norm), ("blockquote",))[0]
        ok = all(checks.values())
        failures += not ok
        failed = ", ".join(k for k, v in checks.items() if not v)
        note = f"  blockquote {quotes[0]}/{quotes[1]} (merged, text kept)" if quotes[0] != quotes[1] else ""
        print(f"{'ok  ' if ok else 'FAIL'} {name:52s} commonmark {cm} mkdocs {pm}{note}{'  failed: ' + failed if failed else ''}")
    print(f"{'all pass' if not failures else f'{failures} failing'} (pre, li, table, h, img)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
