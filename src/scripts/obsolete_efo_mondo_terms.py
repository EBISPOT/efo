#!/usr/bin/env python3
"""
Bulk obsolescence of EFO/Orphanet terms with Mondo replacements.

This script performs two operations on efo-edit.owl:

1. RE-PARENT CHILDREN (Phase 3):
   For each child term whose parent is being obsoleted:
   - If action=replace_with_mondo: replace the SubClassOf target with the Mondo IRI
   - If action=remove_only: remove the SubClassOf axiom (child has other parents)

2. OBSOLETE TERMS (Phase 4):
   For each EFO/Orphanet term in the mappings:
   - Remove all SubClassOf and EquivalentClass axioms
   - Add owl:deprecated = true
   - Prefix rdfs:label with "obsolete_"
   - Add obo:IAO_0100001 (term_replaced_by) = Mondo IRI
   - Add efo:obsoleted_in_version = 3.88
   - Add efo:reason_for_obsolescence
   - Preserve all other annotations (synonyms, xrefs, definitions, etc.)

Usage:
    python obsolete_efo_mondo_terms.py [--dry-run] [--output OUTPUT_FILE]

Input files (relative to repo root):
    - src/ontology/components/mondo_efo_mappings.tsv
    - reports/children_to_reparent.tsv
    - src/ontology/efo-edit.owl

Output:
    - Modified efo-edit.owl (or specified output file)
    - Change log to stdout
"""

import argparse
import re
import sys
from collections import defaultdict


# XML namespace prefixes used in efo-edit.owl
NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "obo": "http://purl.obolibrary.org/obo/",
    "efo": "http://www.ebi.ac.uk/efo/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "oboInOwl": "http://www.geneontology.org/formats/oboInOwl#",
}

# Term replaced by property
IAO_0100001 = "http://purl.obolibrary.org/obo/IAO_0100001"

# EFO-specific properties
EFO_OBSOLETED_IN_VERSION = "http://www.ebi.ac.uk/efo/obsoleted_in_version"
EFO_REASON_FOR_OBSOLESCENCE = "http://www.ebi.ac.uk/efo/reason_for_obsolescence"


def is_efo(iri):
    return "ebi.ac.uk/efo/EFO_" in iri


def is_orphanet(iri):
    return "orpha.net" in iri.lower()


def load_mappings(path):
    """Load mondo_efo_mappings.tsv.

    Returns dict: term_iri -> (mondo_iri, mondo_label, term_label)
    Only includes EFO and Orphanet terms.
    """
    mappings = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            mondo_iri = parts[0].strip()
            term_iri = parts[1].strip()
            mondo_label = parts[2].strip() if len(parts) > 2 else ""
            term_label = parts[3].strip() if len(parts) > 3 else ""

            if is_efo(term_iri) or is_orphanet(term_iri):
                mappings[term_iri] = (mondo_iri, mondo_label, term_label)

    return mappings


def load_reparent_instructions(path):
    """Load children_to_reparent.tsv.

    Returns list of dicts with keys:
        child_iri, old_parent_iri, new_parent_iri, action
    """
    instructions = []
    with open(path) as fh:
        header = None
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            row = dict(zip(header, parts))
            instructions.append({
                "child_iri": row.get("child_iri", ""),
                "old_parent_iri": row.get("old_parent_iri", ""),
                "new_parent_iri": row.get("new_parent_iri", ""),
                "action": row.get("action", "replace_with_mondo"),
            })
    return instructions


def read_owl_file(path):
    """Read OWL file as text."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def write_owl_file(path, content):
    """Write OWL file."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def find_class_block(content, iri):
    """Find the start and end positions of an owl:Class block for the given IRI.

    Returns (start, end) positions, or (None, None) if not found.
    The block includes from <owl:Class rdf:about="IRI"> to </owl:Class>.
    """
    # Escape special regex characters in IRI
    escaped_iri = re.escape(iri)

    # Pattern to find the class declaration
    pattern = rf'(<owl:Class rdf:about="{escaped_iri}"[^>]*>)'
    match = re.search(pattern, content)

    if not match:
        return None, None

    start = match.start()

    # Now find the closing </owl:Class> tag
    # We need to handle nested structures, but owl:Class typically doesn't nest
    # Look for </owl:Class> after the opening tag
    search_start = match.end()

    # Find the closing tag - need to handle that there might be nested anonymous classes
    depth = 1
    pos = search_start
    while depth > 0 and pos < len(content):
        next_open = content.find("<owl:Class", pos)
        next_close = content.find("</owl:Class>", pos)

        if next_close == -1:
            # No closing tag found - malformed
            return None, None

        if next_open != -1 and next_open < next_close:
            # Found another opening tag before the closing tag
            depth += 1
            pos = next_open + 10
        else:
            # Found closing tag
            depth -= 1
            if depth == 0:
                end = next_close + len("</owl:Class>")
                return start, end
            pos = next_close + 12

    return None, None


def extract_label(class_block):
    """Extract the rdfs:label value from a class block."""
    # Match rdfs:label with various formats
    patterns = [
        r'<rdfs:label[^>]*>([^<]+)</rdfs:label>',
        r'<rdfs:label[^>]*xml:lang="[^"]*">([^<]+)</rdfs:label>',
    ]
    for pattern in patterns:
        match = re.search(pattern, class_block)
        if match:
            return match.group(1)
    return ""


def is_already_deprecated(class_block):
    """Check if a class block is already deprecated."""
    return "owl:deprecated" in class_block and ">true<" in class_block


def remove_subclass_axioms(class_block):
    """Remove all rdfs:subClassOf axioms from a class block."""
    # Remove simple subClassOf (named class reference)
    class_block = re.sub(
        r'\s*<rdfs:subClassOf rdf:resource="[^"]+"/>\s*',
        "\n",
        class_block
    )

    # Remove complex subClassOf (with nested restrictions/anonymous classes)
    # These span multiple lines and contain nested elements
    while True:
        # Find subClassOf with nested content
        match = re.search(
            r'\s*<rdfs:subClassOf>\s*.*?</rdfs:subClassOf>\s*',
            class_block,
            re.DOTALL
        )
        if not match:
            break
        class_block = class_block[:match.start()] + "\n" + class_block[match.end():]

    return class_block


def remove_equivalent_class_axioms(class_block):
    """Remove all owl:equivalentClass axioms from a class block."""
    # Remove equivalentClass with nested content
    while True:
        match = re.search(
            r'\s*<owl:equivalentClass>.*?</owl:equivalentClass>\s*',
            class_block,
            re.DOTALL
        )
        if not match:
            break
        class_block = class_block[:match.start()] + "\n" + class_block[match.end():]

    # Also remove simple equivalentClass references (rare but possible)
    class_block = re.sub(
        r'\s*<owl:equivalentClass rdf:resource="[^"]+"/>\s*',
        "\n",
        class_block
    )

    return class_block


def update_label_to_obsolete(class_block):
    """Prefix the rdfs:label with 'obsolete_' if not already prefixed."""
    def replace_label(match):
        prefix = match.group(1)
        label = match.group(2)
        suffix = match.group(3)

        if label.startswith("obsolete_"):
            return match.group(0)  # Already obsolete

        return f"{prefix}obsolete_{label}{suffix}"

    # Handle label with xml:lang attribute
    class_block = re.sub(
        r'(<rdfs:label[^>]*>)(.*?)(</rdfs:label>)',
        replace_label,
        class_block
    )

    return class_block


def add_deprecated_annotation(class_block):
    """Add owl:deprecated annotation if not present."""
    if "owl:deprecated" in class_block:
        return class_block

    # Find a good insertion point - after the opening tag
    match = re.search(r'(<owl:Class rdf:about="[^"]+">)', class_block)
    if match:
        insert_pos = match.end()
        deprecated_xml = '\n        <owl:deprecated rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</owl:deprecated>'
        class_block = class_block[:insert_pos] + deprecated_xml + class_block[insert_pos:]

    return class_block


def add_term_replaced_by(class_block, mondo_iri):
    """Add obo:IAO_0100001 (term_replaced_by) annotation."""
    if IAO_0100001 in class_block or "IAO_0100001" in class_block:
        return class_block  # Already has replaced_by

    # Find insertion point
    match = re.search(r'(<owl:Class rdf:about="[^"]+">)', class_block)
    if match:
        insert_pos = match.end()
        replaced_by_xml = f'\n        <obo:IAO_0100001 rdf:resource="{mondo_iri}"/>'
        class_block = class_block[:insert_pos] + replaced_by_xml + class_block[insert_pos:]

    return class_block


def add_obsoleted_in_version(class_block, version="3.88"):
    """Add efo:obsoleted_in_version annotation."""
    if "obsoleted_in_version" in class_block:
        return class_block  # Already has version

    match = re.search(r'(<owl:Class rdf:about="[^"]+">)', class_block)
    if match:
        insert_pos = match.end()
        version_xml = f'\n        <efo:obsoleted_in_version>{version}</efo:obsoleted_in_version>'
        class_block = class_block[:insert_pos] + version_xml + class_block[insert_pos:]

    return class_block


def add_reason_for_obsolescence(class_block, mondo_iri, mondo_label):
    """Add efo:reason_for_obsolescence annotation."""
    if "reason_for_obsolescence" in class_block:
        return class_block  # Already has reason

    # Extract MONDO ID from IRI for the reason text
    mondo_id = mondo_iri.split("/")[-1].replace("_", ":")
    reason = f"Term merged into Mondo. Use {mondo_id} ({mondo_label})"

    match = re.search(r'(<owl:Class rdf:about="[^"]+">)', class_block)
    if match:
        insert_pos = match.end()
        reason_xml = f'\n        <efo:reason_for_obsolescence>{reason}</efo:reason_for_obsolescence>'
        class_block = class_block[:insert_pos] + reason_xml + class_block[insert_pos:]

    return class_block


def reparent_child(content, child_iri, old_parent_iri, new_parent_iri, action):
    """Re-parent a child term.

    If action=replace_with_mondo: replace the old parent IRI with new parent IRI
    If action=remove_only: remove the SubClassOf axiom entirely

    Returns updated content and a status message.
    """
    start, end = find_class_block(content, child_iri)
    if start is None:
        return content, f"NOT_FOUND: {child_iri}"

    class_block = content[start:end]
    original_block = class_block

    # Escape IRIs for regex
    escaped_old = re.escape(old_parent_iri)

    if action == "remove_only":
        # Remove the SubClassOf axiom pointing to old_parent_iri
        pattern = rf'\s*<rdfs:subClassOf rdf:resource="{escaped_old}"/>'
        new_block = re.sub(pattern, "", class_block)
    else:
        # Replace old_parent_iri with new_parent_iri
        pattern = rf'(<rdfs:subClassOf rdf:resource="){escaped_old}(")'
        new_block = re.sub(pattern, rf'\g<1>{new_parent_iri}\g<2>', class_block)

    if new_block == original_block:
        return content, f"NO_CHANGE: {child_iri} (parent {old_parent_iri} not found in SubClassOf)"

    content = content[:start] + new_block + content[end:]
    return content, f"REPARENTED: {child_iri} ({action})"


def obsolete_term(content, term_iri, mondo_iri, mondo_label, term_label):
    """Obsolete a single term.

    Returns updated content and a status message.
    """
    start, end = find_class_block(content, term_iri)
    if start is None:
        return content, f"NOT_FOUND: {term_iri}"

    class_block = content[start:end]

    # Check if already deprecated
    if is_already_deprecated(class_block):
        return content, f"ALREADY_DEPRECATED: {term_iri}"

    # Apply transformations
    class_block = remove_subclass_axioms(class_block)
    class_block = remove_equivalent_class_axioms(class_block)
    class_block = add_deprecated_annotation(class_block)
    class_block = update_label_to_obsolete(class_block)
    class_block = add_term_replaced_by(class_block, mondo_iri)
    class_block = add_obsoleted_in_version(class_block, "3.88")
    class_block = add_reason_for_obsolescence(class_block, mondo_iri, mondo_label)

    # Clean up multiple consecutive newlines
    class_block = re.sub(r'\n\s*\n\s*\n', '\n\n', class_block)

    content = content[:start] + class_block + content[end:]
    return content, f"OBSOLETED: {term_iri} -> {mondo_iri}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without modifying files",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: overwrite input)",
    )
    parser.add_argument(
        "--mappings",
        default="src/ontology/components/mondo_efo_mappings.tsv",
        help="Path to mappings TSV",
    )
    parser.add_argument(
        "--reparent",
        default="reports/children_to_reparent.tsv",
        help="Path to re-parenting instructions TSV",
    )
    parser.add_argument(
        "--owl",
        default="src/ontology/efo-edit.owl",
        help="Path to efo-edit.owl",
    )
    args = parser.parse_args()

    # Load data
    print(f"Loading mappings from {args.mappings}...", file=sys.stderr)
    mappings = load_mappings(args.mappings)
    print(f"  Loaded {len(mappings)} EFO/Orphanet -> Mondo mappings", file=sys.stderr)

    print(f"Loading re-parenting instructions from {args.reparent}...", file=sys.stderr)
    reparent_instructions = load_reparent_instructions(args.reparent)
    print(f"  Loaded {len(reparent_instructions)} re-parenting instructions", file=sys.stderr)

    print(f"Reading OWL file {args.owl}...", file=sys.stderr)
    content = read_owl_file(args.owl)
    print(f"  Read {len(content):,} bytes", file=sys.stderr)

    # Statistics
    stats = defaultdict(int)

    # Phase 3: Re-parent children
    print("\n=== PHASE 3: Re-parenting children ===", file=sys.stderr)
    for i, instr in enumerate(reparent_instructions):
        if (i + 1) % 100 == 0:
            print(f"  Processing re-parent {i + 1}/{len(reparent_instructions)}...", file=sys.stderr)

        content, status = reparent_child(
            content,
            instr["child_iri"],
            instr["old_parent_iri"],
            instr["new_parent_iri"],
            instr["action"],
        )

        status_type = status.split(":")[0]
        stats[f"reparent_{status_type}"] += 1

        if args.dry_run or "NOT_FOUND" in status or "NO_CHANGE" in status:
            print(status)

    print(f"\nRe-parenting summary:", file=sys.stderr)
    print(f"  REPARENTED: {stats.get('reparent_REPARENTED', 0)}", file=sys.stderr)
    print(f"  NOT_FOUND: {stats.get('reparent_NOT_FOUND', 0)}", file=sys.stderr)
    print(f"  NO_CHANGE: {stats.get('reparent_NO_CHANGE', 0)}", file=sys.stderr)

    # Phase 4: Obsolete terms
    print("\n=== PHASE 4: Obsoleting terms ===", file=sys.stderr)
    terms_to_obsolete = list(mappings.items())
    for i, (term_iri, (mondo_iri, mondo_label, term_label)) in enumerate(terms_to_obsolete):
        if (i + 1) % 100 == 0:
            print(f"  Processing obsolete {i + 1}/{len(terms_to_obsolete)}...", file=sys.stderr)

        content, status = obsolete_term(
            content,
            term_iri,
            mondo_iri,
            mondo_label,
            term_label,
        )

        status_type = status.split(":")[0]
        stats[f"obsolete_{status_type}"] += 1

        if args.dry_run or "NOT_FOUND" in status:
            print(status)

    print(f"\nObsolescence summary:", file=sys.stderr)
    print(f"  OBSOLETED: {stats.get('obsolete_OBSOLETED', 0)}", file=sys.stderr)
    print(f"  ALREADY_DEPRECATED: {stats.get('obsolete_ALREADY_DEPRECATED', 0)}", file=sys.stderr)
    print(f"  NOT_FOUND: {stats.get('obsolete_NOT_FOUND', 0)}", file=sys.stderr)

    # Write output
    if args.dry_run:
        print("\n[DRY RUN] No files modified.", file=sys.stderr)
    else:
        output_path = args.output or args.owl
        print(f"\nWriting output to {output_path}...", file=sys.stderr)
        write_owl_file(output_path, content)
        print(f"  Written {len(content):,} bytes", file=sys.stderr)

    print("\nDone.", file=sys.stderr)


if __name__ == "__main__":
    main()
