#!/usr/bin/env python3
"""Check slide notes against the text extracted from each deck page.

Notes:   i18n/translated/<lang>/slides/chapterN.md
Source:  i18n/.cache/slides/chapterN/page-NNN.txt   (pdftotext -layout, one file per page)

Per notes file:
  [1] sections   one "## Slide k" heading per source page, k = 1..pages, in order and none
                 missing or repeated. The decks of ch5 and ch8 are English: their en page
                 holds only the title and the deck link, so it must have no section at all.
  [2] urls       every http(s) URL of a source page appears in that page's section
                 (substring, so a URL pdftotext cut at a line end still matches its full form).
  [3] numbers    every number of a source page appears in its section as a whole token,
                 as many times as in the source (multiset). A token is a maximal run of
                 ASCII digits with optional ".digits" parts: "2024年" gives 2024, "1.8/7/14"
                 gives 1.8, 7 and 14, and 12 does not match inside 2012. Footer noise is
                 excluded (see footer_noise); the heading line itself is not counted.
  [4] han        no Han characters outside i18n/allowlist.yaml, outside code.
  [5] links      only absolute http(s) links (check_external_only, plus a regex pass for
                 links markdown-it drops but Python-Markdown renders) and no images at all.
  [6] header     line 1 is a "# " title; a link to the deck PDF at the pinned commit
                 (blob, raw or raw.githubusercontent form) is present.

Source page text is untrusted data: it is only read and compared, never executed.

Usage:
  i18n_slides_check.py [FILE ...]   check the given notes (default: every notes file);
                                    exit 1 on any failure, or when there is nothing to check
  i18n_slides_check.py --calibrate  print the footer noise excluded from all source pages
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_links import _MD_LINK, SHA, _mask_code, check_external_only, link_targets  # noqa: E402
from i18n_render_check import load_allowlist, han_outside  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "i18n" / ".cache" / "slides"
TRANSLATED = ROOT / "i18n" / "translated"
ENGLISH_DECKS = {5, 8}
REPO = "Lordog/dive-into-llms"

_FULLWIDTH = str.maketrans("０１２３４５６７８９", "0123456789")
_NUMBER = re.compile(r"(?<![0-9])[0-9]+(?:\.[0-9]+)*")
_URL = re.compile(r"https?://[^\s<>\"'`）（，。；、】【]+")
_URL_TRAIL = ".,;:!?'\"*_"
# A whole-line reference definition: "[label]: target" with an optional quoted title.
_REF_DEF = re.compile(
    r"^ {0,3}\[[^\]\n]+\]:[ \t]*(?:<([^<>\n]*)>|(\S+))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?[ \t]*$",
    re.M,
)
_SLIDE = re.compile(r"^## Slide ([0-9]+)(?:[ \t].*|:.*)?$")
# Beamer footline "author  title  k / M" on the last line: frame number and frame total.
_FRAME = re.compile(r"(?:^|\s{2,})([0-9]+) / ([0-9]+)\s*$")
# A number in its own layout column: a line of its own, or after 2+ spaces at a line end,
# or after a sentence's closing period (ch8 p16: "... PracticalGuide. 2023. 16").
_ALONE = re.compile(r"(?:^|\s{2,}|\.\s)([0-9]+)\s*$")
_MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
_DATE = re.compile(
    r"[0-9]{4}\s*年\s*[0-9]{1,2}\s*月(?:\s*[0-9]{1,2}\s*日)?"
    r"|[0-9]{4}[-/.][0-9]{1,2}[-/.][0-9]{1,2}"
    r"|[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}"
    rf"|{_MONTH}\s+[0-9]{{1,2}},?\s+[0-9]{{4}}"
    rf"|[0-9]{{1,2}}\s+{_MONTH}\s+[0-9]{{4}}"
    rf"|{_MONTH}[- ][0-9]{{4}}"
)


# --- source pages ----------------------------------------------------------------

def load_pages(chapter: int) -> list[str]:
    """The extracted text of every page of a deck, in page order."""
    folder = CACHE / f"chapter{chapter}"
    files = sorted(folder.glob("page-*.txt"))
    expected = [f"page-{i:03d}.txt" for i in range(1, len(files) + 1)]
    if not files or [f.name for f in files] != expected:
        raise ValueError(f"{folder}: page files are not page-001..page-{len(files):03d}")
    return [f.read_text(encoding="utf-8") for f in files]


def deck_pdf(chapter: int) -> str:
    pdfs = sorted((ROOT / "documents" / f"chapter{chapter}").glob("*.pdf"))
    if len(pdfs) != 1:
        raise ValueError(f"chapter {chapter}: expected one deck PDF, found {len(pdfs)}")
    return f"documents/chapter{chapter}/{pdfs[0].name}"


def numbers(text: str) -> Counter[str]:
    return Counter(_NUMBER.findall(text.translate(_FULLWIDTH)))


def urls(text: str) -> list[str]:
    out = []
    for m in _URL.finditer(text):
        url = m.group(0).rstrip(_URL_TRAIL)
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1].rstrip(_URL_TRAIL)
        if url not in out:
            out.append(url)
    return out


def footer_noise(text: str, page: int, total: int) -> list[tuple[str, str]]:
    """(number, why) for each token of a page that is extraction noise, not content.

    Calibrated on the 495 extracted pages (run --calibrate to see what it removes):
      - a beamer footline "k / M" ending the last line (ch5): k and M;
      - otherwise the page number or the deck's page count standing alone (own line,
        or own column after 2+ spaces or after ". " at a line end) on one of the last two
        non-empty lines (ch8 puts a "…" line under the number);
      - the digits of a date on the last non-empty line."""
    lines = [line.replace("\f", "").rstrip() for line in text.translate(_FULLWIDTH).split("\n")]
    filled = [line for line in lines if line.strip()]
    if not filled:
        return []
    out: list[tuple[str, str]] = []
    m = _FRAME.search(filled[-1])
    if m:
        out += [(m.group(1), "footer frame number"), (m.group(2), "footer frame total")]
    else:
        for line in reversed(filled[-2:]):
            m = _ALONE.search(line)
            if m and int(m.group(1)) in (page, total):
                out.append((m.group(1), "page number" if int(m.group(1)) == page else "page count"))
                break
    for d in _DATE.finditer(filled[-1]):
        out += [(n, f"footer date {d.group(0)!r}") for n in _NUMBER.findall(d.group(0))]
    return out


def content_numbers(text: str, page: int, total: int) -> Counter[str]:
    found = numbers(text)
    found.subtract(n for n, _ in footer_noise(text, page, total))
    return +found


# --- notes -------------------------------------------------------------------------

def split_sections(text: str) -> tuple[str, list[tuple[int, int, str]]]:
    """(text before the first section, [(k, line number, body without heading)]).
    Headings inside code are not headings."""
    lines = text.split("\n")
    masked = _mask_code(text).split("\n")
    heads = [(i, int(m.group(1))) for i, line in enumerate(masked) if (m := _SLIDE.match(line))]
    if not heads:
        return text, []
    sections = []
    for idx, (i, k) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        sections.append((k, i + 1, "\n".join(lines[i + 1:end])))
    return "\n".join(lines[:heads[0][0]]), sections


def deck_link_ok(text: str, chapter: int) -> bool:
    path = re.escape(deck_pdf(chapter))
    pattern = re.compile(
        rf"https://(?:github\.com/{REPO}/(?:blob|raw)/{SHA}|raw\.githubusercontent\.com/{REPO}/{SHA})/{path}$"
    )
    try:
        targets = link_targets(text, "deck link")
    except ValueError:
        return False
    return any(pattern.match(target.strip()) for _, target in targets)


def check_notes(text: str, lang: str, chapter: int, pages: list[str], allowed: list[str]) -> tuple[list[str], int]:
    """(errors, number of footer tokens excluded) for one notes file."""
    errors: list[str] = []
    total = len(pages)
    title_only = lang == "en" and chapter in ENGLISH_DECKS

    # [6] header
    first = text.split("\n", 1)[0]
    if not re.match(r"# \S", first):
        errors.append('[6] line 1 is not a "# " title')
    if not deck_link_ok(text, chapter):
        errors.append(f"[6] no link to {deck_pdf(chapter)} at commit {SHA}")

    # [5] links: absolute http(s) only, no images
    try:
        check_external_only(text, "notes")
        for kind, target in link_targets(text, "notes"):
            if kind == "image" or kind.startswith("<img"):
                errors.append(f"[5] image not allowed: {target!r}")
    except ValueError as exc:
        errors.append(f"[5] {exc}")
    # markdown-it drops a link whose scheme it distrusts ("[x](javascript:...)") and so
    # never shows it to check_external_only, but Python-Markdown, which builds the site,
    # renders it live. So every inline link and reference definition is read by regex too.
    masked = _mask_code(text)
    raw = [(m.group("bang"), m.group("aurl") if m.group("aurl") is not None else m.group("url"))
           for m in _MD_LINK.finditer(masked)]
    raw += [("", m.group(1) if m.group(1) is not None else m.group(2)) for m in _REF_DEF.finditer(masked)]
    for bang, target in raw:
        if bang:
            problem = f"[5] image not allowed: {target!r}"
        elif not re.match(r"https?://", target.strip(), re.I):
            problem = f"[5] only http(s) links are allowed here; found {target!r}"
        else:
            continue
        if problem not in errors and not any(e.startswith("[5]") and repr(target) in e for e in errors):
            errors.append(problem)

    # [4] Han outside the allow-list, outside code
    runs = han_outside(_mask_code(text), allowed)
    if runs:
        errors.append(f"[4] Han outside the allow-list: {len(runs)} runs, e.g. {runs[:3]}")

    # [1] sections
    _, sections = split_sections(text)
    got = [k for k, _, _ in sections]
    if title_only:
        if sections:
            errors.append(f"[1] English deck: the en page must have no sections, found {len(sections)}")
        return errors, 0
    if got != list(range(1, total + 1)):
        missing = sorted(set(range(1, total + 1)) - set(got))
        extra = sorted(k for k, n in Counter(got).items() if n > 1 or not 1 <= k <= total)
        detail = []
        if missing:
            detail.append(f"missing {missing[:10]}")
        if extra:
            detail.append(f"repeated or out of range {extra[:10]}")
        if not missing and not extra:
            detail.append(f"out of order: {got[:12]}")
        errors.append(f"[1] sections != 1..{total}: " + "; ".join(detail))

    # [2] urls and [3] numbers, per section (first section of each number counts)
    excluded = 0
    seen: set[int] = set()
    for k, line_no, body in sections:
        if k in seen or not 1 <= k <= total:
            continue
        seen.add(k)
        source = pages[k - 1]
        for url in urls(source):
            if url not in body:
                errors.append(f"[2] Slide {k} (line {line_no}): URL missing: {url}")
        noise = footer_noise(source, k, total)
        excluded += len(noise)
        need = content_numbers(source, k, total)
        have = numbers(body)
        short = {n: c - have[n] for n, c in need.items() if have[n] < c}
        if short:
            shown = ", ".join(f"{n}" + (f" x{c}" if c > 1 else "") for n, c in sorted(short.items())[:10])
            errors.append(f"[3] Slide {k} (line {line_no}): numbers missing: {shown}")
    return errors, excluded


# --- command line ------------------------------------------------------------------

def calibrate() -> int:
    grand = Counter()
    pages_total = 0
    for folder in sorted(CACHE.glob("chapter*"), key=lambda p: int(p.name[7:])):
        chapter = int(folder.name[7:])
        pages = load_pages(chapter)
        pages_total += len(pages)
        kinds: Counter[str] = Counter()
        bare: list[int] = []
        dates: list[str] = []
        for page, text in enumerate(pages, 1):
            noise = footer_noise(text, page, len(pages))
            if not noise:
                bare.append(page)
            for n, why in noise:
                key = why if not why.startswith("footer date") else "footer date digits"
                kinds[key] += 1
                if key == "footer date digits":
                    dates.append(f"p{page}:{why}")
        grand.update(kinds)
        line = ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())) or "nothing"
        print(f"chapter{chapter:<3} {len(pages):>3} pages: excluded {line}; "
              f"{len(bare)} pages with no footer number" + (f" {bare[:12]}{'…' if len(bare) > 12 else ''}" if bare else ""))
        for d in dates:
            print(f"           {d}")
    summary = ", ".join(f"{v} {k}" for k, v in sorted(grand.items()))
    print(f"{pages_total} pages: excluded {sum(grand.values())} tokens ({summary}); "
          f"footer date digits: {grand['footer date digits']}")
    return 0


def notes_files(args: list[str]) -> list[Path]:
    if args:
        return [Path(a).resolve() for a in args]
    return sorted(TRANSLATED.glob("*/slides/chapter*.md"), key=lambda p: (p.parts[-3], int(p.stem[7:])))


def main(argv: list[str]) -> int:
    if argv == ["--calibrate"]:
        return calibrate()
    if any(a.startswith("-") for a in argv):
        print(__doc__, file=sys.stderr)
        return 2
    files = notes_files(argv)
    if not files:
        print(f"FAIL no slide notes found under {TRANSLATED.relative_to(ROOT)}/<lang>/slides/")
        return 1
    allowed = load_allowlist()
    failures = 0
    for path in files:
        try:
            m = re.fullmatch(r"chapter([0-9]+)", path.stem)
            if not m or path.parent.name != "slides":
                raise ValueError("not a <lang>/slides/chapterN.md path")
            lang, chapter = path.parent.parent.name, int(m.group(1))
            pages = load_pages(chapter)
            errors, excluded = check_notes(path.read_text(encoding="utf-8"), lang, chapter, pages, allowed)
            note = f"  ({len(pages)} pages, {excluded} footer tokens excluded)"
        except (OSError, ValueError) as exc:
            errors, note = [str(exc)], ""
        failures += bool(errors)
        name = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"{'ok  ' if not errors else 'FAIL'} {name}{note}" + "".join(f"\n       - {e}" for e in errors))
    print(f"{len(files) - failures}/{len(files)} files pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
