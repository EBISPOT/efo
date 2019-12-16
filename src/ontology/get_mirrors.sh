#!/bin/sh

mkdir -p mirror

echo "Fetching MONDO..."
curl -L https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl

echo "Fetching UBERON..."
curl -L https://www.ebi.ac.uk/ols/ontologies/uberon/download > mirror/uberon.owl

#efo-edit.owl from efo2 branch is no longer needed, edit master efo-edit.owl instead.
#curl -L https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl

#echo "Fetching OTAR therapeutic areas..."
#curl -L https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt

echo "Fetching HANCESTRO..."
curl -L https://raw.githubusercontent.com/EBISPOT/ancestro/master/src/ontology/hancestro-edit.owl > mirror/hancestro.owl