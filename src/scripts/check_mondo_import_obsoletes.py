#!/usr/bin/env python3
"""
QC: Check if any MONDO terms in the import term list are obsolete in the
Mondo mirror, and verify their replacements are also in the term list.

Usage:
    python3 check_mondo_import_obsoletes.py <mondo_mirror_owl> <mondo_terms_txt> [-o <output_tsv>]

Exit codes:
    0 - No issues found (or all replacements are already in the term list)
    1 - Obsolete terms found whose replacements are NOT in the term list
"""

import re
import sys


def parse_mondo_owl_deprecations(mondo_owl_path):
    """Parse mondo.owl (OWL Functional Syntax) for deprecated terms and their replacements.

    Returns:
        deprecated: set of deprecated IRIs
        replaced_by: dict of deprecated IRI -> replacement IRI
    """
    deprecated = set()
    replaced_by = {}

    # For OWL Functional Syntax, look for:
    #   AnnotationAssertion(owl:deprecated <IRI> "true"^^xsd:boolean)
    #   AnnotationAssertion(obo:IAO_0100001 <IRI> <replacement_IRI>)
    deprecated_re = re.compile(
        r'AnnotationAssertion\(owl:deprecated\s+'
        r'<?([^>\s]+)>?\s+"true"')
    replaced_by_re = re.compile(
        r'AnnotationAssertion\(obo:IAO_0100001\s+'
        r'<?([^>\s]+)>?\s+<?([^>\s]+)>?\s*\)')

    # Also handle RDF/XML format
    rdf_about_re = re.compile(r'rdf:about="([^"]+)"')
    rdf_deprecated_re = re.compile(
        r'<owl:deprecated[^>]*>true</owl:deprecated>')
    rdf_iao_resource_re = re.compile(
        r'<obo:IAO_0100001 rdf:resource="([^"]+)"')
    rdf_iao_text_re = re.compile(
        r'<obo:IAO_0100001>([^<]+)</obo:IAO_0100001>')

    current_class = None
    is_deprecated = False
    replacement = None

    with open(mondo_owl_path, 'r') as f:
        for line in f:
            # OWL Functional Syntax
            m = deprecated_re.search(line)
            if m:
                deprecated.add(m.group(1))

            m = replaced_by_re.search(line)
            if m:
                replaced_by[m.group(1)] = m.group(2)

            # RDF/XML
            if '<owl:Class rdf:about=' in line:
                m = rdf_about_re.search(line)
                if m:
                    if current_class and is_deprecated:
                        deprecated.add(current_class)
                        if replacement:
                            replaced_by[current_class] = replacement
                    current_class = m.group(1)
                    is_deprecated = False
                    replacement = None

            if current_class:
                if rdf_deprecated_re.search(line):
                    is_deprecated = True
                m = rdf_iao_resource_re.search(line)
                if m:
                    replacement = m.group(1)
                m = rdf_iao_text_re.search(line)
                if m:
                    replacement = m.group(1)

            if '</owl:Class>' in line and current_class:
                if is_deprecated:
                    deprecated.add(current_class)
                    if replacement:
                        replaced_by[current_class] = replacement
                current_class = None
                is_deprecated = False
                replacement = None

    return deprecated, replaced_by


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 check_mondo_import_obsoletes.py "
              "<mondo_mirror_owl> <mondo_terms_txt> [-o <output_tsv>]")
        sys.exit(1)

    mondo_owl = sys.argv[1]
    terms_file = sys.argv[2]
    output_file = None
    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    # Load term list
    with open(terms_file) as f:
        term_set = set(line.strip() for line in f if line.strip())
    print(f"Loaded {len(term_set)} terms from {terms_file}")

    # Parse deprecations
    print(f"Parsing {mondo_owl} for deprecations...")
    deprecated, replaced_by = parse_mondo_owl_deprecations(mondo_owl)
    print(f"  Found {len(deprecated)} deprecated terms in Mondo")
    print(f"  Found {len(replaced_by)} replaced_by mappings")

    # Check which imported terms are deprecated
    deprecated_imports = term_set & deprecated
    print(f"\nDeprecated terms in import list: {len(deprecated_imports)}")

    issues = []
    warnings = []
    for term in sorted(deprecated_imports):
        replacement = replaced_by.get(term)
        if replacement:
            if replacement in term_set:
                status = "OK"
            else:
                status = "MISSING_REPLACEMENT"
                issues.append((term, replacement))
        else:
            status = "NO_REPLACEMENT"
            warnings.append(term)

        if status == "MISSING_REPLACEMENT":
            print(f"  {status}: {term} -> {replacement}")

    # Write report
    if output_file:
        with open(output_file, 'w') as f:
            f.write("deprecated_term\treplacement\tstatus\n")
            for term in sorted(deprecated_imports):
                replacement = replaced_by.get(term, '')
                if replacement and replacement in term_set:
                    status = "OK"
                elif replacement:
                    status = "MISSING_REPLACEMENT"
                else:
                    status = "NO_REPLACEMENT"
                f.write(f"{term}\t{replacement}\t{status}\n")
        print(f"\nReport written to: {output_file}")

    # Summary
    print(f"\nSummary:")
    print(f"  Total imported terms: {len(term_set)}")
    print(f"  Deprecated in Mondo: {len(deprecated_imports)}")
    print(f"  Missing replacements in term list: {len(issues)}")
    print(f"  No replacement defined: {len(warnings)}")

    if issues:
        print(f"\nERROR: {len(issues)} deprecated terms have replacements "
              f"not in the import term list.")
        print("Add the replacement IRIs to mondo_terms.txt:")
        for term, replacement in issues:
            print(f"  {replacement}")
        sys.exit(1)
    else:
        if warnings:
            print(f"\nWARNING: {len(warnings)} deprecated terms have no "
                  f"replacement defined in Mondo (see report for details).")
        print("\nAll actionable checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
