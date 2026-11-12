#!/usr/bin/env python3
"""Assemble the MkDocs docs/ tree from translations (or, for the spike, from the sources).

Pipeline per page: translated text -> link rewrite map (i18n_links) -> normalise
(i18n_normalize) -> translator's notice, if PAGE_NOTICES names the page -> docs/<lang>/<page>. Notebooks go through build_notebooks first.
Slide notes are only normalised, and may hold absolute http(s) links only.
docs/vi and docs/en are cleared first, so nothing from an earlier run is built.

Layout of translations (mirrors upstream paths):
  i18n/translated/<lang>/README.md
  i18n/translated/<lang>/documents/chapterN/README.md
  i18n/translated/<lang>/documents/chapterN/<notebook>.ipynb   (ch4, ch9, ch11 only)
  i18n/translated/<lang>/slides/chapterN.md                    (slide notes)

Usage:
  assemble_docs.py                 build docs/vi and docs/en from i18n/translated/
  assemble_docs.py --spike OUT     render-test build: the Chinese sources stand in for
                                   both languages; writes OUT/docs and OUT/mkdocs.yml
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_notebooks import to_markdown  # noqa: E402
from i18n_links import ROOT, UNIQUE_NOTEBOOKS, PageContext, check_external_only, rewrite, source_files  # noqa: E402
from i18n_normalize import normalize  # noqa: E402

LANGS = ("vi", "en")

# Translator's notices (plan v5, "Per-chapter notices"): page -> notice key. The text is
# i18n/notices/<lang>/<key>.md, inserted right after the page's first heading. A line
# "{{quote PATH}}" or "{{fence PATH}}" in a notice is replaced by the file at PATH (repo
# root relative, kept byte-identical to the fetched licence text; see legal/licences.json)
# as blockquote lines or as a ```text fence.
NOTICES_DIR = ROOT / "i18n" / "notices"
PAGE_NOTICES = {
    "chapter6/README.md": "dual-use",
    "chapter7/README.md": "dual-use",
    "chapter10/README.md": "dual-use",
    "chapter8/README.md": "chapter8-nextgpt",
    "chapter11/README.md": "chapter11-sources",
    "chapter11/RLHF.md": "chapter11-sources",
}
# Slide-notes pages by deck stem (pre-publish review: the security decks need it as well).
SLIDE_NOTICES = {"chapter6": "dual-use", "chapter7": "dual-use", "chapter10": "dual-use"}
_INCLUDE = re.compile(r"^\{\{(quote|fence) ([^{}\s]+)\}\}$")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_HEADING = re.compile(r"^ {0,3}(#{1,6}(\s|$)|<h[1-6][\s>])")


def notice_text(lang: str, key: str) -> str:
    """The notice with its {{quote}}/{{fence}} lines expanded."""
    out: list[str] = []
    for line in (NOTICES_DIR / lang / f"{key}.md").read_text(encoding="utf-8").splitlines():
        m = _INCLUDE.match(line)
        if not m:
            out.append(line)
            continue
        verbatim = (ROOT / m.group(2)).read_text(encoding="utf-8").rstrip("\n").split("\n")
        if m.group(1) == "quote":
            out.extend(f"> {v}".rstrip() for v in verbatim)
        else:
            if any(v.startswith("```") for v in verbatim):
                raise ValueError(f"{m.group(2)} holds a ``` line; it cannot be fenced")
            out.extend(["```text", *verbatim, "```"])
    text = "\n".join(out)
    if "{{" in text:
        raise ValueError(f"notice {lang}/{key}: unexpanded '{{{{' left")
    return text


def insert_notice(page_text: str, notice: str, where: str) -> str:
    """Insert the notice (then a thematic break) after the first heading outside fences."""
    lines = page_text.split("\n")
    fence: str | None = None
    for i, line in enumerate(lines):
        m = _FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        if _HEADING.match(line):
            return "\n".join(lines[: i + 1] + ["", notice, "", "---", ""] + lines[i + 1 :])
    raise ValueError(f"{where}: no heading to put the notice after")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def build_page(source_rel: str, page: str, lang: str, source_text: str, translated: str) -> str:
    rewritten, _notes, _log = rewrite(translated, PageContext(source_rel, page, lang, source_text))
    return normalize(rewritten)


def _clear(docs: Path) -> None:
    """Remove docs/vi and docs/en before writing, so a page left by an earlier run (or
    any extra file) cannot be built and pass the render check. Only these two folders,
    and only directly inside docs, are ever removed."""
    base = docs.resolve()
    for lang in LANGS:
        folder = docs / lang
        if folder.is_symlink():
            raise ValueError(f"{folder} is a symlink; refusing to clear it")
        if folder.resolve().parent != base:
            raise ValueError(f"{folder} is not directly inside {base}")
        if folder.exists():
            shutil.rmtree(folder)


def assemble(docs: Path, translation_root: Path | None) -> list[str]:
    """Write every page for both languages; return the written docs paths.
    translation_root None = spike: the upstream source stands in for the translation."""
    _clear(docs)
    written: list[str] = []
    if translation_root is not None:
        pages = {page for _, page, _ in source_files()}
        missing = sorted(p for p in PAGE_NOTICES if p not in pages)
        if missing:
            raise ValueError(f"notices name pages that are not built: {missing}")
    for lang in LANGS:
        for source_rel, page, source_text in source_files():
            origin = ROOT / source_rel if translation_root is None else translation_root / lang / source_rel
            if source_rel in UNIQUE_NOTEBOOKS:
                translated = to_markdown(origin, lang, source_rel)
                source_md = to_markdown(ROOT / source_rel, lang, source_rel)  # anchors resolve against it
            else:
                translated = origin.read_text(encoding="utf-8")
                source_md = source_text
            out = docs / lang / page
            text = build_page(source_rel, page, lang, source_md, translated)
            if translation_root is not None and page in PAGE_NOTICES:
                text = insert_notice(text, notice_text(lang, PAGE_NOTICES[page]), str(out))
            _write(out, text)
            written.append(str(out))
        if translation_root is not None:
            for slides in sorted((translation_root / lang / "slides").glob("chapter*.md")):
                # Slide notes have no link map: only absolute http(s) links may appear.
                out = docs / lang / slides.stem / "slides.md"
                text = normalize(slides.read_text(encoding="utf-8"))
                check_external_only(text, str(slides))
                if slides.stem in SLIDE_NOTICES:  # the dual-use decks carry the notice too
                    text = insert_notice(text, notice_text(lang, SLIDE_NOTICES[slides.stem]), str(out))
                _write(out, text)
                written.append(str(out))
    return written


def write_spike_config(out: Path) -> None:
    _write(
        out / "mkdocs.yml",
        f"INHERIT: {ROOT / 'mkdocs.yml'}\n"
        "docs_dir: docs\n"
        "site_dir: site\n"
        "theme:\n"
        f"  custom_dir: {ROOT / 'overrides'}\n",
    )


def main(argv: list[str]) -> int:
    if argv[:1] == ["--spike"] and len(argv) == 2:
        out = Path(argv[1]).resolve()
        written = assemble(out / "docs", None)
        write_spike_config(out)
        print(f"spike: {len(written)} pages under {out / 'docs'}")
        return 0
    if not argv:
        written = assemble(ROOT / "docs", ROOT / "i18n" / "translated")
        print(f"{len(written)} pages under {ROOT / 'docs'}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
