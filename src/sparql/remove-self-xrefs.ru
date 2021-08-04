prefix owl: <http://www.w3.org/2002/07/owl#>
prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

#SELECT ?term_curie ?xref_curie
DELETE {
  ?term oboInOwl:hasDbXref ?xref .
}
WHERE 
{ 
    ?term oboInOwl:hasDbXref ?xref .
  	FILTER (isIRI(?term))
	BIND(
		IF(	
			regex(str(?xref), "http[:][/][/]www[.]ebi[.]ac[.]uk[/]efo[/]EFO[_]")
				|| regex(str(?xref), "http[:][/][/]purl[.]obolibrary[.]org[/]obo[/]")
				|| regex(str(?xref), "http[:][/][/]www[.]orpha.net[/]ORDO[/]"),
			REPLACE(
				REPLACE(STR(?xref), "http[:][/][/]purl[.]obolibrary[.]org[/]obo[/]|http[:][/][/]www[.]ebi[.]ac[.]uk[/]efo[/]|http[:][/][/]www[.]orpha.net[/]ORDO[/]", "", "i"),
			"[_]", ":", "i")
      ,str(?xref)) as ?xref_curie)
    BIND(
		IF(	
			regex(str(?term), "http[:][/][/]www[.]ebi[.]ac[.]uk[/]efo[/]EFO[_]")
				|| regex(str(?term), "http[:][/][/]purl[.]obolibrary[.]org[/]obo[/]")
				|| regex(str(?term), "http[:][/][/]www[.]orpha.net[/]ORDO[/]"),
			REPLACE(
				REPLACE(STR(?term), "http[:][/][/]purl[.]obolibrary[.]org[/]obo[/]|http[:][/][/]www[.]ebi[.]ac[.]uk[/]efo[/]|http[:][/][/]www[.]orpha.net[/]ORDO[/]", "", "i"),
			"[_]", ":", "i")
      , str(?term))  as ?term_curie)
  FILTER(str(?term_curie)=str(?xref_curie))
}
