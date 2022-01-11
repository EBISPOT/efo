PREFIX gwas_trait: <http://www.ebi.ac.uk/efo/gwas_trait>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX xml: <https://www.w3.org/TR/xml#>

CONSTRUCT {
	?s a owl:Class .
	?s gwas_trait: "true"^^xsd:boolean .}

WHERE { 
	?s ?p ?o .
	FILTER NOT EXISTS {?s a owl:ObjectProperty} .
	FILTER NOT EXISTS {?s a owl:AnnotationProperty} 
	FILTER NOT EXISTS {?s a owl:Ontology}. }