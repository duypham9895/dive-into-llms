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

import html
import json
import posixpath
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown as pymarkdown
from markdown_it import MarkdownIt
from pymdownx.slugs import slugify

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_normalize import normalize  # noqa: E402

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

# Links are found by regex over the whole page, with code masked out first so a link
# shown as code is never rewritten. Block code (fence, indented) becomes _BLOCK, which
# nothing below may cross; an inline code span becomes _SPAN, which link text may hold.
_BLOCK, _SPAN = "\x00", "\x01"
_CODE_SPAN = re.compile(r"(?<![`\\])(`+)(?!`)((?:(?!\n[ \t]*\n)[^\x00])+?)(?<!`)\1(?!`)")
_TEXT_CHAR = r"(?:(?!\n[ \t]*\n)[^\[\]\\\x00]|\\[^\x00])"  # link text: no blank line, no block code
# A whole inline link or image. Link text may wrap lines and hold one level of brackets
# ("[![badge](img)](link)"); the destination may be <angle-bracketed> or hold one level
# of parentheses (the ch1 WeChat URL has "build(23C71)"); the title may be "..", '..' or (..).
_MD_LINK = re.compile(
    rf"(?<!\\)(?P<bang>!?)\[(?P<text>(?:{_TEXT_CHAR}|\[{_TEXT_CHAR}*\])*)\]"
    r"\([ \t]*\n?[ \t]*"
    r"(?:<(?P<aurl>(?:[^<>\n\\\x00\x01]|\\[^\n\x00\x01])*)>"
    r"|(?P<url>(?:[^()\s<>\\\x00\x01]|\\[^\s\x00\x01]|\((?:[^()\s\\\x00\x01]|\\[^\s\x00\x01])*\))+))"
    r"(?P<title>\s+(?:\"[^\"\x00]*\"|'[^'\x00]*'|\([^()\x00]*\)))?\s*\)",
    re.S,
)
# A raw HTML start tag (may span lines) and one attribute in it, quoted or not.
_TAG = re.compile(r"<(?P<name>[A-Za-z][A-Za-z0-9-]*)(?=[\s/>])(?P<attrs>(?:[^<>\"'\x00\x01]|\"[^\"\x00]*\"|'[^'\x00]*')*)>")
_ATTR = re.compile(
    r"(?P<name>[^\s\"'<>/=\x00\x01]+)"
    r"(?:(?P<eq>\s*=\s*)(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<uq>[^\s\"'=<>`]+)))?"
)
_REFERENCE_DEF = re.compile(r"^ {0,3}\[[^\]]+\]:\s*\S+")

# Attributes that load or submit to a URL the map does not see. None occurs upstream,
# so any occurrence in a translation is an error rather than something to rewrite.
FORBIDDEN_ATTRS = frozenset({"srcset", "poster", "action", "formaction"})
# Raw HTML is allow-listed: the 15 sources use only these tags and attributes (counted
# 2026-11-12, notebooks after nbconvert), plus a few inert formatting tags. Translators
# are LLMs reading untrusted text, so anything else (script, iframe, object, svg, meta,
# on* handlers, data, xlink:href) is an error, not something to pass through.
ALLOWED_TAGS = frozenset({
    "a", "b", "blockquote", "br", "code", "div", "em", "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "i", "img", "li", "ol", "p", "pre", "span", "strong", "sub", "sup", "u", "ul",
    "table", "thead", "tbody", "tr", "th", "td",
})
ALLOWED_ATTRS = frozenset({
    "align", "alt", "border", "class", "colspan", "height", "href", "id", "name",
    "rowspan", "src", "style", "title", "width",
})
ALLOWED_SCHEMES = ("http", "https", "mailto")
_SCHEME = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*):")


def check_target(url: str) -> None:
    """Raise unless url is http(s), mailto, a relative path or a #fragment.
    Browsers drop tabs and newlines anywhere and C0/space at the ends before reading
    the scheme ("java\\tscript:"), so the check does too; "//host" and "/\\host" are
    scheme-relative, i.e. another site, so they are rejected as well."""
    cleaned = re.sub(r"[\t\n\r]", "", url).strip("".join(map(chr, range(0x21))))
    m = _SCHEME.match(cleaned)
    if m and m.group(1).lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"link scheme {m.group(1)!r} not allowed: {url!r}")
    if re.match(r"[/\\]{2}", cleaned):
        raise ValueError(f"scheme-relative link not allowed: {url!r}")


def _style_loads_url(value: str) -> bool:
    css = re.sub(r"/\*.*?\*/|\\", "", value, flags=re.S)  # comments and escapes can hide "url("
    return re.search(r"url\s*\(", css, re.I) is not None


def _check_attr(name: str, value: str, where: str) -> None:
    if name in FORBIDDEN_ATTRS:
        raise ValueError(f"{where}: raw HTML attribute {name!r} not allowed")
    if name == "style" and _style_loads_url(value):
        raise ValueError(f"{where}: url() inside a style attribute not allowed")


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
    """Return the rule and new target for one link, or None if no rule covers it.
    Raises ValueError for a scheme other than http(s)/mailto (javascript:, data:, file:)."""
    url = url.strip()
    check_target(url)
    if not url:
        return None  # "[x](<>)" would otherwise resolve to the page's own directory
    if url.startswith("#"):
        return Resolution("R5", url)  # the slug is filled in by rewrite(), which knows the headings
    if url.lower().startswith("mailto:"):
        return Resolution("R6", url)

    if re.match(r"https?://", url, re.I):
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
    # "/x" would make ROOT / repo_path an absolute path on this machine.
    if not repo_path.startswith(("..", "/")) and (ROOT / repo_path).exists():
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


def heading_ids(text: str) -> list[str]:
    """Heading ids exactly as MkDocs assigns them, read from Python-Markdown's own toc.

    Re-deriving them (strip markup, slugify, dedupe) drifted from the real ids for
    headings holding "_" or "&amp;", which let a link land silently on a different
    heading whose id happened to match. The text is normalised first, as on the site,
    so both renderers see the same headings."""
    md = pymarkdown.Markdown(
        extensions=["tables", "md_in_html", "pymdownx.superfences", "pymdownx.arithmatex", "toc"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}, "toc": {"slugify": _SLUG}},
    )
    md.convert(normalize(text))
    ids: list[str] = []

    def walk(entries: list[dict]) -> None:
        for entry in entries:
            ids.append(entry["id"])
            walk(entry["children"])

    walk(md.toc_tokens)
    return ids


def _key(s: str) -> str:
    return re.sub(r"[\W_]+", "", s.lower())


def anchor_map(source_text: str, target_text: str) -> dict[str, str | None]:
    """Map each upstream anchor key to the id of the translated heading at the same position.

    A key that two source headings share maps to None: a link to it could mean either
    heading, so rewrite() refuses it. When the source itself links to such a key without
    an explicit <a name>, that is already an error here."""
    src, tgt = headings(source_text), heading_ids(target_text)
    if len(src) != len(tgt):
        raise ValueError(f"heading count differs: source {len(src)}, translation {len(tgt)}")
    keys = [_key(s) for s in src]
    shared = {k for k in keys if keys.count(k) > 1}
    explicit = explicit_anchors(source_text)
    for _kind, href in link_targets(source_text):
        name = unquote(href[1:]) if href.startswith("#") else None
        if name is not None and name not in explicit and _key(name) in shared:
            raise ValueError(
                f"source links to #{name}, but two source headings share that anchor key; "
                "give the intended heading an explicit <a name>"
            )
    return {k: (None if k in shared else "#" + i) for k, i in zip(keys, tgt)}


def explicit_anchors(text: str) -> set[str]:
    found = re.findall(r"""<a\s[^>]*?\b(?:name|id)\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s"'>]+))""", text)
    return {a or b or c for a, b, c in found}


# --- link extraction -------------------------------------------------------------

def _mask_code(text: str) -> str:
    """text with code replaced character for character (newlines kept), so an offset in
    the mask is the same offset in text. Block code lines come from the CommonMark parse,
    not from scanning for ``` ourselves: a fence opened on a bullet line ("  - ```sh")
    would otherwise flip the state."""
    code_lines: set[int] = set()
    for token in _MIT.parse(text):
        if token.type in ("fence", "code_block") and token.map:
            code_lines.update(range(*token.map))
    lines = text.split("\n")
    masked = "\n".join(_BLOCK * len(line) if i in code_lines else line for i, line in enumerate(lines))
    return _CODE_SPAN.sub(lambda m: re.sub(r"[^\n]", _SPAN, m.group(0)), masked)


class _AttrCollector(HTMLParser):
    """href/src of every start tag in a piece of raw HTML, quoted or not; raises on a
    forbidden attribute. html.parser decodes entities, as a browser would."""

    def __init__(self, where: str) -> None:
        super().__init__(convert_charrefs=True)
        self.where = where
        self.targets: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ALLOWED_TAGS:
            raise ValueError(f"{self.where}: raw HTML tag <{tag}> not allowed")
        for name, value in attrs:
            if name not in ALLOWED_ATTRS and name not in FORBIDDEN_ATTRS:
                raise ValueError(f"{self.where}: raw HTML attribute {name!r} on <{tag}> not allowed")
            _check_attr(name, value or "", self.where)
            if name in ("href", "src"):
                self.targets.append((f"<{tag} {name}>", value or ""))


def html_targets(raw: str, where: str = "page") -> list[tuple[str, str]]:
    parser = _AttrCollector(where)
    parser.feed(raw)
    parser.close()
    return parser.targets


def _walk(tokens):
    for token in tokens:
        yield token
        if token.children:
            yield from _walk(token.children)


def link_targets(text: str, where: str = "page") -> list[tuple[str, str]]:
    """(kind, target) for every link and image CommonMark sees outside code, and every
    href/src in raw HTML. Raises ValueError on a forbidden raw HTML attribute.

    This parse is independent of the regex rewrite, which is why rewrite() uses it as
    its post-condition. A Markdown link inside an HTML block is plain text to CommonMark
    but a link to Python-Markdown's md_in_html, so those are collected by regex too."""
    out: list[tuple[str, str]] = []
    for token in _walk(_MIT.parse(text)):
        if token.type == "link_open":
            out.append(("link", str(token.attrGet("href") or "")))
        elif token.type == "image":
            out.append(("image", str(token.attrGet("src") or "")))
        elif token.type in ("html_block", "html_inline"):
            out.extend(html_targets(token.content, where))
            if token.type == "html_block":
                out.extend(
                    ("link in HTML block", m.group("aurl") if m.group("aurl") is not None else m.group("url"))
                    for m in _MD_LINK.finditer(token.content)
                )
    return out


def check_external_only(text: str, where: str) -> None:
    """Pages with no link map (slide notes) may only link to absolute http(s) URLs."""
    for kind, target in link_targets(text, where):
        check_target(target)
        if not re.match(r"https?://", target.strip(), re.I):
            raise ValueError(f"{where}: only http(s) links are allowed here; found {kind} {target!r}")


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


def _rewrite_attrs(orig: str, masked: str, target_for, where: str) -> str:
    out: list[str] = []
    pos = 0
    for a in _ATTR.finditer(masked):
        name = a.group("name").lower()
        group = next((g for g in ("dq", "sq", "uq") if a.group(g) is not None), None)
        value = html.unescape(orig[a.start(group):a.end(group)]) if group else ""
        _check_attr(name, value, where)
        if name not in ("href", "src") or group is None:
            continue
        target = target_for(value, name == "src")
        if target is None:
            raise ValueError(f"{where}: an HTML {name} cannot be dropped: {value!r}")
        if target == value:
            continue
        quoted = group != "uq"
        start, end = a.start(group) - quoted, a.end(group) + quoted
        quote = "'" if group == "sq" else '"'
        out.append(orig[pos:start] + quote + html.escape(target, quote=True) + quote)
        pos = end
    out.append(orig[pos:])
    return "".join(out)


def _rewrite_html(orig: str, masked: str, target_for, where: str) -> str:
    """Rewrite href/src of every raw HTML start tag outside code, quoted or not."""
    out: list[str] = []
    pos = 0
    for tag in _TAG.finditer(masked):
        s, e = tag.span("attrs")
        out.append(orig[pos:s] + _rewrite_attrs(orig[s:e], masked[s:e], target_for, where))
        pos = e
    out.append(orig[pos:])
    return "".join(out)


def _rewrite_links(orig: str, masked: str, target_for, where: str) -> str:
    """Rewrite every Markdown link and image, then raw HTML between them. Link text is
    rewritten recursively, so a badge image inside a link is mapped as well."""
    out: list[str] = []
    pos = 0
    for m in _MD_LINK.finditer(masked):
        out.append(_rewrite_html(orig[pos:m.start()], masked[pos:m.start()], target_for, where))
        pos = m.end()
        s, e = m.span("text")
        text = _rewrite_links(orig[s:e], masked[s:e], target_for, where)
        angle = m.group("aurl") is not None
        us, ue = m.span("aurl" if angle else "url")
        target = target_for(orig[us:ue], m.group("bang") == "!")
        if target is None:
            out.append("" if m.group("bang") else text)
            continue
        title = orig[m.start("title"):m.end("title")] if m.group("title") is not None else ""
        dest = f"<{target}>" if angle or re.search(r"\s", target) else target
        out.append(f"{m.group('bang')}[{text}]({dest}{title})")
    out.append(_rewrite_html(orig[pos:], masked[pos:], target_for, where))
    return "".join(out)


def _canon(url: str) -> str:
    """Compare targets as a browser reads them: entities and percent-escapes decoded."""
    return unquote(html.unescape(url)).strip()


def _assert_closed(text: str, produced: set[str], ctx: PageContext) -> None:
    """Re-parse the rewritten page; every target outside code must be one the map
    produced in this call, or an anchor that exists on the page."""
    allowed = {_canon(t) for t in produced}
    ids = {_canon(i) for i in heading_ids(text)} | explicit_anchors(text)
    for kind, target in link_targets(text, ctx.source_rel):
        check_target(target)
        c = _canon(target)
        if c in allowed or (c.startswith("#") and c[1:] in ids):
            continue
        raise ValueError(f"{ctx.source_rel}: {kind} target {target!r} escaped the link map")


def rewrite(target_text: str, ctx: PageContext) -> tuple[str, list[str], list[tuple[str, str, str]]]:
    """Rewrite every link in a translated page.

    Returns (new_text, translator_notes, log); log holds (rule, old, new) per link.
    Raises ValueError on a link no rule covers, a disallowed scheme or raw HTML
    attribute, an anchor with no heading or an ambiguous one, or a reference-style
    link definition (not supported, so it cannot slip past the map).

    Post-condition: the result is parsed again with markdown-it and html.parser, and a
    link or image the rewrite did not produce raises. A link the regex failed to see
    therefore stops the build instead of shipping unmapped.
    """
    text = _drop_promo_blocks(target_text, ctx.lang) if ctx.page == "index.md" else target_text
    anchors = anchor_map(ctx.source_text, text)
    explicit = explicit_anchors(ctx.source_text)
    notes: list[str] = []
    log: list[tuple[str, str, str]] = []
    produced: set[str] = {UPSTREAM_BLOB + "README.md"} if ctx.page == "index.md" else set()  # promo link

    def target_for(url: str, is_image: bool) -> str | None:
        res = resolve(url, is_image, ctx)
        if res is None:
            raise ValueError(f"{ctx.source_rel}: no rule covers {url!r}")
        target = res.target
        if res.rule == "R5":
            name = unquote(url.strip()[1:])
            if name in explicit:
                target = url
            else:
                key = _key(name)
                if key not in anchors:
                    raise ValueError(f"{ctx.source_rel}: anchor {url!r} matches no heading")
                target = anchors[key]
                if target is None:
                    raise ValueError(f"{ctx.source_rel}: anchor {url!r} is shared by two source headings")
        if res.note:
            bad = url.split("/main/")[-1]
            good = (target or "").split(f"/{SHA}/")[-1]
            note = TEXT[ctx.lang][res.note].format(bad=bad, good=good, path=url)
            if note not in notes:
                notes.append(note)
        log.append((res.rule, url, target if target is not None else "(removed)"))
        if target is not None:
            produced.add(target)
        return target

    masked = _mask_code(text)
    source_lines = text.split("\n")
    for number, line in enumerate(masked.split("\n")):
        if _REFERENCE_DEF.match(line):
            raise ValueError(
                f"{ctx.source_rel}: reference-style link definition not supported: {source_lines[number].strip()!r}"
            )
    result = _rewrite_links(text, masked, target_for, ctx.source_rel)

    if notes:
        bullets = "\n".join(f"- {n}" for n in notes)
        result = result.rstrip("\n") + f"\n\n---\n\n**{TEXT[ctx.lang]['notes']}**\n\n{bullets}\n"
    _assert_closed(result, produced, ctx)
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
