PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX replaced_by: <http://purl.obolibrary.org/obo/IAO_0100001>
prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX EFO: <http://www.ebi.ac.uk/efo/EFO_>

CONSTRUCT {
	?cls a owl:Class .
  	?cls rdfs:label ?label .
}
WHERE {
	?cls a owl:Class .
	?cls rdfs:label ?label .
	?cls rdfs:subClassOf+ EFO:0000616 .
	FILTER NOT EXISTS {?cls owl:deprecated ?dep}
	FILTER (!isBlank(?cls))
}
