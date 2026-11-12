#!/usr/bin/env python3
"""Convert a (translated) notebook to a Markdown page for the site.

mkdocs-jupyter cannot render notebooks under mkdocs-static-i18n's folder mode (it
emits raw JSON and strict mode still passes), so notebooks go through nbconvert.

Outputs that would put third-party or server data on the site are not rendered:
  - image/* outputs (the ch4 training plot) -> a note linking the upstream notebook;
  - Weights & Biases run widgets (ch11)      -> the same note.
HTML tables (the ch11 dataframe) and text outputs are kept. An HTML output loses its
<style> block and blank lines, so CommonMark reads it as one HTML block (otherwise its
indented CSS after a blank line becomes a code block that MkDocs does not render).

Usage: build_notebooks.py NOTEBOOK LANG UPSTREAM_REL > page.md
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter

SHA = "f84c04268794ef94f8949808bbc14ab8636763a0"
UPSTREAM_BLOB = f"https://github.com/Lordog/dive-into-llms/blob/{SHA}/"
NOTE = {
    "vi": "*Kết quả dạng hình hoặc widget không được hiển thị ở đây; xem [notebook gốc]({url}).*",
    "en": "*Image or widget output is not shown here; see the [original notebook]({url}).*",
}


def _hidden(output: dict) -> bool:
    data = output.get("data", {})
    if any(key.startswith("image/") for key in data):
        return True
    html = data.get("text/html", "")
    if isinstance(html, list):
        html = "".join(html)
    return "wandb" in html.lower()


def strip_outputs(nb: nbformat.NotebookNode, lang: str, upstream_rel: str) -> nbformat.NotebookNode:
    """Return a copy with image and widget outputs replaced by one note per cell."""
    note = NOTE[lang].format(url=UPSTREAM_BLOB + upstream_rel)
    result = copy.deepcopy(nb)
    for cell in result.cells:
        if cell.cell_type != "code":
            continue
        kept = [o for o in cell.get("outputs", []) if not _hidden(o)]
        if len(kept) != len(cell.get("outputs", [])):
            kept.append(nbformat.v4.new_output("display_data", data={"text/markdown": note}))
        for output in kept:
            data = output.get("data", {})
            if "text/html" in data:
                html = data["text/html"]
                html = "".join(html) if isinstance(html, list) else html
                html = re.sub(r"<style[\s\S]*?</style>", "", html)
                data["text/html"] = "\n".join(line.strip() for line in html.splitlines() if line.strip())
        cell.outputs = kept
    return result


def to_markdown(path: Path, lang: str, upstream_rel: str) -> str:
    nb = nbformat.read(path, as_version=4)
    body, resources = MarkdownExporter().from_notebook_node(strip_outputs(nb, lang, upstream_rel))
    if resources.get("outputs"):
        raise ValueError(f"{path}: nbconvert extracted files {sorted(resources['outputs'])}; nothing may be re-hosted")
    return body


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    sys.stdout.write(to_markdown(Path(argv[0]), argv[1], argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
