PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# PO:0025127 is a BOT-required intermediate. Qualify its generic source label
# in the EFO import module to avoid collision with UBERON:0001048, while
# retaining the authoritative PO label as an exact synonym.
DELETE {
  <http://purl.obolibrary.org/obo/PO_0025127> rdfs:label "primordium" .
}
INSERT {
  <http://purl.obolibrary.org/obo/PO_0025127> rdfs:label "plant primordium" ;
    oboInOwl:hasExactSynonym "primordium" .
}
WHERE {
  <http://purl.obolibrary.org/obo/PO_0025127> rdfs:label "primordium" .
}
