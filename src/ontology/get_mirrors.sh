#!/bin/bash

mkdir -p mirror

#echo "Fetching MONDO..."
#curl -L http://purl.obolibrary.org/obo/mondo-base.owl > mirror/mondo.owl

echo "Fetching UBERON..."
curl -L http://purl.obolibrary.org/obo/uberon.owl > mirror/uberon.owl

echo "Fetching HPO..."
curl -L http://purl.obolibrary.org/obo/hp.owl > mirror/hp.owl

echo "Fetching MONDO (OWL Version)..."
curl -L http://purl.obolibrary.org/obo/mondo.owl > mirror/mondo-owl.owl

echo "Fetching CHEBI..."
curl -L http://purl.obolibrary.org/obo/chebi.owl > mirror/chebi.owl

echo "Fetching CL..."
curl -L http://purl.obolibrary.org/obo/cl.owl > mirror/cl.owl

echo "Fetching HPOA from Monarch..."
curl -L https://data.monarchinitiative.org/ttl/hpoa.ttl > mirror/hpoa.owl


#efo-edit.owl from efo2 branch is no longer needed, edit master efo-edit.owl instead.
#curl -L https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl

#echo "Fetching OTAR therapeutic areas..."
#curl -L https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt

echo "Fetching HANCESTRO..."
curl -L https://raw.githubusercontent.com/EBISPOT/hancestro/main/hancestro.owl > mirror/hancestro.owl

echo "Fetching FBbt..."
curl -L http://purl.obolibrary.org/obo/fbbt.owl > mirror/fbbt.owl

echo "Fetching OBI..."
curl -L http://purl.obolibrary.org/obo/obi.owl > mirror/obi.owl

echo "Fetching OBA..."
curl -L http://purl.obolibrary.org/obo/oba.owl > mirror/oba.owl

echo "Fetching GO..."
curl -L http://purl.obolibrary.org/obo/go.owl > mirror/go.owl

echo "Fetching GWAS trait list and creating template..."
curl -L https://www.ebi.ac.uk/gwas/api/search/downloads/trait_mappings > ./iri_dependencies/gwas.tsv && cut -d$'\t' -f 3 ./iri_dependencies/gwas.tsv > ./iri_dependencies/gwas_traits.tsv && rm ./iri_dependencies/gwas.tsv && sed -i '' 1d ./iri_dependencies/gwas_traits.tsv && cat ./iri_dependencies/gwas_header.tsv ./iri_dependencies/gwas_traits.tsv > ./iri_dependencies/gwas_terms.tsv