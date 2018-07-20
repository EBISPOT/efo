import re

with open('../ontology/efo-edit.owl', 'rb') as f:   
    label = f.read()
    prefbeg = re.sub('<rdfs:label.*?>', '<skos:prefLabel>', label)
    prefend = re.sub('</rdfs:label>', '</skos:prefLabel>', prefbeg)

    with open ('../ontology/results/efo-edit-skos.owl', 'wb') as file:
        file.write(prefend)


