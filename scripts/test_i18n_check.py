#!/usr/bin/env python3
"""Adversarial cases for the block-level validator (i18n_check.py).

A synthetic Chinese page and a clean Vietnamese translation of it; each case breaks
the translation in one way a translator (an LLM) can, and asserts that the validator
fails for that reason. The clean translation must pass. Cases from code review
round 1 BREAK-IT (dropped paragraph, dropped list item, altered external URL,
translated fence info string) and N1 (a link compared with the rewrite of the SOURCE
link at the same position) are here, plus the rest of the validator's checks.

Review round "validator-pilot" (BLOCKERS 1-3 + the English-row note) adds the content
checks: sibling swaps, a dropped clause on a gloss-heavy line, code swallowed into a
comment, a translated English row; the reviewer's repros run on the real ch2 pilot and only
look at the errors the edit adds, because the pilot is being reworded in parallel.

The last cases are controls on the real corpus: the 12 READMEs and 3 notebooks,
pseudo-translated (Han in prose and comments replaced by Latin text, code and
protected literals untouched), must pass with no false positive; the untranslated
corpus must fail on Han; an empty translations root must fail.

Run from the repo root: .venv/bin/python scripts/test_i18n_check.py   (exit 0 = all pass)
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_check import (  # noqa: E402
    GLOSS_MARK,
    HAN,
    Settings,
    check_markdown_page,
    check_notebook,
    is_protected,
    load_allowlist,
    main,
    terms_in,
)
from i18n_links import ROOT, UNIQUE_NOTEBOOKS  # noqa: E402

REL = "documents/chapter5/README.md"  # link context: relative links resolve from chapter5
SETTINGS = Settings(allowed=tuple(load_allowlist()))
RESULTS: list[bool] = []

SRC = """# 第一章 大模型水印

这是第一段，介绍了本章的主要内容和学习目标。

这是第二段，讲述了如何安装实验环境以及准备数据。

- 第一项：准备好模型参数和相关的配置文件
- 第二项：下载数据集并检查数据格式是否正确
    - 嵌套项：检查数据的长度分布是否合理

| 名称 | 说明 |
|---|---|
| 模型 | 用于生成文本的大规模语言模型 |

> 注意：请先阅读相关论文，再动手进行实验。

参考[第三章](../chapter3/README.md)和[论文](https://arxiv.org/abs/2401.00001)，安装步骤见[安装](#安装环境)。

![水印示意图](./assets/x-sir.png)

## 安装环境

```bash
# 安装依赖
pip install -r requirements.txt
```

```python
prompt = '用萝卜、土豆、茄子做饭，给我个菜谱。'
print(prompt)
```

```python
# 加载模型
model = load("gpt2")
```
"""

TGT = f"""# Chương 1: Watermark cho mô hình lớn

Đây là đoạn thứ nhất, giới thiệu nội dung chính và mục tiêu học tập của chương này.

Đây là đoạn thứ hai, hướng dẫn cách cài đặt môi trường thí nghiệm và chuẩn bị dữ liệu.

- Mục thứ nhất: chuẩn bị sẵn tham số mô hình và các tệp cấu hình liên quan
- Mục thứ hai: tải tập dữ liệu xuống và kiểm tra định dạng dữ liệu có đúng không
    - Mục lồng: kiểm tra phân bố độ dài của dữ liệu có hợp lý không

| Tên | Mô tả |
|---|---|
| Mô hình | Mô hình ngôn ngữ quy mô lớn dùng để sinh văn bản |

> Lưu ý: hãy đọc các bài báo liên quan trước, rồi mới bắt tay vào làm thí nghiệm.

Tham khảo [Chương 3](../chapter3/README.md) và [bài báo](https://arxiv.org/abs/2401.00001); các bước cài đặt xem ở [Cài đặt](#安装环境).

![Sơ đồ minh hoạ watermark](./assets/x-sir.png)

## Cài đặt môi trường

```bash
# Cài các thư viện phụ thuộc
pip install -r requirements.txt
```

```python
prompt = '用萝卜、土豆、茄子做饭，给我个菜谱。'
print(prompt)
```

{GLOSS_MARK}
*Prompt trên có nghĩa: "Nấu ăn với củ cải, khoai tây và cà tím, cho tôi một công thức."*

```python
# Tải mô hình
model = load("gpt2")
```
"""


# Item 1 (review BLOCKER 1): siblings with the same block type but different content.
FP_SRC = """# 实验

1. 使用GPT-2模型在GSM8K上训练3轮。
2. 运行`eval.py`，在MATH上评估准确率。

先安装PyTorch 2.1，再下载权重。

然后在第8张显卡上运行DeepSpeed。

Openai：https://platform.openai.com/playground

See the original paper for details.
"""

FP_TGT = """# Thí nghiệm

1. Dùng mô hình GPT-2 huấn luyện 3 vòng trên GSM8K.
2. Chạy `eval.py` để đánh giá độ chính xác trên MATH.

Cài PyTorch 2.1 trước, rồi tải trọng số.

Sau đó chạy DeepSpeed trên GPU thứ 8.

OpenAI: https://platform.openai.com/playground

See the original paper for details.
"""

# Item 3 (review BLOCKER 3): a statement swallowed into a comment, as in ch2 README:51.
SW_SRC = """```python
x = 1
# 打印结果。if x == 1:
    print(x)
```
"""
SW_TGT = """```python
x = 1
# In kết quả.if x == 1:
    print(x)
```
"""
PILOT = "documents/chapter2/README.md"


def swap(text: str, a: str, b: str) -> str:
    assert a in text and b in text, f"swap: {a!r} or {b!r} not in the text"
    return text.replace(a, "\x00").replace(b, a).replace("\x00", b)


def pilot_new_errors(lang: str, edit) -> tuple[list[str], list[str]]:
    """(errors the edit adds to the real ch2 pilot, errors of the unedited pilot). The
    pilot is being reworded while this runs, so a case only looks at the errors it adds."""
    src = (ROOT / PILOT).read_text(encoding="utf-8")
    tgt = (ROOT / "i18n/translated" / lang / PILOT).read_text(encoding="utf-8")
    base = check_markdown_page(PILOT, lang, src, tgt, SETTINGS).errors
    edited = edit(tgt)
    assert edited != tgt, "edit changed nothing: the pilot wording moved"
    return [e for e in check_markdown_page(PILOT, lang, src, edited, SETTINGS).errors if e not in base], base


def pilot_fail(name: str, lang: str, edit, pattern: str) -> None:
    added, _ = pilot_new_errors(lang, edit)
    check(name, any(re.search(pattern, e) for e in added), f"expected /{pattern}/, got {added}")


def _objectives(tgt: str, i: int, j: int) -> str:
    """Swap items i and j of the first ordered list (ch2 objectives), whatever their wording."""
    lines = tgt.split("\n")
    first = next(k for k, line in enumerate(lines) if line.startswith("1. "))
    a, b = first + i - 1, first + j - 1
    assert lines[a].startswith(f"{i}. ") and lines[b].startswith(f"{j}. "), (lines[a], lines[b])
    lines[a], lines[b] = f"{i}. " + lines[b][3:], f"{j}. " + lines[a][3:]
    return "\n".join(lines)


def _drop_few_shot(tgt: str) -> str:
    """Drop the few-shot clause of ch2 objective 2 (vi line 8), keeping the rest."""
    lines = tgt.split("\n")
    k = next(k for k, line in enumerate(lines) if re.match(r"(2\.|-) ", line) and "few-shot" in line)
    lines[k] = re.sub(r"\s+(?:và|and)\s+few-shot(?:\s*\([^)]*\))?", "", lines[k], count=1)
    return "\n".join(lines)


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}")


def errors_of(tgt: str, src: str = SRC) -> list[str]:
    return check_markdown_page(REL, "vi", src, tgt, SETTINGS).errors


def expect_fail(name: str, old: str, new: str, pattern: str, count: int = 1) -> None:
    """Apply one edit to the clean translation; the validator must fail with pattern."""
    assert TGT.count(old) >= 1, f"case {name}: {old!r} not in the clean translation"
    errors = errors_of(TGT.replace(old, new, count))
    hit = any(re.search(pattern, e) for e in errors)
    check(name, hit, f"expected /{pattern}/, got {errors}")


def nb(cells: list[dict]) -> dict:
    return {"cells": cells, "metadata": {"kernelspec": {"language": "python"}}, "nbformat": 4, "nbformat_minor": 5}


def md_cell(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text: str, outputs: list | None = None) -> dict:
    return {"cell_type": "code", "metadata": {}, "execution_count": 1, "source": text.splitlines(keepends=True),
            "outputs": outputs or []}


OUT = [{"output_type": "stream", "name": "stdout", "text": ["42\n"]}]
NB_SRC = nb([
    md_cell("## 加载数据\n\n这一步我们使用datasets的接口来加载训练数据集。"),
    code_cell("# 使用datasets的api来加载数据集\nds = load_dataset('gsm8k')\nprint(len(ds))", OUT),
])
NB_TGT = nb([
    md_cell("## Tải dữ liệu\n\nỞ bước này chúng ta dùng giao diện của datasets để tải tập dữ liệu huấn luyện."),
    code_cell("# Dùng API của datasets để tải tập dữ liệu\n# (bình luận dài, xuống dòng)\nds = load_dataset('gsm8k')\nprint(len(ds))", OUT),
])
NB_REL = "documents/chapter4/sft_math.ipynb"


def nb_errors(tgt: dict) -> list[str]:
    return check_notebook(NB_REL, "vi", NB_SRC, tgt, SETTINGS).errors


def nb_fail(name: str, edit, pattern: str) -> None:
    tgt = copy.deepcopy(NB_TGT)
    edit(tgt)
    errors = nb_errors(tgt)
    check(name, any(re.search(pattern, e) for e in errors), f"expected /{pattern}/, got {errors}")


# --- pseudo-translation of the real corpus (false-positive control) --------------------

_KEEP = re.compile(r"(`+)[^`]*?\1|\]\([^)]*\)|\b(?:href|src|name|id)\s*=\s*\"[^\"]*\"")


def _latin(run: re.Match[str]) -> str:
    return "vi" * len(run.group(0)) + "a" * len(run.group(0))  # ~3 Latin letters per Han


def _prose(line: str) -> str:
    """Replace Han in a prose line, leaving inline code, link targets and HTML ids alone.
    The first Han run also gets the vi rendering of every checked glossary term in the
    line, as a real translation carries them (G3), so the term check has no false alarm."""
    prose = _KEEP.sub(" ", line)
    extra = [t.vi[0] for t in terms_in(prose, SETTINGS.terms) if t.checked]
    first = [True]

    def latin(run: re.Match[str]) -> str:
        if first[0] and extra:
            first[0] = False
            return _latin(run) + " " + " ".join(extra) + " "
        return _latin(run)

    def keep(span: str) -> str:
        # Inline code holding Han is emphasis and gets translated (policy 2026-11-12).
        if span.startswith("`") and HAN.search(span):
            return re.sub(f"{HAN.pattern}+", _latin, span)
        return span

    out, pos = [], 0
    for m in _KEEP.finditer(line):
        out.append(re.sub(f"{HAN.pattern}+", latin, line[pos:m.start()]) + keep(m.group(0)))
        pos = m.end()
    out.append(re.sub(f"{HAN.pattern}+", latin, line[pos:]))
    return "".join(out)


def _comment(line: str) -> str:
    i = line.find("#")
    return line if i < 0 else line[:i] + re.sub(f"{HAN.pattern}+", _latin, line[i:])


def pseudo_translate(text: str) -> str:
    """Han in prose -> Latin; code fences keep their code, only comments change;
    protected literals are copied; the ch3 prose fence is translated line by line."""
    lines, out, fence, info, body = text.split("\n"), [], None, "", []
    for line in lines:
        m = re.match(r"^\s*(?:[-*+]\s+)?(`{3,}|~{3,})(.*)$", line)
        if fence is None and m:
            fence, info, body = m.group(1), m.group(2), []
            out.append(line)
        elif fence is not None and line.strip().startswith(fence) and not line.strip().strip(fence[0]):
            code = "\n".join(body)
            if "（可选）" in code:
                out.extend(_prose(b) for b in body)
            elif is_protected(code, info):
                out.extend(body)
            else:
                out.extend(_comment(b) for b in body)
            out.append(line)
            fence = None
        elif fence is not None:
            body.append(line)
        else:
            out.append(_prose(line))
    out.extend(body if fence is not None else [])
    return "\n".join(out)


def corpus_root(tmp: Path, translate: bool) -> Path:
    paths = ["README.md"] + [f"documents/chapter{i}/README.md" for i in range(1, 12)] + sorted(UNIQUE_NOTEBOOKS)
    for rel in paths:
        src = (ROOT / rel).read_text(encoding="utf-8")
        dest = tmp / "vi" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not translate:
            dest.write_text(src, encoding="utf-8")
        elif rel.endswith(".ipynb"):
            data = json.loads(src)
            for cell in data["cells"]:
                text = "".join(cell["source"])
                text = pseudo_translate(text) if cell["cell_type"] == "markdown" else "\n".join(
                    _comment(line) for line in text.split("\n"))
                cell["source"] = text.splitlines(keepends=True)
            dest.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        else:
            dest.write_text(pseudo_translate(src), encoding="utf-8")
    return tmp


def run_main(args: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(args)
    return code, buf.getvalue()


def run() -> int:
    errors = errors_of(TGT)
    check("clean translation passes", errors == [], f"{errors}")

    # BREAK-IT table, assigned to this validator
    expect_fail("dropped paragraph",
                "Đây là đoạn thứ hai, hướng dẫn cách cài đặt môi trường thí nghiệm và chuẩn bị dữ liệu.\n\n", "",
                r"blocks do not align|block count")
    expect_fail("dropped list item",
                "- Mục thứ hai: tải tập dữ liệu xuống và kiểm tra định dạng dữ liệu có đúng không\n", "",
                r"blocks do not align")
    expect_fail("merged paragraphs", "chương này.\n\nĐây là", "chương này.\nĐây là", r"block count")
    expect_fail("altered external URL (N1)", "2401.00001)", "2401.00002)", r"link 2: source .* translation")
    expect_fail("altered relative link (N1)", "(../chapter3/README.md)", "(../chapter4/README.md)",
                r"link 1: source .*chapter3.* translation .*chapter4")
    expect_fail("altered image path", "./assets/x-sir.png", "./assets/x-sir2.png", r"link 4: UNMAPPED")
    expect_fail("anchor pointed at another heading", "(#安装环境)", "(#第一章-大模型水印)", r"link 3: source")
    expect_fail("dropped link", "[bài báo](https://arxiv.org/abs/2401.00001)", "bài báo", r"link count")
    expect_fail("translated fence info string", "```bash", "```Vỏ", r"info string 'bash' changed to 'Vỏ'")
    expect_fail("changed code", "pip install -r requirements.txt", "pip install -r requirement.txt",
                r"code differs after stripping comments")
    expect_fail("changed protected literal", "'用萝卜、土豆、茄子做饭，给我个菜谱。'", "'Nấu ăn với củ cải.'",
                r"code differs after stripping comments: source \"prompt = '用萝卜")
    # Plan: comments are translated in every file, including a fence that holds a
    # protected literal; only its code (string literals included) must stay identical.
    commented = TGT.replace("prompt = '用萝卜", "# Câu prompt bằng tiếng Trung\nprompt = '用萝卜", 1)
    commented_src = SRC.replace("prompt = '用萝卜", "# 中文提示词\nprompt = '用萝卜", 1)
    errors = errors_of(commented, commented_src)
    check("protected literal: translated comment passes", errors == [], f"{errors}")
    expect_fail("Han left in prose", "Đây là đoạn thứ nhất, giới thiệu", "Đây là đoạn thứ nhất, 介绍了",
                r"Han outside the allow-list: \['介绍了'\]")
    expect_fail("extra table cell", "| Mô hình | Mô hình ngôn ngữ", "| Mô hình | lớn | Mô hình ngôn ngữ",
                r"table_row 3 cells")
    # further checks this validator owns
    expect_fail("Han left in a code comment", "# Tải mô hình", "# 加载模型", r"comment: Han outside")
    expect_fail("nested item moved to top level", "    - Mục lồng", "- Mục lồng", r"list_item ul@")
    expect_fail("heading level changed", "## Cài đặt môi trường", "### Cài đặt môi trường", r"heading h2")
    expect_fail("paragraph cut short (ratio)",
                "Đây là đoạn thứ nhất, giới thiệu nội dung chính và mục tiêu học tập của chương này.",
                "Đây là đoạn 1.", r"ratio 0\.\d+ outside")
    expect_fail("gloss mark not after a protected literal", "> Lưu ý", f"{GLOSS_MARK}\n> Lưu ý",
                r"only allowed directly after a protected literal")
    expect_fail("changed code in a fence whose comment was translated",
                "model = load(\"gpt2\")", "model = load(\"gpt2-xl\")", r"code differs")
    expect_fail("forbidden raw HTML in the translation", "> Lưu ý", "<script>x</script>\n\n> Lưu ý",
                r"raw HTML tag <script> not allowed")


    # Item 1: content fingerprint (numbers, URLs, inline code, Latin terms) per aligned block
    def fp_errors(tgt: str, src: str = FP_SRC) -> list[str]:
        return check_markdown_page(REL, "vi", src, tgt, SETTINGS).errors

    def fp_fail(name: str, tgt: str, pattern: str) -> None:
        errors = fp_errors(tgt)
        check(name, any(re.search(pattern, e) for e in errors), f"expected /{pattern}/, got {errors}")

    errors = fp_errors(FP_TGT)
    check("fingerprint fixture: clean translation passes (full-width-colon line may be normalised)",
          errors == [], f"{errors}")
    fp_fail("swap of sibling list items with different fingerprints",
            swap(FP_TGT, "Dùng mô hình GPT-2 huấn luyện 3 vòng trên GSM8K.",
                 "Chạy `eval.py` để đánh giá độ chính xác trên MATH."), r"lost or reordered source content")
    fp_fail("swap of sibling paragraphs with different fingerprints",
            swap(FP_TGT, "Cài PyTorch 2.1 trước, rồi tải trọng số.", "Sau đó chạy DeepSpeed trên GPU thứ 8."),
            r"lost or reordered source content \[.*(pytorch|deepspeed)")
    fp_fail("number changed in a Han block", FP_TGT.replace("PyTorch 2.1", "PyTorch 2.2"),
            r"lost or reordered source content \['2\.1'\]")
    pilot_fail("review repro: swap ch2 objectives 1 and 3 (vi)", "vi", lambda t: _objectives(t, 1, 3),
               r"glossary term not rendered \(思维链")
    pilot_fail("review repro: swap ch2 objectives 1 and 3 (en)", "en", lambda t: _objectives(t, 1, 3),
               r"glossary term not rendered \(思维链")

    # Item 2: glossary term coverage per block, and a review line above ratio 6.0
    short_src = "- 掌握零样本和少样本提示工程\n"
    short_tgt = ("- Nắm vững prompt engineering (kỹ thuật thiết kế và tối ưu prompt) theo kiểu zero-shot "
                 "(không đưa ví dụ mẫu nào trong prompt) và few-shot (đưa vài ví dụ mẫu trong prompt)\n")
    report = check_markdown_page(REL, "vi", short_src, short_tgt, SETTINGS)
    check("gloss-heavy short line passes, with a review: warning above ratio 6.0",
          report.errors == [] and any("> 6.0" in w for w in report.warnings), f"{report.errors} {report.warnings}")
    errors = check_markdown_page(REL, "vi", short_src, _drop_few_shot(short_tgt), SETTINGS).errors
    check("dropped few-shot clause on a gloss-heavy line (synthetic)",
          any(re.search(r"glossary term not rendered \(少样本 -> few-shot", e) for e in errors), f"{errors}")
    # review round 2: numbers are whole tokens ("0" must not be satisfied by "0.7")
    pilot_fail("review repro: drop 'temperature > 0' but keep 0.7 (vi)", "vi",
               lambda t: t.replace(" lớn hơn 0", "", 1), r"lost or reordered source content \['0'\]")
    pilot_fail("review repro: 0.7 changed to 0.75 (en)", "en",
               lambda t: t.replace("0.7)", "0.75)", 1), r"lost or reordered source content \['0\.7'\]")
    pilot_fail("review repro: drop the few-shot clause of ch2 objective 2 (vi line 8)", "vi", _drop_few_shot,
               r"glossary term not rendered \(少样本 -> few-shot")
    pilot_fail("review repro: drop the few-shot clause of ch2 objective 2 (en)", "en", _drop_few_shot,
               r"glossary term not rendered \(少样本 -> few-shot")

    # Item 3: code swallowed into a comment keeps its code tail verbatim
    errors = check_markdown_page(REL, "vi", SW_SRC, SW_TGT, SETTINGS).errors
    check("swallowed code: clean translated comment passes", errors == [], f"{errors}")
    for name, tgt in (("== -> != in swallowed code (synthetic)", SW_TGT.replace("x == 1", "x != 1")),
                      ("swallowed code dropped from the comment", SW_TGT.replace(".if x == 1:", ".")),
                      ("comment count changed in a fence", SW_TGT.replace("x = 1\n", "x = 1\n# thêm\n"))):
        errors = check_markdown_page(REL, "vi", SW_SRC, tgt, SETTINGS).errors
        check(name, any(re.search(r"swallowed code|comments, source", e) for e in errors), f"{errors}")
    for lang in ("vi", "en"):
        _, base = pilot_new_errors(lang, lambda t: t + "\n")
        check(f"real ch2 fence: existing translated comments pass ({lang})",
              not any("swallowed code" in e or "comments, source" in e for e in base), f"{base}")
        pilot_fail(f"review repro: == -> != in the swallowed ch2 code ({lang})", lang,
                   lambda t: t.replace("if resp.status_code == HTTPStatus.OK:", "if resp.status_code != HTTPStatus.OK:", 1),
                   r"swallowed code 'if resp\.status_code == HTTPStatus\.OK:'")

    # Inline code holding Han is translated (blind test, 2026-11-12); Latin inline code is not
    ic_src = "# 标题\n\n**步骤1**：加载`冻结参数`。运行`train.py`。\n"
    ic_ok = "# Tiêu đề\n\n**Bước 1**: Tải `tham số đóng băng`. Chạy `train.py`.\n"
    ic_cases = (
        ("inline code with Han translated: passes", ic_ok, None),
        ("inline code with Han left in Chinese: fails", ic_ok.replace("tham số đóng băng", "冻结参数"), r"Han outside the allow-list"),
        ("Latin inline code altered next to a translated span: fails", ic_ok.replace("train.py", "train2.py"), r"inline code .* differs"),
    )
    for name, tgt, pattern in ic_cases:
        errs = check_markdown_page("documents/chapter8/README.md", "vi", ic_src, tgt, SETTINGS).errors
        ok = not errs if pattern is None else any(re.search(pattern, e) for e in errs)
        check(name, ok, f"{errs}")

    # Item 4: Han-free blocks and cells stay byte-identical; inline code spans equal
    fp_fail("English paragraph translated", FP_TGT.replace("See the original paper for details.",
                                                           "Xem bài báo gốc để biết chi tiết."),
            r"holds no Chinese, must stay byte-identical")
    fp_fail("extra inline code span in a Han block", FP_TGT.replace("trên MATH.", "trên `MATH`."),
            r"inline code \['MATH', 'eval\.py'\] differs")
    pilot_fail("review repro: translated English few-shot row (ch2 vi)", "vi",
               lambda t: t.replace("Translate English to Frenchcheese =>", "Dịch tiếng Anh sang tiếng Pháp, cheese =>", 1),
               r"cell 2 holds no Chinese in the source, must stay byte-identical")

    # notebooks
    errors = nb_errors(NB_TGT)
    check("clean notebook passes", errors == [], f"{errors}")
    nb_fail("notebook: changed code cell",
            lambda t: t["cells"][1].__setitem__("source", ["ds = load_dataset('gsm8k', 'main')\n", "print(len(ds))"]),
            r"cell 1: code differs")
    nb_fail("notebook: changed output",
            lambda t: t["cells"][1].__setitem__("outputs", [{"output_type": "stream", "name": "stdout", "text": ["41\n"]}]),
            r"cell 1: outputs differ")
    nb_fail("notebook: cell type changed", lambda t: t["cells"][1].__setitem__("cell_type", "markdown"),
            r"cell types differ")
    nb_fail("notebook: cell dropped", lambda t: t["cells"].pop(), r"cell count")
    nb_fail("notebook: dropped paragraph in a markdown cell",
            lambda t: t["cells"][0].__setitem__("source", ["## Tải dữ liệu\n"]), r"cell 0: .*block")

    # real corpus controls
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run_main(["--root", str(corpus_root(Path(tmp), translate=True))])
        last = out.strip().splitlines()[-1] if out.strip() else ""
        check("pseudo-translated corpus (15 files) passes: no false positive", code == 0 and "15/15 files pass" in last,
              "\n" + "\n".join(line for line in out.splitlines() if not line.startswith("ok  ")))
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run_main(["--root", str(corpus_root(Path(tmp), translate=False))])
        # Han, and the glossary terms an untranslated page cannot carry; nothing structural
        han_only = all(re.search(r"Han outside|glossary term not rendered", line)
                       for line in out.splitlines() if line.startswith("       - "))
        check("untranslated corpus fails, on Han and glossary terms only", code == 1 and "0/15 files pass" in out
              and han_only, out[-2000:])
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run_main(["--root", tmp])
        check("empty translations root fails", code == 1 and "no translated" in out, out)

    passed = sum(RESULTS)
    print(f"{'all pass' if passed == len(RESULTS) else 'FAILURES'} ({passed}/{len(RESULTS)} cases)")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(run())
