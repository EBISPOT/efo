import json
import urllib2
import sys

# download all source ontologies 

def download_source_ontologies(file):

    print ("reading file " + file)
    json_data = open(file).read()
    data = json.loads(json_data)

    for ontology in data:
        print ("downloading latest version of "+ ontology['shortName'] + "...")
        try:
            ontology_file = urllib2.urlopen(ontology["ontologyUrl"])
            with open("mirror/"+ontology["shortName"]+".owl", "wb") as output:
                output.write(ontology_file.read())
        except:
            print ("couldn't download " + ontology["shortName"])

if __name__ == "__main__":
    download_source_ontologies(sys.argv[-1])