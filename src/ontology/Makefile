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
EFO2PREFIX = "EFO2: http://www.ebi.ac.uk/efo/"
ORDOPREFIX = "Orphanet: http://www.orpha.net/ORDO/Orphanet_"
MONDOPREFIX = "MONDO: http://purl.obolibrary.org/obo/MONDO_"
UBERONPREFIX = "UBERON: http://purl.obolibrary.org/obo/UBERON_"
HPPREFIX = "HP: http://purl.obolibrary.org/obo/HP_"
CLPREFIX = "CL: http://purl.obolibrary.org/obo/CL_"
CLPREFIX = "Orphanet: http://www.orpha.net/ORDO/Orphanet_"
BFOPREFIX = "BFO: http://purl.obolibrary.org/obo/BFO_"
ECTOPREFIX = "ECTO: http://purl.obolibrary.org/obo/ECTO_"
EFOPREPRO = $(BUILDDIR)/efo-edit-release.owl
EFOFIXER = ../../bin/efo-fixer.jar
MIRRORDIR=./mirror
HANCESTROGENERATED= ./build/efo-hancestro
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: all_imports all_gwas all_components release qc
qc: sparql_test all_reports
gh_actions: qc $(BUILDDIR)/$(ONT).owl

# ----------------------------------------
# Mirror
# ----------------------------------------

# Currently obtained using the get_mirrors script
# (mondo, hancestro and uberon)

# ----------------------------------------
# Imports
# ----------------------------------------

IMPORTS = mondo hancestro uberon hp cl fbbt obi oba chebi pr go ecto gsso
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

imports/mondo_import.owl: mirror/mondo.owl imports/mondo_terms.txt iri_dependencies/mondo_exclude.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/mondo_terms.txt --method BOT -O $(BASE)/$@ remove -T iri_dependencies/mondo_exclude.txt --term rdfs:comment -o $@
.PRECIOUS: imports/mondo_import.owl
	
imports/hancestro_import.owl: mirror/hancestro.owl imports/hancestro_terms.txt iri_dependencies/hancestro_exclude.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/hancestro_terms.txt --method BOT -O $(BASE)/$@ remove -T iri_dependencies/hancestro_exclude.txt -o $@
.PRECIOUS: imports/hancestro_import.owl
	
imports/oba_import.owl: imports/oba_bot.owl imports/oba_terms.txt $(SRC)
	$(ROBOT) filter -i $< --term-file imports/oba_terms.txt --term RO:0000052 --select "annotations ontology anonymous self" --trim true --signature true -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

# Change the parent of imported PR terms to "protein" (ChEBI:36080) to match existing EFO terms, rather than PR:000000001
# We also need to map to resolve some conflicts with ChEBI and proteins that already exist in EFO so we don't end up with duplicates.
#
imports/pr_import.owl: mirror/pr.owl imports/pr_terms.txt $(SRC)
	$(ROBOT) extract -i $< -T imports/pr_terms.txt --method BOT --copy-ontology-annotations true -O $(BASE)/$@ rename --mappings pr_efo_map.tsv -o $@
.PRECIOUS: imports/pr_import.owl

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
		merge -i build/preserve-axioms-$*.owl --collapse-import-closure false convert -f ofn -o $(SRC)
		
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

D2P_SOURCES=hpoa mondo-owl
D2P_RAW=$(foreach V,$(D2P_SOURCES), components/d2p_$V.ttl)

COMPONENTS=subclasses import_replaced_by mondo_efo_import anatomagram_lung anatomagram_kidney anatomagram_pancreas anatomagram_liver
COMPONENT_FILES=$(patsubst %, components/%.owl, $(COMPONENTS))
FOREIGN_AXIOMS=hancestro uberon
FOREIGN_AXIOM_FILES=$(patsubst %, components/efo_%.owl, $(FOREIGN_AXIOMS))
FOREIGN_AXIOM_FILES_DIFF=$(patsubst %, qc/diff_efo-%.txt, $(FOREIGN_AXIOMS))

components/subclasses.owl: ../templates/subclasses.csv
	$(ROBOT) template --template $< --prefix $(MONDOPREFIX) --prefix "snap: http://www.ifomis.org/bfo/1.1/snap#" --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(HPPREFIX) --prefix $(ECTOPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/subclasses.owl" -o $@

components/d2p_%.ttl: mirror/%.owl
	$(ROBOT) query -f ttl -i $< --query $(SPARQLDIR)/d2p-$*.ru $@

components/import_replaced_by.owl: ../templates/import_replaced_by.csv
	$(ROBOT) template --template $< --prefix $(MONDOPREFIX) --prefix "snap: http://www.ifomis.org/bfo/1.1/snap#" --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(HPPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/import_replaced_by.owl" -o $@

components/efo-rename.tsv: components/mondo_efo_mappings.tsv components/disease_to_phenotype_merged_signature.tsv
	python3 ../scripts/rename_tsv_subset.py $^ $@

# If you change the relation in the sparql query, make sure you add the new relation here as well.
components/legal_diseases.txt: $(SRC) components/disease_to_phenotype_merged.owl
	$(ROBOT) query -i $< -q $(SPARQLDIR)/efo-diseases.sparql $@.efo.txt
	$(ROBOT) query -i components/disease_to_phenotype_merged.owl -q $(SPARQLDIR)/hp_terms.sparql $@.hp.txt
	cat $@.efo.txt $@.hp.txt > $@ && rm $@.hp.txt $@.efo.txt
	echo "http://purl.org/dc/elements/1.1/source" >> $@
	echo "http://www.w3.org/2004/02/skos/core#related" >> $@

components/disease_to_phenotype_merged_signature.tsv: components/disease_to_phenotype_merged.owl
	$(ROBOT) query -i $< -q $(SPARQLDIR)/terms.sparql $@

components/disease_to_phenotype_merged.owl: $(D2P_RAW)
	$(ROBOT) merge $(addprefix -i , $(D2P_RAW)) \
		annotate --ontology-iri "http://www.ebi.ac.uk/efo/$@" -o $@

components/disease_to_phenotype.owl: components/disease_to_phenotype_merged.owl  components/efo-rename.tsv components/legal_diseases.txt
	$(ROBOT) merge -i $< \
		rename --mappings components/efo-rename.tsv \
		remove -T components/legal_diseases.txt --select complement --trim true \
		query --update $(SPARQLDIR)/remove-stray-classes.ru \
		annotate --ontology-iri "http://www.ebi.ac.uk/efo/$@" -o $@

components/mondo_efo_mappings.template.tsv: components/mondo_efo_mappings.tsv
	sed '1s/^/A oboInOwl:hasDbXref\tID\t\t\n/' $< | sed '1s/^/Mondo ID\tEFO id\tMondo Label\tEFO label\n/' | sed 's/http:\/\/purl.obolibrary.org\/obo\/MONDO_/MONDO:/g' > $@

components/mondo_efo_mappings.owl: mirror/mondo.owl components/mondo_efo_mappings.template.tsv
	$(ROBOT) --prefix "oboInOwl: http://www.geneontology.org/formats/oboInOwl#" template --input $< --template components/mondo_efo_mappings.template.tsv -o $@

components/mondo_efo_import.owl: components/mondo_efo_mappings.tsv imports/mondo_import.owl components/mondo_efo_mappings.owl
	java -jar ../../bin/mondo-id-switch.jar components/mondo_efo_mappings.tsv imports/mondo_import.owl $@ &&\
	$(ROBOT) -v merge -i $@ -i components/mondo_efo_mappings.owl \
		annotate --ontology-iri http://www.ebi.ac.uk/efo/components/mondo_efo_import.owl -o $@.ofn && mv $@.ofn $@

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
	$(ROBOT) merge -i $< $(addprefix unmerge -i , $(FOREIGN_AXIOM_FILES)) convert -f ofn -o $(SRC)

# ----------------------------------------
# ORPHANET REPLACEMENT
# ----------------------------------------

#remove_orphanet:
#	$(ROBOT) remove -i $(SRC) -T ../templates/orphanet_obsolete_terms.txt convert -f ofn -o efo-edit.owl 

#components/orphanet_mondo_replacement.owl: ../templates/orphanet_mondo_replacement.tsv remove_orphanet
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(EFO2PREFIX) --prefix $(ORDOPREFIX) -o $@

#components/orphanet_mondo_replacement_import.owl: ../templates/orphanet_obsolete_labels.tsv components/orphanet_mondo_replacement.owl
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(EFO2PREFIX) --prefix $(ORDOPREFIX) merge -i components/orphanet_mondo_replacement.owl annotate --ontology-iri "http://www.ebi.ac.uk/efo/components/orphanet_mondo_replacement_import.owl" -o $@

# ----------------------------------------
# AE anatomagrams components
# ----------------------------------------

#components/anatomagram_lung.owl: ../templates/anatomagram_lung.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_lung.owl" -o $@

#components/anatomagram_kidney.owl: ../templates/anatomagram_kidney.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_kidney.owl" -o $@

#components/anatomagram_pancreas.owl: ../templates/anatomagram_pancreas.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_pancreas.owl" -o $@

#components/anatomagram_liver.owl: ../templates/anatomagram_liver.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_liver.owl" -o $@

#components/anatomagram_placenta.owl: ../templates/anatomagram_liver.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_placenta.owl" -o $@

#components/anatomagram_%.owl: ../templates/anatomagram_%.tsv $(SRC)
#	$(ROBOT) template -i $(SRC) --template $< --prefix $(EFOPREFIX) --prefix $(UBERONPREFIX) --prefix $(CLPREFIX) --ontology-iri "http://www.ebi.ac.uk/efo/components/anatomagram_$*.owl" -o $@

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
release: $(BUILDDIR)/$(ONT).owl $(BUILDDIR)/$(ONT).obo $(BUILDDIR)/$(ONT).json $(BUILDDIR)/$(ONT)-base.owl
	cp $^ $(RELEASEDIR)
	
$(BUILDDIR)/$(ONT).owl: $(SRC)
	$(ROBOT) merge -i $< \
	reason -s true -m false -r hermit -v --equivalent-classes-allowed asserted-only \
	annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT).owl -V  $(BASE)/releases/v`cat version.txt`/$(ONT).owl -o $@

$(BUILDDIR)/$(ONT).obo: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/v`cat version.txt`/efo.owl \
	convert --check false -f obo -o $@
	
$(BUILDDIR)/$(ONT).json: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) annotate -i $< --ontology-iri http://www.ebi.ac.uk/efo/efo.owl --version-iri http://www.ebi.ac.uk/efo/releases/v`cat version.txt`/efo.owl \
	convert -f json -o $@

$(BUILDDIR)/$(ONT)-base.owl: build/efo.owl
	$(ROBOT) remove --input build/efo.owl \
		--base-iri 'http://www.ebi.ac.uk/efo/EFO_' \
		--axioms external \
		--preserve-structure false \
		--trim false \
		annotate -a owl:versionInfo `cat version.txt` -a rdfs:comment `date +%Y-%m-%d` -O $(BASE)/$(ONT)-base.owl -V  $(BASE)/releases/v`cat version.txt`/$(ONT)-base.owl --output $@

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = duplicate-label  nolabels multiple-label no-webulous-uris no-urigen-uris no-www-uris no-dangling id-length deprecated obsolete-replaced-whitespace wrong_efo_purl

# run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(BUILDDIR)/$(ONT).owl
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms obsolete_gwas
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

#REV=1fe0d2e92b0283978668a4391c57326d4f25dc80
REV=master
tmp/$(ONT)-master.owl:
	git show $(REV):src/ontology/$(SRC) > $@
	robot --catalog catalog-v001.xml merge -i $@ -o $@.owl && mv $@.owl $@

tmp/$(ONT)-master-reasoned.owl:
	git show $(REV):src/ontology/$(SRC) > $@
	robot --catalog catalog-v001.xml merge -i $@ reason -o $@.owl && mv $@.owl $@

tmp/$(ONT)-branch.owl:
	robot --catalog catalog-v001.xml merge -i $(SRC) -o $@.owl && mv $@.owl $@

tmp/$(ONT)-branch-reasoned.owl:
	robot --catalog catalog-v001.xml merge -i $(SRC) reason -o $@.owl && mv $@.owl $@


reports/robot_diff.md: tmp/$(ONT)-master.owl tmp/$(ONT)-branch.owl
	robot --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch.owl --labels true -f markdown -o $@
reports/robot_diff.txt: tmp/$(ONT)-master.owl tmp/$(ONT)-branch.owl
	robot --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch.owl --labels true -o $@
reports/robot_reasoned_diff.md: tmp/$(ONT)-master-reasoned.owl tmp/$(ONT)-branch-reasoned.owl
	robot --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch-reasoned.owl --labels true -f markdown -o $@
reports/robot_reasoned_diff.txt: tmp/$(ONT)-master-reasoned.owl tmp/$(ONT)-branch-reasoned.owl
	robot --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch-reasoned.owl --labels true -o $@


.PHONY: feature_diff
feature_diff:
	make IMP=false PAT=false reports/robot_diff.txt -B
	make IMP=false PAT=false reports/robot_reasoned_diff.txt -B

.PHONY: feature_diff_md
feature_diff_md:
	make IMP=false PAT=false reports/robot_diff.md -B
	make IMP=false PAT=false reports/robot_reasoned_diff.md -B

# ----------------------------------------
# Adhoc queries
# ----------------------------------------

build/fbbt-self-xref.txt: $(SRC)
	$(ROBOT) query --input $< --query $(SPARQLDIR)/remove-self-xrefs.sparql $@

remove-fbbt-self-xref: $(SRC)
	$(ROBOT) query --input $< --update $(SPARQLDIR)/remove-fbbt-xrefs.ru convert -f ofn --output $(SRC)
	
remove-defs-no-genus: $(SRC)
	$(ROBOT) query --input $< --update $(SPARQLDIR)/defs-without-genus-no-isabout-to-subclass.ru --output $(SRC).ofn && mv $(SRC).ofn $(SRC)

reports/report-%.tsv: $(SRC)
	$(ROBOT) query --input $< --select $(SPARQLDIR)/$*.sparql $@
	
trait_reports: reports/report-defs-without-genus.tsv reports/report-measurement-is-about.tsv reports/report-defs-without-genus-no-isabout.tsv

	# ----------------------------------------
	# GWAS trait tagging
	# ----------------------------------------
	
all_gwas: components/gwas_import.owl
	
components/gwas_template.owl: $(SRC) iri_dependencies/gwas_terms.tsv
	$(ROBOT) template --input $< -t iri_dependencies/gwas_terms.tsv query -c $(SPARQLDIR)/gwas_trait.ru $@

components/gwas_import.owl: components/gwas_template.owl
	$(ROBOT) annotate -i $< -O "http://www.ebi.ac.uk/efo/components/gwas_import.owl" convert -f ofn -o $@
	rm components/gwas_template.owl
