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
EFOPREPRO = $(BUILDDIR)/efo-edit-release.owl
EFOFIXER = ../../bin/efo-fixer.jar
MIRRORDIR=./mirror
HANCESTROGENERATED= ./build/efo-hancestro
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: all_imports $(BUILDDIR)/$(ONT).owl sparql_test #$(BUILDDIR)/$(ONT).obo
test: all sparql_test
prepare_release: all
	cp $(BUILDDIR)/$(ONT).owl $(BUILDDIR)/$(ONT).obo $(RELEASEDIR) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# create the main efo release by merging and removing import statements
# this will also set the release date and version number


# make changes to efo 2 to base efo 3
#$(BUILDDIR)/efo-edit-fixed.owl: efo-edit.owl

REMOVEONT=mondo hancestro
REMOVEONT_FILES=$(patsubst %, mirror/%.owl, $(REMOVEONT))
COMPONENTS=subclasses
COMPONENT_FILES=$(patsubst %, components/%.owl, $(COMPONENTS))

# --include-annotations true
$(EFOPREPRO): $(SRC) $(REMOVEONT_FILES) components/efo_uberon.owl
	$(ROBOT) merge -i $< $(addprefix unmerge -i , $(REMOVEONT_FILES)) \
	unmerge -i components/efo_uberon.owl -o $@-fixed.owl &&\
	java -jar $(EFOFIXER) $@-fixed.owl $(BUILDDIR)/efo-edit-fixed.owl &&\
	$(ROBOT) merge -i $(BUILDDIR)/efo-edit-fixed.owl -i imports/uberon_import.owl -i imports/hancestro_import.owl -o $@
	#convert -f ofn

components/subclasses.owl: ../templates/subclasses.csv
	$(ROBOT) template --template $< --prefix $(MONDOPREFIX) --prefix "snap: http://www.ifomis.org/bfo/1.1/snap#" --ontology-iri "http://www.ebi.ac.uk/efo/components/subclasses.owl" -o $@

t: $(EFOPREPRO)

components: $(COMPONENT_FILES)


# unmerge imports from edit and add import files

imports/mondo_remove.owl: imports/mondo_import.owl
	$(ROBOT) remove -i imports/mondo_import.owl -T imports/mondo_duplicates.txt -o $@

imports/mondo_efo_import.owl: imports/mondo_efo_mappings.tsv imports/mondo_remove.owl
	java -jar ../../bin/mondo-id-switch.jar imports/mondo_efo_mappings.tsv imports/mondo_remove.owl imports/mondo_efo_import.owl &&\
	$(ROBOT) -v annotate -i imports/mondo_efo_import.owl --ontology-iri http://www.ebi.ac.uk/efo/imports/mondo_efo_import.owl -o $@

#consider using relax instead of -s true
$(BUILDDIR)/$(ONT).owl: $(EFOPREPRO)
	$(ROBOT) reason -i $< -s true -m false -r hermit \
	annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/`cat version.txt`/$(ONT).owl -o $@

$(BUILDDIR)/$(ONT).obo: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/`cat version.txt`/efo.owl \
	query --update ../sparql/inject-subset-declaration.sparql \
	convert --check false -f obo -o $@

#-------------------------------------------------
# uberon updates module
#-------------------------------------------------
#Download Uberon ontology from the EBI/OLS: https://www.ebi.ac.uk/ols/ontologies/uberon/download see get_mirrors.sh file

#Extract all Uberon terms from the efo.owl file
imports/uberon_terms.txt: uberon_terms.txt efo-relations.txt
	cat $^ > $@

imports/uberon_import.owl: mirror/uberon.owl imports/uberon_terms.txt
	$(ROBOT) extract -i $< -T imports/uberon_terms.txt --method BOT -O $(BASE)/$@ \
	filter --term-file imports/uberon_terms.txt --select "annotations ontology anonymous self" --trim true --signature true -o $@
.PRECIOUS: imports/uberon_import.owl

# unmerge imports causing duplicates from add import files
#$(BUILDDIR)/uberon_import.owl: $(MIRRORDIR)/uberon.owl imports/uberon_terms.txt
	#$(ROBOT) extract -i $< -T imports/uberon_terms.txt --method BOT -O $(BASE)/$@ \
	#filter -i $(MIRRORDIR)/uberon.owl -T $(BUILDDIR)/uberon_terms.txt --select "annotations self descendants" \
	#remove -T imports/uberon_duplicates.txt -o $@

components/efo_terms.txt: $(SRC)
	$(ROBOT) query --input $< --select $(SPARQLDIR)/efo_terms.sparql $@

#components/efo_uberon.owl: $(SRC) imports/uberon_terms.txt components/efo_terms.txt
#	$(ROBOT) filter -i $< --term-file imports/uberon_terms.txt --trim false \
#	remove -T components/efo_terms.txt -o $@

efo_no_uberon.owl: $(SRC) components/efo_uberon.owl
	$(ROBOT) merge -i $< --collapse-import-closure false unmerge -i components/efo_uberon.owl -o $@

efo-diff.txt: $(SRC) efo_no_uberon.owl
	$(ROBOT) diff --left $< --right efo_no_uberon.owl -o $@

# ----------------------------------------
# OTAR therapeutic areas
# ----------------------------------------

$(BUILDDIR)/OTAR_terms.owl: efo-edit.owl
	$(ROBOT) filter --input efo-edit.owl --term-file ./imports/OTAR_terms.txt --select annotations --output $@

$(BUILDDIR)/OTAR_tagged.owl: $(BUILDDIR)/OTAR_terms.owl
	$(ROBOT) query --input $(BUILDDIR)/OTAR_terms.owl --query $(SPARQLDIR)/OTAR_therapeutic_areas.sparql $@

# ----------------------------------------
# HANCESTRO import
# ----------------------------------------

#$(HANCESTROGENERATED).owl: $(BUILDDIR)/efo-edit-fixed.owl
#	$(ROBOT) -v merge -i $< -i imports/hancestro_import.owl -o $(BUILDDIR)/efo-edit-fixed.owl

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = mondo hancestro uberon
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
VCHECKS = duplicate-label  nolabels multiple-label no-webulous-uris no-dangling id-length

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
