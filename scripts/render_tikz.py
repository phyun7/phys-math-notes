#!/usr/bin/env python3
"""Compile Markdown TikZ blocks to SVG during deployment (standard library only).

Run from the repository root, before `zensical build`. This changes the build's
checkout only. Do not commit the generated Markdown or SVGs back to GitHub.
"""

import hashlib
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CACHE = ROOT / ".cache" / "tikz"
OUTPUT = DOCS / "assets" / "tikz"
PREAMBLE = ROOT / "scripts" / "tikz-preamble.tex"
BLOCK = re.compile(
    r'^(?P<indent>[ \t]*)<script\b(?P<attrs>[^>]*)>\s*\n'
    r'(?P<body>.*?)^[ \t]*</script>[ \t]*', re.M | re.S | re.I
)
TYPE = re.compile(r'''\btype\s*=\s*(["'])text/tikz\1''', re.I)
FENCE = re.compile(r'^[ \t]*(?P<ticks>`{3,}|~{3,})')


def fenced_ranges(source):
    """Leave sample code inside Markdown fences untouched, including admonitions."""
    start = None
    marker = ""
    offset = 0
    ranges = []
    for line in source.splitlines(keepends=True):
        match = FENCE.match(line)
        if match:
            ticks = match['ticks']
            if start is None:
                start, marker = offset, ticks
            elif ticks[0] == marker[0] and len(ticks) >= len(marker) and not line[match.end():].strip():
                ranges.append((start, offset + len(line)))
                start = None
        offset += len(line)
    if start is not None:
        ranges.append((start, len(source)))
    return ranges


def document(body, shared):
    # Local definitions go first, so existing snippets using \newcommand still
    # work with the fallback \providecommand definitions in the shared file.
    beginning = re.search(r'\\begin\s*\{(?:tikzcd|tikzpicture)\}', body)
    if not beginning:
        raise ValueError("Expected \\begin{tikzcd} or \\begin{tikzpicture}.")
    local, diagram = body[:beginning.start()], body[beginning.start():]
    return (
        "\\documentclass[12pt,border=3pt]{standalone}\n"
        "\\usepackage{amsmath,amssymb,mathtools,bm,mathrsfs,tikz-cd}\n"
        "\\usetikzlibrary{arrows.meta,calc,decorations.markings}\n"
        + local + "\n" + shared + "\n"
        "\\begin{document}\n" + diagram + "\n\\end{document}\n"
    )


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise ValueError("\n".join((result.stdout + result.stderr).splitlines()[-35:]))


def compile_svg(tex, key):
    cached = CACHE / (key + ".svg")
    if cached.exists():
        return cached, True
    for executable in ("pdflatex", "pdftocairo"):
        if not shutil.which(executable):
            raise ValueError(f"Missing {executable}. Use the supplied GitHub workflow.")
    with tempfile.TemporaryDirectory(prefix="notes-tikz-") as folder:
        work = Path(folder)
        (work / "diagram.tex").write_text(tex, encoding="utf-8")
        run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode",
             "-halt-on-error", "-file-line-error", "diagram.tex"], work)
        run(["pdftocairo", "-svg", "diagram.pdf", "diagram.svg"], work)
        ET.parse(work / "diagram.svg")
        CACHE.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(work / "diagram.svg", cached)
    return cached, False


def main():
    shared = PREAMBLE.read_text(encoding="utf-8")
    version = Path(__file__).read_bytes()
    changed = []
    total = hits = 0
    for page in sorted(DOCS.rglob("*.md")):
        source = page.read_text(encoding="utf-8")
        fences = fenced_ranges(source)
        diagram_number = 0

        def replace(match):
            nonlocal total, hits, diagram_number
            if not TYPE.search(match['attrs']) or any(a <= match.start() < b for a, b in fences):
                return match.group()
            diagram_number += 1
            try:
                # Remove the Markdown indentation before sending source to TeX.
                indent = match['indent']
                body = "\n".join(line[len(indent):] if line.startswith(indent) else line
                                 for line in match['body'].splitlines())
                tex = document(body, shared)
                key = hashlib.sha256(version + tex.encode()).hexdigest()[:32]
                cached, hit = compile_svg(tex, key)
                OUTPUT.mkdir(parents=True, exist_ok=True)
                target = OUTPUT / (key + ".svg")
                shutil.copyfile(cached, target)
                svg = ET.parse(target).getroot()
                width = float(svg.attrib['viewBox'].split()[2]) / 12
                height = float(svg.attrib['viewBox'].split()[3]) / 12
                path = quote(os.path.relpath(target, page.parent).replace(os.sep, "/"), safe="/.")
                alt_match = re.search(r'''\bdata-alt\s*=\s*(["'])(.*?)\1''', match['attrs'], re.S)
                alt = html.escape(alt_match[2] if alt_match else "Commutative diagram", quote=True)
                total += 1
                hits += hit
                print(f"{page.relative_to(ROOT)}: diagram {diagram_number} ({'cached' if hit else 'compiled'})")
                # Scale to the prose font size; center and reserve image space.
                return (f'{indent}<img src="{path}" alt="{alt}" '
                        f'width="{width * 16:.2f}" height="{height * 16:.2f}" '
                        f'style="display:block;width:{width:.4f}em;max-width:100%;'
                        'height:auto;margin:1rem auto;" />')
            except (ValueError, OSError, subprocess.TimeoutExpired, ET.ParseError) as error:
                line = source.count("\n", 0, match.start()) + 1
                raise ValueError(f"{page.relative_to(ROOT)}:{line}, diagram {diagram_number}:\n{error}") from error

        rendered = BLOCK.sub(replace, source)
        if rendered != source:
            changed.append((page, rendered))
    # Do not rewrite any Markdown if a later diagram failed to compile.
    for page, rendered in changed:
        page.write_text(rendered, encoding="utf-8")
    print(f"TikZ: {total} diagrams, {hits} from cache.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"TikZ build failed: {error}", file=sys.stderr)
        sys.exit(1)
