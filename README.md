[![Build Status](https://github.com/EBISPOT/efo/actions/workflows/qc.yml/badge.svg)](https://github.com/EBISPOT/efo/actions/workflows/qc.yml)

# EFO

![alt text](efo.gif?raw=true)

The Experimental Factor Ontology (EFO) provides a systematic description of many experimental variables available in EBI databases, and for projects such as the [NHGRI-EBI GWAS catalog](https://www.ebi.ac.uk/gwas/). It combines parts of several biological ontologies, such as [UBERON anatomy](http://uberon.github.io/), [ChEBI chemical compounds](https://www.ebi.ac.uk/chebi/), [Cell Ontology](https://github.com/obophenotype/cell-ontology) and, most recently, the [Monarch Disease Ontology (MONDO)](http://obofoundry.org/ontology/mondo.html). The scope of EFO is to support the annotation, analysis and visualization of data handled by many groups at the EBI and as the core ontology for [Open Targets](http://www.opentargets.org/). EFO is developed by the [EMBL-EBI Samples, Phenotypes and Ontologies Team](http://www.ebi.ac.uk/about/spot-team) (SPOT). We also add terms for external users when requested. If you are new to ontologies, there is a [short introduction](http://ontogenesis.knowledgeblog.org/66) on the subject available and a blog post by James Malone on [what ontologies are for](http://drjamesmalone.blogspot.co.uk/2012/06/common-ontology-questions-1-what-is-it.html). 


## Browse EFO

You can explore EFO 3 in the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols/ontologies/efo)

## Versions

### Changes to EFO in version 3

The disease branch of EFO has undergone major restructuring in order to improve classification based on current medical understanding and in alignment with existing domain ontologies. This has been achieved through mapping the EFO disease and disease staging branches to the [Monarch Disease Ontology](http://www.obofoundry.org/ontology/mondo.html) (MONDO) - using the [Ontology X-ref Service](https://www.ebi.ac.uk/spot/oxo/) (OxO) - and importing these mapped MONDO terms into EFO. All existing EFO terms have retained the EFO ID. The MONDO ID for each mapped term is available within the annotations as a cross reference. Any new terms imported from MONDO have retained their MONDO IDs. 

All mapped terms (EFO terms and their MONDO mapped term) can be found in the `mondo_efo_mappings.tsv` file situated in the imports folder. This file contains on each line: the URI of the MONDO term, the URI of the EFO term, the MONDO label and the EFO label for each mapped pair. All terms that are mapped must be added to this file in order for the MONDO term to be extracted and merged into EFO. Additionally, all MONDO terms to be extracted that are listed in the mappings file are contained in the `mondo_terms.txt` file.

Consequently, this will now allow us to import MONDO terms and receive requests to import terms that exist in MONDO. This will be done through adding these terms to the mondo_terms.txt file, which, in turn, extracts all terms listed in this file from MONDO in an import file which is then merged with EFO.

Any terms that are imported and are not under the desired parent class can be manipulated through the subclass.csv file. This automatically corrects the term classification during the editing pipeline to the desired classification.

Changes in annotation properties are:

- [Alternative_term](http://www.ebi.ac.uk/efo/alternative_term) has been replaced by [has_exact_synonym](http://www.geneontology.org/formats/oboInOwl#hasExactSynonym) 
     - This will allow us to use the spectrum of synonym annotation including [has_broad_synonym](http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym) and [has_narrow_synonym](http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym) more effectively to provide further information per each term.
- [Bioportal_provenance](http://www.ebi.ac.uk/efo/bioportal_provenance) has been removed from EFO3 entirely. 
     - This has cleaned up annotations, removing the imported fingerprints from bioportal provenance from previous importing.
- All definition citations have been replaced by [database_cross_reference](http://www.geneontology.org/formats/oboInOwl#hasDbXref).
- Deprecated terms are no longer children of obsolete class (http://www.geneontology.org/formats/oboInOwl#ObsoleteClass), instead, they are given the annotation property owl:Deprecated (http://www.w3.org/2002/07/owl#deprecated). 

### Stable release versions

The latest version of the ontology can always be found attached to each EFO 3 release, found here:

[https://github.com/EBISPOT/efo/releases](https://github.com/EBISPOT/efo/releases)

This is the asserted ontology and requires an OWL-DL reasoner to view the inferred classification. 


### Editors' version

Editors of this ontology should use the edit version, [efo2 src/ontology/efo-edit.owl](https://github.com/EBISPOT/efo/blob/efo2/src/ontology/efo-edit.owl)

## Term requests and contact

Submit new terms or report bugs using our [issue tracker](https://github.com/EBISPOT/efo/issues), or join [EFO mailing list](https://listserver.ebi.ac.uk/mailman/listinfo/efo-users) for announcement and monthly update.

## Acknowledgements

This ontology repository was created using the [ontology starter kit](https://github.com/INCATools/ontology-starter-kit) 
