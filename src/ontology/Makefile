# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://www.ebi.ac.uk
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
UBERONPREFIX = "UBERON: http://purl.obolibrary.org/obo/UBERON_"
CLPREFIX = "CL: http://purl.obolibrary.org/obo/CL_"
ATLAS_SLIM = clean

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: $(ATLAS_SLIM) $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl $(ONT).obo $(ONT)_full.obo
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

# ----------------------------------------
# Atlas slim
# ----------------------------------------

## extracting the terms from the templates
### each template is merged with a blank upper efo to create an owl file for each
### in order to ensure the uri is maintained during this process, the prefix is added

gxa_anatomical_systems.owl: ../templates/efo-upper.owl ../templates/anatomical_systems.tsv
	$(ROBOT) merge --input ../templates/efo-upper.owl template --merge-before --prefix $(UBERONPREFIX) --template ../templates/anatomical_systems.tsv reason -s true -m false -r ELK --output gxa_anatomical_systems.owl

gxa_cell_types.owl: ../templates/efo-upper.owl ../templates/cell_types.tsv
	$(ROBOT) merge --input ../templates/efo-upper.owl template --merge-before --prefix $(CLPREFIX) --template ../templates/cell_types.tsv reason -s true -m false -r ELK --output gxa_cell_types.owl

gxa_organs.owl: ../templates/efo-upper.owl ../templates/organs.tsv
	$(ROBOT) merge --input ../templates/efo-upper.owl template --merge-before --prefix $(UBERONPREFIX) --template ../templates/organs.tsv reason -s true -m false -r ELK --output gxa_organs.owl

## adding the slim annotation
### each template's owl file undergoes a sparql query that labels each term with the respective slim annotation
### the output is an owl file for each

gxa_anatomical_slim.owl: gxa_anatomical_systems.owl
	$(ROBOT) query --input gxa_anatomical_systems.owl --format ttl --construct $(SPARQLDIR)/construct_slim_anatomy.sparql gxa_anatomical_slim.owl
	
gxa_cell_slim.owl: gxa_cell_types.owl
	$(ROBOT) query --input gxa_cell_types.owl --format ttl --construct $(SPARQLDIR)/construct_slim_cell.sparql gxa_cell_slim.owl
	
gxa_organs_slim.owl: gxa_organs.owl
	$(ROBOT) query --input gxa_organs.owl --format ttl --construct $(SPARQLDIR)/construct_slim_organs.sparql gxa_organs_slim.owl
	
## merging of the template slim owls and the efo-edit.owl file.
### temporarily output into a separate owl file while testing.

gxa-efo: $(SRC) gxa_anatomical_slim.owl gxa_cell_slim.owl gxa_organs_slim.owl
	$(ROBOT) merge --input $(SRC) --input gxa_anatomical_slim.owl --input gxa_cell_slim.owl --input gxa_organs_slim.owl --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) -o $(SRC) 
	
$(ATLAS_SLIM): gxa_anatomical_slim.owl gxa_cell_slim.owl gxa_organs_slim.owl gxa_anatomical_systems.owl gxa_cell_types.owl gxa_organs.owl
	rm -f gxa_anatomical_slim.owl gxa_cell_slim.owl gxa_organs_slim.owl gxa_anatomical_systems.owl gxa_cell_types.owl gxa_organs.owl


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
