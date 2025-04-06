PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

INSERT DATA {
  obo:CHEBI_36080 a owl:Class .
};

DELETE {
  ?s ?p obo:PR_000000001 .
}
INSERT {
  ?s ?p obo:CHEBI_36080 .
}
WHERE {
  ?s ?p obo:PR_000000001 .
};


