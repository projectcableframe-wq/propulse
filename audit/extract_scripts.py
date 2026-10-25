#!/usr/bin/env python3
"""Extract the <script> blocks of the single-file application.

Usage: python3 audit/extract_scripts.py app/yanmar_engine_propeller_selector.html audit/build
Writes build/script_0.js (calculation core + engine database) and
build/script_1.js (UI layer).  The extraction is a plain regex on the
<script>...</script> pairs, in document order; it does not modify the input.
"""
import re
import sys
import pathlib


def extract(html_path, outdir):
    html = pathlib.Path(html_path).read_text(encoding="utf-8")
    blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for i, b in enumerate(blocks):
        (out / ("script_%d.js" % i)).write_text(b, encoding="utf-8")
    return [len(b) for b in blocks]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sizes = extract(sys.argv[1], sys.argv[2])
    print("extracted %d script block(s): %s" % (len(sizes), sizes))
