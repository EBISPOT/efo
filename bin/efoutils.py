


import json
import urllib2

# download all source ontologies 

def download_source_ontologies():

    json_data = open("ontology-config.json").read()
    data = json.loads(json_data)

    for ontology in data:
        print "downloading latest version of "+ ontology["shortName"] + "..."
        try:
            ontology_file = urllib2.urlopen(ontology["ontologyUrl"])
            with open("build/full_imports/"+ontology["shortName"]+".owl", "wb") as output:
                output.write(ontology_file.read())
        except:
            print "couldn't download " + ontology["shortName"]




    # reply = requests.get(self.url, headers=self.headers)
    # self.ingest_api = reply.json()["_links"]


if __name__ == "__main__":
    download_source_ontologies()