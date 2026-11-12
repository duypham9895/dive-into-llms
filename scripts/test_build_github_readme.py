#!/usr/bin/env python3
"""Cases for the GitHub README generator (plan v1, R1 P1).

The slug cases pin GitHub's heading-id rule against ids copied verbatim from a live GET
of the upstream README (gh api -H 'Accept: application/vnd.github.html'
repos/Lordog/dive-into-llms/readme, 2026-11-12; the id on the page is "user-content-"
plus the slug asserted here -- in-page links on the real page use the bare slug, as the
same GET shows: the TOC's `<a href="#项目动机">` is not itself prefixed). That GET is the
ground truth for P1 (blocker 1 of the plan review: an emoji's own symbol is dropped, but
a combining mark right after it, such as U+FE0F, survives and is not something this
repo's own slugifiers do the same way -- see the dedicated case below). Every other case
exercises the one rule those ids pin down, not a second live render.

Run from the repo root: .venv/bin/python scripts/test_build_github_readme.py
Exit status 0 when every case passes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_github_readme import (  # noqa: E402
    FILES,
    ROOT,
    _check_han,
    _check_links,
    _generate_body,
    _retarget_fragments,
    _retarget_urls,
    announce_text,
    generate,
    github_slug,
    github_slugs,
    live_url,
    validate,
)
from i18n_links import PageContext, rewrite  # noqa: E402

RESULTS: list[bool] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}")


def main() -> int:
    # --- github_slug against ids read live off the real upstream README ------------------
    # Each pair is (heading text, "user-content-"-stripped id), copied from the GET above.
    UPSTREAM_IDS = [
        ("《动手学大模型》系列编程实践教程", "动手学大模型系列编程实践教程"),  # book-title marks dropped, no case
        ("💡 Updates", "-updates"),  # emoji (So) dropped, leaves a leading space -> "-"
        ("🎯 项目动机", "-项目动机"),
        ("📚 教程目录", "-教程目录"),
        ("🔥 新上线：国产化《大模型开发全流程》", "-新上线国产化大模型开发全流程"),  # colon + 《》 dropped too
        ("🙏 免责声明", "-免责声明"),
        ("🤝 欢迎贡献", "-欢迎贡献"),
        ("❤️ 贡献者列表", "️-贡献者列表"),  # the mark on the emoji survives; the emoji itself does not
        ("🌟 Star History", "-star-history"),  # English: lowercased, space -> "-"
    ]
    for text, expected in UPSTREAM_IDS:
        got = github_slug(text)
        check(f"github_slug matches the real GitHub id for {text!r}", got == expected, f"got {got!r}")

    # --- the same rule on text no real render was read for -------------------------------
    check(
        "Vietnamese diacritics kept (they are letters, category L, not marks)",
        github_slug("🎯 Động lực của dự án") == "-động-lực-của-dự-án",
        github_slug("🎯 Động lực của dự án"),
    )
    check(
        "curly quotes, a slash and a colon all dropped, not turned into '-'",
        github_slug("A “B/C”: D") == "a-bc-d",
        github_slug("A “B/C”: D"),
    )
    check(
        "an emoji-led English heading keeps no leading mark when the emoji has none",
        github_slug("🚀 Explore") == "-explore",
        github_slug("🚀 Explore"),
    )

    # --- de-duplication: 2nd occurrence "-1", 3rd "-2" ------------------------------------
    dups = github_slugs(["Tóm tắt", "Tóm tắt", "Tóm Tắt", "Khác"])
    check(
        "duplicate slugs numbered -1, -2 in document order; a case-only repeat still collides",
        dups == ["tóm-tắt", "tóm-tắt-1", "tóm-tắt-2", "khác"],
        str(dups),
    )

    # --- fragment retargeting: site slug -> GitHub slug, same heading ---------------------
    ch5_src = "# 标题\n\n见[项目动机](#项目动机)。\n\n## 🎯 项目动机\n\n正文。\n"
    ch5_tr = "# Tiêu đề\n\nXem [động lực](#项目动机).\n\n## 🎯 Động lực\n\nVăn bản.\n"
    out, _, _ = rewrite(ch5_tr, PageContext("README.md", "index.md", "vi", ch5_src))
    out = _retarget_fragments(out)
    check(
        "fragment retargeted from the site's slug to GitHub's slug for the same heading",
        "(#-động-lực)" in out,
        out,
    )

    # --- live URL mapping (MkDocs use_directory_urls) -------------------------------------
    check("index-like page maps to its own directory", live_url("vi", "chapter3/README.md") == "https://duypham9895.github.io/dive-into-llms/chapter3/")
    check("en prefix inserted", live_url("en", "chapter3/README.md") == "https://duypham9895.github.io/dive-into-llms/en/chapter3/")
    check(
        "a notebook page maps to a same-named subdirectory",
        live_url("vi", "chapter4/sft_math.md") == "https://duypham9895.github.io/dive-into-llms/chapter4/sft_math/",
    )

    # --- R1 relative targets become live URLs; same-dir README links are left alone -------
    body = "[a](chapter3/README.md) and [b](README.en.md) and [c](/README.md) and [d](https://example.com/x.md)"
    out, used = _retarget_urls(body, "vi")
    check(
        "only the relative <dir>/<file>.md target is converted; the rest pass through",
        out == "[a](https://duypham9895.github.io/dive-into-llms/chapter3/) and [b](README.en.md) "
        "and [c](/README.md) and [d](https://example.com/x.md)"
        and used == ["chapter3/README.md"],
        out,
    )

    # --- the real files: content matches what the generator would write, 0 errors --------
    data = generate()
    for lang in ("vi", "en"):
        text, pages_used = data[lang]
        on_disk = FILES[lang].read_text(encoding="utf-8")
        check(f"{lang}: .github file matches the generator's output", on_disk == text)
        errors = validate(lang, text, pages_used)
        check(f"{lang}: 0 post-condition errors on the real file", errors == [], "; ".join(errors))
        check(f"{lang}: no upstream /main/ link remains", "/main/" not in text, text[:0])
        check(f"{lang}: language line and site link present", "duypham9895.github.io/dive-into-llms" in text.splitlines()[2])

    # --- the attribution notice is read from overrides/main.html, not duplicated ----------
    html = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
    vi_sentence = re.search(r"Không liên kết.*?các tác giả gốc\.", html, re.S)
    en_sentence = re.search(r"Not affiliated.*?original authors\.", html, re.S)
    check(
        "the vi notice's core sentence is read verbatim from overrides/main.html",
        vi_sentence is not None and " ".join(vi_sentence.group(0).split()) in announce_text("vi"),
    )
    check(
        "the en notice's core sentence is read verbatim from overrides/main.html",
        en_sentence is not None and " ".join(en_sentence.group(0).split()) in announce_text("en"),
    )

    # --- post-conditions catch a bad link, as a translation edit could introduce one ------
    bad = "[x](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter1/README.md)"
    check("a /main/ link is caught", any("pinned SHA" in e for e in _check_links(bad)), str(_check_links(bad)))
    bad2 = "[x](chapter99/README.md)"
    check("an unrecognised relative target is caught", any("not allowed" in e for e in _check_links(bad2)), str(_check_links(bad2)))
    bad3 = "[x](#no-such-heading)"
    check("a fragment matching no heading is caught", any("matches no heading" in e for e in _check_links(bad3)), str(_check_links(bad3)))
    bad4 = "[x](//evil.example/p)"
    try:
        _check_links(bad4)
        check("a scheme-relative link raises", False, "no error raised")
    except ValueError:
        check("a scheme-relative link raises", True)

    # --- Han check: the switch label 中文 passes; a stray Han character does not ----------
    check("中文 alone passes (this script's own switch-label allowance)", _check_han("[中文](/README.md)") == [])
    check("an unlisted Han run is caught", _check_han("random 随便 text") != [])

    failures = RESULTS.count(False)
    print(f"{'all pass' if not failures else f'{failures} failing'} ({len(RESULTS)} cases)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
