#!/bin/sh

mkdir -p mirror

curl https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl

curl https://www.ebi.ac.uk/ols/ontologies/uberon/download > mirror/uberon.owl

curl https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/efo-edit.owl > efo-edit.owl

curl https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt
