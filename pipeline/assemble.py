#!/usr/bin/env python3
"""Assemble fragments into original.tex and run houselint."""
import sys
import os

ROMAN_FRAGMENTS = ['v', 'vi', 'vii', 'viii', 'ix', 'x']

def assemble(max_page: int):
    preamble = "\\documentclass{article}\n\\usepackage{readmasters}\n\n\\begin{document}\n"
    frags = []
    for rp in ROMAN_FRAGMENTS:
        frag_path = f"scratch/weyl-1913-idee-riemannschen-flaeche/fragments/p{rp}.tex"
        if os.path.exists(frag_path):
            with open(frag_path, encoding="utf-8") as f:
                frags.append(f.read().strip())
    for p in range(1, max_page + 1):
        frag_path = f"scratch/weyl-1913-idee-riemannschen-flaeche/fragments/p{p}.tex"
        if not os.path.exists(frag_path):
            raise FileNotFoundError(f"Missing fragment {frag_path}")
        with open(frag_path, encoding="utf-8") as f:
            frags.append(f.read().strip())
    body = "\n\n".join(frags)
    postamble = "\n\\end{document}\n"
    content = preamble + body + postamble
    out_path = "corpus/weyl-1913-idee-riemannschen-flaeche/original.tex"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Assembled {len(frags)} fragments into {out_path} ({len(content)} bytes)")

if __name__ == "__main__":
    max_p = int(sys.argv[1]) if len(sys.argv) > 1 else 169
    assemble(max_p)
