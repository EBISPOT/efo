#!/usr/bin/env python3
"""QC check: verify all Mondo terms in iri_dependencies/mondo_terms.txt are present in EFO.

For obsoleted terms, checks whether the term_replaced_by annotation points to a Mondo
term.  If it does, verifies the replacement exists in mirror/mondo.owl before
suggesting it be added to mondo_terms.txt.  Invalid or non-existent replacement terms
are flagged as warnings.
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
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    terms.add(line)
    except FileNotFoundError:
        pass
    return terms


def save_terms_file(path, terms):
    """Write a sorted set of IRIs back to a text file."""
    with open(path, "w") as fh:
        for t in sorted(terms):
            fh.write(t + "\n")


def parse_mondo_mirror(mondo_path):
    """Parse mirror/mondo.owl and return the set of all Mondo IRIs that exist."""
    mondo_iris = set()

    tree = ET.parse(mondo_path)
    root = tree.getroot()

    for cls in root.iter("{http://www.w3.org/2002/07/owl#}Class"):
        about = cls.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", "")
        if MONDO_IRI_RE.fullmatch(about):
            mondo_iris.add(about)

    return mondo_iris


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
        "-m",
        "--mondo-mirror",
        default="mirror/mondo.owl",
        help="Path to mirror/mondo.owl for validating Mondo terms (default: mirror/mondo.owl)",
    )
    parser.add_argument(
        "-e",
        "--mondo-exclude",
        default="iri_dependencies/mondo_exclude.txt",
        help="Path to iri_dependencies/mondo_exclude.txt (default: iri_dependencies/mondo_exclude.txt)",
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
        help="If set, automatically add missing replacement Mondo terms to mondo_terms.txt (only if they exist in mondo.owl)",
    )
    args = parser.parse_args()

    print("Parsing mirror/mondo.owl …")
    try:
        valid_mondo_iris = parse_mondo_mirror(args.mondo_mirror)
        print(f"  Valid Mondo terms in mirror: {len(valid_mondo_iris)}")
    except FileNotFoundError:
        print(f"  WARNING: {args.mondo_mirror} not found, skipping validation")
        valid_mondo_iris = None

    print("Loading mondo_exclude.txt …")
    exclude_list = load_terms_file(args.mondo_exclude)
    print(f"  Terms in mondo_exclude.txt: {len(exclude_list)}")

    print("Parsing efo.owl …")
    all_mondo_iris, deprecated, replaced_by, labels = parse_efo_owl(args.efo_owl)
    print(f"  Mondo terms in efo.owl: {len(all_mondo_iris)}")
    print(f"  Deprecated Mondo terms: {len(deprecated)}")

    mondo_list = load_terms_file(args.mondo_terms)
    print(f"  Terms in mondo_terms.txt: {len(mondo_list)}")

    warnings = []
    missing_from_efo = []
    missing_in_exclude = []
    missing_not_in_exclude = []
    added_replacements = []
    invalid_replacements = []

    for term in sorted(mondo_list):
        if term not in all_mondo_iris:
            missing_from_efo.append(term)
            if term in exclude_list:
                missing_in_exclude.append(term)
            else:
                missing_not_in_exclude.append(term)
            continue

        if term in deprecated:
            replacements = replaced_by.get(term, [])
            mondo_replacements = [r for r in replacements if MONDO_IRI_RE.fullmatch(r)]

            if mondo_replacements:
                for repl in mondo_replacements:
                    if repl not in mondo_list:
                        # Check if replacement exists in mondo.owl mirror
                        if valid_mondo_iris is not None and repl not in valid_mondo_iris:
                            # Replacement doesn't exist in Mondo - flag as warning
                            label = labels.get(term, "")
                            invalid_replacements.append((term, label, repl))
                        else:
                            # Valid replacement - can be added
                            added_replacements.append((term, repl))
                            if args.update:
                                mondo_list.add(repl)
            else:
                label = labels.get(term, "")
                non_mondo_replacements = replacements if replacements else ["none"]
                warnings.append(
                    (term, label, "; ".join(non_mondo_replacements))
                )

    # Write warning report
    with open(args.output, "w") as fh:
        fh.write("obsolete_mondo_term\tlabel\treplaced_by (non-Mondo or invalid)\n")
        for term, label, repl in warnings:
            fh.write(f"{term}\t{label}\t{repl}\n")
        for term, label, repl in invalid_replacements:
            fh.write(f"{term}\t{label}\t{repl} (NOT IN MONDO)\n")

    # Summary
    print()
    if missing_from_efo:
        print(f"WARNING: {len(missing_from_efo)} term(s) in mondo_terms.txt but NOT in efo.owl:")
        if missing_in_exclude:
            print(f"  {len(missing_in_exclude)} term(s) ARE in mondo_exclude.txt (expected):")
            for t in missing_in_exclude[:10]:
                print(f"    {t}")
            if len(missing_in_exclude) > 10:
                print(f"    … and {len(missing_in_exclude) - 10} more")
        if missing_not_in_exclude:
            print(f"  {len(missing_not_in_exclude)} term(s) are NOT in mondo_exclude.txt (unexpected):")
            for t in missing_not_in_exclude[:20]:
                print(f"    {t}")
            if len(missing_not_in_exclude) > 20:
                print(f"    … and {len(missing_not_in_exclude) - 20} more")

    if invalid_replacements:
        print(
            f"WARNING: {len(invalid_replacements)} term_replaced_by target(s) do not exist in Mondo:"
        )
        for orig, label, repl in invalid_replacements[:20]:
            print(f"  {orig} ({label}) → {repl}")
        if len(invalid_replacements) > 20:
            print(f"  … and {len(invalid_replacements) - 20} more")

    if added_replacements:
        print(
            f"INFO: {len(added_replacements)} valid Mondo replacement(s) to add to mondo_terms.txt:"
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

    if not missing_from_efo and not warnings and not added_replacements and not invalid_replacements:
        print("All Mondo terms in mondo_terms.txt are present and active in efo.owl")

    sys.exit(0)


if __name__ == "__main__":
    main()
