#!/usr/bin/env python3
"""Sort the space-separated tokens inside basic-report.tsv's xrefs column.

SPARQL's group_concat has no defined ordering, so the xref cell shuffles on
every regeneration; sorting the tokens makes the report byte-stable so it
diffs cleanly and the release-notes consistency gate can compare rebuilds
(refs #2826). Run in place: canonicalize_basic_report.py reports/basic-report.tsv
"""

import sys


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    out = []
    for i, line in enumerate(lines):
        cells = line.rstrip("\n").split("\t")
        if i > 0 and len(cells) >= 3 and len(cells[2]) >= 2 and cells[2][0] == cells[2][-1] == '"':
            tokens = cells[2][1:-1].split(" ")
            cells[2] = '"' + " ".join(sorted(tokens)) + '"'
        out.append("\t".join(cells) + "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out)


if __name__ == "__main__":
    main()
