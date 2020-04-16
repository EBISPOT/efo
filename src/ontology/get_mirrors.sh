#!/bin/bash

mkdir -p mirror

echo "Fetching MONDO..."
#TEMPORARY REMOVAL OF OLS MIRROR DOWNLOAD
#curl -L https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl
#TEMPORARY DOWNLOAD OF MONDO MIRROR
curl -L https://github.com/monarch-initiative/mondo/releases/download/current/mondo.obo > mirror/mondo.obo && ../../bin/robot convert -i mirror/mondo.obo -f owl -o mirror/mondo.owl

echo "Fetching UBERON..."
curl -L http://purl.obolibrary.org/obo/uberon.owl > mirror/uberon.owl

echo "Fetching HPO..."
curl -L http://purl.obolibrary.org/obo/hp.owl > mirror/hp.owl

echo "Fetching CL..."
curl -L http://purl.obolibrary.org/obo/cl.owl > mirror/cl.owl

#efo-edit.owl from efo2 branch is no longer needed, edit master efo-edit.owl instead.
#curl -L https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl

#echo "Fetching OTAR therapeutic areas..."
#curl -L https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt

echo "Fetching HANCESTRO..."
curl -L https://raw.githubusercontent.com/EBISPOT/ancestro/master/src/ontology/hancestro-edit.owl > mirror/hancestro.owl

echo "Fetching FBbt..."
curl -L http://purl.obolibrary.org/obo/fbbt.owl > mirror/fbbt.owl

#echo "Fetching GO..."
#curl -L https://www.ebi.ac.uk/ols/ontologies/go/download > mirror/go.owl
