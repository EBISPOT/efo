prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix owl: <http://www.w3.org/2002/07/owl#>

DELETE { 
  ?stray a owl:Class
 }

WHERE {
  ?stray a owl:Class .
  FILTER NOT EXISTS {
    ?stray ?p ?x .
    FILTER(?p!=rdf:type)
  }
}
