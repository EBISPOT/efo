
# Pipeline review

1. Get MIRRORS
	1. mkdir -p mirror
	1. curl https://www.ebi.ac.uk/ols/ontologies/mondo/download > mirror/mondo.owl
	1. curl https://www.ebi.ac.uk/ols/ontologies/uberon/download > mirror/uberon.owl # http://purl.obolibrary.org/obo/uberon.owl 
	1. curl https://raw.githubusercontent.com/EBISPOT/efo/efo2/src/ontology/efo-edit.owl > efo-edit.owl
		1. Why?
	1. curl https://raw.githubusercontent.com/opentargets/platform-therapeutic-areas/master/tas.tsv | awk '{print $1}' > imports/OTAR_terms.txt
	1. # Using real download link?
	1. Removed mirror goals in Makefile? -> Should be reworked in there 
1. Change version number: - Edit the version.txt one increment	e.g. 3.0.0 -> 3.1.0
1. Makefile
	1. Imports extraction: Only Mondo is extracted as a regular import!
	1. catalog file is a mess! Clean up!
	1. mondo_import created, efo_mondo_import used
	1. Creating efo.owl: Merge/reason/annotate efo3-edit:
		1. efo-upper (contains imports reference to mondo_efo_import.owl)
		1. efo-edit-fixed-raw.owl
			1. efo-edit-fixed.owl (efo-edit manipulated by efo-fixer.jar; should be made more transparent)
			1. OTAR_tagged.owl
				1. imports/OTAR_terms.txt (downloaded from OTAR)
				1. build/OTAR_terms.owl (annotations in EFO edit or OTAR terms)
				1. build/OTAR_tagged.owl (build/OTAR_terms.owl -> queried OTAR therapeutic areas)
			1. uberon import
				1. $(BUILDDIR)/uberon_terms.txt: obtained UBERON seed from efo-edit-fixed.owl (why fixed; seems this could be done in the standard way, as we are only interested in signature)
				1. $(BUILDDIR)/efo-minus-uberon.owl: Create a version of the fixed efo-edit file without the UBERON annotations. *This step is redundant, as the full, not stripped down, version of efo-fixed is later merged into the final efo.owl.*
				1. $(BUILDDIR)/uberon_filtered.owl: Using filter, all UBERON terms, their annotations and subclasses are extracted from the UBERON mirror. *There should be a reasoning step here to avoid missing inferred subsumptions.*
				1. $(BUILDDIR)/uberon_remove.owl: This step removes a bunch of classes from UBERON, apparantly motivated by technical problems when it was designed. *This step is hugely non-transparent and needs to be ommitted, or justified.*
				1. $(BUILDDIR)/uberon_import.owl: The final module is a merged down version of uberon_remove and this efo-minus-uberon file. *IMHO, this should be simply uberon_filtered.owl as is.*
			1. MONDO module (imports/mondo_efo_import.owl):
				1. Creating imports/mondo_import.owl in the usual ODK style way
				1. Removing a bunch of duplicates from the ODK imports file (imports/mondo_duplicates.txt). *This step is not transparent and must be documented better!*
				1. The final module is compiled by applying the MONDO id switch jar (*Document!*) and then robot annotating the module.
		1. subclasses.tsv (Currently only MONDO:disease susceptibility sub quality, and quality is dangerously ambiguous)
	1. A bunch of manual steps that should be automated (reasons well, diff within reason, etc.)

# Dependend jar files 
mondo-id-switch.jar
efo-fixer.jar
