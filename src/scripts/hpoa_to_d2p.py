#!/usr/bin/env python3
"""
Convert the HPO annotation file (phenotype.hpoa) into the disease-to-phenotype
component Turtle consumed by the disease_to_phenotype_merged.owl build.

Each annotation row becomes `disease skos:related phenotype`, with a reified
owl:Axiom carrying `dc:source <http://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa>`
— the same shape the MONDO-derived half of the component uses. Disease IRIs:
ORPHA ids map to ORDO IRIs (the form EFO's disease branch contains, so they
survive the legal-diseases filter downstream); OMIM and DECIPHER ids map to
their canonical entry URLs (filtered out downstream, kept here for
completeness). Rows with the NOT qualifier assert the absence of a phenotype
and are skipped. All aspects are kept, including inheritance and clinical
course.

Usage:
    python3 hpoa_to_d2p.py <phenotype.hpoa> -o <output.ttl>

Output is deterministic: one row per distinct (disease, phenotype) pair,
sorted.
"""

import argparse
import csv
import sys

HPOA_SOURCE = "http://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa"

PREFIXES = """\
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .

dc:source rdf:type owl:AnnotationProperty .
"""


def disease_iri(database_id):
    """Map a phenotype.hpoa database_id to a disease IRI, or None if the
    prefix is unknown."""
    prefix, _, local = database_id.partition(":")
    local = local.strip()
    if not local:
        return None
    if prefix == "ORPHA":
        return f"http://www.orpha.net/ORDO/Orphanet_{local}"
    if prefix == "OMIM":
        return f"https://omim.org/entry/{local}"
    if prefix == "DECIPHER":
        return f"https://www.deciphergenomics.org/syndrome/{local}"
    return None


def phenotype_iri(hpo_id):
    prefix, _, local = hpo_id.partition(":")
    if prefix != "HP" or not local.strip():
        return None
    return f"http://purl.obolibrary.org/obo/HP_{local.strip()}"


def read_pairs(path):
    """Distinct (disease IRI, phenotype IRI) pairs from a phenotype.hpoa file."""
    pairs = set()
    skipped_unknown = 0
    with open(path, newline="", encoding="utf-8") as f:
        rows = csv.reader(
            (line for line in f if not line.startswith("#")), delimiter="\t"
        )
        header = next(rows, None)
        if header is None or "database_id" not in header or "hpo_id" not in header:
            sys.exit(
                f"error: {path} does not look like a phenotype.hpoa file "
                "(no database_id/hpo_id header row)"
            )
        col = {name: i for i, name in enumerate(header)}
        qualifier_col = col.get("qualifier")
        for row in rows:
            if len(row) <= max(col["database_id"], col["hpo_id"]):
                continue
            if qualifier_col is not None and len(row) > qualifier_col:
                if row[qualifier_col].strip() == "NOT":
                    continue
            disease = disease_iri(row[col["database_id"]].strip())
            phenotype = phenotype_iri(row[col["hpo_id"]].strip())
            if disease is None or phenotype is None:
                skipped_unknown += 1
                continue
            pairs.add((disease, phenotype))
    return pairs, skipped_unknown


def write_ttl(pairs, out):
    out.write(PREFIXES)
    for disease, phenotype in sorted(pairs):
        out.write(
            f"\n<{disease}> rdf:type owl:Class ;\n"
            f"    skos:related <{phenotype}> .\n"
            f"<{phenotype}> rdf:type owl:Class .\n"
            f"[ rdf:type owl:Axiom ;\n"
            f"  owl:annotatedSource <{disease}> ;\n"
            f"  owl:annotatedProperty skos:related ;\n"
            f"  owl:annotatedTarget <{phenotype}> ;\n"
            f"  dc:source <{HPOA_SOURCE}> ] .\n"
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("hpoa", help="path to phenotype.hpoa")
    ap.add_argument("-o", "--output", required=True, help="output Turtle file")
    args = ap.parse_args()

    pairs, skipped_unknown = read_pairs(args.hpoa)
    if not pairs:
        sys.exit(f"error: no disease-phenotype pairs read from {args.hpoa}")
    with open(args.output, "w", encoding="utf-8") as out:
        write_ttl(pairs, out)
    print(
        f"hpoa_to_d2p: {len(pairs)} distinct disease-phenotype pairs "
        f"({skipped_unknown} rows with unrecognised ids skipped)"
    )


if __name__ == "__main__":
    main()
