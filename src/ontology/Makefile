# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://www.ebi.ac.uk
OBOREAL=http://purl.obolibrary.org/obo
ONT=efo
ONT_INF=efo_inferred
ONT_INF_ALL=efo_inferred_all
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
RELEASEDIR=../..
ROBOT= ../../bin/robot
EFO2OBO= ../../bin/efo2obo
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
HANCESTROGENERATED= ./results/efo-hancestro

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: all_imports $(HANCESTROGENERATED).owl $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl sparql_test #$(ONT).obo $(ONT)_full.obo
test: all sparql_test
prepare_release: all
	cp $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl $(ONT).obo $(ONT)_full.obo $(RELEASEDIR) &&\
	(test -f subsets/*owl && cp subsets/*{owl,obo} $(RELEASEDIR)/subsets && git add $(RELEASEDIR)/subsets/* || echo "no subsets") &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# create the main efo release by merging and removing imrpot statments
# this will also set the release date and version number
 
$(HANCESTROGENERATED).owl: $(SRC)
	$(ROBOT) -v merge -i $< -i imports/hancestro_import.owl -o $(SRC)

$(ONT).owl: $(SRC)
	$(ROBOT) -v merge -c true -i  $< annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@

$(ONT_INF).owl: $(ONT).owl
	$(ROBOT) -v reason -s true -m true -r hermit -i $< -o $@

$(ONT_INF_ALL).owl: $(ONT).owl
	$(ROBOT) -vv merge -i $< -i $(ONT_INF).owl -o $(ONT_INF_ALL).owl

$(ONT).obo: $(ONT_INF).owl
	$(EFO2OBO) -i $(ONT_INF).owl -o $(ONT).obo

$(ONT)_full.obo: $(ONT_INF_ALL).owl
	$(EFO2OBO) -i $(ONT_INF_ALL).owl -o $(ONT)_full.obo

#	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = hancestro
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -o $@
.PRECIOUS: imports/%_import.owl

# clone remote ontology locally, perfoming some excision of relations and annotations
#mirror/%.owl: $(SRC)
#	$(OWLTOOLS) $(OBOREAL)/$*.owl --remove-annotation-assertions -l -s -d --remove-dangling-annotations  -o $@
#.PRECIOUS: mirror/%.owl

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
sparql_test: $(ONT).owl
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	robot query -f tsv -i $< $(REPORT_ARGS)
