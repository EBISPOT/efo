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

# EFO uses version.txt for release versioning (not dates).
# VERSION holds the bare version (e.g. 3.87.0) used for owl:versionInfo.
# RELEASE_VERSION adds the "v" prefix (e.g. v3.87.0) used in version IRI paths.
VERSION = $(shell cat version.txt)
RELEASE_VERSION = v$(VERSION)
EFO_MASTER = https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/efo-edit.owl

# Override the ODK-generated ANNOTATE_ONTOLOGY_VERSION to use RELEASE_VERSION
# in version IRIs. This is a recursively-expanded variable, so it propagates
# to all ODK targets that use $(ANNOTATE_ONTOLOGY_VERSION) or $(ANNOTATE_CONVERT_FILE).
ANNOTATE_ONTOLOGY_VERSION = annotate -V $(ONTBASE)/releases/$(RELEASE_VERSION)/$@ --annotation owl:versionInfo $(VERSION)

# ----------------------------------------
# Import Overrides
# ----------------------------------------
# Only imports with non-empty exclude files or additional processing steps
# need explicit overrides here. All other imports use the ODK pattern rule.
#
# Non-empty exclude files: uberon (15 terms), hancestro (10 terms),
#   pr (5 terms), mondo (4138 terms).
# Empty exclude files (no override needed): chebi, hp, ecto, cl, gsso,
#   fbbt, obi, oba, fbbi, go.
#
# Each override replicates the full ODK v1.6 pipeline (odk:normalize,
# extract, annotation-property filtering, repair) and appends the
# exclude removal step. This ensures consistency with ODK-managed imports.

ifeq ($(IMP),true)

# Uberon import: exclude step for non-EFO terms
$(IMPORTDIR)/uberon_import.owl: $(MIRRORDIR)/uberon.owl $(IMPORTDIR)/uberon_terms.txt $(IMPORTSEED) | all_robot_plugins
	$(ROBOT) annotate --input $< --remove-annotations \
		odk:normalize --add-source true \
		extract --term-file $(IMPORTDIR)/uberon_terms.txt $(T_IMPORTSEED) \
			--force true --copy-ontology-annotations true \
			--individuals exclude --method BOT \
		remove $(foreach p,$(ANNOTATION_PROPERTIES),--term $(p)) \
			--term-file $(IMPORTDIR)/uberon_terms.txt $(T_IMPORTSEED) \
			--select complement --select annotation-properties \
		odk:normalize --base-iri $(URIBASE) \
			--subset-decls true --synonym-decls true \
		repair --merge-axiom-annotations true \
		remove -T iri_dependencies/uberon_exclude.txt \
		$(ANNOTATE_CONVERT_FILE)
.PRECIOUS: $(IMPORTDIR)/uberon_import.owl

# HANCESTRO import: exclude step for non-EFO terms
$(IMPORTDIR)/hancestro_import.owl: $(MIRRORDIR)/hancestro.owl $(IMPORTDIR)/hancestro_terms.txt $(IMPORTSEED) | all_robot_plugins
	$(ROBOT) annotate --input $< --remove-annotations \
		odk:normalize --add-source true \
		extract --term-file $(IMPORTDIR)/hancestro_terms.txt $(T_IMPORTSEED) \
			--force true --copy-ontology-annotations true \
			--individuals exclude --method BOT \
		remove $(foreach p,$(ANNOTATION_PROPERTIES),--term $(p)) \
			--term-file $(IMPORTDIR)/hancestro_terms.txt $(T_IMPORTSEED) \
			--select complement --select annotation-properties \
		odk:normalize --base-iri $(URIBASE) \
			--subset-decls true --synonym-decls true \
		repair --merge-axiom-annotations true \
		remove -T iri_dependencies/hancestro_exclude.txt \
		$(ANNOTATE_CONVERT_FILE)
.PRECIOUS: $(IMPORTDIR)/hancestro_import.owl

# PR import: rename step (PR terms → EFO/ChEBI equivalents) + exclude.
# This overrides ODK's is_large explicit target for PR.
ifeq ($(IMP_LARGE),true)
$(IMPORTDIR)/pr_import.owl: $(MIRRORDIR)/pr.owl $(IMPORTDIR)/pr_terms.txt $(IMPORTSEED) | all_robot_plugins
	$(ROBOT) annotate --input $< --remove-annotations \
		odk:normalize --add-source true \
		extract --term-file $(IMPORTDIR)/pr_terms.txt $(T_IMPORTSEED) \
			--force true --copy-ontology-annotations true \
			--individuals exclude --method BOT \
		remove $(foreach p,$(ANNOTATION_PROPERTIES),--term $(p)) \
			--term-file $(IMPORTDIR)/pr_terms.txt $(T_IMPORTSEED) \
			--select complement --select annotation-properties \
		odk:normalize --base-iri $(URIBASE) \
			--subset-decls true --synonym-decls true \
		repair --merge-axiom-annotations true \
		rename --mappings pr_efo_map.tsv \
		remove -T iri_dependencies/pr_exclude.txt \
		$(ANNOTATE_CONVERT_FILE)
.PRECIOUS: $(IMPORTDIR)/pr_import.owl
endif # IMP_LARGE=true

# MONDO intermediate import: not a direct import in efo-edit.owl.
# Built from the custom mondo mirror, used as input to the
# mondo_efo_import component (via mondo-id-switch.jar).
# Simpler pipeline (no odk:normalize/repair) since this is an
# intermediate artifact, not a final import module.
$(IMPORTDIR)/mondo_import.owl: $(MIRRORDIR)/mondo.owl $(IMPORTDIR)/mondo_terms.txt iri_dependencies/mondo_exclude.txt
	$(ROBOT) extract -i $< \
		--term-file $(IMPORTDIR)/mondo_terms.txt \
		--method BOT --copy-ontology-annotations true --force true \
		--individuals exclude \
		-O $(ONTBASE)/$@ \
		remove -T iri_dependencies/mondo_exclude.txt -o $@
.PRECIOUS: $(IMPORTDIR)/mondo_import.owl

endif # IMP=true

# ----------------------------------------
# Custom Mirrors (non-import data sources)
# ----------------------------------------

# MONDO base mirror: needed for imports/mondo_import.owl extraction.
# Declared here (not in efo-odk.yaml) to prevent update_repo from adding
# mondo_import.owl directly to efo-edit.owl (EFO routes MONDO through the
# mondo_efo_import component built by mondo-id-switch.jar instead).
$(MIRRORDIR)/mondo.owl:
	if [ $(MIR) = true ]; then curl -L --retry 4 --max-time 200 \
		http://purl.obolibrary.org/obo/mondo/mondo-base.owl -o $@.tmp.owl && \
		mv $@.tmp.owl $@; fi
.PRECIOUS: $(MIRRORDIR)/mondo.owl

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
# These overrides add $(OTHER_SRC) and $(IMPORT_FILES) as prerequisites (so
# components and imports are built before the release), use the correct
# ROBOT_RELEASE_IMPORT_MODE (which merges imports via catalog), and add the
# relax/reduce steps that ODK normally includes.

# Full: imports merged, reasoned, relaxed, reduced.
$(ONT)-full.owl: $(EDIT_PREPROCESSED) $(OTHER_SRC) $(IMPORT_FILES)
	$(ROBOT_RELEASE_IMPORT_MODE) \
		reason --reasoner $(REASONER) --equivalent-classes-allowed asserted-only \
			--exclude-tautologies structural \
		relax $(RELAX_OPTIONS) \
		reduce -r $(REASONER) $(REDUCE_OPTIONS) \
		annotate -a owl:versionInfo "$(VERSION)" \
			-a rdfs:comment "$$(date +%Y-%m-%d)" \
			-O $(ONTBASE)/$(ONT).owl \
			-V $(ONTBASE)/releases/$(RELEASE_VERSION)/$(ONT).owl \
			--output $@.tmp.owl && mv $@.tmp.owl $@

# Full JSON: re-annotate with canonical efo.owl IRI (not efo-full.json).
$(ONT)-full.json: $(ONT)-full.owl
	$(ROBOT) annotate --input $< \
		-O $(ONTBASE)/$(ONT).owl \
		-V $(ONTBASE)/releases/$(RELEASE_VERSION)/$(ONT).owl \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@

# Base: external axioms removed, only EFO-namespace terms retained.
$(ONT)-base.owl: $(EDIT_PREPROCESSED) $(OTHER_SRC) $(IMPORT_FILES)
	$(ROBOT_RELEASE_IMPORT_MODE) \
		reason --reasoner $(REASONER) --equivalent-classes-allowed asserted-only \
			--exclude-tautologies structural --annotate-inferred-axioms false \
		relax $(RELAX_OPTIONS) \
		reduce -r $(REASONER) $(REDUCE_OPTIONS) \
		remove --base-iri http://www.ebi.ac.uk/efo/EFO_ \
			--base-iri "http://www.ebi.ac.uk/efo/EFO#" \
			--axioms external --preserve-structure false --trim false \
		annotate -a owl:versionInfo "$(VERSION)" \
			-a rdfs:comment "$$(date +%Y-%m-%d)" \
			--link-annotation http://purl.org/dc/elements/1.1/type http://purl.obolibrary.org/obo/IAO_8000001 \
			-O $(ONTBASE)/$(ONT)-base.owl \
			-V $(ONTBASE)/releases/$(RELEASE_VERSION)/$(ONT)-base.owl \
			--output $@.tmp.owl && mv $@.tmp.owl $@

# Main release product: fix ontology IRI (ODK uses URIBASE which is wrong for EFO).
$(ONT).owl: $(ONT)-full.owl
	$(ROBOT) annotate --input $< \
		-O $(ONTBASE)/$(ONT).owl \
		-V $(ONTBASE)/releases/$(RELEASE_VERSION)/$(ONT).owl \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

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
# Label/Synonym Duplicate Check
# ----------------------------------------
# Detects duplicate lexical strings across rdfs:label and oboInOwl:hasExactSynonym.
# Runs as a warning-only check (exits 0 even with duplicates).

$(TMPDIR)/label-synonym-data.tsv: $(ONT)-full.owl
	$(ROBOT) query -f tsv -i $< -q $(SPARQLDIR)/label-synonym-dup-extract.sparql $@

.PHONY: label_synonym_dup_check
label_synonym_dup_check: $(TMPDIR)/label-synonym-data.tsv
	python3 ../scripts/detect_label_synonym_duplicates.py $< -o reports/label-synonym-duplicates.tsv

# Add label_synonym_dup_check as a prerequisite of the ODK test target.
# GNU Make allows multiple rules for the same target as long as at most one
# has a recipe; this adds a prerequisite without replacing the generated recipe.
test: label_synonym_dup_check

# Fix for ODK v1.6: update_repo runs `odk.py update` which calls `robot odk:import`,
# but the ODK ROBOT plugin (odk.jar) is not loaded unless ROBOT_PLUGINS_DIRECTORY
# is populated. The Makefile exports ROBOT_PLUGINS_DIRECTORY=$(TMPDIR)/plugins and
# all_robot_plugins copies odk.jar there, but update_repo doesn't declare it as a
# prerequisite. Adding it here ensures the plugin is available before odk.py runs.
update_repo: all_robot_plugins

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
