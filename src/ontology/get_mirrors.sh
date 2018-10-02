#!/bin/sh

mkdir -p mirror

#curl https://www.ebi.ac.uk/ols/ontologies/hancestro/download > mirror/hancestro.owl

curl https://raw.githubusercontent.com/EBISPOT/ancestro/master/src/ontology/hancestro-edit.owl > mirror/hancestro.owl
