#EFO-MONDO
# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://www.ebi.ac.uk
ONT=efo
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
BUILDDIR=build
RELEASEDIR=../..
ROBOT= ../../bin/robot
EFO2OBO= ../../bin/efo2obo
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
MONDO = ../templates/mondo.obo
UPPER = ./imports/upper_class.owl
PARENTSGENERATED = ./results/efoparents.owl
GENERATED = ./results/efo-mondo-generated.owl
EFOPREFIX = "EFO: http://www.ebi.ac.uk/efo/EFO_"
ORDOPREFIX = "Orphanet: http://www.orpha.net/ORDO/Orphanet_"
MONDOPREFIX = "MONDO: http://purl.obolibrary.org/obo/MONDO_"
EFO3EDIT = efo-3-edit.owl
EFOFIXER = ../../bin/efo-fixer.jar
MIRRORDIR=./mirror
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: $(BUILDDIR)/$(ONT).owl #$(BUILDDIR)/$(ONT).obo
test: all sparql_test
prepare_release: all
	cp $(BUILDDIR)/$(ONT).owl $(BUILDDIR)/$(ONT).obo $(RELEASEDIR) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# create the main efo release by merging and removing import statements
# this will also set the release date and version number 
$(BUILDDIR)/$(ONT).owl: $(EFO3EDIT)
	$(ROBOT) merge --input $(EFO3EDIT) -c true -i $< reason -s true -m false -r hermit annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@

$(BUILDDIR)/$(ONT).obo: $(BUILDDIR)/$(ONT).owl
	$(EFO2OBO) -i $< -o $@


# make changes to efo 2 to base efo 3
$(BUILDDIR)/efo-edit-fixed.owl: efo-edit.owl
	java -jar $(EFOFIXER) efo-edit.owl $(BUILDDIR)/efo-edit-fixed.owl

# unmerge mondo

$(BUILDDIR)/efo-edit-fixed-raw.owl: $(BUILDDIR)/efo-edit-fixed.owl imports/mondo_efo_import.owl $(BUILDDIR)/OTAR_tagged.owl $(BUILDDIR)/uberon_import.owl
	$(ROBOT) merge -i $(BUILDDIR)/efo-edit-fixed.owl -i imports/mondo_efo_import.owl -i $(BUILDDIR)/uberon_import.owl -i $(BUILDDIR)/OTAR_tagged.owl unmerge -i imports/mondo_efo_import.owl -o $@

# add import statements to editors edition

$(EFO3EDIT): efo-upper.owl $(BUILDDIR)/efo-edit-fixed-raw.owl ../templates/subclasses.csv
	$(ROBOT) merge --collapse-import-closure false -i efo-upper.owl -i $(BUILDDIR)/efo-edit-fixed-raw.owl template --merge-before --template ../templates/subclasses.csv --prefix $(MONDOPREFIX) convert -f ofn -o $@


# unmerge imports from edit and add import files

imports/mondo_efo_import.owl: imports/mondo_efo_mappings.tsv imports/mondo_remove.owl
	java -jar ../../bin/mondo-id-switch.jar imports/mondo_efo_mappings.tsv imports/mondo_remove.owl imports/mondo_efo_import.owl && $(ROBOT) -v annotate -i imports/mondo_efo_import.owl --ontology-iri http://www.ebi.ac.uk/efo/imports/mondo_efo_import.owl -o $@

imports/mondo_remove.owl: imports/mondo_import.owl
	$(ROBOT) remove -i $< -T imports/mondo_duplicates.txt -o $@


#-------------------------------------------------
# uberon updates module
#-------------------------------------------------
#Download Uberon ontology from the EBI/OLS: https://www.ebi.ac.uk/ols/ontologies/uberon/download see get_mirrors.sh file
#Extract all Uberon terms from the efo.owl file

$(BUILDDIR)/uberon_terms.txt: efo-edit.owl
	$(ROBOT) query --input efo-edit.owl --select $(SPARQLDIR)/uberon_terms.sparql $@

#creates the subset owl file from uberon terms
$(BUILDDIR)/uberon_filtered.owl: $(BUILDDIR)/uberon_terms.txt
	$(ROBOT) filter -i $(MIRRORDIR)/uberon.owl --term-file $(BUILDDIR)/uberon_terms.txt --select "annotations self descendants" -o $@

$(BUILDDIR)/uberon_import.owl: $(BUILDDIR)/uberon_filtered.owl
	$(ROBOT) remove -i $< -T imports/uberon_duplicates.txt -o $@


# ----------------------------------------
# OTAR therapeutic areas
# ----------------------------------------

$(BUILDDIR)/OTAR_terms.owl: efo-edit.owl
	$(ROBOT) filter --input efo-edit.owl --term-file ./imports/OTAR_terms.txt --select annotations --output $@

$(BUILDDIR)/OTAR_tagged.owl: $(BUILDDIR)/OTAR_terms.owl
	$(ROBOT) query --input $(BUILDDIR)/OTAR_terms.owl --query $(SPARQLDIR)/OTAR_therapeutic_areas.sparql $@


# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = mondo
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_terms.txt,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

# Add '--check false' flag if your OWL is not obo-strict
imports/%_import.obo: imports/%_import.owl
	$(ROBOT) convert --check false -i $< -o $@

# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl $(ONT).obo $(ONT)_full.obo
	cp $^ $(RELEASEDIR) 

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = duplicate-label  nolabels multiple-label no-webulous-uris no-dangling

# run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	robot query -f tsv -i $< $(REPORT_ARGS)
