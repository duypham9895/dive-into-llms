#!/usr/bin/env python3
"""Closed link and image rewrite map for the vi/en site (plan v5).

Every link or image target in a translated page is resolved by exactly one rule.
A target no rule covers is an error, so nothing ships pointing somewhere unplanned.

  R1  upstream chapter README / unique notebook  -> site page, same language
  R2  duplicate notebook (or ch7 code-only)      -> upstream file at the pinned SHA
  R3  PDF                                        -> upstream file at the SHA (3 dead links corrected)
  R4  relative path missing upstream (ch8)       -> NExT-GPT at its pinned SHA, else plain text
  R5  in-page anchor                             -> slug of the translated heading;
                                                    explicit HTML anchors (<a name>) kept
  R6  external URL, repo meta link               -> unchanged (WeChat share URL reduced
                                                    to its canonical parameters)
  R7  other upstream file (e.g. requirements.txt) -> upstream file at the SHA
  IMG relative image -> raw.githubusercontent at the SHA; external image unchanged;
      the root promo images are dropped (replaced by one link upstream)

Usage:
  i18n_links.py --check      resolve every link in the 12 READMEs and 3 unique notebooks;
                             exit 1 if any target is unassigned
"""
from __future__ import annotations

import json
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from markdown_it import MarkdownIt
from pymdownx.slugs import slugify

ROOT = Path(__file__).resolve().parent.parent
SHA = "f84c04268794ef94f8949808bbc14ab8636763a0"
NEXTGPT_SHA = "b005e807b4b9086557eca1c386e5b643154b6f7f"
UPSTREAM = "https://github.com/Lordog/dive-into-llms"
UPSTREAM_BLOB = f"{UPSTREAM}/blob/{SHA}/"
UPSTREAM_RAW = f"https://raw.githubusercontent.com/Lordog/dive-into-llms/{SHA}/"
NEXTGPT = "https://github.com/NExT-GPT/NExT-GPT"

UNIQUE_NOTEBOOKS = {
    "documents/chapter4/sft_math.ipynb",
    "documents/chapter9/GUIagent.ipynb",
    "documents/chapter11/RLHF.ipynb",
}
DEAD_PDFS = {  # upstream link target -> file that exists
    "documents/chapter7/agents.pdf": "documents/chapter10/dive-into-safety.pdf",
    "documents/chapter6/mllms.pdf": "documents/chapter8/mllms.pdf",
    "documents/chapter8/GUIagent.pdf": "documents/chapter9/GUIagent.pdf",
}
PROMO_IMAGES = {"pics/icon/title.jpg", "pics/icon/cover.png", "pics/icon/team.png", "pics/icon/agent.png"}
REPO_META = ("/stargazers", "/network/members", "/issues")
IMAGE_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp)$", re.I)
WECHAT_KEEP = ("__biz", "mid", "idx", "sn")

TEXT = {
    "vi": {
        "notes": "Ghi chú của người dịch",
        "dead_pdf": "Liên kết tới `{bad}` trong bản gốc không tồn tại; đã trỏ sang `{good}`.",
        "missing_path": "`{path}` là đường dẫn trong dự án NExT-GPT, không có trong repo gốc; liên kết đã được bỏ.",
        "promo": "Ảnh giới thiệu khoá học: xem trong [README gốc]({url}).",
    },
    "en": {
        "notes": "Translator's notes",
        "dead_pdf": "The original links to `{bad}`, which does not exist; the link points to `{good}` instead.",
        "missing_path": "`{path}` is a path in the NExT-GPT project, not in the original repo; the link was removed.",
        "promo": "Course images: see the [original README]({url}).",
    },
}

_MIT = MarkdownIt("commonmark").enable("table")
_SLUG = slugify(case="lower")
_HTML_ATTR = re.compile(r"""(?P<attr>\b(?:href|src))\s*=\s*(?P<q>["'])(?P<url>[^"']*)(?P=q)""", re.I)
# A whole inline link or image; link text may hold one level of brackets ("[[here]](x)").
_MD_LINK = re.compile(
    r"(?P<bang>!?)\[(?P<text>(?:[^\[\]]|\[[^\[\]]*\])*)\]"
    r"\(\s*(?P<lt><?)(?P<url>[^)\s>]+)(?P<gt>>?)(?P<title>\s+\"[^\"]*\")?\s*\)"
)
_REFERENCE_DEF = re.compile(r"^ {0,3}\[[^\]]+\]:\s*\S+")


@dataclass(frozen=True)
class Resolution:
    rule: str
    target: str | None  # None: drop the link, keep its text
    note: str | None = None  # TEXT key for a translator's note


@dataclass(frozen=True)
class PageContext:
    source_rel: str  # upstream file, e.g. documents/chapter8/README.md
    page: str  # site page relative to docs/<lang>/, e.g. chapter8/README.md
    lang: str
    source_text: str


def _load_nextgpt_tree() -> dict[str, str]:
    path = ROOT / "i18n/data/nextgpt-tree-b005e807.tsv"
    rows = (line.split("\t", 1) for line in path.read_text(encoding="utf-8").splitlines() if "\t" in line)
    return {p: kind for kind, p in rows}


_NEXTGPT_TREE = _load_nextgpt_tree()


def site_page_for(repo_path: str) -> str | None:
    """Site page (relative to docs/<lang>/) for an upstream file, if the site has one."""
    if repo_path == "README.md":
        return "index.md"
    m = re.fullmatch(r"documents/(chapter\d+)/README\.md", repo_path)
    if m:
        return f"{m.group(1)}/README.md"
    if repo_path in UNIQUE_NOTEBOOKS:
        chapter, name = repo_path.split("/")[1:3]
        return f"{chapter}/{Path(name).stem}.md"
    return None


def _relative(from_page: str, to_page: str) -> str:
    return posixpath.relpath(to_page, posixpath.dirname(from_page) or ".")


def _canonical_wechat(url: str) -> str:
    """Keep only the article identifiers; drop the sharer's session parameters.
    Pairs are kept byte-for-byte so the original percent-encoding is preserved."""
    parts = urlsplit(url)
    kept = [pair for pair in parts.query.split("&") if pair.split("=", 1)[0] in WECHAT_KEEP]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "&".join(kept), ""))


def _upstream_path(url: str) -> str | None:
    m = re.match(rf"{re.escape(UPSTREAM)}/(?:tree|blob)/main/(.+)$", url)
    return m.group(1) if m else None


def resolve(url: str, is_image: bool, ctx: PageContext) -> Resolution | None:
    """Return the rule and new target for one link, or None if no rule covers it."""
    url = url.strip()
    if url.startswith("#"):
        return Resolution("R5", url)  # the slug is filled in by rewrite(), which knows the headings

    if re.match(r"https?://", url):
        if url.startswith(UPSTREAM) and url[len(UPSTREAM):].startswith(REPO_META):
            return Resolution("R6", url)
        repo_path = _upstream_path(url)
        if repo_path is None:
            if "mp.weixin.qq.com" in url:
                return Resolution("R6", _canonical_wechat(url))
            return Resolution("IMG" if is_image else "R6", url)
        return _resolve_repo_path(repo_path, is_image, ctx)

    path_part = url.split("#", 1)[0].split("?", 1)[0]
    repo_path = posixpath.normpath(posixpath.join(posixpath.dirname(ctx.source_rel), path_part))
    if not repo_path.startswith("..") and (ROOT / repo_path).exists():
        return _resolve_repo_path(repo_path, is_image, ctx)
    if repo_path in DEAD_PDFS:
        return _resolve_repo_path(repo_path, is_image, ctx)

    if ctx.source_rel == "documents/chapter8/README.md":
        nextgpt_path = posixpath.normpath(path_part).rstrip("/")
        kind = _NEXTGPT_TREE.get(nextgpt_path)
        if kind:
            view = "tree" if kind == "tree" else "blob"
            return Resolution("R4", f"{NEXTGPT}/{view}/{NEXTGPT_SHA}/{nextgpt_path}")
        return Resolution("R4", None, "missing_path")
    return None


def _resolve_repo_path(repo_path: str, is_image: bool, ctx: PageContext) -> Resolution:
    if is_image or IMAGE_EXT.search(repo_path):
        if repo_path in PROMO_IMAGES:
            return Resolution("IMG", None)
        return Resolution("IMG", UPSTREAM_RAW + repo_path)
    if repo_path.endswith(".pdf"):
        good = DEAD_PDFS.get(repo_path)
        if good:
            return Resolution("R3", UPSTREAM_BLOB + good, "dead_pdf")
        return Resolution("R3", UPSTREAM_BLOB + repo_path)
    page = site_page_for(repo_path)
    if page:
        return Resolution("R1", _relative(ctx.page, page))
    if repo_path.endswith(".ipynb"):
        return Resolution("R2", UPSTREAM_BLOB + repo_path)
    return Resolution("R7", UPSTREAM_BLOB + repo_path)


# --- anchors -----------------------------------------------------------------

def _plain(inline: str) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", inline)
    return re.sub(r"[`*_]", "", text).strip()


def headings(text: str) -> list[str]:
    tokens = _MIT.parse(text)
    return [_plain(tokens[i + 1].content) for i, t in enumerate(tokens) if t.type == "heading_open"]


def _key(s: str) -> str:
    return re.sub(r"[\W_]+", "", s.lower())


def anchor_map(source_text: str, target_text: str) -> dict[str, str]:
    """Map each upstream anchor key to the slug of the translated heading at the same position."""
    src, tgt = headings(source_text), headings(target_text)
    if len(src) != len(tgt):
        raise ValueError(f"heading count differs: source {len(src)}, translation {len(tgt)}")
    return {_key(s): "#" + _SLUG(t, "-") for s, t in zip(src, tgt)}


def explicit_anchors(text: str) -> set[str]:
    return set(re.findall(r"""<a\s+(?:name|id)\s*=\s*["']([^"']+)["']""", text))


# --- rewriting ---------------------------------------------------------------

def _drop_promo_blocks(text: str, lang: str) -> str:
    """Replace the HTML block holding the root promo images with one link upstream;
    drop the commented-out copy of the same images."""
    promo = "|".join(re.escape("./" + p) for p in sorted(PROMO_IMAGES))
    pattern = re.compile(
        rf"(<!--(?:(?!-->).)*?(?:{promo}).*?-->|<p[^>]*>\s*(?:<img[^>]*(?:{promo})[^>]*>\s*)+</p>)", re.S
    )
    link = TEXT[lang]["promo"].format(url=UPSTREAM_BLOB + "README.md")
    used = False

    def repl(m: re.Match[str]) -> str:
        nonlocal used
        if m.group(0).startswith("<!--") or used:
            return ""
        used = True
        return link

    return pattern.sub(repl, text)


def rewrite(target_text: str, ctx: PageContext) -> tuple[str, list[str], list[tuple[str, str, str]]]:
    """Rewrite every link in a translated page.

    Returns (new_text, translator_notes, log); log holds (rule, old, new) per link.
    Raises ValueError on a link no rule covers, an anchor with no heading, or a
    reference-style link definition (not supported, so it cannot slip past the map).
    """
    text = _drop_promo_blocks(target_text, ctx.lang) if ctx.page == "index.md" else target_text
    anchors = anchor_map(ctx.source_text, text)
    explicit = explicit_anchors(ctx.source_text)
    notes: list[str] = []
    log: list[tuple[str, str, str]] = []

    def target_for(url: str, is_image: bool) -> str | None:
        res = resolve(url, is_image, ctx)
        if res is None:
            raise ValueError(f"{ctx.source_rel}: no rule covers {url!r}")
        target = res.target
        if res.rule == "R5":
            name = url[1:]
            target = url if name in explicit else anchors.get(_key(name))
            if target is None:
                raise ValueError(f"{ctx.source_rel}: anchor {url!r} matches no heading")
        if res.note:
            bad = url.split("/main/")[-1]
            good = (target or "").split(f"/{SHA}/")[-1]
            note = TEXT[ctx.lang][res.note].format(bad=bad, good=good, path=url)
            if note not in notes:
                notes.append(note)
        log.append((res.rule, url, target if target is not None else "(removed)"))
        return target

    def md_sub(m: re.Match[str]) -> str:
        target = target_for(m.group("url"), m.group("bang") == "!")
        if target is None:
            return "" if m.group("bang") else m.group("text")
        return (
            f"{m.group('bang')}[{m.group('text')}]"
            f"({m.group('lt')}{target}{m.group('gt')}{m.group('title') or ''})"
        )

    def html_sub(m: re.Match[str]) -> str:
        target = target_for(m.group("url"), m.group("attr").lower() == "src")
        return f'{m.group("attr")}={m.group("q")}{target or ""}{m.group("q")}'

    # Code lines come from the CommonMark parse, not from scanning for ``` ourselves:
    # a fence opened on a bullet line ("  - ```sh") would otherwise flip the state.
    code_lines: set[int] = set()
    for token in _MIT.parse(text):
        if token.type in ("fence", "code_block") and token.map:
            code_lines.update(range(*token.map))

    out_lines: list[str] = []
    for number, line in enumerate(text.split("\n")):
        if number in code_lines:
            out_lines.append(line)
            continue
        if _REFERENCE_DEF.match(line):
            raise ValueError(f"{ctx.source_rel}: reference-style link definition not supported: {line.strip()!r}")
        out_lines.append(_HTML_ATTR.sub(html_sub, _MD_LINK.sub(md_sub, line)))

    result = "\n".join(out_lines)
    if notes:
        bullets = "\n".join(f"- {n}" for n in notes)
        result = result.rstrip("\n") + f"\n\n---\n\n**{TEXT[ctx.lang]['notes']}**\n\n{bullets}\n"
    return result, notes, log


# --- source check --------------------------------------------------------------

def source_files() -> list[tuple[str, str, str]]:
    """(source_rel, site page, text) for the 12 READMEs and the 3 unique notebooks."""
    items = [("README.md", "index.md", (ROOT / "README.md").read_text(encoding="utf-8"))]
    for p in sorted((ROOT / "documents").glob("chapter*/README.md"), key=lambda p: int(p.parent.name[7:])):
        rel = str(p.relative_to(ROOT))
        items.append((rel, site_page_for(rel), p.read_text(encoding="utf-8")))
    for rel in sorted(UNIQUE_NOTEBOOKS):
        cells = json.loads((ROOT / rel).read_text(encoding="utf-8"))["cells"]
        text = "\n\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "markdown")
        items.append((rel, site_page_for(rel), text))
    return items


def check_sources() -> int:
    counts: dict[str, int] = {}
    errors = 0
    for rel, page, text in source_files():
        try:
            _, notes, log = rewrite(text, PageContext(rel, page, "en", text))
        except ValueError as exc:
            print(f"UNASSIGNED {exc}")
            errors += 1
            continue
        for rule, _, _ in log:
            counts[rule] = counts.get(rule, 0) + 1
        print(f"ok  {rel:44s} {len(log):3d} links  notes={len(notes)}")
    print("by rule:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())), f"| total {sum(counts.values())}")
    return 1 if errors else 0


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        sys.exit(check_sources())
    print(__doc__, file=sys.stderr)
    sys.exit(2)
