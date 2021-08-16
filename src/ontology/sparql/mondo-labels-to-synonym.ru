PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX replaced_by: <http://purl.obolibrary.org/obo/IAO_0100001>
prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX EFO: <http://www.ebi.ac.uk/efo/EFO_>

DELETE {
	?cls rdfs:label ?label .
	?cls oboInOwl:id ?oid .
}

INSERT {
	?cls a owl:Class .
  	?cls oboInOwl:hasExactSynonym ?label .
		?cls oboInOwl:hasDbXref ?curie .
  [] a owl:Axiom ;
   owl:annotatedSource ?cls ;
   owl:annotatedProperty oboInOwl:hasExactSynonym ;
   owl:annotatedTarget ?label ;
   rdfs:comment "Mondo preferred label 15.08.2021." ;
	 oboInOwl:hasDbXref ?curie .
 	
}

WHERE {
	?cls a owl:Class .
	?cls rdfs:label ?label .
	OPTIONAL {
		?cls oboInOwl:id ?oid .
	}
	FILTER NOT EXISTS {?cls owl:deprecated ?dep}
	FILTER (isIRI(?cls) && regex(str(?cls), "^http://purl.obolibrary.org/obo/MONDO_"))
	FILTER (!isBlank(?cls))
	BIND(REPLACE(?cls, "http://purl.obolibrary.org/obo/MONDO_", "MONDO:", "i") AS ?curie)
}
