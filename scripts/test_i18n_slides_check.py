#!/usr/bin/env python3
"""Synthetic cases for i18n_slides_check.py: one clean notes file, then one broken copy
per check, each of which must fail with that check's tag and no other. The last cases
pin the footer calibration on the real 495 extracted pages and run main() end to end.

Run from the repo root: .venv/bin/python scripts/test_i18n_slides_check.py
Exit status 0 when every case passes.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_links import SHA  # noqa: E402
from i18n_render_check import load_allowlist  # noqa: E402
from i18n_slides_check import (  # noqa: E402
    check_notes, content_numbers, footer_noise, load_pages, main, numbers, urls,
)

ALLOWED = load_allowlist()
RESULTS: list[bool] = []
DECK = f"https://github.com/Lordog/dive-into-llms/blob/{SHA}/documents/chapter2/dive-into-prompting.pdf"

# Three synthetic source pages in pdftotext -layout style, with footer noise.
PAGES = [
    "提示学习\n\n  张三  2023\n\n\n                1\n\f",
    "方法  见 https://arxiv.org/abs/2201.11903。\n  准确率 78.7% → 92.3%，共 12 个任务\n"
    "  教程 https://github.com/f/awesome-chat\n\n                2\n\f",
    "总结：3 个要点                                  3\n\f",
]
CLEAN = f"""# Prompting (slide notes)

Deck: [dive-into-prompting.pdf]({DECK})

## Slide 1

Prompt learning. Zhang San, 2023.

## Slide 2

Method, see <https://arxiv.org/abs/2201.11903>. Accuracy 78.7% → 92.3% over 12 tasks.
Tutorial: [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts).

```text
代码里的中文不算
```

## Slide 3

Summary: 3 key points.
"""


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}")


def run(text: str, lang: str = "vi", chapter: int = 2, pages: list[str] = PAGES) -> list[str]:
    return check_notes(text, lang, chapter, pages, ALLOWED)[0]


def expect_only(name: str, text: str, tag: str, needle: str = "", **kw) -> None:
    errors = run(text, **kw)
    ok = bool(errors) and all(e.startswith(tag) for e in errors) and any(needle in e for e in errors)
    check(name, ok, repr(errors))


# --- helpers ------------------------------------------------------------------------
check("numbers: whole tokens, 12 not inside 2012", numbers("in 2012, v1.5, 1.8/7/14 and 2024年")
      == Counter({"2012": 1, "1.5": 1, "1.8": 1, "7": 1, "14": 1, "2024": 1}))
check("numbers: full-width digits read as ASCII", numbers("２０２４") == Counter({"2024": 1}))
check("urls: trailing punctuation and full-width brackets stripped",
      urls("（https://arxiv.org/pdf/2308.06463.pdf） and https://arxiv.org/pdf/2306.13549), x.")
      == ["https://arxiv.org/pdf/2308.06463.pdf", "https://arxiv.org/pdf/2306.13549"])
check("footer: page number on its own line excluded", footer_noise(PAGES[0], 1, 3) == [("1", "page number")])
check("footer: page number in its own column excluded", footer_noise(PAGES[2], 3, 3) == [("3", "page number")])
check("footer: content number kept", content_numbers(PAGES[2], 3, 3) == Counter({"3": 1}))
check("footer: beamer 'k / M' excluded",
      footer_noise("Outline\n\n       Zhiwei He    Watermark for LLMs   8 / 44\n", 10, 48)
      == [("8", "footer frame number"), ("44", "footer frame total")])
check("footer: page number above a '…' line excluded (ch8 layout)",
      footer_noise("[1] A survey. 2023                    9\n…\n", 9, 81) == [("9", "page number")])
check("footer: date on the last line excluded",
      [n for n, _ in footer_noise("Title\n   Talk   April 14, 2024        5\n", 5, 9)] == ["5", "14", "2024"])
check("footer: a number that is neither page nor count is kept", footer_noise("x\n\n      7\n", 5, 9) == [])

# --- clean case ---------------------------------------------------------------------
errors, excluded = check_notes(CLEAN, "vi", 2, PAGES, ALLOWED)
check("clean notes pass", errors == [], repr(errors))
check("clean notes: 3 footer page numbers excluded", excluded == 3, str(excluded))

# --- [1] sections ---------------------------------------------------------------------
expect_only("[1] missing section", CLEAN.replace("## Slide 3\n\nSummary: 3 key points.\n", ""), "[1]", "missing [3]")
swapped = CLEAN.replace("## Slide 1", "## Slide X").replace("## Slide 2", "## Slide 1").replace("## Slide X", "## Slide 2")
errors = run(swapped)
check("[1] sections out of order", any(e.startswith("[1]") and "out of order" in e for e in errors), repr(errors))
expect_only("[1] repeated section", CLEAN.replace("## Slide 3", "## Slide 2"), "[1]", "repeated")
check("[1] heading inside code is not a section",
      run(CLEAN.replace("代码里的中文不算", "## Slide 3")) == [])

# --- [2] URLs and [3] numbers ---------------------------------------------------------
expect_only("[2] dropped URL", CLEAN.replace("<https://arxiv.org/abs/2201.11903>", "arXiv 2201.11903"), "[2]", "2201.11903")
check("[2] truncated source URL matches its full form",
      not [e for e in run(CLEAN) if "awesome-chat" in e])
expect_only("[3] dropped number", CLEAN.replace("over 12 tasks", "over all tasks"), "[3]", "Slide 2")
expect_only("[3] number only in the heading does not count",
            CLEAN.replace("Summary: 3 key points.", "Summary: three key points."), "[3]", "Slide 3")
expect_only("[3] number must be a whole token", CLEAN.replace("over 12 tasks", "over 2012 tasks"), "[3]", "12")
expect_only("[3] vi decimal comma is a different token", CLEAN.replace("78.7%", "78,7%"), "[3]", "78.7")

# --- [4] Han ----------------------------------------------------------------------------
expect_only("[4] Han left in prose", CLEAN.replace("Summary:", "总结："), "[4]")
check("[4] Han inside code and allow-listed Han pass",
      run(CLEAN.replace("Prompt learning.", "Dive into LLMs (动手学大模型).")) == [])

# --- [5] links ----------------------------------------------------------------------------
expect_only("[5] relative link", CLEAN.replace("Summary:", "[see](../chapter3/README.md) Summary:"), "[5]", "only http(s)")
expect_only("[5] image (even absolute)", CLEAN.replace("Summary:", "![fig](https://example.com/a.png) Summary:"), "[5]", "image")
expect_only("[5] raw <img>", CLEAN.replace("Summary:", '<img src="https://example.com/a.png"> Summary:'), "[5]", "image")
expect_only("[5] javascript: link (markdown-it drops it, Python-Markdown renders it)",
            CLEAN.replace("Summary:", "[x](javascript:alert(1)) Summary:"), "[5]", "javascript")
expect_only("[5] reference definition to a relative target",
            CLEAN + "\n[ref]: ../chapter3/README.md\n", "[5]", "README")
check("[5] a citation line '[1]: Title: subtitle. 2023' is not a reference definition",
      run(CLEAN.replace("Summary: 3 key points.", "Summary: 3 key points.\n\n[1]: VideoChat: Chat-Centric. 2023")) == [])

# --- [6] header ---------------------------------------------------------------------------
expect_only("[6] no title on line 1", "\n" + CLEAN, "[6]", "title")
expect_only("[6] deck link missing", CLEAN.replace(f"[dive-into-prompting.pdf]({DECK})", "the deck"), "[6]", SHA)
expect_only("[6] deck link at another commit", CLEAN.replace(SHA, "main"), "[6]", SHA)
expect_only("[6] deck link as plain text does not count", CLEAN.replace(f"[dive-into-prompting.pdf]({DECK})", DECK), "[6]")
raw_deck = CLEAN.replace(DECK, f"https://raw.githubusercontent.com/Lordog/dive-into-llms/{SHA}/documents/chapter2/dive-into-prompting.pdf")
check("[6] raw.githubusercontent deck link passes", run(raw_deck) == [])

# --- English decks: en page is title + link only -------------------------------------
DECK5 = f"https://github.com/Lordog/dive-into-llms/blob/{SHA}/documents/chapter5/watermark.pdf"
EN5 = f"# Watermark for LLMs\n\nThe slides are in English: [watermark.pdf]({DECK5})\n"
check("[1] English deck en page: title + link passes", run(EN5, lang="en", chapter=5, pages=["x"] * 48) == [])
expect_only("[1] English deck en page: a section fails", EN5 + "\n## Slide 1\n\nText.\n", "[1]", "no sections",
            lang="en", chapter=5, pages=["x"] * 48)
errors = run(EN5, lang="vi", chapter=5, pages=["x\n"] * 2)
check("[1] English deck vi page still needs every section", any(e.startswith("[1]") and "missing [1, 2]" in e for e in errors), repr(errors))

# --- calibration on the real 495 pages --------------------------------------------------
kinds: Counter[str] = Counter()
page_count = 0
for chapter in range(1, 12):
    pages = load_pages(chapter)
    page_count += len(pages)
    for page, text in enumerate(pages, 1):
        kinds.update(why if not why.startswith("footer date") else "date" for _, why in footer_noise(text, page, len(pages)))
check("calibration: 495 pages read", page_count == 495, str(page_count))
check("calibration: 287 page numbers, 48+48 beamer footer tokens, 0 dates, 0 page counts",
      kinds == Counter({"page number": 287, "footer frame number": 48, "footer frame total": 48}), repr(kinds))

# --- main() end to end ----------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    good = Path(tmp) / "en" / "slides" / "chapter5.md"
    good.parent.mkdir(parents=True)
    good.write_text(EN5, encoding="utf-8")
    bad = Path(tmp) / "vi" / "slides" / "chapter5.md"
    bad.parent.mkdir(parents=True)
    bad.write_text(EN5, encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code_good = main([str(good)])
        code_bad = main([str(bad)])
        code_misplaced = main([str(Path(tmp) / "notes.md")])
    text = out.getvalue()
    check("main: clean file exits 0 with an ok line", code_good == 0 and "ok   " in text, text)
    check("main: broken file exits 1 with a FAIL line and errors", code_bad == 1 and "FAIL" in text and "- [1]" in text, text)
    check("main: a path outside <lang>/slides/ fails", code_misplaced == 1, text)

passed = sum(RESULTS)
print(f"{passed}/{len(RESULTS)} cases pass")
sys.exit(0 if passed == len(RESULTS) else 1)
