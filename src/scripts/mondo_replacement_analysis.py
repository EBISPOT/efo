#!/usr/bin/env python3
"""
Phase 1 Analysis: Analyze mondo_efo_mappings.tsv against efo-edit.owl to produce
a report of terms to obsolete, children to reparent, and axiom references to update.

Usage:
    python3 mondo_replacement_analysis.py <mappings_tsv> <efo_edit_owl> <output_dir>

Example:
    python3 mondo_replacement_analysis.py \
        ../ontology/components/mondo_efo_mappings.tsv \
        ../ontology/efo-edit.owl \
        ../ontology/tmp
"""

import csv
import re
import sys
import os
from collections import defaultdict


def load_mappings(mappings_file):
    """Load mondo_efo_mappings.tsv: mondo_iri -> target_iri (EFO/DOID/Orphanet)."""
    mappings = {}  # target_iri -> mondo_iri
    reverse = {}   # mondo_iri -> target_iri
    labels = {}    # target_iri -> (mondo_label, target_label)

    with open(mappings_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 3:
                continue
            mondo_iri, target_iri = row[0], row[1]
            # Handle rows with 3 or 4+ columns (some rows have spaces instead of tab between labels)
            mondo_label = row[2] if len(row) >= 3 else ''
            target_label = row[3] if len(row) >= 4 else mondo_label
            mappings[target_iri] = mondo_iri
            reverse[mondo_iri] = target_iri
            labels[target_iri] = (mondo_label, target_label)

    return mappings, reverse, labels


def classify_iri(iri):
    """Classify an IRI as EFO, DOID, or Orphanet."""
    if 'ebi.ac.uk/efo/EFO_' in iri:
        return 'EFO'
    elif 'purl.obolibrary.org/obo/DOID_' in iri:
        return 'DOID'
    elif 'orpha.net/ORDO/Orphanet_' in iri:
        return 'Orphanet'
    return 'Unknown'


def scan_efo_edit(efo_edit_file, target_iris):
    """
    Scan efo-edit.owl for:
    1. Class definitions of the target IRIs
    2. References to target IRIs as superclass targets (children)
    3. Other axiom references to target IRIs
    """
    target_set = set(target_iris)

    # Track results
    defined_in_edit = set()       # target IRIs that have class definitions in efo-edit.owl
    children = defaultdict(list)  # target_iri -> [child_iri, ...]
    axiom_refs = defaultdict(list)  # target_iri -> [(line_num, context), ...]
    label_map = {}                # iri -> label (from efo-edit.owl)

    # Regex patterns for RDF/XML
    class_about_re = re.compile(r'<owl:Class rdf:about="([^"]+)"')
    subclass_of_re = re.compile(r'<rdfs:subClassOf rdf:resource="([^"]+)"')
    resource_ref_re = re.compile(r'rdf:resource="([^"]+)"')
    label_re = re.compile(r'<rdfs:label[^>]*>([^<]+)</rdfs:label>')

    # Track class context using a stack approach for top-level owl:Class elements
    current_class = None
    # Also detect top-level elements of other types to avoid misattributing
    top_level_re = re.compile(r'<owl:(Class|AnnotationProperty|ObjectProperty|DatatypeProperty|NamedIndividual|Axiom) rdf:about="([^"]+)"')
    top_level_end_re = re.compile(r'</owl:(Class|AnnotationProperty|ObjectProperty|DatatypeProperty|NamedIndividual|Axiom)>')
    rdf_desc_about_re = re.compile(r'<rdf:Description rdf:about="([^"]+)"')
    iao_replaced_by_re = re.compile(r'<obo:IAO_0100001[^>]*>([^<]+)</obo:IAO_0100001>')

    with open(efo_edit_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            # Track top-level class/entity context
            m = top_level_re.search(line)
            if m:
                entity_type = m.group(1)
                entity_iri = m.group(2)
                if entity_type == 'Class':
                    current_class = entity_iri
                else:
                    current_class = None  # Don't track non-class entities

            # Track labels
            m = label_re.search(line)
            if m and current_class:
                label_map[current_class] = m.group(1)

            # Check if this line defines one of our target classes
            m = class_about_re.search(line)
            if m and m.group(1) in target_set:
                defined_in_edit.add(m.group(1))

            # Check for subClassOf references pointing to target IRIs
            m = subclass_of_re.search(line)
            if m and m.group(1) in target_set:
                parent_iri = m.group(1)
                if current_class and current_class != parent_iri and current_class not in target_set:
                    children[parent_iri].append((current_class, line_num))

            # Check for any rdf:resource references to target IRIs
            for m in resource_ref_re.finditer(line):
                ref_iri = m.group(1)
                if ref_iri in target_set:
                    # Skip if this is the class definition itself (rdf:about)
                    if 'rdf:about=' in line and ref_iri == current_class:
                        continue
                    # Classify the reference type
                    if 'subClassOf' in line:
                        ref_type = 'subClassOf'
                    elif 'someValuesFrom' in line:
                        ref_type = 'someValuesFrom'
                    elif 'equivalentClass' in line:
                        ref_type = 'equivalentClass'
                    elif 'intersectionOf' in line:
                        ref_type = 'intersectionOf'
                    elif 'unionOf' in line:
                        ref_type = 'unionOf'
                    elif 'owl:imports' in line:
                        ref_type = 'import'
                    elif 'annotatedSource' in line:
                        ref_type = 'annotatedSource'
                    elif 'annotatedTarget' in line:
                        ref_type = 'annotatedTarget'
                    elif 'rdf:Description' in line:
                        ref_type = 'rdf:Description'
                    elif 'IAO_0100001' in line:
                        ref_type = 'replaced_by'
                    else:
                        ref_type = 'other'

                    axiom_refs[ref_iri].append({
                        'line': line_num,
                        'type': ref_type,
                        'context_class': current_class,
                        'line_text': line.strip()[:200]
                    })

            # Detect end of top-level element
            m = top_level_end_re.search(line)
            if m:
                current_class = None

    return defined_in_edit, children, axiom_refs, label_map


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 mondo_replacement_analysis.py <mappings_tsv> <efo_edit_owl> <output_dir>")
        sys.exit(1)

    mappings_file = sys.argv[1]
    efo_edit_file = sys.argv[2]
    output_dir = sys.argv[3]

    os.makedirs(output_dir, exist_ok=True)

    print("Loading mappings...")
    mappings, reverse, labels = load_mappings(mappings_file)
    print(f"  Loaded {len(mappings)} mappings")

    # Classify
    counts = defaultdict(int)
    for target_iri in mappings:
        counts[classify_iri(target_iri)] += 1
    for iri_type, count in sorted(counts.items()):
        print(f"  {iri_type}: {count}")

    print("\nScanning efo-edit.owl...")
    defined_in_edit, children, axiom_refs, label_map = scan_efo_edit(efo_edit_file, mappings.keys())
    print(f"  Terms defined in efo-edit.owl: {len(defined_in_edit)}")
    print(f"  Terms with children to reparent: {len(children)}")
    print(f"  Terms referenced in axioms: {len(axiom_refs)}")

    # Terms NOT defined in efo-edit.owl (only in mondo_efo_import.owl)
    not_in_edit = set(mappings.keys()) - defined_in_edit
    if not_in_edit:
        print(f"\n  WARNING: {len(not_in_edit)} mapped terms NOT found in efo-edit.owl:")
        for iri in sorted(not_in_edit)[:20]:
            print(f"    {iri}")
        if len(not_in_edit) > 20:
            print(f"    ... and {len(not_in_edit) - 20} more")

    # Write main report
    report_file = os.path.join(output_dir, 'mondo_replacement_report.tsv')
    with open(report_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'target_iri', 'mondo_iri', 'iri_type', 'target_label', 'mondo_label',
            'in_efo_edit', 'num_children', 'num_axiom_refs'
        ])
        for target_iri, mondo_iri in sorted(mappings.items()):
            mondo_label, target_label = labels.get(target_iri, ('', ''))
            writer.writerow([
                target_iri,
                mondo_iri,
                classify_iri(target_iri),
                target_label,
                mondo_label,
                'yes' if target_iri in defined_in_edit else 'no',
                len(children.get(target_iri, [])),
                len(axiom_refs.get(target_iri, []))
            ])
    print(f"\nMain report written to: {report_file}")

    # Write children report
    children_file = os.path.join(output_dir, 'mondo_replacement_children.tsv')
    with open(children_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'child_iri', 'child_label', 'old_parent_iri', 'old_parent_label',
            'new_parent_mondo_iri', 'line_num'
        ])
        for parent_iri, child_list in sorted(children.items()):
            mondo_iri = mappings[parent_iri]
            _, parent_label = labels.get(parent_iri, ('', ''))
            for child_iri, line_num in child_list:
                child_label = label_map.get(child_iri, '')
                writer.writerow([
                    child_iri, child_label, parent_iri, parent_label,
                    mondo_iri, line_num
                ])
    total_children = sum(len(v) for v in children.values())
    print(f"Children report written to: {children_file} ({total_children} children)")

    # Write axiom references report
    axiom_file = os.path.join(output_dir, 'mondo_replacement_axiom_refs.tsv')
    with open(axiom_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'referenced_iri', 'mondo_replacement', 'ref_type',
            'context_class', 'line_num', 'line_text'
        ])
        for ref_iri, refs in sorted(axiom_refs.items()):
            mondo_iri = mappings[ref_iri]
            for ref in refs:
                writer.writerow([
                    ref_iri, mondo_iri, ref['type'],
                    ref['context_class'], ref['line'], ref['line_text']
                ])
    total_refs = sum(len(v) for v in axiom_refs.values())
    print(f"Axiom refs report written to: {axiom_file} ({total_refs} references)")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total terms to obsolete: {len(mappings)}")
    for iri_type, count in sorted(counts.items()):
        print(f"  {iri_type}: {count}")
    print(f"Terms in efo-edit.owl: {len(defined_in_edit)}")
    print(f"Terms NOT in efo-edit.owl: {len(not_in_edit)}")
    print(f"Children to reparent: {total_children}")
    print(f"Axiom references to update: {total_refs}")

    # Breakdown axiom refs by type
    ref_type_counts = defaultdict(int)
    for refs in axiom_refs.values():
        for ref in refs:
            ref_type_counts[ref['type']] += 1
    print("\nAxiom reference types:")
    for ref_type, count in sorted(ref_type_counts.items(), key=lambda x: -x[1]):
        print(f"  {ref_type}: {count}")


if __name__ == '__main__':
    main()
