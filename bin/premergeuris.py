import csv

with open('../templates/efotomondo.tsv', 'rb') as f, \
     open('../ontology/results/extracted-efo.owl', 'rb') as o:
    reader = csv.reader(f, delimiter='\t')
    ontology = o.read()
    mondo_uri = []
    efo_uri = []
    mondo_label = []
    efo_label = []
    for row in reader:
        mondo_uri.append(row[0])
        efo_uri.append(row[1])
        mondo_label.append(row[2])
        efo_label.append(row[3])

uris = dict(zip(mondo_uri,efo_uri))
labels = dict(zip(mondo_label,efo_label))

#replaces MONDO URIs with EFO URIs
def replace(f, dic):
    for i, j in dic.iteritems():
        f = f.replace(i,j)
        with open('../ontology/results/extracteduris.owl', 'wb') as file:
            file.write(f)

replace(ontology, uris)
 
#with open('../ontology/results/extracteduris.owl', 'rb') as ru:
#    replaced = ru.read()
    
######## BELOW no longer used ########
#Did replace the labels/merge any labels that were the same
#will be using a manual change and Simon's script for this
#want to have distinction between MONDO label and EFO label.
def labels(x):
    combined = x.replace('<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">',\
                            '<rdfs:label xml:lang="en">')
    complete = combined.replace('<rdfs:label>',\
                                '<rdfs:label xml:lang="en">')
    with open ('../ontology/results/complete.owl', 'wb') as c:
        c.write(complete)
