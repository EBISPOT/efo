#!/bin/sh

mkdir -p mirror

curl https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl

curl https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/efo-edit.owl > efo-edit.owl