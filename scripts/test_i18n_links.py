#!/usr/bin/env python3
"""Pin the link rewrite map against the ways a translation can slip a link past it.

Each case is a finding from code review round 1 (CORRECTNESS + BREAK-IT): a link the
old per-line regex mis-matched or never saw, a scheme or raw HTML attribute that
bypassed the map, and anchors that resolved to the wrong heading. Every case asserts
the new behaviour: the link is rewritten whole, or rewrite() raises.
The last case runs --check over the real 12 READMEs and 3 notebooks.

Run from the repo root: .venv/bin/python scripts/test_i18n_links.py
Exit status 0 when every case passes.
"""
from __future__ import annotations

import contextlib
import io
import re
import sys
from pathlib import Path

import markdown
from pymdownx.slugs import slugify

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_links import ROOT, PageContext, check_external_only, check_sources, rewrite  # noqa: E402

CH5 = "documents/chapter5/README.md"
CH5_TEXT = (ROOT / CH5).read_text(encoding="utf-8")
CH1 = "documents/chapter1/README.md"
CH1_TEXT = (ROOT / CH1).read_text(encoding="utf-8")
# As the root README links chapters. (A bare directory link goes to R7, the blob at the SHA.)
MAIN_CH3 = "https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter3/README.md"
RESULTS: list[bool] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}")


def ch5(snippet: str, source: str = CH5_TEXT) -> str:
    """Rewrite ch5 with snippet appended, as if a translator had added it."""
    text, _notes, _log = rewrite(CH5_TEXT + "\n\n" + snippet + "\n", PageContext(CH5, "chapter5/README.md", "vi", source))
    return text


def raises(snippet: str, pattern: str, source: str = CH5_TEXT, page_source: str | None = None) -> tuple[bool, str]:
    try:
        if page_source is None:
            ch5(snippet, source)
        else:
            rewrite(snippet, PageContext(CH5, "chapter5/README.md", "vi", page_source))
    except ValueError as exc:
        return re.search(pattern, str(exc)) is not None, str(exc)
    return False, "no error raised"


def tail(text: str) -> str:
    """The appended snippet: everything after ch5's last line."""
    return text.split("并评估其在不同攻击方法下的性能", 1)[1]


def main() -> int:
    # --- URL with parentheses (the ch1 WeChat link) ---------------------------------
    out, _, log = rewrite(CH1_TEXT, PageContext(CH1, "chapter1/README.md", "vi", CH1_TEXT))
    wechat = "https://mp.weixin.qq.com/s?__biz=Mzk0MTYzMzMxMA==&mid=2247484539&idx=1&sn=6ee42baab4ad792e74ac6a89d7dd87d9"
    check(
        "ch1 WeChat URL with build(23C71) rewritten whole",
        f"[综述]({wechat})（Word2Vec作者出品）" in out and "wx_header" not in out and "23C71" not in out,
    )
    t = tail(ch5("Xem [đây](https://example.com/a_(b)_c) nhé."))
    check("paren URL kept whole", "[đây](https://example.com/a_(b)_c) nhé." in t, t)
    t = tail(ch5(f"Xem [đây]({MAIN_CH3}?x=(1)) nhé."))
    check(
        "paren URL on an upstream path is matched as one link",
        t.count("](") == 1 and t.strip().endswith("?x=(1)) nhé.") and "/main/" not in t,
        t,
    )

    # --- link text wrapped over two lines ---------------------------------------------
    t = tail(ch5(f"Xem [kho mã\nX-SIR]({MAIN_CH3}) và tiếp."))
    check("multi-line link text rewritten (R1)", "[kho mã\nX-SIR](../chapter3/README.md)" in t and "tree/main" not in t, t)

    # --- titles and angle brackets ------------------------------------------------------
    t = tail(ch5(f"[c3]({MAIN_CH3} 'Chương 3')"))
    check("single-quoted title kept, target rewritten", "[c3](../chapter3/README.md 'Chương 3')" in t, t)
    t = tail(ch5(f"[c3]({MAIN_CH3} (Chương 3))"))
    check("parenthesised title kept, target rewritten", "[c3](../chapter3/README.md (Chương 3))" in t, t)
    t = tail(ch5(f'[c3]({MAIN_CH3} "Chương 3")'))
    check("double-quoted title kept, target rewritten", '[c3](../chapter3/README.md "Chương 3")' in t, t)
    t = tail(ch5(f"[c3](<{MAIN_CH3}>)"))
    check("angle-bracket destination rewritten", "[c3](<../chapter3/README.md>)" in t, t)

    # --- raw HTML attributes ------------------------------------------------------------
    t = tail(ch5(f"<a href={MAIN_CH3}>y</a>"))
    check("unquoted href rewritten", '<a href="../chapter3/README.md">y</a>' in t, t)
    t = tail(ch5(f"<a\n  href='{MAIN_CH3}'>y</a>"))
    check("single-quoted href on a wrapped tag rewritten", "href='../chapter3/README.md'" in t, t)
    ok, msg = raises("<a href=../chapter99/README.md>y</a>", r"no rule covers")
    check("unquoted relative href to a missing page raises", ok, msg)
    for snippet in (
        "<a href=javascript:alert(1)>x</a>",
        '<a href="javascript:alert(1)">x</a>',
        '<a href="&#106;avascript:alert(1)">x</a>',
        '<a href="java\tscript:alert(1)">x</a>',
        "[x](javascript:alert(1))",
        "[x](data:text/html,hi)",
        "![x](file:///etc/passwd)",
        "[x](//evil.example/p)",
    ):
        ok, msg = raises(snippet, r"not allowed")
        check(f"disallowed target raises: {snippet!r}", ok, msg)
    for snippet in (
        '<img srcset="a.png 1x">',
        "<video poster=a.png></video>",
        '<form action="https://x.example/"></form>',
        '<button formaction="https://x.example/">b</button>',
        "<div style=\"background: url('a.png')\">d</div>",
        '<div style="background: u\\rl(a.png)">d</div>',
    ):
        ok, msg = raises(snippet, r"not allowed")
        check(f"forbidden raw HTML attribute raises: {snippet!r}", ok, msg)
    t = tail(ch5('<p style="text-align: center;">c</p> [m](mailto:a@example.org)'))
    check("style without url() and mailto: pass", "mailto:a@example.org" in t, t)
    for snippet in (  # re-review 2: raw HTML outside the allow-list
        "<span onmouseover=alert(1)>x</span>",
        "<script>alert(1)</script>",
        "<iframe src=https://example.org></iframe>",
        "<object data=javascript:alert(1)></object>",
        '<svg><a xlink:href="javascript:alert(1)">x</a></svg>',
        '<meta http-equiv=refresh content="0;url=javascript:alert(1)">',
    ):
        ok, msg = raises(snippet, r"not allowed")
        check(f"raw HTML outside the allow-list raises: {snippet!r}", ok, msg)

    # --- heading ids come from Python-Markdown itself (re-review 2) -----------------------
    us_src = "# 标题\n\n见[第一](#数据a)。\n\n## 数据a\n\n一。\n\n## 数据b\n\n二。\n"
    us_tr = "# Tiêu đề\n\nXem [một](#数据a).\n\n## dataset_a\n\nMột.\n\n## dataseta\n\nHai.\n"
    out, _, _ = rewrite(us_tr, PageContext(CH5, "chapter5/README.md", "vi", us_src))
    built = markdown.markdown(out, extensions=["toc"], extension_configs={"toc": {"slugify": slugify(case="lower")}})
    ids = re.findall(r'<h2 id="([^"]+)"', built)
    check(
        "heading with '_' keeps its real toc id: link goes to the first heading",
        len(ids) == 2 and f"(#{ids[0]})" in out and ids[0] != ids[1],
        f"{out!r} ids={ids}",
    )

    # --- code is never rewritten -------------------------------------------------------
    t = tail(ch5("Dùng `[x](../chapter99/README.md)` và `<a href=javascript:x>`.\n\n```md\n[y](../chapter99/README.md)\n```"))
    check("links inside inline code and fences left alone", "`[x](../chapter99/README.md)`" in t and "[y](../chapter99" in t, t)

    # --- a badge image inside a link: both mapped ---------------------------------------
    t = tail(ch5(f"[![b](./assets/x-sir.png)]({MAIN_CH3})"))
    check("image inside link text rewritten too", "![b](https://raw.githubusercontent.com/" in t and "(../chapter3/README.md)" in t, t)

    # --- a link the regex cannot see must not ship ---------------------------------------
    ok, msg = raises(f"[a [b [c] d] e]({MAIN_CH3})", r"escaped the link map")
    check("Lordog /main/ link the regex misses is caught by the post-condition", ok, msg)

    # --- heading slug collision in the translation ---------------------------------------
    src = "# 标题\n\n见[第二节](#数据集合)。\n\n## 数据集\n\n文字一。\n\n## 数据集合\n\n文字二。\n"
    tr = "# Tiêu đề\n\nXem [mục hai](#数据集合).\n\n## Tập dữ liệu\n\nVăn bản một.\n\n## Tập dữ liệu\n\nVăn bản hai.\n"
    out, _, _ = rewrite(tr, PageContext(CH5, "chapter5/README.md", "vi", src))
    built = markdown.markdown(out, extensions=["toc"], extension_configs={"toc": {"slugify": slugify(case="lower")}})
    ids = re.findall(r'<h2 id="([^"]+)"', built)
    check(
        "colliding translated headings: link goes to the second one's id",
        "(#tập-dữ-liệu_1)" in out and len(ids) == 2 and ids[1] == "tập-dữ-liệu_1",
        f"{out!r} ids={ids}",
    )

    # A raw <h2> directly followed by an ATX heading: CommonMark swallows the ATX line into
    # the HTML block, Python-Markdown does not, so the same text yields different heading
    # counts (source side is counted by markdown-it, translation side by Python-Markdown).
    # No upstream source has this today; it must stay a loud error, never a silent misroute.
    raw_src = "# 标题\n\n见[下节](#下节)。\n\n<h2>原始</h2>\n# 下节\n\n文字。\n"
    raw_tr = "# Tiêu đề\n\nXem [mục sau](#下节).\n\n<h2>Thô</h2>\n# Mục sau\n\nVăn bản.\n"
    ok, msg = raises(raw_tr, r"heading count differs", page_source=raw_src)
    check("raw <h2> then ATX heading: heading count mismatch raises", ok, msg)

    # --- two source headings with the same anchor key -------------------------------------
    dup_src = "# 标题\n\n见[总结](#总结)。\n\n## 总结\n\n一。\n\n## 总结\n\n二。\n"
    dup_tr = "# Tiêu đề\n\nXem [tóm tắt](#总结).\n\n## Tóm tắt A\n\nMột.\n\n## Tóm tắt B\n\nHai.\n"
    ok, msg = raises(dup_tr, r"share", page_source=dup_src)
    check("source links to a key two source headings share: raises", ok, msg)
    named_src = dup_src.replace("见[总结](#总结)", '见[总结](#总结)<a name="总结"></a>')
    named_tr = dup_tr.replace("Xem [tóm tắt](#总结).", 'Xem [tóm tắt](#总结).<a name="总结"></a>')
    try:
        out, _, _ = rewrite(named_tr, PageContext(CH5, "chapter5/README.md", "vi", named_src))
        check("same, with an explicit <a name>: kept as-is", "(#总结)" in out)
    except ValueError as exc:
        check("same, with an explicit <a name>: kept as-is", False, str(exc))
    quiet_src = dup_src.replace("见[总结](#总结)。", "见总结。")
    ok, msg = raises(dup_tr, r"shared by two source headings", page_source=quiet_src)
    check("translation alone links to a shared key: raises", ok, msg)

    # --- slide notes: http(s) only --------------------------------------------------------
    try:
        check_external_only("## Slide 1\n\n[deck](https://github.com/Lordog/dive-into-llms/blob/x/a.pdf)\n", "slides")
        check("slide notes: http(s) link passes", True)
    except ValueError as exc:
        check("slide notes: http(s) link passes", False, str(exc))
    for snippet in ("[a](../chapter3/README.md)", "![a](pic.png)", '<a href="x.html">a</a>', "[a](#x)"):
        try:
            check_external_only(f"## Slide 1\n\n{snippet}\n", "slides")
            check(f"slide notes: non-http link raises: {snippet!r}", False, "no error raised")
        except ValueError:
            check(f"slide notes: non-http link raises: {snippet!r}", True)

    # --- the real sources still pass ------------------------------------------------------
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        status = check_sources()
    check("i18n_links.py --check on the 12 READMEs + 3 notebooks", status == 0, buf.getvalue()[-400:])

    failures = RESULTS.count(False)
    print(f"{'all pass' if not failures else f'{failures} failing'} ({len(RESULTS)} cases)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
