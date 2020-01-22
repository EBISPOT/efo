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

IMPORTS = mondo hancestro uberon
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_terms.txt,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

imports/%_terms.txt: iri_dependencies/%_terms.txt
	cat $^ | sort | uniq > $@

imports/mondo_import.owl: mirror/mondo.owl imports/mondo_terms.txt iri_dependencies/mondo_blacklist.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/mondo_terms.txt --method BOT -O $(BASE)/$@ remove -T iri_dependencies/mondo_blacklist.txt -o $@
.PRECIOUS: imports/mondo_import.owl
	
imports/uberon_terms.txt: iri_dependencies/uberon_terms.txt iri_dependencies/efo-relations.txt
	cat $^ | sort | uniq > $@

imports/uberon_bot.owl: mirror/uberon.owl imports/uberon_terms.txt
	$(ROBOT) extract -i $< -T imports/uberon_terms.txt --method BOT -O $(BASE)/$@ -o $@

imports/uberon_import.owl: imports/uberon_bot.owl imports/uberon_terms.txt $(SRC)
	$(ROBOT) filter -i $< --term-file imports/uberon_terms.txt --select "annotations ontology anonymous self" --trim true --signature true -O $(BASE)/$@ -o $@
.PRECIOUS: imports/uberon_import.owl



# ----------------------------------------
# Components
# ----------------------------------------

COMPONENTS=subclasses mondo_efo_import
COMPONENT_FILES=$(patsubst %, components/%.owl, $(COMPONENTS))
FOREIGN_AXIOMS=hancestro uberon
FOREIGN_AXIOM_FILES=$(patsubst %, components/efo_%.owl, $(FOREIGN_AXIOMS))
FOREIGN_AXIOM_FILES_DIFF=$(patsubst %, qc/diff_efo-%.txt, $(FOREIGN_AXIOMS))

components/subclasses.owl: ../templates/subclasses.csv
	$(ROBOT) template --template $< --prefix $(MONDOPREFIX) --prefix "snap: http://www.ifomis.org/bfo/1.1/snap#" --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/subclasses.owl" -o $@

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
	annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/`cat version.txt`/$(ONT).owl -o $@

$(BUILDDIR)/$(ONT).obo: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/`cat version.txt`/efo.owl \
	query --update ../sparql/inject-subset-declaration.sparql \
	convert --check false -f obo -o $@
	
$(BUILDDIR)/$(ONT).json: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/`cat version.txt`/efo.owl \
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
	$(ROBOT) query --input-iri https://www.ebi.ac.uk/efo/$* --select $(SPARQLDIR)/all_classes.sparql $@.tmp &&\
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
	# Custom SPARQL queries
	# ----------------------------------------

#$(BUILDDIR)/$(ONT).owl:
#	echo "Skipped."

$(BUILDDIR)/$(ONT)-mod.owl: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) remove -i $(BUILDDIR)/$(ONT).owl --term http://purl.obolibrary.org/obo/IAO_0000136 --term http://purl.obolibrary.org/obo/RO_0002314 -o $@

measurement_anatomy: $(BUILDDIR)/$(ONT).owl $(SPARQLDIR)/measurementisaboutanatomy.sparql
	$(ROBOT) materialize -i $< -r ELK --term IAO:0000136 query --use-graphs true -q $(SPARQLDIR)/measurementisaboutanatomy.sparql $@.csv

measurement_grouping: $(BUILDDIR)/$(ONT).owl $(SPARQLDIR)/measurementgroupingclasses.sparql
	$(ROBOT) materialize -i $< -r ELK --term IAO:0000136 query --use-graphs true -q $(SPARQLDIR)/measurementgroupingclasses.sparql $@.csv

$(BUILDDIR)/define_measurements.owl: $(BUILDDIR)/$(ONT).owl ../templates/definemeasurements.tsv
	$(ROBOT) template -i $< --template ../templates/definemeasurements.tsv --prefix "EFO: http://www.ebi.ac.uk/efo/EFO_" --prefix "RO: http://purl.obolibrary.org/obo/RO_" --prefix "UBERON: http://purl.obolibrary.org/obo/UBERON_" -o $@

$(BUILDDIR)/$(ONT)-iipo.owl: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) materialize -i $< -r ELK --term IAO:0000136 query --use-graphs true --update $(SPARQLDIR)/updatemeasurementisaboutanatomytoinheresin.ru remove --term http://purl.obolibrary.org/obo/IAO_0000136 --output $@

$(BUILDDIR)/$(ONT)-iipo-def.owl: $(BUILDDIR)/$(ONT)-iipo.owl $(BUILDDIR)/define_measurements.owl
	$(ROBOT) merge -i $< -i $(BUILDDIR)/define_measurements.owl -o reason -r HERMIT remove --term http://purl.obolibrary.org/obo/RO_0002314 $@

iipo_exp.txt: $(BUILDDIR)/$(ONT)-mod.owl $(BUILDDIR)/$(ONT)-iipo-def.owl
	$(ROBOT) diff --left $(BUILDDIR)/$(ONT)-mod.owl --right $(BUILDDIR)/$(ONT)-iipo-def.owl -o $@
