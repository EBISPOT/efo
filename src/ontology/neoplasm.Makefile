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
SPARQL=sparql/efo_neoplasm.sparql

tmp/ metadata/:
	mkdir -p $@

tmp/efo_mondo.tsv: | tmp/
	wget "$(MAPPING_AUGMENTED_EFO_MONDO)" -O $@.tmp
	cut -f 1,2 $@.tmp > $@ && rm $@.tmp

#	sed -i '1s/^/o1\to2\n/' $@.tmp

tmp/mondo_efo.tsv: | tmp/
	wget "$(MAPPING_MONDO_EFO)" -O $@

tmp/unmapped.tsv: | tmp/
	wget "$(UNMAPPED_TERMS)" -O $@

$(O1):
	cp efo-edit.owl $@

tmp/mondo.owl:
	echo "Skipped $@" #wget $(MONDO) -O $@

tmp/%.json: tmp/%.owl
	$(ROBOT) merge -i $< convert --check false -f json -o $@
.PRECIOUS: tmp/%.json

SSSOM_META=scripts/efo.sssom.yml

tmp/%.sssom.tsv: tmp/%.json
	sssom parse -i $< -I obographs-json -m $(SSSOM_META) --curie-map-mode merged -o $@
.PRECIOUS: tmp/%.sssom.tsv

sssom: tmp/mondo.sssom.tsv tmp/efo.sssom.tsv

download_all: tmp/mondo_efo.tsv tmp/efo_mondo.tsv $(O1) tmp/mondo.owl tmp/ncit.owl

metadata/efo_cancer.tsv: | metadata/
	$(ROBOT) query -i $(O1) --query sparql/efo_cancer.sparql $@

metadata/%_synonyms.tsv: | metadata/
	$(ROBOT) query -i tmp/$*.owl --query sparql/synonyms.sparql $@

metadata/%_labels.tsv: | metadata/
	$(ROBOT) query -i tmp/$*.owl --query sparql/labels.sparql $@

extract_metadata: metadata/ncit_synonyms.tsv metadata/mondo_synonyms.tsv metadata/efo_synonyms.tsv
extract_metadata: metadata/mondo_labels.tsv metadata/efo_labels.tsv

$(TERMLIST): $(O1) $(SPARQL)
	$(ROBOT) query -i $(O1) --query $(SPARQL) $@
	sed -i 's/[<>]//g' $@

tmp/reclassified.owl: $(O2) $(MAP) $(TERMLIST)
	$(ROBOT) merge -i $(O2) \
		rename --mappings $(MAP) --allow-missing-entities true \
		filter -T $(TERMLIST) --select "self annotations" -o $@

$(UNMAPPED_TERMS_FILTERED): $(O1) $(UNMAPPED)
	$(ROBOT) filter -i $< -T $(UNMAPPED) --trim false -o $@

tmp/reclassify.owl: $(O1) tmp/reclassified.owl $(UNMAPPED_TERMS_FILTERED) $(TERMLIST)
	$(ROBOT) remove -i $(O1) -T $(TERMLIST) \
		merge -i tmp/reclassified.owl -i $(UNMAPPED_TERMS_FILTERED) --collapse-import-closure false -o $@

tmp/diff.txt: $(O1) tmp/reclassify.owl
	$(ROBOT) diff --left $(O1) --right tmp/reclassify.owl -o $@

mv_efo:
	$(ROBOT) convert -i tmp/reclassify.owl -f ofn -o efo-edit.owl

sed:
	sed -i 's/obo1:/obo2:/g' efo-edit.owl
	sed -i 's/chebi5:/chebi6:/g' efo-edit.owl
	sed -i 's/chebi4:/chebi5:/g' efo-edit.owl
	sed -i 's/chebi3:/chebi4:/g' efo-edit.owl
	sed -i 's/chebi2:/chebi3:/g' efo-edit.owl

