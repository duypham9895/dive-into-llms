#!/usr/bin/env python3
"""Assemble the MkDocs docs/ tree from translations (or, for the spike, from the sources).

Pipeline per page: translated text -> link rewrite map (i18n_links) -> normalise
(i18n_normalize) -> docs/<lang>/<page>. Notebooks go through build_notebooks first.
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

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_notebooks import to_markdown  # noqa: E402
from i18n_links import ROOT, UNIQUE_NOTEBOOKS, PageContext, check_external_only, rewrite, source_files  # noqa: E402
from i18n_normalize import normalize  # noqa: E402

LANGS = ("vi", "en")


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
            _write(out, build_page(source_rel, page, lang, source_md, translated))
            written.append(str(out))
        if translation_root is not None:
            for slides in sorted((translation_root / lang / "slides").glob("chapter*.md")):
                # Slide notes have no link map: only absolute http(s) links may appear.
                out = docs / lang / slides.stem / "slides.md"
                text = normalize(slides.read_text(encoding="utf-8"))
                check_external_only(text, str(slides))
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
