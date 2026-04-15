#!/usr/bin/env python3
"""
Phase 2: Apply Mondo replacements to efo-edit.owl.

This script:
1. Replaces all axiom references to mapped EFO/DOID/Orphanet IRIs with MONDO IRIs
2. Obsoletes all 2,658 mapped terms with proper deprecation annotations
3. Removes subClassOf and equivalentClass axioms from obsoleted terms
4. Preserves annotatedSource references (annotation axioms about the term)

Usage:
    python3 apply_mondo_replacements.py <mappings_tsv> <efo_edit_owl> [--dry-run]
"""

import csv
import os
import re
import sys
from collections import defaultdict


def load_mappings(mappings_file):
    """Load mondo_efo_mappings.tsv: target_iri -> mondo_iri."""
    mappings = {}
    labels = {}

    with open(mappings_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 3:
                continue
            mondo_iri, target_iri = row[0], row[1]
            mondo_label = row[2] if len(row) >= 3 else ''
            target_label = row[3] if len(row) >= 4 else mondo_label
            mappings[target_iri] = mondo_iri
            labels[target_iri] = (mondo_label, target_label)

    return mappings, labels


def classify_iri(iri):
    """Classify an IRI as EFO, DOID, or Orphanet."""
    if 'ebi.ac.uk/efo/EFO_' in iri:
        return 'EFO'
    elif 'purl.obolibrary.org/obo/DOID_' in iri:
        return 'DOID'
    elif 'orpha.net/ORDO/Orphanet_' in iri:
        return 'Orphanet'
    return 'Unknown'


def extract_mondo_id(mondo_iri):
    """Extract MONDO_XXXXXXX from full IRI."""
    m = re.search(r'(MONDO_\d+)', mondo_iri)
    return m.group(1) if m else mondo_iri


def build_reason(target_iri, mondo_iri):
    """Build the reason_for_obsolescence string."""
    mondo_id = extract_mondo_id(mondo_iri)
    iri_type = classify_iri(target_iri)

    if iri_type == 'EFO':
        return (f"Replaced by Mondo term {mondo_id}, with which this term "
                f"was previously merged. Use: {mondo_iri}")
    else:
        return (f"Replaced by Mondo term {mondo_id}, with which this term "
                f"was previously merged. This term is an old static import "
                f"into EFO and is therefore out of date. It is being "
                f"obsoleted in EFO for preservation and tracking. This term "
                f"should be considered obsolete in EFO only if it differs "
                f"from the domain source. Replaced by: {mondo_iri}")


def build_obsolescence_annotations(target_iri, mondo_iri, indent="        "):
    """Build the XML elements for obsolescence annotations."""
    reason = build_reason(target_iri, mondo_iri)
    lines = [
        f'{indent}<obo:IAO_0100001>{mondo_iri}</obo:IAO_0100001>',
        f'{indent}<efo:obsoleted_in_version>3.88.0</efo:obsoleted_in_version>',
        f'{indent}<efo:reason_for_obsolescence>{reason}</efo:reason_for_obsolescence>',
        f'{indent}<owl:deprecated rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</owl:deprecated>',
    ]
    return lines


def process_efo_edit(efo_edit_file, mappings, labels, dry_run=False):
    """Process efo-edit.owl line by line."""
    target_set = set(mappings.keys())
    output_lines = []
    stats = defaultdict(int)

    # Regex patterns
    class_about_re = re.compile(r'<owl:Class rdf:about="([^"]+)"')
    class_end_re = re.compile(r'</owl:Class>')
    top_level_re = re.compile(
        r'<owl:(AnnotationProperty|ObjectProperty|DatatypeProperty|'
        r'NamedIndividual|Axiom) rdf:about="([^"]+)"')
    top_level_end_re = re.compile(
        r'</owl:(Class|AnnotationProperty|ObjectProperty|DatatypeProperty|'
        r'NamedIndividual|Axiom)>')
    subclass_simple_re = re.compile(
        r'\s*<rdfs:subClassOf rdf:resource="[^"]+"/>\s*$')
    subclass_open_re = re.compile(r'\s*<rdfs:subClassOf[\s>]')
    equiv_simple_re = re.compile(
        r'\s*<owl:equivalentClass rdf:resource="[^"]+"/>\s*$')
    equiv_open_re = re.compile(r'\s*<owl:equivalentClass[\s>]')
    disjoint_simple_re = re.compile(
        r'\s*<owl:disjointWith rdf:resource="[^"]+"/>\s*$')
    disjoint_open_re = re.compile(r'\s*<owl:disjointWith[\s>]')
    label_re = re.compile(r'(<rdfs:label[^>]*>)([^<]+)(</rdfs:label>)')
    resource_re = re.compile(r'rdf:resource="([^"]+)"')
    annotated_source_re = re.compile(r'owl:annotatedSource')
    imports_re = re.compile(
        r'<owl:imports rdf:resource='
        r'"http://www.ebi.ac.uk/efo/components/mondo_efo_import.owl"/>')

    # State
    current_class = None
    in_mapped_class = False
    skip_until_close = False
    skip_depth = 0
    added_obsolescence = False
    processed_label = False

    with open(efo_edit_file, 'r') as f:
        all_lines = f.readlines()

    for line in all_lines:
        # === Handle import statement swap ===
        if imports_re.search(line):
            output_lines.append(
                line.replace(
                    'http://www.ebi.ac.uk/efo/components/mondo_efo_import.owl',
                    'http://www.ebi.ac.uk/efo/imports/mondo_import.owl'))
            stats['import_swapped'] += 1
            continue

        # === Track class context ===
        m = class_about_re.search(line)
        if m and 'rdf:resource=' not in line:
            current_class = m.group(1)
            in_mapped_class = current_class in target_set
            added_obsolescence = False
            processed_label = False
            if in_mapped_class:
                stats['classes_obsoleted'] += 1

        # Track non-class top-level elements to reset state
        if top_level_re.search(line):
            current_class = None
            in_mapped_class = False

        # === Handle skip state (multi-line block removal) ===
        if skip_until_close:
            opens = len(re.findall(
                r'<(?:rdfs:subClassOf|owl:equivalentClass|'
                r'owl:disjointWith|owl:Class|owl:Restriction)[\s>]', line))
            closes = len(re.findall(
                r'</(?:rdfs:subClassOf|owl:equivalentClass|'
                r'owl:disjointWith|owl:Class|owl:Restriction)>', line))
            skip_depth += opens - closes
            if skip_depth <= 0:
                skip_until_close = False
                skip_depth = 0
            continue

        # === Inside a mapped class: remove structural axioms ===
        if in_mapped_class:
            # Skip simple subClassOf
            if subclass_simple_re.match(line):
                stats['subclass_removed'] += 1
                continue

            # Skip complex subClassOf (multi-line)
            if (subclass_open_re.match(line) and
                    '/>' not in line and
                    '</rdfs:subClassOf>' not in line):
                skip_until_close = True
                skip_depth = 1
                stats['subclass_removed'] += 1
                continue

            # Skip simple equivalentClass
            if equiv_simple_re.match(line):
                stats['equiv_removed'] += 1
                continue

            # Skip complex equivalentClass (multi-line)
            if (equiv_open_re.match(line) and
                    '/>' not in line and
                    '</owl:equivalentClass>' not in line):
                skip_until_close = True
                skip_depth = 1
                stats['equiv_removed'] += 1
                continue

            # Skip disjointWith (simple, self-closing)
            if disjoint_simple_re.match(line):
                stats['disjoint_removed'] += 1
                continue

            # Skip complex disjointWith (multi-line)
            if (disjoint_open_re.match(line) and
                    '/>' not in line and
                    '</owl:disjointWith>' not in line):
                skip_until_close = True
                skip_depth = 1
                stats['disjoint_removed'] += 1
                continue

            # Rename label to obsolete_
            m = label_re.search(line)
            if m and not processed_label:
                old_label = m.group(2)
                if not old_label.startswith('obsolete_'):
                    new_label = f'obsolete_{old_label}'
                    line = line[:m.start(2)] + new_label + line[m.end(2):]
                    stats['labels_renamed'] += 1
                processed_label = True

        # === Replace rdf:resource references to mapped IRIs ===
        # Skip annotatedSource lines (these are annotation axioms about
        # the obsoleted term itself and should keep their original IRI)
        if not annotated_source_re.search(line):
            for m in resource_re.finditer(line):
                ref_iri = m.group(1)
                if ref_iri in target_set:
                    if f'rdf:about="{ref_iri}"' in line:
                        continue
                    mondo_iri = mappings[ref_iri]
                    line = line.replace(
                        f'rdf:resource="{ref_iri}"',
                        f'rdf:resource="{mondo_iri}"',
                        1)
                    stats['refs_replaced'] += 1
        else:
            for m in resource_re.finditer(line):
                if m.group(1) in target_set:
                    stats['annotated_source_skipped'] += 1

        # === Replace mapped IRIs in IAO_0100001 text content ===
        # Pattern: <obo:IAO_0100001>http://www.ebi.ac.uk/efo/EFO_XXXX</obo:IAO_0100001>
        # These are replaced_by pointers on *other* obsolete terms
        if ('<obo:IAO_0100001>' in line and
                not in_mapped_class):
            for target_iri in target_set:
                old_text = f'<obo:IAO_0100001>{target_iri}</obo:IAO_0100001>'
                if old_text in line:
                    mondo_iri = mappings[target_iri]
                    new_text = f'<obo:IAO_0100001>{mondo_iri}</obo:IAO_0100001>'
                    line = line.replace(old_text, new_text, 1)
                    stats['replaced_by_updated'] += 1
                    break  # Only one IAO_0100001 per line

        # === Insert obsolescence annotations before </owl:Class> ===
        if (in_mapped_class and class_end_re.search(line)
                and not added_obsolescence):
            mondo_iri = mappings[current_class]
            obs_lines = build_obsolescence_annotations(
                current_class, mondo_iri)
            for obs_line in obs_lines:
                output_lines.append(obs_line + '\n')
            added_obsolescence = True

        # === Reset at end of top-level element ===
        if top_level_end_re.search(line):
            if in_mapped_class:
                in_mapped_class = False
            current_class = None

        output_lines.append(line)

    return output_lines, stats


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 apply_mondo_replacements.py "
              "<mappings_tsv> <efo_edit_owl> [--dry-run]")
        sys.exit(1)

    mappings_file = sys.argv[1]
    efo_edit_file = sys.argv[2]
    dry_run = '--dry-run' in sys.argv

    print("Loading mappings...")
    mappings, labels = load_mappings(mappings_file)
    print(f"  Loaded {len(mappings)} mappings")

    print(f"\nProcessing {efo_edit_file}...")
    output_lines, stats = process_efo_edit(
        efo_edit_file, mappings, labels, dry_run)

    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    for key, value in sorted(stats.items()):
        print(f"  {key}: {value}")

    # Sanity checks
    expected = len(mappings)
    warnings = []
    if stats['classes_obsoleted'] != expected:
        warnings.append(
            f"Expected {expected} obsoletions, got {stats['classes_obsoleted']}")
    if stats['labels_renamed'] != expected:
        warnings.append(
            f"Expected {expected} label renames, got {stats['labels_renamed']}")
    if stats.get('import_swapped', 0) != 1:
        warnings.append(
            f"Expected 1 import swap, got {stats.get('import_swapped', 0)}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if dry_run:
        output_file = efo_edit_file + '.dry-run'
        print(f"\nDRY RUN: Writing to {output_file}")
    else:
        output_file = efo_edit_file
        print(f"\nWriting modified file to {output_file}")

    with open(output_file, 'w') as f:
        f.writelines(output_lines)

    # Write log file
    log_dir = os.path.join(os.path.dirname(efo_edit_file), 'tmp')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mondo_replacement_changes.log')
    with open(log_file, 'w') as f:
        f.write("MONDO REPLACEMENT LOG\n")
        f.write("=" * 60 + "\n\n")
        for key, value in sorted(stats.items()):
            f.write(f"{key}: {value}\n")
        if warnings:
            f.write("\nWARNINGS:\n")
            for w in warnings:
                f.write(f"  - {w}\n")
    print(f"Log written to: {log_file}")

    print(f"Done. Output: {output_file}")
    print(f"Total lines: {len(output_lines)}")


if __name__ == '__main__':
    main()
