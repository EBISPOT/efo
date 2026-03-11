#!/usr/bin/env python3
"""QC check: verify all Mondo terms in iri_dependencies/mondo_terms.txt are present in EFO.

For obsoleted terms, checks whether the term_replaced_by annotation points to a Mondo
term.  If it does, ensures that replacement is also listed in mondo_terms.txt (and adds
it when missing).  Terms obsoleted without a Mondo replacement are collected in a
warning report.
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET


MONDO_IRI_RE = re.compile(r"http://purl\.obolibrary\.org/obo/MONDO_\d{7}")

NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "obo": "http://purl.obolibrary.org/obo/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
}

# IAO_0100001 = term_replaced_by
TERM_REPLACED_BY = "http://purl.obolibrary.org/obo/IAO_0100001"


def load_terms_file(path):
    """Read an IRI-per-line text file, returning a set of IRIs."""
    terms = set()
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                terms.add(line)
    return terms


def save_terms_file(path, terms):
    """Write a sorted set of IRIs back to a text file."""
    with open(path, "w") as fh:
        for t in sorted(terms):
            fh.write(t + "\n")


def parse_efo_owl(efo_path):
    """Parse efo.owl and return sets/mappings for Mondo terms.

    Returns
    -------
    all_mondo_iris : set[str]
        Every Mondo IRI that appears anywhere in efo.owl.
    deprecated : set[str]
        Mondo IRIs that carry owl:deprecated true.
    replaced_by : dict[str, list[str]]
        Mondo IRI → list of term_replaced_by IRIs.
    labels : dict[str, str]
        Mondo IRI → rdfs:label (for reporting).
    """
    all_mondo_iris = set()
    deprecated = set()
    replaced_by = {}
    labels = {}

    tree = ET.parse(efo_path)
    root = tree.getroot()

    for cls in root.iter("{http://www.w3.org/2002/07/owl#}Class"):
        about = cls.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", "")
        if not MONDO_IRI_RE.fullmatch(about):
            continue

        all_mondo_iris.add(about)

        # Check deprecation
        for dep in cls.iter("{http://www.w3.org/2002/07/owl#}deprecated"):
            if dep.text and dep.text.strip().lower() == "true":
                deprecated.add(about)

        # Collect term_replaced_by values
        replacements = []
        for child in cls:
            tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            full_tag = child.tag
            if full_tag == "{http://purl.obolibrary.org/obo/}IAO_0100001" or \
               full_tag == TERM_REPLACED_BY:
                resource = child.get(
                    "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", ""
                )
                if resource:
                    replacements.append(resource)
                elif child.text and child.text.strip():
                    replacements.append(child.text.strip())
        if replacements:
            replaced_by[about] = replacements

        # Label
        for lbl in cls.iter("{http://www.w3.org/2000/01/rdf-schema#}label"):
            if lbl.text:
                labels[about] = lbl.text.strip()

    return all_mondo_iris, deprecated, replaced_by, labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "efo_owl",
        help="Path to efo.owl (the release OWL file)",
    )
    parser.add_argument(
        "mondo_terms",
        help="Path to iri_dependencies/mondo_terms.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="reports/mondo-qc-warnings.tsv",
        help="Path for the warning report (default: reports/mondo-qc-warnings.tsv)",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="If set, automatically add missing replacement Mondo terms to mondo_terms.txt",
    )
    args = parser.parse_args()

    print("Parsing efo.owl …")
    all_mondo_iris, deprecated, replaced_by, labels = parse_efo_owl(args.efo_owl)
    print(f"  Mondo terms in efo.owl: {len(all_mondo_iris)}")
    print(f"  Deprecated Mondo terms: {len(deprecated)}")

    mondo_list = load_terms_file(args.mondo_terms)
    print(f"  Terms in mondo_terms.txt: {len(mondo_list)}")

    warnings = []
    missing_from_efo = []
    added_replacements = []

    for term in sorted(mondo_list):
        if term not in all_mondo_iris:
            missing_from_efo.append(term)
            continue

        if term in deprecated:
            replacements = replaced_by.get(term, [])
            mondo_replacements = [r for r in replacements if MONDO_IRI_RE.fullmatch(r)]

            if mondo_replacements:
                for repl in mondo_replacements:
                    if repl not in mondo_list:
                        added_replacements.append((term, repl))
                        mondo_list.add(repl)
            else:
                label = labels.get(term, "")
                non_mondo_replacements = replacements if replacements else ["none"]
                warnings.append(
                    (term, label, "; ".join(non_mondo_replacements))
                )

    # Write warning report
    with open(args.output, "w") as fh:
        fh.write("obsolete_mondo_term\tlabel\treplaced_by (non-Mondo)\n")
        for term, label, repl in warnings:
            fh.write(f"{term}\t{label}\t{repl}\n")

    # Summary
    print()
    if missing_from_efo:
        print(f"ERROR: {len(missing_from_efo)} term(s) in mondo_terms.txt but NOT in efo.owl:")
        for t in missing_from_efo[:20]:
            print(f"  {t}")
        if len(missing_from_efo) > 20:
            print(f"  … and {len(missing_from_efo) - 20} more")

    if added_replacements:
        print(
            f"INFO: {len(added_replacements)} Mondo replacement(s) added to mondo_terms.txt:"
        )
        for orig, repl in added_replacements[:20]:
            print(f"  {orig} → {repl}")
        if len(added_replacements) > 20:
            print(f"  … and {len(added_replacements) - 20} more")
        if args.update:
            save_terms_file(args.mondo_terms, mondo_list)
            print(f"  mondo_terms.txt updated ({len(mondo_list)} terms)")
        else:
            print(
                "  Re-run with --update to write these additions to mondo_terms.txt"
            )

    if warnings:
        print(
            f"WARNING: {len(warnings)} obsolete Mondo term(s) with no Mondo replacement"
        )
        print(f"  See {args.output} for details")

    if not missing_from_efo and not warnings and not added_replacements:
        print("All Mondo terms in mondo_terms.txt are present and active in efo.owl")

    # Exit with error only if terms are missing from efo.owl
    if missing_from_efo:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
