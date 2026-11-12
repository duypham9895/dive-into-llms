#!/usr/bin/env python3
"""Check the built site against the Markdown it was built from (plan v5).

For every docs/<lang>/**/*.md page and its built HTML:
  - render fidelity: inside <article class="md-content__inner">, the counts of <pre>,
    <li>, <table>, <h1-6>, <img> equal what markdown-it-py renders from the page
    (Material adds an <h1> when the page has none; that is accounted for);
  - <html lang> matches the page's language;
  - the removal-request channel appears on the page, and no placeholder does;
  - every same-page fragment (href="#x") names an id on the page;
  - every href/src in the article (parsed with html.parser, quoted or not) is http,
    https or mailto, or a relative link that resolves to a built file, and its fragment
    (if any) to an id there; any other scheme (javascript:, data:, file:) fails;
  - tables: every row of every Markdown table in the page has exactly as many cells
    (split on unescaped "|") as its header, and the article has as many <td>+<th> as the
    page's cells. Both renderers silently drop a cell an extra "|" creates;
  - no Han characters in the article text, the <title> or the nav labels, outside
    <pre>/<code> and the strings in i18n/allowlist.yaml (field han).
Strict mode's exit code is not trusted on its own: mkdocs-jupyter once built raw
JSON and still reported success.

Usage: i18n_render_check.py [--no-han] SITE_DIR DOCS_DIR      exit 1 on any failure
  --no-han   skip the Han check (the spike, where the Chinese sources stand in for
             the translations)
"""
from __future__ import annotations

import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

CONTACT = "https://github.com/duypham9895/dive-into-llms/issues"
PLACEHOLDERS = ("<contact>", "&lt;contact&gt;", "<G4", "&lt;G4", "Removal requests: .", "Yêu cầu gỡ bỏ: .")
TAGS = ("pre", "li", "table", "h[1-6]", "img")
DEFAULT_LANG = "vi"
_MIT = MarkdownIt("commonmark").enable("table")
_ARTICLE = re.compile(r'<article class="md-content__inner md-typeset">(.*?)</article>', re.S)
ALLOWLIST = Path(__file__).resolve().parent.parent / "i18n" / "allowlist.yaml"
ALLOWED_SCHEMES = ("http", "https", "mailto")
_SCHEME = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*):")
HAN = re.compile("[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0003134f]")


class _Page(HTMLParser):
    """One pass over built HTML: href/src values (html.parser reads them quoted or not,
    entities decoded), and text by where it sits. Text inside <pre>/<code> is code, which
    the translation keeps byte-identical, so the Han check never reads it."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str, str]] = []  # (tag, attribute, value)
        self.text: dict[str, list[str]] = {"body": [], "title": [], "nav": []}
        self._depth = {"code": 0, "title": 0, "nav": 0}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ("href", "src"):
                self.links.append((tag, name, value or ""))
        if tag in ("pre", "code"):
            self._depth["code"] += 1
        elif tag in ("title", "nav"):
            self._depth[tag] += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ("href", "src"):
                self.links.append((tag, name, value or ""))

    def handle_endtag(self, tag: str) -> None:
        key = "code" if tag in ("pre", "code") else tag
        if key in self._depth and self._depth[key]:
            self._depth[key] -= 1

    def handle_data(self, data: str) -> None:
        if self._depth["code"]:
            return
        if self._depth["title"]:
            self.text["title"].append(data)
        elif self._depth["nav"]:
            self.text["nav"].append(data)
        else:
            self.text["body"].append(data)


def parse(html: str) -> _Page:
    page = _Page()
    page.feed(html)
    page.close()
    return page


def load_allowlist(path: Path = ALLOWLIST) -> list[str]:
    """Allowed Han strings, longest first, so a long name is removed before a part of it."""
    entries = yaml.safe_load(path.read_text(encoding="utf-8"))["entries"]
    return sorted({e["han"] for e in entries if HAN.search(str(e["han"]))}, key=len, reverse=True)


def han_outside(text: str, allowed: list[str]) -> list[str]:
    """Han runs left after removing allow-listed strings."""
    for s in allowed:
        text = text.replace(s, " ")
    return re.findall(f"{HAN.pattern}+", text)


def scheme_error(url: str) -> str | None:
    """Same reading as a browser: tabs/newlines dropped, C0 and spaces trimmed."""
    cleaned = re.sub(r"[\t\n\r]", "", url).strip("".join(map(chr, range(0x21))))
    m = _SCHEME.match(cleaned)
    if m and m.group(1).lower() not in ALLOWED_SCHEMES:
        return f"scheme {m.group(1)!r} not allowed"
    if re.match(r"[/\\]{2}", cleaned):
        return "scheme-relative link"
    return None


def _cells(row: str) -> int:
    """Cells in a raw table row, split on unescaped "|" as GFM does (code spans included)."""
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return len(re.split(r"(?<!\\)\|", row))


def table_errors(md_text: str, article: str) -> list[str]:
    """Row widths of every Markdown table, and the built <td>+<th> count."""
    errors: list[str] = []
    tokens = _MIT.parse(md_text)
    lines = md_text.split("\n")
    raw_cells = parsed_cells = 0
    for token in tokens:
        if token.type == "table_open" and token.map:
            start, end = token.map
            rows = [lines[i] for i in range(start, end) if i != start + 1]  # skip the delimiter row
            width = _cells(rows[0])
            for offset, row in enumerate(rows[1:], start=2):
                if _cells(row) != width:
                    errors.append(f"table at line {start + 1}: row {offset} has {_cells(row)} cells, header has {width}")
            raw_cells += sum(_cells(r) for r in rows)
        elif token.type in ("th_open", "td_open"):
            parsed_cells += 1
    html_cells = len(re.findall(r"<t[dh][\s>]", _MIT.render(md_text))) - parsed_cells  # raw HTML tables
    built = len(re.findall(r"<t[dh][\s>]", article))
    if built != raw_cells + html_cells:
        errors.append(f"<td>+<th> in the article: {built}, cells in the page: {raw_cells + html_cells}")
    return errors


def counts(html: str) -> tuple[int, ...]:
    return tuple(len(re.findall(rf"<{tag}[\s>]", html)) for tag in TAGS)


def built_path(site: Path, lang: str, page: str) -> Path:
    """MkDocs URL rules with use_directory_urls: README.md/index.md -> dir/index.html."""
    prefix = "" if lang == DEFAULT_LANG else f"{lang}/"
    stem = posixpath.splitext(page)[0]
    name, folder = posixpath.basename(stem), posixpath.dirname(stem)
    if name in ("index", "README"):
        return site / posixpath.join(prefix, folder, "index.html")
    return site / posixpath.join(prefix, folder, name, "index.html")


def ids(html: str) -> set[str]:
    """Fragment targets: any id, plus <a name> (upstream ch5 uses <a name="eval">)."""
    return set(re.findall(r'\bid="([^"]+)"', html)) | set(re.findall(r'<a\s[^>]*\bname="([^"]+)"', html))


def check_page(site: Path, lang: str, page: str, md_text: str, allowed: list[str] | None = None) -> list[str]:
    """allowed None skips the Han check."""
    out = built_path(site, lang, page)
    if not out.exists():
        return [f"not built: {out.relative_to(site)}"]
    html = out.read_text(encoding="utf-8")
    m = _ARTICLE.search(html)
    if not m:
        return ["no <article> in built page (not rendered as Markdown?)"]
    article = m.group(1)
    errors: list[str] = []

    source_html = _MIT.render(md_text)
    expected = list(counts(source_html))
    if "<h1" not in source_html:
        expected[3] += 1  # Material inserts the page title as <h1>
    got = counts(article)
    if tuple(expected) != got:
        errors.append(f"render counts {dict(zip(TAGS, got))} != source {dict(zip(TAGS, expected))}")

    if not re.search(rf'<html[^>]*\blang="{lang}"', html):
        errors.append(f'<html lang> is not "{lang}"')
    if CONTACT not in html:
        errors.append("removal-request channel missing")
    errors.extend(f"placeholder present: {ph!r}" for ph in PLACEHOLDERS if ph in html)

    errors.extend(table_errors(md_text, article))

    body = parse(article)
    if allowed is not None:
        whole = parse(html)
        for where, chunks in (("article", body.text["body"]), ("title", whole.text["title"]), ("nav", whole.text["nav"])):
            runs = han_outside(" ".join(chunks), allowed)
            if runs:
                errors.append(f"Han outside the allow-list in {where}: {len(runs)} runs, e.g. {runs[:3]}")

    page_ids = ids(html)
    url_dir = posixpath.dirname(str(out.relative_to(site)))
    for tag, attr, href in body.links:
        problem = scheme_error(href)
        if problem:
            errors.append(f"<{tag} {attr}>: {problem}: {href!r}")
            continue
        if re.match(r"(?i)(https?|mailto):", href.strip()):
            continue
        target, _, frag = href.partition("#")
        if not target:
            if frag and frag not in page_ids:
                errors.append(f"broken fragment #{frag}")
            continue
        dest = site / posixpath.normpath(posixpath.join(url_dir, target))
        if dest.is_dir() or target.endswith("/"):
            dest = dest / "index.html"
        if not dest.exists():
            errors.append(f"broken {attr} {href}")
        elif frag and frag not in ids(dest.read_text(encoding="utf-8")):
            errors.append(f"broken fragment {href}")
    return errors


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--no-han"]
    if len(args) != 2 or any(a.startswith("--") for a in args):
        print(__doc__, file=sys.stderr)
        return 2
    allowed = None if "--no-han" in argv else load_allowlist()
    site, docs = Path(args[0]), Path(args[1])
    failures = pages = 0
    for md in sorted(docs.rglob("*.md")):
        parts = md.relative_to(docs).parts
        lang, page = parts[0], "/".join(parts[1:])
        errors = check_page(site, lang, page, md.read_text(encoding="utf-8"), allowed)
        pages += 1
        failures += bool(errors)
        print(f"{'ok  ' if not errors else 'FAIL'} {lang}/{page}" + "".join(f"\n       - {e}" for e in errors))
    print(f"{pages - failures}/{pages} pages pass{'  (Han check skipped: --no-han)' if allowed is None else ''}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
