#[![Build Status](https://travis-ci.org/EBISPOT/efo.svg?branch=master)](https://travis-ci.org/EBISPOT/efo)
#[![DOI](https://zenodo.org/badge/13996/EBISPOT/efo.svg)](https://zenodo.org/badge/latestdoi/13996/EBISPOT/efo)


We are transitioning EFO development to GitHub. This is our development area for our monthly release. Please get the latest version of EFO by visiting http://wwww.ebi.ac.uk/efo.

# EFO

![alt text](efo.gif?raw=true)

The Experimental Factor Ontology (EFO) provides a systematic description of many experimental variables available in EBI databases, and for external projects such as the NHGRI GWAS catalog. 
It combines parts of several biological ontologies, such as UBERON anatomy, ChEBI chemical compounds, and Cell Ontology. The scope of EFO is to support the annotation, analysis and visualization of data handled by many groups at the EBI and as the core ontology for [Open Targets](http://www.opentargets.org/). 
EFO is developed by the EMBL-EBI [Samples, Phenotypes and Ontologies Team](http://www.ebi.ac.uk/about/spot-team) (SPOT). We also add terms for external users when requested. If you are new to ontologies, there is a [short introduction](http://ontogenesis.knowledgeblog.org/66) on the subject available and a blog post by James Malone on [what ontologies are for](http://drjamesmalone.blogspot.co.uk/2012/06/common-ontology-questions-1-what-is-it.html).

## Browse EFO

EFO is best viewed in the [EMBL-EBI Ontology Lookup Service](http://www.ebi.ac.uk/ols/ontologies/efo)

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

http://www.ebi.ac.uk/efo/efo.owl

This is the asserted ontology and requires an OWL-DL reasoner to view the inferred classification. 

### Other release versions 

The latest inferred version that provides a non-redundant view of the class hierarchy can be found at:

http://www.ebi.ac.uk/efo/efo_inferred.owl

A merged view of the release including inferred axioms can be found at:

http://www.ebi.ac.uk/efo/efo_inferred_all.owl

A simple OBO version of the file can be found at:

http://www.ebi.ac.uk/efo/efo.obo

### Editors' version

Editors of this ontology should use the edit version, [src/ontology/efo-edit.owl](src/ontology/efo-edit.owl)

## Term requests and contact

Submit new terms or report bugs using our [issue tracker](https://github.com/EBISPOT/efo/issues), or join [EFO mailing list](https://sourceforge.net/projects/efo/lists/efo-users) for announcement and monthly update.

## Acknowledgements

This ontology repository was created using the [ontology starter kit](https://github.com/INCATools/ontology-starter-kit)
