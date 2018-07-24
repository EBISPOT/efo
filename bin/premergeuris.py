import csv

with open('../templates/efotomondo.tsv', 'rb') as f, \
     open('../ontology/results/extracted-efo.owl', 'rb') as o:
    reader = csv.reader(f, delimiter='\t')
    ontology = o.read()
    mondo_uri = [] #empty list for mondo ids
    efo_uri = [] #empty list of efo ids

    #appends the corresponding columns to the lists from the tsv file
    #mondo is in column 0, efo in column 1
    for row in reader:
        mondo_uri.append(row[0])
        efo_uri.append(row[1])

#the uri lists are then placed in a dictionary to correspond with each other
# eg. MONDO_x: EFO_y

uris = dict(zip(mondo_uri,efo_uri))

#replaces MONDO URIs with EFO URIs using the dictionary keys
def replace(f, dic):
    for i, j in dic.iteritems():
        f = f.replace(i,j)
        with open('../ontology/results/extracteduris.owl', 'wb') as file:
            file.write(f)

replace(ontology, uris)
 
