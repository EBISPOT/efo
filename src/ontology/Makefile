#EFO-MONDO
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
MONDO = ../templates/mondo.obo
UPPER = ./imports/upper_class.owl
PARENTSGENERATED = ./results/efoparents.owl
GENERATED = ./results/efo-mondo-generated.owl
EFOPREFIX = "EFO: http://www.ebi.ac.uk/efo/EFO_"
ORDOPREFIX = "Orphanet: http://www.orpha.net/ORDO/Orphanet_"
MONDOPREFIX = "MONDO: http://purl.obolibrary.org/obo/MONDO_"

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all:  combined.owl $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl $(ONT).obo $(ONT)_full.obo
test: all sparql_test
prepare_release: all
	cp $(ONT).owl $(ONT_INF).owl $(ONT_INF_ALL).owl $(ONT).obo $(ONT)_full.obo $(RELEASEDIR) &&\
	(test -f subsets/*owl && cp subsets/*{owl,obo} $(RELEASEDIR)/subsets && git add $(RELEASEDIR)/subsets/* || echo "no subsets") &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# create the main efo release by merging and removing import statements
# this will also set the release date and version number 
$(ONT).owl: ./results/combined.owl
	$(ROBOT) merge --input ./results/combined.owl -c true -i  $< annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@

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

### PREP CODE FOR EXTRACTING EFO DISEASE TERMS FOR MAPPING ###

disease_subclasses.csv: $(SRC) $(SPARQLDIR)/disease_subclass.sparql
	$(ROBOT) query --input $(SRC) --format csv --select $(SPARQLDIR)/disease_subclass.sparql disease_subclasses.csv
	
disease_staging_subclasses.csv: $(SRC) $(SPARQLDIR)/disease_subclass.sparql
	$(ROBOT) query --input $(SRC) --format csv --select $(SPARQLDIR)/disease_staging_subclass.sparql disease_staging_subclasses.csv

#diseaseparentchild.csv: $(SRC) $(SPARQLDIR)/diseaseparentchild.sparql
#	$(ROBOT) query --input $(ONT).owl --format csv --select $(SPARQLDIR)/diseaseparentchild.sparql diseaseparentchild.csv


### THE PLAN ###

#reads the template file containing all of the disease terms from EFO, HP and MONDO
efomondoslim.owl: ../templates/disease.tsv
	$(ROBOT) merge --input $(UPPER) template --merge-before --prefix $(EFOPREFIX) --prefix $(ORDOPREFIX) --prefix $(MONDOPREFIX) --template ../templates/disease.tsv reason -s true -m false -r ELK --output ./results/efomondoslim.owl

#constructs a slim annotation of efo_mondo for all terms
efo-slim.owl: efomondoslim.owl
	$(ROBOT) query --input ./results/efomondoslim.owl --format ttl --construct $(SPARQLDIR)/construct_slim.sparql ./results/efo-slim.owl

#merges all unmapped terms into the current owl file under their mondo mapped parents
$(PARENTSGENERATED):../templates/efoparents.tsv
	$(ROBOT) merge --input $(MONDO) template --merge-before --prefix $(EFOPREFIX) --prefix $(ORDOPREFIX) --prefix $(MONDOPREFIX)  --template ../templates/efoparents.tsv reason -s true -m false -r ELK --output $(PARENTSGENERATED)

$(GENERATED):../templates/unmapped.tsv $(PARENTSGENERATED)
	$(ROBOT) merge --input $(PARENTSGENERATED) template --merge-before --prefix $(EFOPREFIX) --prefix $(ORDOPREFIX) --prefix $(MONDOPREFIX)  --template ../templates/unmapped.tsv reason -s true -m false -r ELK --output $(GENERATED)

#merges the unmapped terms with their parents into the owl file with the slim annotation, creating branching
annotated-efo.owl: $(GENERATED) efo-slim.owl
	$(ROBOT) merge --input $(GENERATED) --input ./results/efo-slim.owl --output ./results/annotated-efo.owl 
	
#all terms with the slim annotation and their child terms extracted and ready for merging with efo
extracted-efo.owl: annotated-efo.owl
	$(OWLTOOLS) ./results/annotated-efo.owl --extract-ontology-subset -u $(BASE).owl -s efo_mondo -o ./results/extracted-efo.owl

#add the python script that replaces the URIs here (premergeuris.py)
#it is important to swap the URIs pre-merge with EFO to avoid problems in the file
#currently the swapping script depends on having a tsv file with the EFO and mapped MONDO URIs.

extracteduris.owl: extracted-efo.owl
	python ../templates/premergeuris.py
	
efo-edit-skos.owl: extracteduris.owl
	python ../templates/labels.py > efo-edit-skos.owl
	
#all terms combined with EFO
combined.owl: efo-edit-skos.owl
	$(ROBOT) merge --input ./results/efo-edit-skos.owl --input ./results/extracteduris.owl --output ./results/combined.owl

## CHANGE EFO LABELS TO SKOS:PREFLABEL ##



#### create a module of MONDO using the templates to create a list of URIs
#### Commented out below as not being used right now.

# results/mondo-xrefs.txt: ../templates/module.py
# 	python ../templates/module.py > results/mondo-xrefs.txt

# results/mondo_module.owl: results/mondo-xrefs.txt
# 	$(ROBOT) extract  --method BOT --input $(MONDO) --term-file results/mondo-xrefs.txt --output results/mondo_module.owl
	
# ensures all labels are of datatype string to avoid duplicates
#results/mondo_module2.owl: results/replacelabel.py
#	python results/replacelabel.py > results/mondo_module2.owl

# create a module of EFO in the same way?
# merge these modules and annotate with slim annotation
# merge this into the template file (may need to merge multiple templates into one owl file?)
# owl tools to extract only the terms with annotations
# replace MONDO URIs with EFO URIs
# merge into EFO




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
