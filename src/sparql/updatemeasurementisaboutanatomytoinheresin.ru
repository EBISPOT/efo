PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


DELETE {
?measurement rdfs:subClassOf ?x .
?x rdf:type owl:Restriction ;
  owl:onProperty <http://purl.obolibrary.org/obo/IAO_0000136>;
  owl:someValuesFrom ?anatomy .
}
INSERT {
?measurement rdfs:subClassOf ?x .
?x rdf:type owl:Restriction ;
  owl:onProperty <http://purl.obolibrary.org/obo/RO_0002314>;
  owl:someValuesFrom ?anatomy .
}

WHERE {
?measurement rdfs:subClassOf ?x .
?x rdf:type owl:Restriction ;
  owl:onProperty <http://purl.obolibrary.org/obo/IAO_0000136>;
  owl:someValuesFrom ?anatomy .
?measurement rdfs:subClassOf* <http://www.ebi.ac.uk/efo/EFO_0001444> .
?anatomy rdfs:subClassOf* <http://purl.obolibrary.org/obo/UBERON_0001062> .
?measurement rdfs:label ?measurementlabel .
?anatomy rdfs:label ?anatomylabel .
FILTER(isIRI(?anatomy) && isIRI(?measurement))
}