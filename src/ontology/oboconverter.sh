export ROBOT_JAVA_ARGS=-Xmx8G

../../bin/robot annotate -i ./build/efo.owl --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/`cat version.txt`/efo.owl \
query --update ../sparql/inject-subset-declaration.sparql \
convert --check false -f obo -o ./build/efo.obo

#curl -L https://github.com/EBISPOT/efo/releases/download/current/efo.obo > ./build/oldefo.obo

#PREVIOUSOBORELEASE=./build/oldefo.obo

#../../bin/robot diff --left $PREVIOUSOBORELEASE --right ./build/efo.obo -o ./build/obodiff.txt