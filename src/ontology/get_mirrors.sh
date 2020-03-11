#!/bin/bash

mkdir -p mirror

echo "Fetching MONDO..."
#TEMPORARY REMOVAL OF OLS MIRROR DOWNLOAD
#curl -L https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl
#TEMPORARY DOWNLOAD OF MONDO MIRROR
curl -L https://github.com/monarch-initiative/mondo/releases/download/v2020-03-05/mondo.obo > mirror/mondo.obo && bin/robot convert -i mirror/mondo.obo -f owl -o mondo.owl

echo "Fetching UBERON..."
curl -L https://www.ebi.ac.uk/ols/ontologies/uberon/download > mirror/uberon.owl

echo "Fetching HPO..."
curl -L https://www.ebi.ac.uk/ols/ontologies/hp/download > mirror/hp.owl

echo "Fetching CL..."
curl -L https://www.ebi.ac.uk/ols/ontologies/cl/download > mirror/cl.owl


#efo-edit.owl from efo2 branch is no longer needed, edit master efo-edit.owl instead.
#curl -L https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl

#echo "Fetching OTAR therapeutic areas..."
#curl -L https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt

echo "Fetching HANCESTRO..."
curl -L https://raw.githubusercontent.com/EBISPOT/ancestro/master/src/ontology/hancestro-edit.owl > mirror/hancestro.owl