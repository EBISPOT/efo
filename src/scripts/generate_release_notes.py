#!/usr/bin/env python3
"""Generate "ExFactor Ontology release notes.txt" deterministically (refs #2826).

Every dynamic section is derived from artifacts of one single build:

  - added / modified classes: the Bubastis diff between the previously
    *published* efo.owl and this release's build/efo.owl;
  - obsoleted classes: the delta of the owl:deprecated report (obsoletes.tsv)
    between the previous release and this build — never IRI set-difference,
    so a live class can no longer be reported as deleted;
  - header counts and class count: counted from those same inputs.

The notes report obsoletions only. Classes genuinely absent from the build
(e.g. merged away upstream) are not published in the notes; they are printed
to stderr so the release engineer sees them.

The script refuses to write notes whose inputs contradict each other (e.g. a
"deleted" class that the obsoletes report still sees, which would mean the
diff and the reports were produced from different snapshots).
"""

import argparse
import datetime
import re
import sys


def fail(msg):
    sys.exit("generate_release_notes: ERROR: %s" % msg)


def strip_term(value):
    """Normalize a SPARQL TSV term: <iri> or "literal" -> bare string."""
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def read_obsoletes(path):
    """Read an obsoletes.tsv (cls / replCls / consCls) into {iri: (repl, consider)}."""
    result = {}
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0 and line.startswith("?"):
                continue
            cells = line.rstrip("\n").split("\t")
            if not cells or not cells[0].strip():
                continue
            cls = strip_term(cells[0])
            repl = strip_term(cells[1]) if len(cells) > 1 and cells[1].strip() else ""
            cons = strip_term(cells[2]) if len(cells) > 2 and cells[2].strip() else ""
            if cls not in result or (repl, cons) > result[cls]:
                result[cls] = (repl, cons)
    return result


def read_labels(path):
    labels = {}
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0 and line.startswith("?"):
                continue
            cells = line.rstrip("\n").split("\t")
            if len(cells) < 2 or not cells[0].strip():
                continue
            cls = strip_term(cells[0])
            label = strip_term(cells[1])
            labels.setdefault(cls, []).append(label)
    return labels


def read_class_count(path):
    total = 0
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0 and line.startswith("?"):
                continue
            cells = line.rstrip("\n").split("\t")
            if len(cells) < 2 or not cells[1].strip():
                continue
            total += int(strip_term(cells[1]))
    return total


def parse_bubastis(path):
    """Split a Bubastis diff into its @-marked sections.

    Returns {marker: (verbatim_block_text, [class_iris])} plus the summary
    counts Bubastis printed, for cross-checking.
    """
    text = open(path, encoding="utf-8").read()
    chunks = re.split(r"^#{4,}\s*$", text, flags=re.M)
    summary, sections = chunks[0], chunks[1:]

    counts = {}
    for kind in ("changed", "added", "deleted"):
        m = re.search(r"^Number of classes %s: (\d+)" % kind, summary, re.M)
        if not m:
            fail("Bubastis summary lacks a 'Number of classes %s' line" % kind)
        counts[kind] = int(m.group(1))

    parsed = {}
    for chunk in sections:
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        lines = chunk.split("\n")
        marker = lines[0].strip()
        if not marker.startswith("@"):
            fail("Bubastis section does not start with an @ marker: %r" % marker)
        body = "\n".join(lines[1:]).strip("\n")
        iris = re.findall(r"^Class: (\S+)", body, re.M)
        parsed[marker] = (body, iris)
    return parsed, counts


def format_obsoleted(newly, labels):
    blocks = []
    for iri in sorted(newly):
        repl, cons = newly[iri]
        label_list = labels.get(iri)
        if label_list:
            label = ", ".join(sorted(label_list))
        else:
            label = "(no label)"
            print("generate_release_notes: WARNING: no label found for obsoleted class %s" % iri,
                  file=sys.stderr)
        block = "Class: %s\nLabel(s): %s" % (iri, label)
        if repl:
            block += "\nReplaced by: %s" % repl
        elif cons:
            block += "\nConsider: %s" % cons
        else:
            block += "\nReplaced by: none"
        blocks.append(block)
    return "\n\n".join(blocks) if blocks else "None."


def ordinal_date(dt):
    day = dt.day
    if 11 <= day % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return "%d%s %s %d" % (day, suffix, dt.strftime("%B"), dt.year)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bubastis", required=True,
                    help="Bubastis diff: previous published efo.owl vs this build/efo.owl")
    ap.add_argument("--obsoletes", required=True,
                    help="reports/obsoletes.tsv regenerated from this build")
    ap.add_argument("--previous-obsoletes", required=True,
                    help="obsoletes.tsv computed from the previous published efo.owl")
    ap.add_argument("--labels", required=True,
                    help="class-labels TSV computed from this build")
    ap.add_argument("--class-counts", required=True,
                    help="reports/class-count-by-prefix.tsv regenerated from this build")
    ap.add_argument("--template", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--date", default=None,
                    help='e.g. "15th September 2026"; defaults to today')
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()

    sections, bub_counts = parse_bubastis(args.bubastis)

    def section(marker):
        if marker not in sections:
            return ("None.", [])
        return sections[marker]

    new_body, new_iris = section("@Classes new to this version")
    mod_body, mod_iris = section("@Classes modified from previous")
    _, del_iris = section("@Classes deleted from this version")

    for kind, found in (("added", new_iris), ("changed", mod_iris), ("deleted", del_iris)):
        if bub_counts[kind] != len(found):
            fail("Bubastis says %d classes %s but its diff lists %d"
                 % (bub_counts[kind], kind, len(found)))

    cur_obs = read_obsoletes(args.obsoletes)
    prev_obs = read_obsoletes(args.previous_obsoletes)
    labels = read_labels(args.labels)
    newly = {iri: cur_obs[iri] for iri in cur_obs if iri not in prev_obs}

    # Consistency gates: all inputs must describe the same build.
    live_missing = [iri for iri in new_iris if iri not in labels]
    if live_missing:
        fail("classes reported new are not declared in this build (snapshot mismatch?): %s"
             % ", ".join(live_missing[:5]))
    obsolete_but_deleted = [iri for iri in del_iris if iri in cur_obs]
    if obsolete_but_deleted:
        fail("classes reported deleted are still present as obsoleted classes in "
             "obsoletes.tsv — the diff and the reports disagree: %s"
             % ", ".join(obsolete_but_deleted[:5]))
    obsolete_and_new = [iri for iri in newly if iri in new_iris]
    if obsolete_and_new:
        fail("classes are simultaneously newly obsoleted and new to this version: %s"
             % ", ".join(obsolete_and_new[:5]))

    if del_iris:
        print("generate_release_notes: NOTE: %d class(es) are gone from this build "
              "(not published in the notes, which report obsoletions only): %s"
              % (len(del_iris), ", ".join(del_iris)), file=sys.stderr)

    date = args.date or ordinal_date(datetime.date.today())
    replacements = {
        "@@VERSION@@": args.version,
        "@@DATE@@": date,
        "@@CLASS_COUNT@@": format(read_class_count(args.class_counts), ","),
        "@@N_CHANGED@@": str(bub_counts["changed"]),
        "@@N_ADDED@@": str(bub_counts["added"]),
        "@@N_OBSOLETED@@": str(len(newly)),
        "@@NEW_CLASSES@@": new_body or "None.",
        "@@MODIFIED_CLASSES@@": mod_body or "None.",
        "@@OBSOLETED_CLASSES@@": format_obsoleted(newly, labels),
    }

    notes = open(args.template, encoding="utf-8").read()
    for token, value in replacements.items():
        if token not in notes:
            fail("template is missing token %s" % token)
        notes = notes.replace(token, value)
    leftover = re.findall(r"@@[A-Z_]+@@", notes)
    if leftover:
        fail("unreplaced tokens remain: %s" % ", ".join(sorted(set(leftover))))

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(notes)
    print("generate_release_notes: wrote %s (version %s: %d added, %d changed, "
          "%d obsoleted)"
          % (args.output, args.version, bub_counts["added"], bub_counts["changed"],
             len(newly)))


if __name__ == "__main__":
    main()
