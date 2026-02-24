#!/usr/bin/env python3
"""Detect duplicate lexical strings across rdfs:label and oboInOwl:hasExactSynonym."""

import argparse
import csv
import re
import sys
import unicodedata
from collections import defaultdict


def normalize(s):
    """Normalize a string for duplicate detection.

    Applies NFKD unicode normalization, lowercases, and strips whitespace,
    hyphens, underscores, and non-word characters.
    """
    s = unicodedata.normalize("NFKD", s)
    s = s.lower()
    s = re.sub(r"[\s\-_]", "", s)
    s = re.sub(r"[^\w]", "", s)
    return s


def parse_robot_tsv(filepath):
    """Parse a ROBOT-generated TSV file into a list of (term, property, value) tuples.

    Reads the raw tab-separated output from ROBOT query to avoid Python csv
    module quoting interference. Handles ROBOT output conventions: ?-prefixed
    headers, <> wrapped IRIs, and quoted string literals with optional
    language or datatype tags.
    """
    entries = []
    with open(filepath) as f:
        f.readline()  # skip header
        for line in f:
            line = line.rstrip("\n\r")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            term = parts[0].strip("<>")
            prop = parts[1].strip("<>")
            value = parts[2]
            # Strip RDF literal encoding: "value", "value"@lang, "value"^^<datatype>
            m = re.match(r'^"(.*)"(?:@[\w-]+|\^\^.*)?$', value)
            if m:
                value = m.group(1)
            if term and prop and value:
                entries.append((term, prop, value))
    return entries


def find_duplicates(entries):
    """Group entries by normalized form and return clusters with 2+ distinct terms.

    Duplicates within the same term IRI are not counted as collisions.
    """
    groups = defaultdict(list)
    for term, prop, value in entries:
        norm = normalize(value)
        if norm:
            groups[norm].append((term, prop, value))

    duplicates = {}
    for norm in sorted(groups):
        members = groups[norm]
        distinct_terms = {m[0] for m in members}
        if len(distinct_terms) >= 2:
            duplicates[norm] = members
    return duplicates


def write_report(duplicates, output_path):
    """Write a TSV report of duplicate clusters in wide format.

    Each row represents one collision cluster with all colliding terms
    and their properties/values spread across columns.
    """
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        # Header: normalized_form, then triplets of (term, property, original)
        writer.writerow(["normalized_form", "collision_description"])

        for norm in sorted(duplicates):
            members = sorted(duplicates[norm])
            # Build collision description showing all terms involved
            collision_parts = []
            for term, prop, value in members:
                # Shorten URIs for readability
                term_short = term.split("/")[-1]
                prop_short = prop.split("#")[-1].split("/")[-1]
                collision_parts.append(f"{term_short}[{prop_short}={value}]")

            collision_desc = " | ".join(collision_parts)
            writer.writerow([norm, collision_desc])


def print_summary(total_entries, total_normalized_forms, duplicates, output_path):
    """Print human-readable summary statistics to stdout."""
    terms_involved = set()
    for members in duplicates.values():
        for term, _, _ in members:
            terms_involved.add(term)

    print("=== Label/Synonym Duplicate Check ===")
    print(f"Total label/synonym entries scanned: {total_entries}")
    print(f"Unique normalized forms: {total_normalized_forms}")
    print(f"Duplicate clusters found: {len(duplicates)}")
    print(f"Terms involved in duplicates: {len(terms_involved)}")
    print(f"Report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect duplicate lexical strings across rdfs:label and oboInOwl:hasExactSynonym"
    )
    parser.add_argument("input", help="Input TSV file from SPARQL extraction query")
    parser.add_argument(
        "-o",
        "--output",
        default="reports/label-synonym-duplicates.tsv",
        help="Output TSV report path (default: reports/label-synonym-duplicates.tsv)",
    )
    args = parser.parse_args()

    entries = parse_robot_tsv(args.input)
    duplicates = find_duplicates(entries)

    # Count unique normalized forms across all entries (not just duplicates)
    all_normalized = set()
    for _, _, value in entries:
        norm = normalize(value)
        if norm:
            all_normalized.add(norm)

    write_report(duplicates, args.output)
    print_summary(len(entries), len(all_normalized), duplicates, args.output)

    # Always exit 0 - this is a warning-only check, not a blocker
    if duplicates:
        print(f"WARNING: {len(duplicates)} label/synonym collisions detected")
    else:
        print("✓ No label/synonym collisions detected")
    sys.exit(0)


if __name__ == "__main__":
    main()
