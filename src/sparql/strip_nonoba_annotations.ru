PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

# Remove annotations (label, definition, synonyms, comment) from every non-OBA
# subject in the OBA import. The imported OBA terms carry relations to fillers in
# other ontologies (UBERON, PR, GO, CHEBI...); those fillers are labelled by their
# OWN ontology import, so leaving a copy of their label here produces duplicate
# labels after all imports merge into efo.owl. Stripping them leaves fillers as
# bare stubs whose single label comes from the owning import.
DELETE { ?s ?p ?o }
WHERE {
  ?s ?p ?o .
  FILTER( isIRI(?s) && !STRSTARTS(STR(?s), "http://purl.obolibrary.org/obo/OBA_") )
  FILTER( ?p = rdfs:label
       || ?p = <http://purl.obolibrary.org/obo/IAO_0000115>
       || ?p = oboInOwl:hasExactSynonym  || ?p = oboInOwl:hasRelatedSynonym
       || ?p = oboInOwl:hasNarrowSynonym || ?p = oboInOwl:hasBroadSynonym
       || ?p = rdfs:comment )
}
