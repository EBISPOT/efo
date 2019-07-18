#!/bin/sh

mkdir -p mirror

curl https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl

curl https://www.ebi.ac.uk/ols/ontologies/uberon/download > mirror/uberon.owl

#efo-edit.owl from efo2 branch is no longer needed, edit master efo-edit.owl instead.
#curl https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl

curl https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt
