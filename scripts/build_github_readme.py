#!/usr/bin/env python3
"""Build the GitHub-rendered README pair for the fork's repository page (plan v1, R1 P1-P7).

GitHub shows `.github/README.md` in front of the root README.md for a repo that has both
(docs: "About READMEs"). This writes that file (Vietnamese) and `.github/README.en.md`
(English); root README.md stays the untouched upstream Chinese file (a pipeline input and
the upstream-sync target) and is never written here.

Both files are generated from the SAME translated source and the SAME link-rewrite map as
the MkDocs site home page: i18n_links.rewrite() with the index-page context
(PageContext("README.md", "index.md", lang, source_text)), so the content, the pinned-SHA
links and the promo-image policy match the site exactly. Two things then differ from the
site build:
  - every site-relative R1 target (a relative path to another translated page) becomes an
    absolute URL on the live site: vi https://duypham9895.github.io/dive-into-llms/<page>/,
    en .../dive-into-llms/en/<page>/ (MkDocs' use_directory_urls: README.md/index.md -> the
    page's own directory; any other page -> a same-named subdirectory);
  - every in-page "#fragment" is re-targeted from the site's own heading slug (pymdownx,
    used by mkdocs) to the slug GitHub's renderer assigns the SAME translated heading.
    GitHub's rule (read off a live GET of the upstream README, 2026-11-12:
    gh api -H 'Accept: application/vnd.github.html' repos/Lordog/dive-into-llms/readme):
    lowercase; delete every character that is not a Unicode letter (L), mark (M), number
    (N), connector punctuation (Pc), "-" or space; space -> "-"; a duplicate slug gets
    "-1", "-2", ... A mark (e.g. the U+FE0F on an emoji) survives even when the emoji
    itself (category So) is dropped, so an emoji-led heading keeps a leading invisible
    mark before the "-" (confirmed on the upstream "❤️ 贡献者列表" -> "user-content-️-贡献者列表").

A header is prepended to each file: a language-switch line, a line to the live site whose
link text is the full URL, the attribution/removal notice (read verbatim from
overrides/main.html's `announce` Jinja block, so a wording edit there cannot drift from
what ships here -- its current wording is an open owner decision, read as-is), and one
sentence noting that the star/fork/issue badges and the Star History chart below belong to
the upstream repository (its numbers, not the fork's; translation errors go to the fork's
own issue tracker instead).

Usage:
  build_github_readme.py            write .github/README.md and .github/README.en.md
  build_github_readme.py --check    exit 1 if either file would differ from what this
                                     writes, or a post-condition below fails; writes nothing

Post-conditions (on any failure: nothing is written, the error is printed, exit 1):
  - every link/image target is http(s), mailto, a "/"-rooted repo path that exists, a
    same-directory README link (README.md, README.en.md), or a "#fragment" matching a
    GitHub heading slug in the same file;
  - no github.com/Lordog/dive-into-llms/(tree|blob)/main/ link remains (every upstream
    link must be pinned to the SHA, like the site);
  - no Han character outside i18n/allowlist.yaml's entries, plus the zh switch label 中文
    (the switch label is this script's own addition, not a translated string, so it is not
    added to the shared allowlist file);
  - every live-site URL's page exists under site/ (MkDocs' own output). Skipped, with a
    one-line warning, when site/ does not exist yet -- run `mkdocs build` first for a real
    check (PUBLISH.md step 0 and .github/workflows/pages.yml both do this already).
"""
from __future__ import annotations

import posixpath
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_links import (  # noqa: E402
    ROOT,
    PageContext,
    check_target,
    explicit_anchors,
    headings,
    heading_ids,
    link_targets,
    rewrite,
)
from i18n_render_check import han_outside, load_allowlist  # noqa: E402

LANGS = ("vi", "en")
GITHUB_DIR = ROOT / ".github"
FILES = {"vi": GITHUB_DIR / "README.md", "en": GITHUB_DIR / "README.en.md"}
TRANSLATED = {lang: ROOT / "i18n" / "translated" / lang / "README.md" for lang in LANGS}
OVERRIDES = ROOT / "overrides" / "main.html"
SITE_DIR = ROOT / "site"

SITE_BASE = "https://duypham9895.github.io/dive-into-llms/"
SITE_URL = {"vi": SITE_BASE, "en": SITE_BASE + "en/"}
ISSUES_URL = "https://github.com/duypham9895/dive-into-llms/issues"
UPSTREAM_MAIN_LINK = re.compile(r"github\.com/Lordog/dive-into-llms/(tree|blob)/main/")
SAME_DIR_LINKS = frozenset({"README.md", "README.en.md"})
# "中文" is this script's own switch-label text, not translated content, so it is kept here
# rather than added to the shared i18n/allowlist.yaml (out of scope for this change).
EXTRA_HAN_ALLOWED = ("中文",)

HEADER = {
    "vi": {
        "lang_line": "**Tiếng Việt** · [English](README.en.md) · [中文 (bản gốc)](/README.md)",
        "site_line": "📖 Đọc bản dịch trên web: [{url}]({url})",
        "badge_note": (
            "Huy hiệu sao/fork/issue, huy hiệu \"PRs Welcome\", biểu đồ Star History, và mục "
            "\"Contributing\" bên dưới đều là của repo gốc (Lordog/dive-into-llms), không "
            "phải của bản fork này -- chúng mời đóng góp vào dự án gốc, không phải vào bản "
            f"dịch này. Lỗi bản dịch: mở issue tại [{ISSUES_URL}]({ISSUES_URL})."
        ),
    },
    "en": {
        "lang_line": "[Tiếng Việt](README.md) · **English** · [中文 (original)](/README.md)",
        "site_line": "📖 Read the translation on the web: [{url}]({url})",
        "badge_note": (
            "The star/fork/issue badges, the \"PRs Welcome\" badge, the Star History chart, "
            "and the \"Contributing\" section below all belong to the original repository "
            "(Lordog/dive-into-llms), not to this fork -- they invite contributions to the "
            "original project, not to this translation. "
            f"Translation errors: open an issue at [{ISSUES_URL}]({ISSUES_URL})."
        ),
    },
}

_ANCHOR = re.compile(r'<a\s+href="([^"]+)"\s*>([^<]*)</a>')
_ANNOUNCE_BLOCK = re.compile(r"\{%-?\s*block announce\s*-?%\}(.*?)\{%-?\s*endblock\s*-?%\}", re.S)
_ANNOUNCE_IF = re.compile(
    r'\{%-?\s*if config\.theme\.language == "en" -?%\}(.*?)'
    r'\{%-?\s*else\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}',
    re.S,
)
# R1 targets are the only kind of relative, scheme-less ".md" link rewrite() can produce
# for the home page (see i18n_links.resolve/_resolve_repo_path): always "<dir>/<name>.md",
# i.e. holds a "/", which is what tells one apart from this file's own same-dir links.
_REL_MD_LINK = re.compile(r"\]\((?P<path>[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.md)\)")


# --- GitHub's own heading-slug rule -------------------------------------------------

def github_slug(text: str) -> str:
    """One heading's slug, GitHub's rule (see module docstring for how it was read off
    a live render). Unlike the site's pymdownx slugger, punctuation is deleted outright,
    never turned into "-", and a combining mark survives on its own."""
    text = text.lower()
    kept = [
        ch for ch in text
        if unicodedata.category(ch)[0] in ("L", "M", "N")
        or unicodedata.category(ch) == "Pc"
        or ch in (" ", "-")
    ]
    return "".join(kept).replace(" ", "-")


def github_slugs(texts: list[str]) -> list[str]:
    """Slugs for headings in document order, with GitHub's de-duplication: the 2nd
    heading with the same slug gets "-1", the 3rd gets "-2", and so on."""
    seen: dict[str, int] = {}
    out = []
    for t in texts:
        slug = github_slug(t)
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        out.append(slug if n == 0 else f"{slug}-{n}")
    return out


def _retarget_fragments(text: str) -> str:
    """Replace every in-page "#<site-slug>" left by rewrite() with GitHub's slug for the
    SAME heading (same position): rewrite()'s anchor_map already matched each fragment to
    the right translated heading; only the slug dialect needs to change here. The README's
    TOC links are raw HTML (href="#id"), not Markdown links, so both quoting styles are
    matched: "#id" is replaced wherever it is immediately followed by a closing paren or
    quote, never in the middle of a longer id."""
    site_ids = heading_ids(text)
    texts = headings(text)
    if len(site_ids) != len(texts):
        raise ValueError(f"heading_ids/headings length mismatch: {len(site_ids)} vs {len(texts)}")
    gh_ids = github_slugs(texts)
    for site_id, gh_id in sorted(zip(site_ids, gh_ids), key=lambda p: -len(p[0])):
        pattern = re.compile(r"#" + re.escape(site_id) + r"(?=[\"'\)])")
        text = pattern.sub("#" + gh_id, text)
    return text


# --- site-relative link -> live URL -------------------------------------------------

def live_url(lang: str, page: str) -> str:
    """Live-site URL for a site page (relative to docs/<lang>/), mirroring MkDocs'
    use_directory_urls (README.md/index.md -> its own directory; see i18n_render_check's
    built_path, which this mirrors for the live site instead of the local site/ tree)."""
    stem = posixpath.splitext(page)[0]
    name, folder = posixpath.basename(stem), posixpath.dirname(stem)
    dir_path = folder if name in ("index", "README") else posixpath.join(folder, name)
    return SITE_URL[lang] + (dir_path + "/" if dir_path else "")


def _site_file_for(lang: str, page: str) -> Path:
    """Local site/ output expected for the same page, for the --check post-condition."""
    stem = posixpath.splitext(page)[0]
    name, folder = posixpath.basename(stem), posixpath.dirname(stem)
    dir_path = folder if name in ("index", "README") else posixpath.join(folder, name)
    prefix = "" if lang == "vi" else "en"
    rel = posixpath.join(*(p for p in (prefix, dir_path, "index.html") if p))
    return SITE_DIR / rel


def _retarget_urls(text: str, lang: str) -> tuple[str, list[str]]:
    """Turn every R1 relative ".md" target into its live URL; return the rewritten text
    and the list of site pages it now points at (for the live-site existence check)."""
    used: list[str] = []

    def repl(m: re.Match[str]) -> str:
        page = m.group("path")
        used.append(page)
        return f"]({live_url(lang, page)})"

    return _REL_MD_LINK.sub(repl, text), used


# --- the attribution/removal notice, read from overrides/main.html -----------------

def _announce_branches() -> tuple[str, str]:
    """(en, vi) raw Jinja text of overrides/main.html's announce block."""
    html = OVERRIDES.read_text(encoding="utf-8")
    block = _ANNOUNCE_BLOCK.search(html)
    if not block:
        raise ValueError(f"{OVERRIDES}: no {{% block announce %}} found")
    branches = _ANNOUNCE_IF.search(block.group(1))
    if not branches:
        raise ValueError(f"{OVERRIDES}: announce block has no en/else branch")
    return branches.group(1), branches.group(2)


def _html_block_to_md(raw: str) -> str:
    text = _ANCHOR.sub(r"[\2](\1)", raw)
    return " ".join(text.split())


def announce_text(lang: str) -> str:
    en, vi = _announce_branches()
    return _html_block_to_md(en if lang == "en" else vi)


# --- assembling one language's file -------------------------------------------------

def _generate_body(lang: str) -> tuple[str, list[str]]:
    translated = TRANSLATED[lang].read_text(encoding="utf-8")
    source_text = (ROOT / "README.md").read_text(encoding="utf-8")
    ctx = PageContext("README.md", "index.md", lang, source_text)
    rewritten, _notes, _log = rewrite(translated, ctx)
    rewritten = _retarget_fragments(rewritten)
    return _retarget_urls(rewritten, lang)


def build(lang: str) -> tuple[str, list[str]]:
    body, pages_used = _generate_body(lang)
    h = HEADER[lang]
    header = "\n\n".join([
        h["lang_line"],
        h["site_line"].format(url=SITE_URL[lang]),
        announce_text(lang),
        h["badge_note"],
        "---",
    ])
    text = header + "\n\n" + body.lstrip("\n")
    if not text.endswith("\n"):
        text += "\n"
    return text, pages_used


def generate() -> dict[str, tuple[str, list[str]]]:
    return {lang: build(lang) for lang in LANGS}


# --- post-conditions -----------------------------------------------------------------

def _check_links(text: str) -> list[str]:
    errors: list[str] = []
    final_ids = set(github_slugs(headings(text)))
    anchors = explicit_anchors(text)
    for kind, target in link_targets(text):
        target = target.strip()
        if not target:
            continue
        check_target(target)  # raises ValueError on a disallowed scheme
        if re.match(r"(?i)https?://", target):
            if UPSTREAM_MAIN_LINK.search(target):
                errors.append(f"{kind} {target!r} points at an upstream /main/ link, not the pinned SHA")
            continue
        if target.lower().startswith("mailto:"):
            continue
        if target.startswith("#"):
            frag = target[1:]
            if frag not in final_ids and frag not in anchors:
                errors.append(f"{kind} fragment {target!r} matches no heading slug")
            continue
        if target.startswith("/"):
            if not (ROOT / target[1:]).exists():
                errors.append(f"{kind} repo-root target does not exist: {target!r}")
            continue
        if target in SAME_DIR_LINKS:
            continue
        errors.append(f"{kind} target not allowed by the post-conditions: {target!r}")
    return errors


def _check_han(text: str) -> list[str]:
    allowed = sorted(set(load_allowlist()) | set(EXTRA_HAN_ALLOWED), key=len, reverse=True)
    runs = han_outside(text, allowed)
    return [f"Han outside the allow-list: {len(runs)} runs, e.g. {runs[:3]}"] if runs else []


def _check_site_pages(lang: str, pages_used: list[str]) -> list[str]:
    if not SITE_DIR.exists():
        print(f"warning: {SITE_DIR} missing; skipping the live-URL-exists check (run mkdocs build)", file=sys.stderr)
        return []
    errors = []
    for page in pages_used:
        f = _site_file_for(lang, page)
        if not f.exists():
            errors.append(f"live URL for {page!r} has no built page: {f.relative_to(ROOT)}")
    return errors


def validate(lang: str, text: str, pages_used: list[str]) -> list[str]:
    errors = _check_links(text)
    errors += _check_han(text)
    errors += _check_site_pages(lang, pages_used)
    return [f"{lang}: {e}" for e in errors]


def main(argv: list[str]) -> int:
    if argv not in ([], ["--check"]):
        print(__doc__, file=sys.stderr)
        return 2
    check_only = argv == ["--check"]
    try:
        data = generate()
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 1

    errors: list[str] = []
    for lang in LANGS:
        text, pages_used = data[lang]
        errors += validate(lang, text, pages_used)
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1

    if check_only:
        stale = [
            str(FILES[lang].relative_to(ROOT))
            for lang in LANGS
            if not FILES[lang].exists() or FILES[lang].read_text(encoding="utf-8") != data[lang][0]
        ]
        if stale:
            print("stale: " + ", ".join(stale))
            return 1
        print("ok: .github/README.md and .github/README.en.md match i18n/translated/")
        return 0

    for lang in LANGS:
        FILES[lang].write_text(data[lang][0], encoding="utf-8")
    print("wrote " + ", ".join(str(FILES[lang].relative_to(ROOT)) for lang in LANGS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
