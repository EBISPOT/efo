##################################
### Cancer Mapping Pipeline ######
##################################
ROBOT=robot --catalog catalog-v001.xml
MAPPING_EFO_MONDO=https://raw.githubusercontent.com/EBISPOT/efo/master/src/ontology/components/mondo_efo_mappings.tsv
MAPPING_MONDO_EFO=https://raw.githubusercontent.com/monarch-initiative/mondo/sssom-rewrite/src/ontology/mappings/mondo_hasdbxref_efo.sssom.tsv
MAPPING_AUGMENTED_EFO_MONDO=https://docs.google.com/spreadsheets/d/e/2PACX-1vQb6EtOFekjNUAfnnQLfm6KDFY3DH8WPV2Gjb_2WXLofZ87HvmR2m0wchNxplpDGwzucsWy6BGfaILp/pub?gid=2147444170&single=true&output=tsv
UNMAPPED_TERMS=https://docs.google.com/spreadsheets/d/e/2PACX-1vQb6EtOFekjNUAfnnQLfm6KDFY3DH8WPV2Gjb_2WXLofZ87HvmR2m0wchNxplpDGwzucsWy6BGfaILp/pub?gid=665705711&single=true&output=tsv
MONDO=http://purl.obolibrary.org/obo/mondo.owl

O1=efo-edit-tmp.owl
O2=tmp/mondo.owl
MAP=tmp/efo_mondo.tsv

UNMAPPED_TERMS_FILTERED=tmp/keep_unmapped.owl
TERMLIST=tmp/neoplasm_branch.tsv
UNMAPPED=tmp/unmapped.tsv
SPARQL_TERMLIST=sparql/efo_neoplasm.sparql
SPARQL_LABELS=sparql/efo-original-labels.ru
MIR=false

tmp/ metadata/:
	mkdir -p $@

tmp/efo_mondo.tsv: | tmp/
	if [ $(MIR) = true ]; then wget "$(MAPPING_AUGMENTED_EFO_MONDO)" -O $@.tmp &&\
	cut -f 1,2 $@.tmp > $@ && rm $@.tmp; fi

#	sed -i '1s/^/o1\to2\n/' $@.tmp

tmp/mondo_efo.tsv: | tmp/
	if [ $(MIR) = true ]; then wget "$(MAPPING_MONDO_EFO)" -O $@; fi

tmp/unmapped.tsv: | tmp/
	if [ $(MIR) = true ]; then wget "$(UNMAPPED_TERMS)" -O $@; fi

$(O1):
	cp efo-edit.owl $@

MON=false
tmp/mondo.owl:
	if [ $(MON) = true ]; then wget $(MONDO) -O $@; fi

download_all: tmp/mondo_efo.tsv tmp/efo_mondo.tsv $(O1) tmp/mondo.owl tmp/ncit.owl

metadata/efo_cancer.tsv: | metadata/
	$(ROBOT) query -i $(O1) --query sparql/efo_cancer.sparql $@

metadata/%_synonyms.tsv: | metadata/
	$(ROBOT) query -i tmp/$*.owl --query sparql/synonyms.sparql $@

metadata/%_labels.tsv: | metadata/
	$(ROBOT) query -i tmp/$*.owl --query sparql/labels.sparql $@

extract_metadata: metadata/ncit_synonyms.tsv metadata/mondo_synonyms.tsv metadata/efo_synonyms.tsv
extract_metadata: metadata/mondo_labels.tsv metadata/efo_labels.tsv

$(TERMLIST): $(O1) $(SPARQL_TERMLIST)
	$(ROBOT) query -i $(O1) --query $(SPARQL_TERMLIST) $@
	sed -i 's/[<>]//g' $@

tmp/original_labels.ttl: $(O1) $(SPARQL_LABELS)
	$(ROBOT) query -i $(O1) --query $(SPARQL_LABELS) $@

# filter trim true will omit axioms in the neoplasm branch that mention entities
# outside the neoplasm branch, in particular A sub R some C (where R, or C, are not in the neoplasm branch)
tmp/reclassified.owl: $(O2) $(MAP) $(TERMLIST)
	$(ROBOT) merge -i $(O2) \
		query --update sparql/mondo-labels-to-synonym.ru \
		rename --mappings $(MAP) --allow-missing-entities true \
		filter -T $(TERMLIST) --select "self annotations" -o $@

$(UNMAPPED_TERMS_FILTERED): $(O1) $(UNMAPPED)
	$(ROBOT) filter -i $< -T $(UNMAPPED) --trim false -o $@

reclassify.owl: $(O1) tmp/reclassified.owl tmp/original_labels.ttl $(UNMAPPED_TERMS_FILTERED) $(TERMLIST)
	$(ROBOT) remove -i $(O1) -T $(TERMLIST) \
		merge -i tmp/reclassified.owl -i $(UNMAPPED_TERMS_FILTERED) -i tmp/original_labels.ttl -i tmp/lost_illegal.owl --collapse-import-closure false -o $@

tmp/diff.txt: $(O1) reclassify.owl
	$(ROBOT) diff --left $(O1) --right reclassify.owl -o $@

tmp/diff2.txt: o1_merged.owl reclassify_merged.owl
	$(ROBOT) diff --left o1_merged.owl --right reclassify_merged.owl -o $@


# I want to get everything that has been lost for a wrong reason.
reclassify_merged.owl: #reclassify.owl
	$(ROBOT) remove -i reclassify.owl --select imports -o $@

o1_merged.owl: #$(O1)
	$(ROBOT) remove -i $(O1) --select imports -o $@

tmp/types.owl: #$(O1)
	$(ROBOT) query -i $(O1) --query sparql/efo-types.ru $@

unmerged.owl: tmp/types.owl reclassify_merged.owl o1_merged.owl
	$(ROBOT) unmerge -i o1_merged.owl -i reclassify_merged.owl \
		merge -i tmp/types.owl -o $@

tmp/lost.owl: unmerged.owl
	$(ROBOT) filter -i $< -T $(TERMLIST) --select complement --select classes --trim false \
		convert -f ofn -o $@

mv_efo:
	$(ROBOT) convert -i reclassify.owl -f ofn -o efo-edit.owl

sed:
	sed -i 's/obo1:/obo2:/g' efo-edit.owl
	sed -i 's/chebi5:/chebi6:/g' efo-edit.owl
	sed -i 's/chebi4:/chebi5:/g' efo-edit.owl
	sed -i 's/chebi3:/chebi4:/g' efo-edit.owl
	sed -i 's/chebi2:/chebi3:/g' efo-edit.owl

