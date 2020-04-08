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
UBERONPREFIX = "UBERON: http://purl.obolibrary.org/obo/UBERON_"
HPPREFIX = "HP: http://purl.obolibrary.org/obo/HP_"
EFOPREPRO = $(BUILDDIR)/efo-edit-release.owl
EFOFIXER = ../../bin/efo-fixer.jar
MIRRORDIR=./mirror
HANCESTROGENERATED= ./build/efo-hancestro
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: all_imports all_components release qc
qc: sparql_test all_reports

# ----------------------------------------
# Mirror
# ----------------------------------------

# Currently obtained using the get_mirrors script
# (mondo, hancestro and uberon)

# ----------------------------------------
# Imports
# ----------------------------------------

IMPORTS = mondo hancestro uberon hp cl fbbt
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_terms.txt,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

imports/%_bot.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: imports/%_bot.owl imports/%_terms.txt $(SRC)
	$(ROBOT) filter -i $< --term-file imports/$*_terms.txt --select "annotations ontology anonymous self" --trim true --signature true -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

imports/%_terms.txt: iri_dependencies/%_terms.txt iri_dependencies/efo-relations.txt
	cat $^ | sort | uniq > $@

imports/mondo_import.owl: mirror/mondo.owl imports/mondo_terms.txt iri_dependencies/mondo_blacklist.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/mondo_terms.txt --method BOT -O $(BASE)/$@ remove -T iri_dependencies/mondo_blacklist.txt -o $@
.PRECIOUS: imports/mondo_import.owl
	
imports/hancestro_import.owl: mirror/hancestro.owl imports/hancestro_terms.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/hancestro_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/hancestro_import.owl

# ----------------------------------------
# Pipeline for removing a merged ontology
# and replacing by dynamic import
# ----------------------------------------

# 1. make seed of all terms currently used in EFO edit, for example all HP terms. 
# For this you need to create the respective xyz_terms.sparql query.

# this is only used to create initial term list and then never again
%_terms_in_src: $(SRC) $(SPARQLDIR)/%_terms.sparql
	$(ROBOT) query -i $< -q $(SPARQLDIR)/$*_terms.sparql iri_dependencies/$*_terms.txt

build/filtered-%-mirror.owl: mirror/%.owl iri_dependencies/%_terms.txt
	$(ROBOT) filter -i mirror/$*.owl -T iri_dependencies/$*_terms.txt --trim false -o $@

build/efo-edit-without-%.owl: $(SRC) build/filtered-%-mirror.owl
	$(ROBOT) remove -i $< --select imports --trim false unmerge -i build/filtered-$*-mirror.owl -o $@

build/remaining-%.ofn: build/efo-edit-without-%.owl iri_dependencies/%_terms.txt
	$(ROBOT) filter -i $< --term-file iri_dependencies/$*_terms.txt --trim false -o $@

#These are only the x-refs that are NOT in the ontology mirror
build/preserve-axioms-%.ttl: build/remaining-%.ofn
	$(ROBOT) query -i $< -c $(SPARQLDIR)/preserve_$*_axioms.sparql $@

build/preserve-axioms-%.owl: build/preserve-axioms-%.ttl
	$(ROBOT) convert -i $< -f owl -o $@

# 2. Dump all axioms from the ontology apart from the set of preserved axioms. 
# Preserved axioms are extracted using the preserve_xyz_axioms.sparql query (for example xrefs.)

dump_%: $(SRC) build/preserve-axioms-%.owl
	$(ROBOT) remove -i $< -T iri_dependencies/$*_terms.txt --axioms "annotation" --trim true  --preserve-structure false \
		remove -T iri_dependencies/$*_terms.txt --trim false --preserve-structure false \
		merge -i build/preserve-axioms-$*.owl --collapse-import-closure false -o $(SRC)
		
build/efo-edit-functional.owl: $(SRC)
	$(ROBOT) convert -i $(SRC) -f ofn -o $@

efo_edit_git_diff.txt:
	git diff $(SRC) > efo_edit_git_diff.txt
	
EFO_MASTER=https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/efo-edit.owl

master-$(SRC):
	wget $(EFO_MASTER) -O $@

efo_edit_robot_diff.txt: master-$(SRC) $(SRC)
	$(ROBOT) diff --left $(SRC) --right master-$(SRC) -o $@

edit_diff: efo_edit_git_diff.txt efo_edit_robot_diff.txt



# ----------------------------------------
# Components
# ----------------------------------------

COMPONENTS=subclasses mondo_efo_import
COMPONENT_FILES=$(patsubst %, components/%.owl, $(COMPONENTS))
FOREIGN_AXIOMS=hancestro uberon
FOREIGN_AXIOM_FILES=$(patsubst %, components/efo_%.owl, $(FOREIGN_AXIOMS))
FOREIGN_AXIOM_FILES_DIFF=$(patsubst %, qc/diff_efo-%.txt, $(FOREIGN_AXIOMS))

components/subclasses.owl: ../templates/subclasses.csv
	$(ROBOT) template --template $< --prefix $(MONDOPREFIX) --prefix "snap: http://www.ifomis.org/bfo/1.1/snap#" --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(HPPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/subclasses.owl" -o $@

components/mondo_efo_import.owl: components/mondo_efo_mappings.tsv imports/mondo_import.owl
	java -jar ../../bin/mondo-id-switch.jar components/mondo_efo_mappings.tsv imports/mondo_import.owl $@ &&\
	$(ROBOT) -v annotate -i $@ --ontology-iri http://www.ebi.ac.uk/efo/components/mondo_efo_import.owl -o $@.ofn && mv $@.ofn $@

components/efo_terms.txt: $(SRC) $(SPARQLDIR)/efo_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/efo_terms.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp

qc/%_terms.txt: mirror/%.owl $(SPARQLDIR)/%_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/$*_terms.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp
.PRECIOUS: qc/%_terms.txt
	
components/efo_foreign_preserve_terms.txt: $(SRC) $(SPARQLDIR)/efo_foreign_preserve_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/efo_foreign_preserve_terms.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp

components/efo_%.owl: $(SRC) qc/%_terms.txt components/efo_terms.txt components/efo_foreign_preserve_terms.txt
	$(ROBOT) filter -i $< --term-file qc/$*_terms.txt --trim false \
	remove -T components/efo_foreign_preserve_terms.txt \
	remove -T components/efo_terms.txt -o $@

qc/efo_no_%.owl: $(SRC) components/efo_%.owl
	$(ROBOT) remove --catalog catalog-v001.xml -i $< --select imports unmerge -i components/efo_$*.owl -o $@
.PRECIOUS: qc/efo_no_%.owl

qc/diff_efo-%.txt: $(SRC) qc/efo_no_%.owl
	$(ROBOT) diff --catalog catalog-v001.xml --left $< --right qc/efo_no_$*.owl -o $@

all_components: $(COMPONENT_FILES)

foreign_axioms: $(FOREIGN_AXIOM_FILES)

foreign_axiom_diff: $(FOREIGN_AXIOM_FILES_DIFF)
	
nuclear_strike: $(SRC) foreign_axiom_diff
	cp $(SRC) cp-$(SRC)
	$(ROBOT) merge -i $< $(addprefix unmerge -i , $(FOREIGN_AXIOM_FILES)) -o $(SRC)

# ----------------------------------------
# OTAR therapeutic areas
# ----------------------------------------

#Not currently used (13/08/2019)

#$(BUILDDIR)/OTAR_terms.owl: efo-edit.owl
#	$(ROBOT) filter --input efo-edit.owl --term-file ./imports/OTAR_terms.txt --select annotations --output $@

#$(BUILDDIR)/OTAR_tagged.owl: $(BUILDDIR)/OTAR_terms.owl
#	$(ROBOT) query --input $(BUILDDIR)/OTAR_terms.owl --query $(SPARQLDIR)/OTAR_therapeutic_areas.sparql $@

# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(BUILDDIR)/$(ONT).owl $(BUILDDIR)/$(ONT).obo $(BUILDDIR)/$(ONT).json
	cp $^ $(RELEASEDIR)
	
$(BUILDDIR)/$(ONT).owl: $(SRC)
	$(ROBOT) merge -i $< \
	reason -s true -m false -r hermit \
	annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/v`cat version.txt`/$(ONT).owl -o $@

$(BUILDDIR)/$(ONT).obo: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/v`cat version.txt`/efo.owl \
	query --update ../sparql/inject-subset-declaration.sparql \
	convert --check false -f obo -o $@
	
$(BUILDDIR)/$(ONT).json: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/v`cat version.txt`/efo.owl \
	query --update ../sparql/inject-subset-declaration.sparql \
	convert -f json -o $@

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
all_reports: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) query -f tsv -i $< $(REPORT_ARGS)
	
DIFF_REPORTS=efo.owl
DIFF_REPORTS_FILES=$(patsubst %, qc/diff_%_latest_release.txt, $(DIFF_REPORTS))
ENTITY_DIFF_FILES=$(patsubst %, qc/diff_%_entities.txt, $(DIFF_REPORTS))
	
qc/diff_%_latest_release.txt: $(BUILDDIR)/%
	$(ROBOT) diff --left $< --right-iri https://www.ebi.ac.uk/efo/$* -o $@
	
qc/current_%_entities.txt: $(BUILDDIR)/%
	$(ROBOT) query --input $< --select $(SPARQLDIR)/all_classes.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp
.PRECIOUS: qc/current_%_entities.txt

#$(BUILDDIR)/efo.owl:
#	echo "skipped"
	
#$(BUILDDIR)/efo.obo:
#	echo "skipped"

qc/latest_%_entities.txt: 
	$(ROBOT) query --input-iri https://github.com/EBISPOT/efo/releases/download/current/$* --select $(SPARQLDIR)/all_classes.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp
.PRECIOUS: qc/latest_%_entities.txt

qc/diff_%_entities.txt: qc/current_%_entities.txt qc/latest_%_entities.txt
	diff $^ > $@ || true

qc/uberon_consider_terms.txt: imports/uberon_bot.owl
	$(ROBOT) query --input $< --select $(SPARQLDIR)/uberon_terms.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp
	
qc/uberon_current_terms.txt: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) query --input $< --select $(SPARQLDIR)/uberon_terms.sparql $@.tmp &&\
	cat $@.tmp  | sort | uniq > $@ &&\
	rm $@.tmp
	
qc/uberon_diff.txt: qc/uberon_consider_terms.txt qc/uberon_current_terms.txt
	diff -u $^ | grep '^-[^-]' | sed 's/^-//'

all_diffs: $(ENTITY_DIFF_FILES) $(DIFF_REPORTS_FILES)
	
# ----------------------------------------
# Adhoc queries
# ----------------------------------------

build/fbbt-self-xref.txt: $(SRC)
	$(ROBOT) query --input $< --query $(SPARQLDIR)/remove-self-xrefs.sparql $@

remove-fbbt-self-xref: $(SRC)
	$(ROBOT) query --input $< --update $(SPARQLDIR)/remove-fbbt-xrefs.ru --output $(SRC)
