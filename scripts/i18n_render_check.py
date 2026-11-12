#!/usr/bin/env python3
"""Check the built site against the Markdown it was built from (plan v5).

For every docs/<lang>/**/*.md page and its built HTML:
  - render fidelity: inside <article class="md-content__inner">, the counts of <pre>,
    <li>, <table>, <h1-6>, <img> equal what markdown-it-py renders from the page
    (Material adds an <h1> when the page has none; that is accounted for);
  - <html lang> matches the page's language;
  - the removal-request channel appears on the page, and no placeholder does;
  - every same-page fragment (href="#x") names an id on the page;
  - every relative link to another page resolves to a built file, and its fragment
    (if any) to an id there.
Strict mode's exit code is not trusted on its own: mkdocs-jupyter once built raw
JSON and still reported success.

Usage: i18n_render_check.py SITE_DIR DOCS_DIR      exit 1 on any failure
"""
from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

CONTACT = "https://github.com/duypham9895/dive-into-llms/issues"
PLACEHOLDERS = ("<contact>", "&lt;contact&gt;", "<G4", "&lt;G4", "Removal requests: .", "Yêu cầu gỡ bỏ: .")
TAGS = ("pre", "li", "table", "h[1-6]", "img")
DEFAULT_LANG = "vi"
_MIT = MarkdownIt("commonmark").enable("table")
_ARTICLE = re.compile(r'<article class="md-content__inner md-typeset">(.*?)</article>', re.S)


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


def check_page(site: Path, lang: str, page: str, md_text: str) -> list[str]:
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

    page_ids = ids(html)
    url_dir = posixpath.dirname(str(out.relative_to(site)))
    for href in re.findall(r'href="([^"]+)"', article):
        if href.startswith(("http://", "https://", "mailto:", "javascript:")):
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
            errors.append(f"broken link {href}")
        elif frag and frag not in ids(dest.read_text(encoding="utf-8")):
            errors.append(f"broken fragment {href}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    site, docs = Path(argv[0]), Path(argv[1])
    failures = pages = 0
    for md in sorted(docs.rglob("*.md")):
        parts = md.relative_to(docs).parts
        lang, page = parts[0], "/".join(parts[1:])
        errors = check_page(site, lang, page, md.read_text(encoding="utf-8"))
        pages += 1
        failures += bool(errors)
        print(f"{'ok  ' if not errors else 'FAIL'} {lang}/{page}" + "".join(f"\n       - {e}" for e in errors))
    print(f"{pages - failures}/{pages} pages pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
