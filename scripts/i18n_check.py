#!/usr/bin/env python3
"""Block-level validator: every translated page against its upstream source (plan v5).

For each file under i18n/translated/<lang>/ (Markdown pages and notebooks), compared
with the upstream file at the same path, after both go through i18n_normalize:

  blocks    the block sequences align 1:1 by type: heading (with level), paragraph,
            list item (with list type and nesting), table row (with its raw cell count,
            split on unescaped "|", because both renderers silently drop extra cells),
            blockquote, fence, indented code, HTML block, rule. Paragraphs and quotes
            carry their nesting too, so a block moved out of a list is a mismatch.
  ratio     per aligned text block whose source holds Han and at least --min-len
            characters: len(translation) / len(source), visible text without spaces,
            must sit inside --band. The default band is a PLACEHOLDER until the ch2
            pilot calibrates it; every file prints its observed ratios for that.
  fences    same info string; code identical after stripping comments (Python fences
            and notebook code cells via tokenize; unlabelled, shell and YAML fences:
            "#" comments; anything else: no stripping). A fence whose code (outside
            comments) holds Han is a protected literal: its code, string literals
            included, must match the source exactly, while its comments are translated
            like any other comment (plan: "comments translated in every file").
            One listed fence (PROSE_FENCES, ch3 install steps) is prose and translated:
            its lines without Han stay byte-identical, line for line.
  gloss     directly after a protected literal, a translation may add one block that
            glosses it, marked by a line holding only GLOSS_MARK. That block is left
            out of the alignment and still Han-checked. Anywhere else the mark fails.
  content   per aligned heading, paragraph, table row and HTML block whose source is
            Chinese-authored (Han or CJK punctuation): (a) fingerprint: every number, URL,
            inline-code span and Latin token of 3+ characters of the source (Latin tokens:
            not for headings, which translate "Optional") is in the translation, as a
            multiset (FP_ORDERED); added Latin terms are fine. This is what fails a swap of
            two siblings whose content differs. (b) glossary terms (i18n/glossary.yaml):
            every term whose zh is in the source block, keep_english_in_vi true and not
            AMBIGUOUS, is rendered in the block (vi or en field, alternatives split on | or
            /, "A (B)" also accepts A or B; longest zh match wins, so 摘要思维链 needs
            Sum-CoT, not chain-of-thought). This fails a swap of Han-only siblings and a
            dropped clause on a short, gloss-heavy line. (c) inline-code spans equal as a
            multiset. (d) a paragraph or table cell with no Han and no CJK punctuation in the
            source (English prose, the ch2 English few-shot rows) is byte-identical, link
            destinations aside. Ratio above REVIEW_RATIO prints a "review:" line, not a failure.
  comments  per fence the comment count is equal (notebook cells: only when (e) applies,
            so a translated comment may still wrap there). (e) a Python comment that
            swallowed code because upstream lost a newline (prose, then if/elif/else/for/
            while/return/print(/import/from ... to the end of a '#' segment): the translated
            comment with the same index keeps that code verbatim at the end of the segment.
  links     for every link/image in the source at position k, the rewrite map applied
            to it (i18n_links.resolve, anchors via anchor_map) equals the rewrite map
            applied to the translation's link at position k, and the counts are equal.
            Comparing a translated link only with its own rewrite would pass any URL.
  Han       no Han outside the allow-list (i18n/allowlist.yaml, field han), in prose,
            headings, table cells, alt/title text and HTML text; code is exempt, except
            comments in non-protected code, which the policy says are translated.
  notebooks same cell count and cell types; code cells identical after comment
            stripping (same protected-literal rule); outputs identical; markdown cells
            checked as above, cell by cell; links over all markdown cells together.

Slide notes (i18n/translated/<lang>/slides/) have no Markdown source and are skipped;
the plan gives them their own check (section count == page count).

Upstream text is data: it is parsed, never executed (tokenize only lexes).

Usage:
  i18n_check.py [--root DIR] [--band MIN MAX] [--min-len N] [--ratios] [FILE ...]
    --root DIR     translations root (default i18n/translated); FILEs, if given, are
                   paths under it, e.g. vi/documents/chapter2/README.md
    --band MIN MAX ratio band (default PLACEHOLDER 1.0 6.0)
    --min-len N    smallest source block (non-space chars) the band applies to (default 12)
    --ratios       print every block's ratio, for calibration
Exit 1 on any failure, or when no translated file is found; 2 on bad usage.
"""
from __future__ import annotations

import difflib
import io
import json
import re
import statistics
import sys
import tokenize
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

import yaml
from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_links import (  # noqa: E402
    ROOT,
    PageContext,
    _key,
    anchor_map,
    explicit_anchors,
    heading_ids,
    link_targets,
    resolve,
    site_page_for,
)
from i18n_normalize import normalize  # noqa: E402
from i18n_render_check import HAN, _cells, han_outside, load_allowlist  # noqa: E402

TRANSLATED = ROOT / "i18n" / "translated"
# PLACEHOLDER: calibrate on the ch2 pilot (plan step 6) from the ratios this script prints.
# Calibrated 2026-11-12 on the ch2 pilot (vi+en, n=96 aligned text blocks): min 1.00,
# p5 1.00, median 1.37, p95 4.20, max 14.54. zh -> vi/en never came out shorter than the
# source, so the floor (0.9) is what catches a cut paragraph. The ceiling only has to
# admit G3 first-use glosses packed into a short source line (14.5 seen); an invented
# sentence inside a long block stays under it, which is the translation review's job.
RATIO_BAND = (0.9, 16.0)
# Above this the band cannot tell a G3 gloss from a dropped clause (6.0 was the pre-v5
# ceiling), so such blocks get a "review:" line for the translation review; not a failure.
REVIEW_RATIO = 6.0
MIN_LEN = 12
GLOSSARY = ROOT / "i18n" / "glossary.yaml"
# CJK symbols and punctuation, full-width forms: a block holding them is Chinese-authored
# even without Han ("Openai：https://..."), so it is translated, not kept byte-identical.
CJK_PUNCT = re.compile("[　-〿＀-｠￠-￯]")
# Fingerprint items must appear in the same order in the translation (True), or only be
# present, as a multiset (False). False: zh -> vi/en reorders terms inside a sentence, and
# the ordered check failed the real ch2 pilot twice ("利用Miniconda或Anaconda进行Python环境管理"
# -> "Manage Python environments with Miniconda or Anaconda"). A sibling swap is still caught,
# because what fails it is the other block's content, not the order.
FP_ORDERED = False
GLOSS_MARK = "<!-- i18n:gloss -->"
# Fences that are prose, not code (plan: "exception list for prose inside fences
# (ch3:32, translated)"). Keyed by source file and a line of the source fence.
PROSE_FENCES = {("documents/chapter3/README.md", "（可选）conda create -n EasyEdit python=3.9.7")}
PYTHON_INFO = {"python", "py", "python3", "ipython", "ipython3"}
HASH_INFO = {"", "sh", "bash", "shell", "zsh", "console", "yaml", "yml", "toml", "ini", "dockerfile"}

_MIT = MarkdownIt("commonmark").enable("table")
_TEXT_BLOCKS = {"heading", "paragraph", "table_row", "html_block", "fence"}


# --- code and comments ------------------------------------------------------------

def _hash_split(code: str) -> tuple[list[str], list[str]]:
    """(code lines without '#' comments, comments). A '#' opens a comment at the line
    start or after whitespace, outside quotes (quote state resets per line)."""
    lines: list[str] = []
    comments: list[str] = []
    for line in code.split("\n"):
        quote = None
        cut = len(line)
        for i, ch in enumerate(line):
            if quote:
                if ch == quote and line[i - 1] != "\\":
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch == "#" and (i == 0 or line[i - 1].isspace()):
                cut = i
                break
        comments.append(line[cut:])
        lines.append(line[:cut])
    return lines, comments


def _python_split(code: str) -> tuple[list[str], list[str]] | None:
    """Same as _hash_split, with comment spans taken from tokenize; None if it cannot lex."""
    lines = code.split("\n")
    comments: list[str] = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.COMMENT:
                row, col = tok.start
                comments.append(lines[row - 1][col:])
                lines[row - 1] = lines[row - 1][:col]
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return None
    return lines, comments


def _lang(info: str) -> str:
    return info.strip().split(maxsplit=1)[0].lower() if info.strip() else ""


def _split_parts(code: str, info: str) -> tuple[list[str], list[str]] | None:
    """(code lines without comments, comment tokens in order), or None: no stripping."""
    lang = _lang(info)
    parts = None
    if lang in PYTHON_INFO:
        parts = _python_split(code)
    if parts is None and (lang in HASH_INFO or lang in PYTHON_INFO):
        parts = _hash_split(code)
    return parts


def split_code(code: str, info: str) -> tuple[str, str]:
    """(code with comments removed, trailing spaces and empty lines dropped; comment text).
    Dropping empty lines lets a translated comment wrap onto more lines."""
    parts = _split_parts(code, info)
    if parts is None:
        return code, ""
    lines, comments = parts
    return "\n".join(line.rstrip() for line in lines if line.strip()), "\n".join(comments)


def comment_tokens(code: str, info: str) -> list[str]:
    """The comments of a fence or code cell, one per comment token, empty ones dropped."""
    parts = _split_parts(code, info)
    return [c for c in parts[1] if c.strip()] if parts else []


# Code swallowed into a comment: upstream lost a newline, so tokenize reads a statement as
# the tail of the comment before it (ch2 README:43, :51-53: "...message.if resp.status_code
# == HTTPStatus.OK:"). A comment is split on "#" into segments; a segment that holds prose
# and then one of these statement forms, running to the end of the segment, carries a code
# tail. Each form is anchored at the segment end, so prose that merely mentions a keyword
# ("we then import the dataset") does not match.
_CODE_TAIL = [re.compile(p) for p in (
    r"(?:el)?if\s+\S.*:\s*$",
    r"while\s+\S.*:\s*$",
    r"else\s*:\s*$",
    r"for\s+[\w ,()]+\s+in\s+\S.*:\s*$",
    r"return(?:\s+[\w.\[\]()'\"]+)?\s*$",
    r"print\(.*\)\s*$",
    r"import\s+[\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+)*\s*$",
    r"from\s+[\w.]+\s+import\s+\S.*$",
)]


def code_tail(segment: str) -> str | None:
    """The code after prose in one '#' segment of a comment, or None."""
    starts = [m.start() for p in _CODE_TAIL for m in [p.search(segment)] if m]
    if not starts:
        return None
    start = min(starts)
    if not segment[:start].strip():  # nothing before it: a commented-out line, not swallowed code
        return None
    return segment[start:].rstrip()


def compare_comments(src: str, tgt: str, info: str, where: str, count_always: bool) -> list[str]:
    """Comment k of the translation keeps the code tail that comment k of the source
    swallowed (Python only). Comment counts must match when count_always, and always when
    a swallowed tail exists, because the tails are matched by comment index."""
    s_com, t_com = comment_tokens(src, info), comment_tokens(tgt, info)
    tails = []
    if _lang(info) in PYTHON_INFO:
        for k, c in enumerate(s_com):
            for n, seg in enumerate(c.split("#")):
                tail = code_tail(seg)
                if tail:
                    tails.append((k, n, tail))
    errors: list[str] = []
    if len(s_com) != len(t_com) and (count_always or tails):
        errors.append(f"{where}: {len(t_com)} comments, source {len(s_com)}")
        return errors
    for k, n, tail in tails:
        t_seg = t_com[k].split("#")
        if n >= len(t_seg) or not t_seg[n].rstrip().endswith(tail):
            errors.append(f"{where}: comment {k + 1} swallowed code {tail!r} (upstream lost a newline); "
                          f"the translated comment must keep it verbatim at the end of the text after '#' no. {n}")
    return errors


def is_protected(code: str, info: str) -> bool:
    """Code that holds Han outside comments is a model-input or data literal."""
    return HAN.search(split_code(code, info)[0]) is not None


def compare_code(src: str, tgt: str, info: str, where: str) -> tuple[list[str], str]:
    """Errors, and the comment text of the translation that the Han check must read.

    The code (string literals included) must match the source after stripping
    comments; for a protected literal that is what keeps the Chinese model input
    intact. Comments are translated everywhere, so they are returned for the Han check
    rather than compared."""
    s_code, _ = split_code(src, info)
    t_code, t_comments = split_code(tgt, info)
    if s_code != t_code:
        diff = next(
            (f"source {a!r} vs translation {b!r}" for a, b in zip(s_code.split("\n"), t_code.split("\n")) if a != b),
            f"source {len(s_code.split(chr(10)))} code lines, translation {len(t_code.split(chr(10)))}",
        )
        return [f"{where}: code differs after stripping comments: {diff}"], t_comments
    return [], t_comments


# --- blocks ---------------------------------------------------------------------------

class _HtmlText(HTMLParser):
    """Visible text of raw HTML, plus alt/title values; comments are not text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.extend(v for k, v in attrs if k in ("alt", "title") and v)

    handle_startendtag = handle_starttag

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_text(raw: str) -> str:
    parser = _HtmlText()
    parser.feed(raw)
    parser.close()
    return "".join(parser.parts)


def inline_text(token) -> str:
    """Visible text of an inline token: text, image alt, HTML text; no code, no URLs."""
    return _inline(token)[0]


def _inline(token) -> tuple[str, str, list[str]]:
    """(visible text, visible text with inline code in place, inline code spans)."""
    parts: list[str] = []
    fp: list[str] = []
    codes: list[str] = []
    for child in token.children or []:
        piece = None
        if child.type in ("text", "image"):
            piece = child.content
        elif child.type == "html_inline":
            piece = html_text(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            piece = " "
        elif child.type == "code_inline" and HAN.search(child.content):
            # Inline code holding Han is emphasis, not code (ch8 `冻结参数`): it is
            # translated (Duy's blind-test scores, 2026-11-12), so it counts as visible
            # text for the Han check, and only its count is kept ("\x01" marks it).
            piece = child.content
            codes.append("\x01")
        elif child.type == "code_inline":
            codes.append(child.content)
            fp.append("\x00" + child.content + "\x00")
        if piece is not None:
            parts.append(piece)
            fp.append(piece)
    return "".join(parts), "".join(fp), codes


@dataclass
class Block:
    kind: str
    detail: str
    line: int  # 1-based line in the normalised text
    text: str = ""  # visible text, for the ratio and the Han check
    info: str = ""  # fences
    code: str = ""  # fences and indented code
    fp: str = ""  # visible text with inline code in place, inline code wrapped in \x00
    codes: list[str] = field(default_factory=list)  # inline code spans
    raw: list[str] = field(default_factory=list)  # raw inline Markdown: [paragraph] or one per cell

    @property
    def sig(self) -> tuple[str, str]:
        return self.kind, self.detail

    def label(self) -> str:
        snippet = re.sub(r"\s+", " ", self.text or self.code).strip()[:50]
        return f"{self.kind}{' ' + self.detail if self.detail else ''} (line {self.line}) {snippet!r}"


def _row_cells(line: str) -> int:
    return _cells(re.sub(r"^[ \t]*(?:>[ \t]?)*", "", line))


def blocks(text: str) -> tuple[list[Block], list[Block], list[str]]:
    """(aligned blocks, gloss blocks, errors) of normalised Markdown."""
    tokens = _MIT.parse(text)
    lines = text.split("\n")
    out: list[Block] = []
    gloss: list[Block] = []
    errors: list[str] = []
    lists: list[str] = []
    quotes = 0
    after_mark = False

    def ctx() -> str:
        return f"in {'/'.join(lists) or '-'} q{quotes}"

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        line = tok.map[0] + 1 if tok.map else 0
        if after_mark:
            # The block group right after GLOSS_MARK is the gloss: left out of the
            # alignment, its text kept for the Han check.
            after_mark = False
            if tok.nesting == -1:
                errors.append(f"line {line}: {GLOSS_MARK} glosses nothing")
            else:
                depth = 0
                while True:
                    inner = tokens[i]
                    if inner.type == "inline":
                        gloss.append(Block("gloss", "", inner.map[0] + 1 if inner.map else line, inline_text(inner)))
                    elif inner.type == "html_block":
                        gloss.append(Block("gloss", "", line, html_text(inner.content)))
                    depth += inner.nesting
                    i += 1
                    if depth <= 0:
                        break
                continue
        new: Block | None = None
        t = tok.type
        if t in ("heading_open", "paragraph_open"):
            text, fp, codes = _inline(tokens[i + 1])
            kind, detail = ("heading", tok.tag) if t == "heading_open" else ("paragraph", ctx())
            new = Block(kind, detail, line, text, fp=fp, codes=codes, raw=[tokens[i + 1].content])
        elif t in ("bullet_list_open", "ordered_list_open"):
            lists.append("ol" if t.startswith("ordered") else "ul")
        elif t in ("bullet_list_close", "ordered_list_close"):
            lists.pop()
        elif t == "list_item_open":
            new = Block("list_item", f"{lists[-1]}@{len(lists)}", line)
        elif t == "blockquote_open":
            new = Block("blockquote", ctx(), line)
            quotes += 1
        elif t == "blockquote_close":
            quotes -= 1
        elif t == "tr_open" and tok.map:
            j, parts, fps, codes, raw = i + 1, [], [], [], []
            while tokens[j].type != "tr_close":
                if tokens[j].type == "inline":
                    text, fp, c = _inline(tokens[j])
                    parts.append(text)
                    fps.append(fp)
                    codes.extend(c)
                    raw.append(tokens[j].content)
                j += 1
            n = _row_cells(lines[tok.map[0]])
            new = Block("table_row", f"{n} cells", line, " | ".join(parts), fp=" | ".join(fps), codes=codes, raw=raw)
        elif t == "fence":
            new = Block("fence", "", line, info=tok.info.strip(), code=tok.content)
        elif t == "code_block":
            new = Block("code_block", "", line, code=tok.content)
        elif t == "html_block" and tok.content.strip() == GLOSS_MARK:
            prev = out[-1] if out else None
            if prev is None or prev.kind != "fence" or not is_protected(prev.code, prev.info):
                errors.append(f"line {line}: {GLOSS_MARK} is only allowed directly after a protected literal")
            after_mark = True
        elif t == "html_block":
            text = html_text(tok.content)
            new = Block("html_block", ctx(), line, text, fp=text)
        elif t == "hr":
            new = Block("hr", "", line)
        if new is not None:
            out.append(new)
        i += 1
    if after_mark:
        errors.append(f"{GLOSS_MARK} at the end of the text glosses nothing")
    return out, gloss, errors


def _prose_fence(source_rel: str, code: str) -> bool:
    return any(rel == source_rel and key in code.split("\n") for rel, key in PROSE_FENCES)


# --- reports --------------------------------------------------------------------------

@dataclass
class Report:
    name: str
    errors: list[str] = field(default_factory=list)
    ratios: list[tuple[float, Block]] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    skipped: str | None = None
    warnings: list[str] = field(default_factory=list)  # for translation review; not failures


# --- glossary terms ---------------------------------------------------------------------

@dataclass(frozen=True)
class Term:
    zh: str
    vi: tuple[str, ...]  # accepted renderings, lower case
    en: tuple[str, ...]
    checked: bool  # keep_english_in_vi and not AMBIGUOUS


def _renderings(field_value: str) -> tuple[str, ...]:
    """Alternatives split on "|" or "/"; "A (B)" also accepts A alone and B alone, since a
    glossary parenthesis is an expansion that later uses drop ("Qwen (Tongyi Qianwen)")."""
    out: set[str] = set()
    for alt in re.split(r"[|/]", field_value or ""):
        alt = alt.strip().lower()
        if not alt:
            continue
        out.add(alt)
        head = re.sub(r"\s*\([^)]*\)", "", alt).strip()
        if head:
            out.add(head)
        out.update(p.strip() for p in re.findall(r"\(([^)]*)\)", alt) if p.strip())
    return tuple(sorted(out))


@lru_cache(maxsize=None)
def load_glossary(path: Path = GLOSSARY) -> tuple[Term, ...]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return tuple(
        Term(str(t["zh"]), _renderings(str(t.get("vi") or "")), _renderings(str(t.get("en") or "")),
             bool(t.get("keep_english_in_vi")) and "AMBIGUOUS" not in str(t.get("note") or ""))
        for t in data["terms"] if t.get("zh")
    )


def terms_in(text: str, terms: tuple[Term, ...]) -> list[Term]:
    """Glossary terms in a source text, longest match first at each position, so a long
    term claims its span (摘要思维链 = Sum-CoT, not 思维链). Unchecked terms claim spans
    too. A Latin zh (API, conda) must stand as its own word."""
    by_first: dict[str, list[Term]] = {}
    for term in sorted(terms, key=lambda x: len(x.zh), reverse=True):
        by_first.setdefault(term.zh[0], []).append(term)
    found: list[Term] = []
    i = 0
    while i < len(text):
        for term in by_first.get(text[i], []):
            if not text.startswith(term.zh, i):
                continue
            if not HAN.search(term.zh) and (
                (i > 0 and text[i - 1].isascii() and text[i - 1].isalnum())
                or (i + len(term.zh) < len(text) and text[i + len(term.zh)].isascii() and text[i + len(term.zh)].isalnum())
            ):
                continue
            found.append(term)
            i += len(term.zh)
            break
        else:
            i += 1
    return found


@dataclass(frozen=True)
class Settings:
    band: tuple[float, float] = RATIO_BAND
    min_len: int = MIN_LEN
    allowed: tuple[str, ...] = ()
    terms: tuple[Term, ...] = field(default_factory=load_glossary)


def _vis_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def _zh(text: str) -> bool:
    """Chinese-authored: Han, or CJK/full-width punctuation ("Openai：https://...")."""
    return bool(HAN.search(text) or CJK_PUNCT.search(text))


_FP_ITEM = re.compile(
    r"\x00(?P<code>[^\x00]*)\x00"
    r"|(?P<url>https?://[!-~]+)"
    r"|(?P<word>[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)*)"
    r"|(?P<num>\d+(?:[.,:]\d+)*)"
)
# Whole number tokens in a translation, matched like the fingerprint's "num" group.
_NUMBER = re.compile(r"(?<![\d.,:])\d+(?:[.,:]\d+)*(?!\d)")


def fingerprint(fp: str, words: bool = True) -> list[tuple[str, str]]:
    """Items of a source block that survive translation, in order: inline code, URLs,
    Latin-script tokens of 3+ characters, numbers."""
    out: list[tuple[str, str]] = []
    for m in _FP_ITEM.finditer(fp):
        kind = m.lastgroup
        item = m.group(kind)
        if kind == "url":
            item = item.rstrip(".,;:!?)]}'\"*")
        elif kind == "word":
            if len(item) < 3 or not words:
                continue
            item = item.lower()
        out.append((kind, item))
    return out


def fingerprint_missing(items: list[tuple[str, str]], target_fp: str, ordered: bool) -> list[str]:
    """Source items the translation lost: in order (each found after the previous one), or
    as a multiset (each found at least as often as the source holds it)."""
    hay = target_fp.replace("\x00", "")
    low = hay.lower()
    missing: list[str] = []
    if ordered:
        pos = 0
        for kind, item in items:
            h = low if kind == "word" else hay
            k = h.find(item, pos)
            if k < 0:
                missing.append(item)
            else:
                pos = k + len(item)
        return missing
    need: dict[tuple[str, str], int] = {}
    for key in items:
        need[key] = need.get(key, 0) + 1
    # Numbers are counted as whole tokens: a substring count let the "0" of "0.7" stand
    # in for a dropped "temperature 大于0" (review round 2, measured on the ch2 pilot).
    numbers = _NUMBER.findall(hay)
    for (kind, item), n in need.items():
        have = numbers.count(item) if kind == "num" else (low if kind == "word" else hay).count(item)
        if have < n:
            missing.append(item)
    return missing


def _mask_links(raw: str) -> str:
    """Link destinations are the link check's business; mask them for byte identity."""
    return re.sub(r"(\]\()(<[^>]*>|[^)\s]*)", r"\1", raw)


def _han_errors(where: str, text: str, allowed: tuple[str, ...]) -> list[str]:
    runs = han_outside(text, list(allowed))
    return [f"{where}: Han outside the allow-list: {runs[:3]}"] if runs else []


def compare_markdown(source_rel: str, src_text: str, tgt_text: str, settings: Settings, report: Report,
                     prefix: str = "", lang: str = "vi") -> None:
    """Blocks, ratios, fences and Han for one Markdown text (a page or a notebook cell)."""
    src_blocks, _, src_err = blocks(normalize(src_text))
    tgt_blocks, gloss, tgt_err = blocks(normalize(tgt_text))
    report.errors.extend(f"{prefix}source: {e}" for e in src_err)
    report.errors.extend(f"{prefix}{e}" for e in tgt_err)
    report.counts["blocks"] = report.counts.get("blocks", 0) + len(src_blocks)

    # 1:1 alignment by type
    matcher = difflib.SequenceMatcher(a=[b.sig for b in src_blocks], b=[b.sig for b in tgt_blocks], autojunk=False)
    pairs: list[tuple[Block, Block]] = []
    shown = 0
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":
            pairs.extend(zip(src_blocks[a0:a1], tgt_blocks[b0:b1]))
            continue
        if shown < 5:
            missing = "; ".join(b.label() for b in src_blocks[a0:a1][:3]) or "-"
            extra = "; ".join(b.label() for b in tgt_blocks[b0:b1][:3]) or "-"
            report.errors.append(f"{prefix}blocks do not align ({op}): source [{missing}] vs translation [{extra}]")
        shown += 1
    if shown > 5:
        report.errors.append(f"{prefix}... {shown - 5} more block misalignments")
    if len(src_blocks) != len(tgt_blocks):
        report.errors.append(f"{prefix}block count: source {len(src_blocks)}, translation {len(tgt_blocks)}")

    # fences, by order (independent of the alignment above)
    src_f = [b for b in src_blocks if b.kind in ("fence", "code_block")]
    tgt_f = [b for b in tgt_blocks if b.kind in ("fence", "code_block")]
    report.counts["fences"] = report.counts.get("fences", 0) + len(src_f)
    if len(src_f) != len(tgt_f):
        report.errors.append(f"{prefix}code block count: source {len(src_f)}, translation {len(tgt_f)}")
    han_text: list[tuple[str, str]] = []
    for k, (s, t) in enumerate(zip(src_f, tgt_f), start=1):
        where = f"{prefix}fence {k} (line {t.line})"
        if s.kind != t.kind:
            report.errors.append(f"{where}: {s.kind} became {t.kind}")
            continue
        if s.info != t.info:
            report.errors.append(f"{where}: info string {s.info!r} changed to {t.info!r}")
        if s.kind == "fence" and _prose_fence(source_rel, s.code):
            s_lines, t_lines = s.code.split("\n"), t.code.split("\n")
            if len(s_lines) != len(t_lines):
                report.errors.append(f"{where}: prose fence has {len(t_lines)} lines, source {len(s_lines)}")
            for a, b in zip(s_lines, t_lines):
                if not HAN.search(a) and a != b:
                    report.errors.append(f"{where}: command line {a!r} changed to {b!r}")
            han_text.append((f"{where} (prose fence)", t.code))
            t.text, s.text = t.code, s.code  # ratio applies to the prose fence
            continue
        errors, comments = compare_code(s.code, t.code, s.info, where)
        report.errors.extend(errors)
        report.errors.extend(compare_comments(s.code, t.code, s.info, where, count_always=True))
        if comments:
            han_text.append((f"{where} comment", comments))

    # length ratio over aligned text blocks
    lo, hi = settings.band
    for s, t in pairs:
        if s.kind not in _TEXT_BLOCKS or not HAN.search(s.text):
            continue
        n = _vis_len(s.text)
        if n < settings.min_len:
            continue
        ratio = _vis_len(t.text) / n
        report.ratios.append((ratio, t))
        if not lo <= ratio <= hi:
            report.errors.append(f"{prefix}ratio {ratio:.2f} outside [{lo}, {hi}]: {s.label()} -> {t.label()}")
        elif ratio > REVIEW_RATIO:
            report.warnings.append(f"{prefix}ratio {ratio:.2f} > {REVIEW_RATIO}: gloss or dropped clause? "
                                   f"{s.label()} -> {t.label()}")

    # content of aligned text blocks: what a sibling swap, a dropped clause or a
    # translated English row would change while the block types still align
    for s, t in pairs:
        if s.kind not in ("heading", "paragraph", "table_row", "html_block"):
            continue
        where = f"{prefix}{t.kind} line {t.line}"
        # Latin inline code must survive unchanged; each Han span of the source ("\x01")
        # is translated, and may come back as at most one new inline-code span.
        s_codes = Counter(c for c in s.codes if c != "\x01")
        t_codes = Counter(c for c in t.codes if c != "\x01")
        translated = s.codes.count("\x01")
        lost, added = s_codes - t_codes, t_codes - s_codes
        if lost or sum(added.values()) > translated:
            report.errors.append(
                f"{where}: inline code {sorted(t_codes.elements())} differs from the source's "
                f"{sorted(s_codes.elements())} (+{translated} translated Han spans)"
            )
        # English prose and the English few-shot rows stay byte-identical (plan, "Keep
        # byte-identical"); headings and HTML text are translated anyway.
        if s.kind == "paragraph" and not _zh(s.raw[0]) and _mask_links(s.raw[0]) != _mask_links(t.raw[0]):
            report.errors.append(f"{where}: source paragraph holds no Chinese, must stay byte-identical: "
                                 f"{s.raw[0][:60]!r} became {t.raw[0][:60]!r}")
        if s.kind == "table_row" and len(s.raw) == len(t.raw):
            for c, (a, b) in enumerate(zip(s.raw, t.raw), start=1):
                if not _zh(a) and _mask_links(a) != _mask_links(b):
                    report.errors.append(f"{where}: cell {c} holds no Chinese in the source, must stay "
                                         f"byte-identical: {a[:60]!r} became {b[:60]!r}")
        if not _zh(s.fp):
            continue
        lost = fingerprint_missing(fingerprint(s.fp, words=s.kind != "heading"), t.fp, FP_ORDERED)
        if lost:
            report.errors.append(f"{where}: lost or reordered source content {lost[:4]} "
                                 f"(numbers, URLs, inline code, Latin terms): {s.label()} -> {t.label()}")
        if HAN.search(s.text):
            low = t.fp.replace("\x00", "").lower()
            missing: dict[str, tuple[str, ...]] = {}
            for term in terms_in(s.text, settings.terms):
                renderings = term.vi if lang == "vi" else term.en
                if term.checked and not any(r in low for r in renderings):
                    missing[term.zh] = renderings
            if missing:
                listed = "; ".join(f"{zh} -> {' / '.join(r)}" for zh, r in missing.items())
                report.errors.append(f"{where}: glossary term not rendered ({listed}): {t.label()}")

    # Han outside code
    for b in tgt_blocks + gloss:
        if b.kind not in ("fence", "code_block"):
            han_text.append((f"{b.kind} line {b.line}", b.text))
    for where, text in han_text:
        report.errors.extend(f"{prefix}{e}" for e in _han_errors(where, text, settings.allowed))


def _map_link(kind: str, url: str, ctx: PageContext, anchors: dict[str, str | None] | None,
              explicit: set[str], tgt_ids: set[str]) -> tuple[str, str, str | None]:
    """(kind, rule, target) the rewrite map gives one link."""
    is_image = kind == "image" or kind.endswith(" src>")
    try:
        res = resolve(url, is_image, ctx)
    except ValueError as exc:
        return kind, "ERROR", str(exc)
    if res is None:
        return kind, "UNMAPPED", url
    if res.rule != "R5":
        return kind, res.rule, res.target
    name = unquote(url.strip()[1:])
    if name in explicit:
        return kind, "R5", "#" + name
    if anchors is None:
        return kind, "R5", "(headings do not align)"
    if _key(name) in anchors:
        return kind, "R5", anchors[_key(name)]
    if name in tgt_ids:  # the translation already holds the translated slug
        return kind, "R5", "#" + name
    return kind, "R5", f"(no heading for #{name})"


def compare_links(source_rel: str, lang: str, src_text: str, tgt_text: str, report: Report) -> None:
    """Link k of the translation must map to what link k of the source maps to."""
    page = site_page_for(source_rel) or source_rel
    ctx = PageContext(source_rel, page, lang, src_text)
    try:
        src_links = link_targets(normalize(src_text), source_rel)
        tgt_links = link_targets(normalize(tgt_text), source_rel)
    except ValueError as exc:
        report.errors.append(f"links: {exc}")
        return
    try:
        anchors: dict[str, str | None] | None = anchor_map(src_text, tgt_text)
    except ValueError as exc:
        anchors = None
        report.errors.append(f"anchors: {exc}")
    explicit = explicit_anchors(src_text)
    tgt_ids = set(heading_ids(tgt_text)) | explicit_anchors(tgt_text)
    report.counts["links"] = len(src_links)
    if len(src_links) != len(tgt_links):
        report.errors.append(f"link count: source {len(src_links)}, translation {len(tgt_links)}")
    for k, ((sk, su), (tk, tu)) in enumerate(zip(src_links, tgt_links), start=1):
        s = _map_link(sk, su, ctx, anchors, explicit, tgt_ids)
        t = _map_link(tk, tu, ctx, anchors, explicit, tgt_ids)
        if t[1] in ("ERROR", "UNMAPPED"):
            report.errors.append(f"link {k}: {t[1]} {tu!r}: {t[2]}")
        elif s != t:
            report.errors.append(f"link {k}: source {sk} {su!r} maps to {s[1:]}, translation {tk} {tu!r} maps to {t[1:]}")


def check_markdown_page(source_rel: str, lang: str, src_text: str, tgt_text: str, settings: Settings,
                        name: str | None = None) -> Report:
    report = Report(name or f"{lang}/{source_rel}")
    compare_markdown(source_rel, src_text, tgt_text, settings, report, lang=lang)
    compare_links(source_rel, lang, src_text, tgt_text, report)
    return report


def check_notebook(source_rel: str, lang: str, src_nb: dict, tgt_nb: dict, settings: Settings,
                   name: str | None = None) -> Report:
    report = Report(name or f"{lang}/{source_rel}")
    s_cells, t_cells = src_nb.get("cells", []), tgt_nb.get("cells", [])
    report.counts["cells"] = len(s_cells)
    if len(s_cells) != len(t_cells):
        report.errors.append(f"cell count: source {len(s_cells)}, translation {len(t_cells)}")
    s_types = [c.get("cell_type") for c in s_cells]
    t_types = [c.get("cell_type") for c in t_cells]
    if s_types != t_types:
        k = next((i for i, (a, b) in enumerate(zip(s_types, t_types)) if a != b), min(len(s_types), len(t_types)))
        report.errors.append(f"cell types differ from cell {k}: source {s_types[k:k + 3]}, translation {t_types[k:k + 3]}")
        return report
    info = src_nb.get("metadata", {}).get("kernelspec", {}).get("language", "python")
    for k, (s, t) in enumerate(zip(s_cells, t_cells)):
        s_src, t_src = "".join(s.get("source", [])), "".join(t.get("source", []))
        where = f"cell {k}"
        if s["cell_type"] == "code":
            errors, comments = compare_code(s_src, t_src, info, where)
            report.errors.extend(errors)
            # a cell's translated comment may wrap onto more lines, unless a tail is matched by index
            report.errors.extend(compare_comments(s_src, t_src, info, where, count_always=False))
            report.errors.extend(_han_errors(f"{where} comment", comments, settings.allowed))
            if s.get("outputs", []) != t.get("outputs", []):
                report.errors.append(f"{where}: outputs differ from the source")
        elif s["cell_type"] == "markdown":
            compare_markdown(source_rel, s_src, t_src, settings, report, prefix=f"{where}: ", lang=lang)
        elif s_src != t_src:
            report.errors.append(f"{where}: {s['cell_type']} cell changed")
    md = lambda cells: "\n\n".join("".join(c.get("source", [])) for c in cells if c.get("cell_type") == "markdown")  # noqa: E731
    compare_links(source_rel, lang, md(s_cells), md(t_cells), report)
    return report


def check_file(path: Path, root: Path, settings: Settings) -> Report:
    rel_parts = path.relative_to(root).parts
    lang, source_rel = rel_parts[0], "/".join(rel_parts[1:])
    name = f"{lang}/{source_rel}"
    if rel_parts[1:2] == ("slides",):
        return Report(name, skipped="slide notes have no Markdown source (separate check)")
    source = ROOT / source_rel
    if not source.is_file():
        return Report(name, errors=[f"no upstream source at {source_rel}"])
    try:
        if path.suffix == ".ipynb":
            return check_notebook(source_rel, lang, json.loads(source.read_text(encoding="utf-8")),
                                  json.loads(path.read_text(encoding="utf-8")), settings, name)
        return check_markdown_page(source_rel, lang, source.read_text(encoding="utf-8"),
                                   path.read_text(encoding="utf-8"), settings, name)
    except (ValueError, KeyError) as exc:  # malformed JSON, a parse the map refuses
        return Report(name, errors=[f"could not check: {type(exc).__name__}: {exc}"])


def _summary(values: list[float]) -> str:
    if not values:
        return "n=0"
    q = statistics.quantiles(values, n=20) if len(values) >= 2 else [values[0]] * 19
    return (f"n={len(values)} min {min(values):.2f} p5 {q[0]:.2f} median {statistics.median(values):.2f} "
            f"p95 {q[18]:.2f} max {max(values):.2f}")


def print_report(report: Report, show_ratios: bool) -> None:
    if report.skipped:
        print(f"skip {report.name}: {report.skipped}")
        return
    counts = " ".join(f"{k} {v}" for k, v in report.counts.items())
    status = "ok  " if not report.errors else "FAIL"
    print(f"{status} {report.name}  {counts}  ratio {_summary([r for r, _ in report.ratios])}")
    for e in report.errors:
        print(f"       - {e}")
    for w in report.warnings:
        print(f"       review: {w}")
    if show_ratios:
        for ratio, block in report.ratios:
            print(f"       ratio {ratio:5.2f}  {block.label()}")


def main(argv: list[str]) -> int:
    args = list(argv)
    root, band, min_len, show = TRANSLATED, RATIO_BAND, MIN_LEN, False
    files: list[str] = []
    try:
        while args:
            a = args.pop(0)
            if a == "--root":
                root = Path(args.pop(0))
            elif a == "--band":
                band = (float(args.pop(0)), float(args.pop(0)))
            elif a == "--min-len":
                min_len = int(args.pop(0))
            elif a == "--ratios":
                show = True
            elif a.startswith("--"):
                raise ValueError(a)
            else:
                files.append(a)
    except (IndexError, ValueError):
        print(__doc__, file=sys.stderr)
        return 2
    root = root.resolve()
    settings = Settings(band, min_len, tuple(load_allowlist()))
    paths = [root / f for f in files] if files else sorted(
        p for p in root.rglob("*") if p.suffix in (".md", ".ipynb") and p.is_file()
    )
    if not paths:
        print(f"FAIL no translated .md or .ipynb found under {root}")
        return 1
    reports = [check_file(p, root, settings) for p in paths]
    every: list[float] = []
    for r in reports:
        print_report(r, show)
        every.extend(x for x, _ in r.ratios)
    checked = [r for r in reports if not r.skipped]
    failed = sum(1 for r in checked if r.errors)
    print(f"{len(checked) - failed}/{len(checked)} files pass, {len(reports) - len(checked)} skipped; "
          f"band [{band[0]}, {band[1]}] (calibrated on the ch2 pilot); all ratios {_summary(every)}")
    return 1 if failed or not checked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
