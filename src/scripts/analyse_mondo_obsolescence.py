#!/usr/bin/env python3
"""Phase 1 analysis: dry-run pre-flight for bulk Mondo obsolescence.

Reads mondo_efo_mappings.tsv and efo-edit.owl to produce four reports:

  reports/mondo_obsolescence_plan.tsv   - all EFO/Orphanet terms to obsolete
  reports/children_to_reparent.tsv      - children needing a new parent
  reports/mondo_terms_to_import.tsv     - Mondo IRIs not yet in iri_dependencies
  reports/other_terms_in_mappings.tsv   - non-EFO/non-Orphanet rows (DOID etc.)

This script is READ-ONLY. It does not modify any files.
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
OWL = "http://www.w3.org/2002/07/owl#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OBO = "http://purl.obolibrary.org/obo/"


def is_efo(iri):
    return "ebi.ac.uk/efo/EFO_" in iri


def is_orphanet(iri):
    return "orpha.net" in iri.lower()


def load_mappings(path):
    """Returns list of (mondo_iri, term_iri, mondo_label, term_label)."""
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                mondo_iri = parts[0].strip()
                term_iri = parts[1].strip()
                mondo_label = parts[2].strip() if len(parts) > 2 else ""
                term_label = parts[3].strip() if len(parts) > 3 else ""
                rows.append((mondo_iri, term_iri, mondo_label, term_label))
    return rows


def parse_owl(owl_path):
    """Parse efo-edit.owl.

    Returns a dict:  IRI -> {label, deprecated, parents: set[IRI], children: set[IRI]}

    Only named superclasses (rdf:resource on rdfs:subClassOf) are captured;
    anonymous restriction parents are ignored for the purpose of this analysis.
    """
    print(f"Parsing {owl_path} …", flush=True)
    tree = ET.parse(owl_path)
    root = tree.getroot()

    classes = {}

    for cls in root.iter(f"{{{OWL}}}Class"):
        iri = cls.get(f"{{{RDF}}}about")
        if not iri:
            continue

        info = {
            "label": "",
            "deprecated": False,
            "parents": set(),
        }

        for child in cls:
            tag = child.tag

            if tag == f"{{{RDFS}}}label":
                info["label"] = child.text or ""

            elif tag == f"{{{OWL}}}deprecated":
                if (child.text or "").strip().lower() == "true":
                    info["deprecated"] = True

            elif tag == f"{{{RDFS}}}subClassOf":
                parent_iri = child.get(f"{{{RDF}}}resource")
                if parent_iri:
                    info["parents"].add(parent_iri)

        classes[iri] = info

    # Build children index
    for iri, info in classes.items():
        info["children"] = set()
    for iri, info in classes.items():
        for parent_iri in info["parents"]:
            if parent_iri in classes:
                classes[parent_iri]["children"].add(iri)

    print(f"  Parsed {len(classes):,} classes.", flush=True)
    return classes


def load_mondo_terms(path):
    terms = set()
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                terms.add(line)
    return terms


def namespace_of(iri):
    """Return a short namespace label for reporting."""
    if "purl.obolibrary.org/obo/DOID_" in iri:
        return "DOID"
    if "purl.obolibrary.org/obo/HP_" in iri:
        return "HP"
    if "purl.obolibrary.org/obo/MONDO_" in iri:
        return "MONDO"
    # generic: take the last path segment before the local ID
    try:
        return iri.rsplit("/", 1)[-1].split("_")[0]
    except Exception:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mappings",
        default="src/ontology/components/mondo_efo_mappings.tsv",
    )
    parser.add_argument("--owl", default="src/ontology/efo-edit.owl")
    parser.add_argument(
        "--mondo-terms",
        default="src/ontology/iri_dependencies/mondo_terms.txt",
    )
    parser.add_argument("--reports-dir", default="reports")
    args = parser.parse_args()

    os.makedirs(args.reports_dir, exist_ok=True)

    # ------------------------------------------------------------------ load
    rows = load_mappings(args.mappings)
    classes = parse_owl(args.owl)
    current_mondo = load_mondo_terms(args.mondo_terms)

    # ---------------------------------------------------------------- categorise rows
    efo_orphanet_rows = []
    other_rows = []

    for mondo_iri, term_iri, mondo_label, term_label in rows:
        if is_efo(term_iri) or is_orphanet(term_iri):
            efo_orphanet_rows.append((mondo_iri, term_iri, mondo_label, term_label))
        else:
            other_rows.append((mondo_iri, term_iri, mondo_label, term_label))

    # --------------------------------------------- analyse EFO/Orphanet terms
    to_obsolete = []
    already_deprecated = []
    not_found_in_owl = []

    for mondo_iri, term_iri, mondo_label, term_label in efo_orphanet_rows:
        info = classes.get(term_iri)
        if info is None:
            not_found_in_owl.append((mondo_iri, term_iri, mondo_label, term_label))
        elif info["deprecated"]:
            already_deprecated.append((mondo_iri, term_iri, mondo_label, term_label))
        else:
            to_obsolete.append((mondo_iri, term_iri, mondo_label, term_label))

    being_obsoleted = {term_iri for _, term_iri, _, _ in to_obsolete}

    # ---------------------------------------- children that need re-parenting
    # For every active term being obsoleted, find its children that are:
    #   (a) NOT themselves being obsoleted
    #   (b) NOT already deprecated
    # Those children need a new parent.
    #
    # A child may have multiple parents; we record each (child, old_parent) pair
    # separately so the Phase 3 script can handle them individually.
    # We also record whether the child has other non-obsoleted named parents,
    # which governs whether the Mondo IRI must be added or just the old one removed.

    reparent_rows = []

    for mondo_iri, term_iri, mondo_label, term_label in to_obsolete:
        info = classes.get(term_iri, {})
        for child_iri in sorted(info.get("children", set())):
            child_info = classes.get(child_iri, {})
            if child_iri in being_obsoleted:
                continue
            if child_info.get("deprecated", False):
                continue

            # Count how many of this child's parents are *not* being obsoleted
            # and are not deprecated
            other_active_parents = [
                p
                for p in child_info.get("parents", set())
                if p != term_iri
                and p not in being_obsoleted
                and not classes.get(p, {}).get("deprecated", False)
            ]

            reparent_rows.append(
                {
                    "child_iri": child_iri,
                    "child_label": child_info.get("label", ""),
                    "old_parent_iri": term_iri,
                    "old_parent_label": term_label,
                    "new_parent_iri": mondo_iri,
                    "new_parent_label": mondo_label,
                    "child_other_active_parents": len(other_active_parents),
                    "action": (
                        "remove_only"
                        if other_active_parents
                        else "replace_with_mondo"
                    ),
                }
            )

    # ----------------------------------------- Mondo IRIs not yet imported
    mondo_iris_needed = {m for m, _, _, _ in to_obsolete}
    missing_mondo = sorted(mondo_iris_needed - current_mondo)

    # ----------------------------------------------------------------- print summary
    n_efo = sum(1 for _, t, _, _ in to_obsolete if is_efo(t))
    n_orph = sum(1 for _, t, _, _ in to_obsolete if is_orphanet(t))

    print()
    print("=== SUMMARY ===")
    print(f"Total rows in mappings file          : {len(rows):>6,}")
    print(f"  EFO terms active  (to obsolete)    : {n_efo:>6,}")
    print(f"  Orphanet terms active (to obsolete): {n_orph:>6,}")
    print(f"  Already deprecated (skip)          : {len(already_deprecated):>6,}")
    print(f"  Not found in efo-edit.owl          : {len(not_found_in_owl):>6,}")
    print(f"  Other namespace (excluded)         : {len(other_rows):>6,}")
    print()
    print(f"Children needing re-parenting        : {len(reparent_rows):>6,}")
    print(f"  action=replace_with_mondo          : {sum(1 for r in reparent_rows if r['action'] == 'replace_with_mondo'):>6,}")
    print(f"  action=remove_only (has other parents): {sum(1 for r in reparent_rows if r['action'] == 'remove_only'):>6,}")
    print()
    print(f"Mondo IRIs not yet in mondo_terms.txt: {len(missing_mondo):>6,}")

    if not_found_in_owl:
        print()
        print(f"WARNING: {len(not_found_in_owl)} term(s) listed in mappings but NOT found in efo-edit.owl:")
        for mondo_iri, term_iri, mondo_label, term_label in not_found_in_owl:
            print(f"  {term_iri}  ({term_label})")

    # ---------------------------------------------------------------- write reports

    # 1. Obsolescence plan
    plan_path = os.path.join(args.reports_dir, "mondo_obsolescence_plan.tsv")
    with open(plan_path, "w") as fh:
        fh.write(
            "term_iri\tterm_label\tterm_type\tmondo_iri\tmondo_label"
            "\tall_children_count\tactive_children_needing_reparent\n"
        )
        for mondo_iri, term_iri, mondo_label, term_label in sorted(
            to_obsolete, key=lambda x: x[1]
        ):
            ttype = "EFO" if is_efo(term_iri) else "Orphanet"
            info = classes.get(term_iri, {})
            all_children = len(info.get("children", set()))
            reparent_count = sum(
                1
                for r in reparent_rows
                if r["old_parent_iri"] == term_iri
            )
            fh.write(
                f"{term_iri}\t{term_label}\t{ttype}\t{mondo_iri}\t{mondo_label}"
                f"\t{all_children}\t{reparent_count}\n"
            )
    print(f"Written : {plan_path}  ({len(to_obsolete):,} rows)")

    # 2. Children to re-parent
    reparent_path = os.path.join(args.reports_dir, "children_to_reparent.tsv")
    with open(reparent_path, "w") as fh:
        fh.write(
            "child_iri\tchild_label\told_parent_iri\told_parent_label"
            "\tnew_parent_iri\tnew_parent_label"
            "\tchild_other_active_parents\taction\n"
        )
        for row in sorted(reparent_rows, key=lambda x: x["child_iri"]):
            fh.write(
                f"{row['child_iri']}\t{row['child_label']}\t"
                f"{row['old_parent_iri']}\t{row['old_parent_label']}\t"
                f"{row['new_parent_iri']}\t{row['new_parent_label']}\t"
                f"{row['child_other_active_parents']}\t{row['action']}\n"
            )
    print(f"Written : {reparent_path}  ({len(reparent_rows):,} rows)")

    # 3. Mondo terms to import
    import_path = os.path.join(args.reports_dir, "mondo_terms_to_import.tsv")
    mondo_to_efo = {
        m: (t, tl) for m, t, ml, tl in efo_orphanet_rows
    }
    with open(import_path, "w") as fh:
        fh.write("mondo_iri\treplaces_iri\treplaces_label\n")
        for m_iri in missing_mondo:
            t_iri, t_label = mondo_to_efo.get(m_iri, ("", ""))
            fh.write(f"{m_iri}\t{t_iri}\t{t_label}\n")
    print(f"Written : {import_path}  ({len(missing_mondo):,} rows)")

    # 4. Other-namespace terms
    other_path = os.path.join(args.reports_dir, "other_terms_in_mappings.tsv")
    with open(other_path, "w") as fh:
        fh.write(
            "term_iri\tterm_label\tterm_namespace\tmondo_iri\tmondo_label"
            "\tin_efo_edit_owl\n"
        )
        for mondo_iri, term_iri, mondo_label, term_label in sorted(
            other_rows, key=lambda x: x[1]
        ):
            ns = namespace_of(term_iri)
            in_owl = "yes" if term_iri in classes else "no"
            fh.write(
                f"{term_iri}\t{term_label}\t{ns}\t{mondo_iri}\t{mondo_label}\t{in_owl}\n"
            )
    print(f"Written : {other_path}  ({len(other_rows):,} rows)")

    print()
    print("Phase 1 complete. Review reports before proceeding to Phase 2.")


if __name__ == "__main__":
    main()
