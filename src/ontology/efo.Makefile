# ========================================
# EFO Custom Makefile
# ========================================
# This file is included by the ODK-generated Makefile.
# It contains ONLY EFO-specific targets that are not handled
# by the standard ODK pipeline.
#
# If you need to customize your Makefile, make changes here
# rather than in the main Makefile.
# ========================================

# ----------------------------------------
# Custom Variables
# ----------------------------------------

# EFO uses version.txt for release versioning (not dates)
VERSION = $(shell cat version.txt)
EFO_MASTER = https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/efo-edit.owl

# ----------------------------------------
# Import Overrides
# ----------------------------------------

# PR import: needs rename step to remap PR terms to EFO/ChEBI equivalents
# and remove excluded terms. This overrides the ODK-generated pr_import target.
$(IMPORTDIR)/pr_import.owl: $(MIRRORDIR)/pr.owl $(IMPORTDIR)/pr_terms_combined.txt iri_dependencies/pr_exclude.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T $(IMPORTDIR)/pr_terms_combined.txt \
		--method BOT --copy-ontology-annotations true \
		-O $(ONTBASE)/$@ \
		rename --mappings pr_efo_map.tsv \
		remove -T iri_dependencies/pr_exclude.txt -o $@; fi
.PRECIOUS: $(IMPORTDIR)/pr_import.owl

# ----------------------------------------
# Custom Mirrors (non-import data sources)
# ----------------------------------------

# Full MONDO OWL (not base) is needed for the disease-to-phenotype pipeline
$(MIRRORDIR)/mondo-owl.owl:
	if [ $(MIR) = true ]; then curl -L --retry 4 --max-time 200 \
		http://purl.obolibrary.org/obo/mondo.owl -o $@.tmp.owl && \
		mv $@.tmp.owl $@; fi

# HPOA data is needed for the disease-to-phenotype pipeline
# TODO: Update this URL - the old Monarch URL (https://data.monarchinitiative.org/ttl/hpoa.ttl) returns 404
$(MIRRORDIR)/hpoa.owl:
	if [ $(MIR) = true ]; then curl -L --retry 4 --max-time 200 \
		https://data.monarchinitiative.org/ttl/hpoa.ttl -o $@.tmp.owl && \
		mv $@.tmp.owl $@; fi

# ----------------------------------------
# MONDO-EFO Import Component
# ----------------------------------------

# This pipeline:
# 1. Generates a ROBOT template with MONDO-to-EFO xref mappings
# 2. Runs mondo-id-switch.jar to remap MONDO IDs to EFO IDs in the import
# 3. Merges the xref annotations with the remapped import

components/mondo_efo_mappings.template.tsv: components/mondo_efo_mappings.tsv
	sed '1s/^/A oboInOwl:hasDbXref\tID\t\t\n/' $< | \
		sed '1s/^/Mondo ID\tEFO id\tMondo Label\tEFO label\n/' | \
		sed 's/http:\/\/purl.obolibrary.org\/obo\/MONDO_/MONDO:/g' > $@

components/mondo_efo_mappings.owl: $(MIRRORDIR)/mondo.owl components/mondo_efo_mappings.template.tsv
	$(ROBOT) --prefix "oboInOwl: http://www.geneontology.org/formats/oboInOwl#" \
		template --input $< --template components/mondo_efo_mappings.template.tsv -o $@

components/mondo_efo_import.owl: components/mondo_efo_mappings.tsv $(IMPORTDIR)/mondo_import.owl components/mondo_efo_mappings.owl
	java -jar $(MONDOIDSWITCHER) components/mondo_efo_mappings.tsv $(IMPORTDIR)/mondo_import.owl $@ && \
	$(ROBOT) -v merge -i $@ -i components/mondo_efo_mappings.owl \
		annotate --ontology-iri $(ONTBASE)/components/mondo_efo_import.owl -o $@.ofn && mv $@.ofn $@

# ----------------------------------------
# Disease-to-Phenotype Component
# ----------------------------------------

D2P_SOURCES = hpoa mondo-owl
D2P_RAW = $(foreach V,$(D2P_SOURCES), components/d2p_$V.ttl)

components/d2p_%.ttl: $(MIRRORDIR)/%.owl
	$(ROBOT) query -f ttl -i $< --query $(SPARQLDIR)/d2p-$*.ru $@

components/disease_to_phenotype_merged.owl: $(D2P_RAW)
	$(ROBOT) merge $(addprefix -i , $(D2P_RAW)) \
		annotate --ontology-iri "$(ONTBASE)/$@" -o $@

components/disease_to_phenotype_merged_signature.tsv: components/disease_to_phenotype_merged.owl
	$(ROBOT) query -i $< -q $(SPARQLDIR)/terms.sparql $@

components/efo-rename.tsv: components/mondo_efo_mappings.tsv components/disease_to_phenotype_merged_signature.tsv
	python3 ../scripts/rename_tsv_subset.py $^ $@

# If you change the relation in the sparql query, make sure you add the new relation here as well.
components/legal_diseases.txt: $(SRC) components/disease_to_phenotype_merged.owl
	$(ROBOT) query -i $< -q $(SPARQLDIR)/efo-diseases.sparql $@.efo.txt
	$(ROBOT) query -i components/disease_to_phenotype_merged.owl -q $(SPARQLDIR)/hp_terms.sparql $@.hp.txt
	cat $@.efo.txt $@.hp.txt > $@ && rm $@.hp.txt $@.efo.txt
	echo "http://purl.org/dc/elements/1.1/source" >> $@
	echo "http://www.w3.org/2004/02/skos/core#related" >> $@

components/disease_to_phenotype.owl: components/disease_to_phenotype_merged.owl components/efo-rename.tsv components/legal_diseases.txt
	$(ROBOT) merge -i $< \
		rename --mappings components/efo-rename.tsv \
		remove -T components/legal_diseases.txt --select complement --trim true \
		query --update $(SPARQLDIR)/remove-stray-classes.ru \
		annotate --ontology-iri "$(ONTBASE)/$@" -o $@

# ----------------------------------------
# GWAS Trait Tagging Component
# ----------------------------------------

.PHONY: all_gwas
all_gwas: components/gwas_import.owl

components/gwas_template.owl: $(SRC) iri_dependencies/gwas_terms.tsv
	$(ROBOT) template --input $< -t iri_dependencies/gwas_terms.tsv \
		query -c $(SPARQLDIR)/gwas_trait.ru $@

components/gwas_import.owl: components/gwas_template.owl
	$(ROBOT) annotate -i $< -O "$(ONTBASE)/components/gwas_import.owl" convert -f ofn -o $@
	rm components/gwas_template.owl

# ----------------------------------------
# Foreign Axioms Management
# ----------------------------------------
# These targets extract axioms from the edit file that belong to external
# ontologies (HANCESTRO, UBERON). Used for cleanup via the nuclear_strike target.

FOREIGN_AXIOMS = hancestro uberon
FOREIGN_AXIOM_FILES = $(patsubst %, components/efo_%.owl, $(FOREIGN_AXIOMS))
FOREIGN_AXIOM_FILES_DIFF = $(patsubst %, qc/diff_efo-%.txt, $(FOREIGN_AXIOMS))

components/efo_terms.txt: $(SRC) $(SPARQLDIR)/efo_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/efo_terms.sparql $@.tmp && \
	cat $@.tmp | sort | uniq > $@ && rm $@.tmp

qc/%_terms.txt: $(MIRRORDIR)/%.owl $(SPARQLDIR)/%_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/$*_terms.sparql $@.tmp && \
	cat $@.tmp | sort | uniq > $@ && rm $@.tmp
.PRECIOUS: qc/%_terms.txt

components/efo_foreign_preserve_terms.txt: $(SRC) $(SPARQLDIR)/efo_foreign_preserve_terms.sparql
	$(ROBOT) query --input $< --select $(SPARQLDIR)/efo_foreign_preserve_terms.sparql $@.tmp && \
	cat $@.tmp | sort | uniq > $@ && rm $@.tmp

components/efo_%.owl: $(SRC) qc/%_terms.txt components/efo_terms.txt components/efo_foreign_preserve_terms.txt
	$(ROBOT) filter -i $< --term-file qc/$*_terms.txt --trim false \
		remove -T components/efo_foreign_preserve_terms.txt \
		remove -T components/efo_terms.txt -o $@

qc/efo_no_%.owl: $(SRC) components/efo_%.owl
	$(ROBOT) remove --catalog catalog-v001.xml -i $< --select imports unmerge -i components/efo_$*.owl -o $@
.PRECIOUS: qc/efo_no_%.owl

qc/diff_efo-%.txt: $(SRC) qc/efo_no_%.owl
	$(ROBOT) diff --catalog catalog-v001.xml --left $< --right qc/efo_no_$*.owl -o $@

.PHONY: foreign_axioms foreign_axiom_diff nuclear_strike
foreign_axioms: $(FOREIGN_AXIOM_FILES)

foreign_axiom_diff: $(FOREIGN_AXIOM_FILES_DIFF)

nuclear_strike: $(SRC) foreign_axiom_diff
	cp $(SRC) cp-$(SRC)
	$(ROBOT) merge -i $< $(addprefix unmerge -i , $(FOREIGN_AXIOM_FILES)) convert -f ofn -o $(SRC)

# ----------------------------------------
# Release Overrides
# ----------------------------------------
# EFO uses version.txt-based version IRIs instead of ODK's date-based versions.

$(ONT)-full.owl: $(EDIT_PREPROCESSED)
	$(ROBOT) merge --input $< \
		reason --reasoner $(REASONER) -s true -m false \
			--equivalent-classes-allowed $(EQUIV_ENTITIES_ALLOWED) \
		annotate -a owl:versionInfo "$(VERSION)" \
			-a rdfs:comment "$$(date +%Y-%m-%d)" \
			-O $(ONTBASE)/$(ONT).owl \
			-V $(ONTBASE)/releases/v$(VERSION)/$(ONT).owl \
			--output $@

$(ONT)-full.obo: $(ONT)-full.owl
	$(ROBOT) annotate -i $< \
		--ontology-iri $(ONTBASE)/$(ONT).owl \
		--version-iri $(ONTBASE)/releases/v$(VERSION)/$(ONT).owl \
		convert --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@

$(ONT)-full.json: $(ONT)-full.owl
	$(ROBOT) annotate -i $< \
		--ontology-iri $(ONTBASE)/$(ONT).owl \
		--version-iri $(ONTBASE)/releases/v$(VERSION)/$(ONT).owl \
		convert -f json -o $@

$(ONT)-base.owl: $(EDIT_PREPROCESSED)
	$(ROBOT) remove --input $< \
		--base-iri 'http://www.ebi.ac.uk/efo/EFO_' \
		--base-iri 'http://www.ebi.ac.uk/efo/EFO#' \
		--axioms external \
		--preserve-structure false \
		--trim false \
		annotate -a owl:versionInfo "$(VERSION)" \
			-a rdfs:comment "$$(date +%Y-%m-%d)" \
			-O $(ONTBASE)/$(ONT)-base.owl \
			-V $(ONTBASE)/releases/v$(VERSION)/$(ONT)-base.owl \
			--output $@

# ----------------------------------------
# Feature Diff (branch vs master)
# ----------------------------------------

REV = master

tmp/$(ONT)-master.owl:
	git show $(REV):src/ontology/$(SRC) > $@
	$(ROBOT) --catalog catalog-v001.xml merge -i $@ -o $@.owl && mv $@.owl $@

tmp/$(ONT)-master-reasoned.owl:
	git show $(REV):src/ontology/$(SRC) > $@
	$(ROBOT) --catalog catalog-v001.xml merge -i $@ reason -o $@.owl && mv $@.owl $@

tmp/$(ONT)-branch.owl:
	$(ROBOT) --catalog catalog-v001.xml merge -i $(SRC) -o $@.owl && mv $@.owl $@

tmp/$(ONT)-branch-reasoned.owl:
	$(ROBOT) --catalog catalog-v001.xml merge -i $(SRC) reason -o $@.owl && mv $@.owl $@

reports/robot_diff.md: tmp/$(ONT)-master.owl tmp/$(ONT)-branch.owl
	$(ROBOT) --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch.owl --labels true -f markdown -o $@

reports/robot_diff.txt: tmp/$(ONT)-master.owl tmp/$(ONT)-branch.owl
	$(ROBOT) --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch.owl --labels true -o $@

reports/robot_reasoned_diff.md: tmp/$(ONT)-master-reasoned.owl tmp/$(ONT)-branch-reasoned.owl
	$(ROBOT) --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch-reasoned.owl --labels true -f markdown -o $@

reports/robot_reasoned_diff.txt: tmp/$(ONT)-master-reasoned.owl tmp/$(ONT)-branch-reasoned.owl
	$(ROBOT) --catalog catalog-v001.xml diff --left $< --right tmp/$(ONT)-branch-reasoned.owl --labels true -o $@

.PHONY: feature_diff feature_diff_md
feature_diff:
	$(MAKE) IMP=false PAT=false reports/robot_diff.txt -B
	$(MAKE) IMP=false PAT=false reports/robot_reasoned_diff.txt -B

feature_diff_md:
	$(MAKE) IMP=false PAT=false reports/robot_diff.md -B
	$(MAKE) IMP=false PAT=false reports/robot_reasoned_diff.md -B

# ----------------------------------------
# Ad-hoc Utility Targets
# ----------------------------------------

# Extract FBbt self-xrefs for review
build/fbbt-self-xref.txt: $(SRC)
	$(ROBOT) query --input $< --query $(SPARQLDIR)/remove-self-xrefs.sparql $@

# Remove FBbt self-referential xrefs
.PHONY: remove-fbbt-self-xref remove-defs-no-genus trait_reports
remove-fbbt-self-xref: $(SRC)
	$(ROBOT) query --input $< --update $(SPARQLDIR)/remove-fbbt-xrefs.ru convert -f ofn --output $(SRC)

# Remove definitions without genus
remove-defs-no-genus: $(SRC)
	$(ROBOT) query --input $< --update $(SPARQLDIR)/defs-without-genus-no-isabout-to-subclass.ru --output $(SRC).ofn && mv $(SRC).ofn $(SRC)

# Ad-hoc report generation
reports/report-%.tsv: $(SRC)
	$(ROBOT) query --input $< --select $(SPARQLDIR)/$*.sparql $@

trait_reports: reports/report-defs-without-genus.tsv reports/report-measurement-is-about.tsv reports/report-defs-without-genus-no-isabout.tsv

# ----------------------------------------
# Ontology extraction pipeline
# ----------------------------------------
# Used for initial extraction of terms from the edit file when transitioning
# a merged ontology to a dynamic import. Run once, then not needed again.

%_terms_in_src: $(SRC) $(SPARQLDIR)/%_terms.sparql
	$(ROBOT) query -i $< -q $(SPARQLDIR)/$*_terms.sparql iri_dependencies/$*_terms.txt

# Release diff against latest published version
qc/diff_%_latest_release.txt: $(ONT)-full.owl
	$(ROBOT) diff --left $< --right-iri https://www.ebi.ac.uk/efo/$* -o $@
