prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix OBAN: <http://purl.org/oban/>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix RO: <http://purl.obolibrary.org/obo/RO_>

CONSTRUCT { 
  dc:source rdf:type owl:AnnotationProperty .
  ?phenotype rdf:type owl:Class .
  ?disease rdf:type owl:Class ;
    <http://www.w3.org/2004/02/skos/core#related> ?phenotype .
   [ rdf:type owl:Axiom ;
     owl:annotatedSource ?disease ;
     owl:annotatedProperty <http://www.w3.org/2004/02/skos/core#related> ;
     owl:annotatedTarget ?phenotype ;
     dc:source <http://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa>  ] .
 }

WHERE {
  ?disease rdfs:subClassOf [ rdf:type owl:Restriction ;
    owl:onProperty ?p ;
    owl:someValuesFrom ?phenotype ] .
   FILTER ( regex(str(?disease), "^http://purl.obolibrary.org/obo/MONDO_"))
   FILTER ( regex(str(?phenotype), "^http://purl.obolibrary.org/obo/HP_"))
}
