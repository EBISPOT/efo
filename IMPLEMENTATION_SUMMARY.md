# Implementation Summary: Add CHEBI terms to 'response to ...' EFO terms

## Overview
This implementation addresses issue #2826 by adding `has_primary_input` (RO:0004009) axioms to EFO "response to" terms that correspond to chemical entities in CHEBI.

## Scope
Based on the new requirement to focus only on chemical terms (excluding vaccines, diets, therapies, procedures), the task was scoped to:
- 116 total "response to" terms in EFO
- 37 terms eliminated as non-chemical (vaccines, diets, therapies, transplants, exposures, etc.)
- 79 chemical-related terms evaluated
- **38 terms found matching CHEBI entities** (19 specific drugs + 19 drug classes)

## Implementation Status

### ✅ Completed (14 terms)
Successfully added `has_primary_input` (RO:0004009) axioms to 14 EFO terms with CHEBI entities that were already imported:

| EFO ID | EFO Label | CHEBI ID | CHEBI Label |
|--------|-----------|----------|-------------|
| EFO_0005195 | response to cholinesterase inhibitor | CHEBI_37733 | EC 3.1.1.8 (cholinesterase) inhibitor |
| EFO_0005325 | response to angiotensin-converting enzyme inhibitor | CHEBI_35457 | EC 3.4.15.1 (peptidyl-dipeptidase A) inhibitor |
| EFO_0005417 | response to mTOR inhibitor | CHEBI_68481 | mTOR inhibitor* |
| EFO_0005533 | response to non-steroidal anti-inflammatory | CHEBI_35475 | non-steroidal anti-inflammatory drug |
| EFO_0007767 | response to calcium channel blocker | CHEBI_38215 | calcium channel blocker |
| EFO_0009170 | response to tyrosine kinase inhibitor | CHEBI_38637 | tyrosine kinase inhibitor |
| EFO_0009748 | response to ketamine | CHEBI_6121 | ketamine |
| EFO_0010051 | response to immunosuppressant | CHEBI_35705 | immunosuppressive agent |
| EFO_0010062 | response to salmeterol | CHEBI_9011 | salmeterol |
| EFO_0010969 | response to growth hormone | CHEBI_37845 | growth hormone |
| EFO_0020862 | response to verapamil | CHEBI_9948 | verapamil |
| EFO_0020976 | response to steroid | CHEBI_35341 | steroid |
| EFO_0021424 | response to sevoflurane | CHEBI_9130 | sevoflurane |
| EFO_0021896 | response to rosuvastatin | CHEBI_38545 | rosuvastatin |

*Note: CHEBI_68481 (mTOR inhibitor) was in iri_dependencies but not in the current import file.

### 📋 Ready for Import (23 terms)
The following 23 CHEBI terms have been added to `src/ontology/iri_dependencies/chebi_terms.txt` and are ready to be imported when network access is available:

**Specific Drugs:**
- CHEBI_9123: sertraline
- CHEBI_10023: voriconazole
- CHEBI_9648: tramadol
- CHEBI_133833: benznidazole
- CHEBI_231601: trastuzumab
- CHEBI_231614: Nivolumab
- CHEBI_32246: tolvaptan
- CHEBI_51041: acamprosate
- CHEBI_6822: Methazolamide
- CHEBI_7773: Ondansetron
- CHEBI_84500: varenicline

**Drug Classes:**
- CHEBI_35442: antiparasitic agent
- CHEBI_35530: beta-adrenergic antagonist
- CHEBI_35674: antihypertensive agent
- CHEBI_36044: antiviral drug
- CHEBI_36809: tricyclic antidepressant
- CHEBI_37670: protease inhibitor
- CHEBI_47956: thiocarboxamide
- CHEBI_51373: GABA agonist
- CHEBI_53213: diisocyanate
- CHEBI_61016: angiotensin receptor antagonist
- CHEBI_64857: cosmetic
- CHEBI_68481: mTOR inhibitor

### ❌ Not Found in CHEBI (13 terms)
These terms were not found in CHEBI (mostly biologics - monoclonal antibodies and proteins):
- bevacizumab, dalcetrapib, cetuximab, flupirtine, ranibizumab, darapladib
- mepolizumab, synacthen, supplemental oxygen, radioiodine, belimumab
- peginterferon alfa-2a, piromelatine, secukinumab, ropeginterferon alfa-2b
- recombinant tissue-plasminogen activator, levodopa

### 🚫 Excluded (37 non-chemical terms)
Terms excluded based on the requirement to focus only on chemical entities:
- Vaccines, diets, therapies, procedures, transplants, exposures, etc.

## Files Modified
1. **src/ontology/efo-edit.owl** - Added RO:0004009 restrictions to 14 terms
2. **src/ontology/iri_dependencies/chebi_terms.txt** - Added 23 new CHEBI IRIs

## Next Steps
To complete the implementation for all 38 terms with CHEBI matches:

1. **Update mirrors** (when network access is available):
   ```bash
   cd src/ontology
   ./get_mirrors.sh
   ```

2. **Regenerate CHEBI import**:
   ```bash
   make imports/chebi_import.owl -B
   ```

3. **Add axioms for the remaining 24 terms** using the EFO-ontologist agent or manual editing

4. **Run normalization**:
   ```bash
   make normalize_src
   ```

5. **Validate changes**:
   ```bash
   robot reason -i efo-edit.owl
   ```

## Technical Details

### Example Axiom Added
```xml
<rdfs:subClassOf>
    <owl:Restriction>
        <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/RO_0004009"/>
        <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/CHEBI_38637"/>
    </owl:Restriction>
</rdfs:subClassOf>
```

### Relation Used
- **Property**: RO:0004009 (has_primary_input)
- **Source**: Already available via OBA import
- **Purpose**: Links response terms to the chemical entities they respond to

## Verification
A table of all terms with the `has_primary_input` axiom has been generated and saved to `/tmp/has_primary_input_table.csv`.

To regenerate this table at any time:
```bash
grep -B 5 "RO_0004009" src/ontology/efo-edit.owl | grep -E "(EFO_|CHEBI_)"
```
