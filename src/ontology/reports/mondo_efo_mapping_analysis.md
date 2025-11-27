# Mondo-EFO Mapping Analysis Report

This report analyzes the first 100 term mappings from `mondo_efo_mappings.tsv` to document
xrefs and synonyms that exist in EFO terms which should be verified against the corresponding
Mondo terms before completing the migration.

## Summary

- **Total terms analyzed**: 100
- **Terms with xrefs**: 67
- **Terms with synonyms**: 62
- **Total xrefs to verify**: 380
- **Total synonyms to verify**: 452

## Methodology

For each EFO term in the mapping, the following metadata was extracted:
- Database cross-references (xrefs)
- Synonyms (exact, related, broad, narrow)

This metadata should be compared against the corresponding Mondo term to ensure
no valuable information is lost during the migration process.

## Detailed Analysis

### MONDO:0004960 ↔ EFO:0000203

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004960`
- **Mondo Label**: monoclonal gammopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000203`
- **EFO Label**: monoclonal gammopathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:7442`
- `MESH:D008998`
- `MedDRA:10060880`
- `NCIt:C35548`
- `SNOMEDCT:277577000`
- `SNOMEDCT:35601003`
- `SNOMEDCT:58648008`

**EFO Synonyms** (to verify in Mondo):

- Benign Monoclonal Gammopathy *(type: exact)*
- MGUS *(type: exact)*
- MGUS - Monoclonal gammopathy of uncertain significance *(type: exact)*
- Monoclonal Gammopathy Of Undetermined Significance (MGUS) *(type: exact)*
- Monoclonal Gammopathy of Unknown Significance *(type: exact)*
- Monoclonal gammopathy of uncertain significance *(type: exact)*
- Monoclonal gammopathy of uncertain significance (disorder) *(type: exact)*
- Monoclonal gammopathy of undetermined significance *(type: exact)*
- Monoclonal gammopathy of undetermined significance (morphologic abnormality) *(type: exact)*
- Paraproteinaemia *(type: exact)*
- Paraproteinemia *(type: exact)*

---

### MONDO:0004972 ↔ EFO:0000232

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004972`
- **Mondo Label**: adenoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000232`
- **EFO Label**: adenoma

**EFO Xrefs** (to verify in Mondo):

- `DOID:657`
- `EFO:0000232`
- `ICDO:8140/0`
- `MESH:D000236`
- `NCIT:C2855`
- `SCTID:443416007`
- `UMLS:C0001430`

**EFO Synonyms** (to verify in Mondo):

- acinar cell adenoma *(type: exact)*
- acinar cell adenoma (morphologic abnormality) *(type: exact)*
- acinic cell adenoma *(type: exact)*
- adenoma *(type: exact)*
- adenoma, benign *(type: narrow)*
- adenomas *(type: exact)*

---

### MONDO:0004994 ↔ EFO:0000318

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004994`
- **Mondo Label**: cardiomyopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000318`
- **EFO Label**: cardiomyopathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:0050700`
- `ICD10:I42`
- `ICD9:425`
- `MESH:D009202`
- `MedDRA:10007636`
- `NCIt:C34830`
- `SNOMEDCT:85898001`

**EFO Synonyms** (to verify in Mondo):

- CARDIOMYOPATH IN OTH DIS *(type: exact)*
- CARDIOMYOPATHIES SECOND *(type: exact)*
- Cardiomyopathies *(type: exact)*
- Cardiomyopathies, Primary *(type: exact)*
- Cardiomyopathies, Secondary *(type: exact)*
- Cardiomyopathy (disorder) *(type: exact)*
- Cardiomyopathy NOS *(type: exact)*
- Cardiomyopathy NOS (disorder) *(type: exact)*
- Cardiomyopathy in other diseases classified elsewhere *(type: exact)*
- Cardiomyopathy, NOS *(type: exact)*
- Cardiomyopathy, Primary *(type: exact)*
- Cardiomyopathy, Secondary *(type: exact)*
- Other primary cardiomyopathies *(type: exact)*
- Other primary cardiomyopathies (disorder) *(type: exact)*
- Other primary cardiomyopathy NOS *(type: exact)*
- Other primary cardiomyopathy NOS (disorder) *(type: exact)*
- PRIM CARDIOMYOPATHY NEC *(type: exact)*
- Primary Cardiomyopathies *(type: exact)*
- Primary Cardiomyopathy *(type: exact)*
- Secondary Cardiomyopathies *(type: exact)*
- Secondary Cardiomyopathy *(type: exact)*
- [X]Cardiomyopathy in other diseases classified elsewhere *(type: exact)*
- [X]Cardiomyopathy in other diseases classified elsewhere (disorder) *(type: exact)*

---

### MONDO:0004995 ↔ EFO:0000319

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004995`
- **Mondo Label**: cardiovascular disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000319`
- **EFO Label**: cardiovascular disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:1287`
- `ICD10:I98`
- `ICD10:I99`
- `ICD9:390-459.99`
- `ICD9:420-429.99`
- `ICD9:423`
- `ICD9:423.8`
- `ICD9:424`
- `ICD9:429`
- `ICD9:429.2`
- `ICD9:429.7`
- `ICD9:429.8`
- `ICD9:429.81`
- `ICD9:429.89`
- `ICD9:459.9`
- `MESH:D002318`
- `MedDRA:10007648`
- `NCIt:C2931`
- `SNOMEDCT:105980002`
- `SNOMEDCT:49601007`

**EFO Synonyms** (to verify in Mondo):

- ASCVD *(type: exact)*
- CARDIOVASC DIS *(type: exact)*
- CIRCULATORY DISEASE NOS *(type: exact)*
- CVD *(type: exact)*
- CVD, NOS *(type: exact)*
- CVS disease *(type: exact)*
- Cardiovascular Disease (CVD) *(type: exact)*
- Cardiovascular Diseases *(type: exact)*
- Cardiovascular Disorder *(type: exact)*
- Cardiovascular Disorders *(type: exact)*
- Cardiovascular disease, NOS *(type: exact)*
- Cardiovascular disease, unspecified *(type: exact)*
- Cardiovascular disorder, NOS *(type: exact)*
- Cardiovascular system disease *(type: exact)*
- Certain sequelae of myocardial infarction, not elsewhere classified *(type: exact)*
- Circulatory system disease NOS *(type: exact)*
- Circulatory system disease NOS (disorder) *(type: exact)*
- DISEASES OF THE CIRCULATORY SYSTEM *(type: exact)*
- Disease affecting entire cardiovascular system *(type: exact)*
- Disease affecting entire cardiovascular system (disorder) *(type: exact)*
- Disease of cardiovascular system *(type: exact)*
- Disease of cardiovascular system (disorder) *(type: exact)*
- Disease of cardiovascular system, NOS *(type: exact)*
- Disease, Cardiovascular *(type: exact)*
- Diseases, Cardiovascular *(type: exact)*
- Disorder of cardiovascular system *(type: exact)*
- Disorder of cardiovascular system (disorder) *(type: exact)*
- Disorder of circulatory system *(type: exact)*
- Disorder of circulatory system, NOS *(type: exact)*
- Disorder of the circulatory system *(type: exact)*
- ILL-DEFINED HRT DIS NEC *(type: exact)*
- Ill-defined descriptions and complications of heart disease *(type: exact)*
- OTHER SEQUELAE OF MI NEC *(type: exact)*
- Other diseases of endocardium *(type: exact)*
- Other diseases of endocardium (disorder) *(type: exact)*
- Other diseases of pericardium *(type: exact)*
- Other diseases of pericardium (disorder) *(type: exact)*
- Other disorders of papillary muscle *(type: exact)*
- Other forms of heart disease *(type: exact)*
- Other forms of heart disease (disorder) *(type: exact)*
- Other heart disease *(type: exact)*
- Other heart disease (disorder) *(type: exact)*
- Other heart disease NOS *(type: exact)*
- Other heart disease NOS (disorder) *(type: exact)*
- Other ill-defined heart disease *(type: exact)*
- Other ill-defined heart disease (disorder) *(type: exact)*
- Other ill-defined heart disease NOS *(type: exact)*
- Other ill-defined heart disease NOS (disorder) *(type: exact)*
- Other ill-defined heart diseases *(type: exact)*
- Other pericardial disease NOS *(type: exact)*
- Other pericardial disease NOS (disorder) *(type: exact)*
- Other sequelae of myocardial infarction, not elsewhere classified *(type: exact)*
- Other specified diseases of pericardium *(type: exact)*
- Other specified pericardial disease NOS *(type: exact)*
- Other specified pericardial disease NOS (disorder) *(type: exact)*
- PAPILLARY MUSCLE DIS NEC *(type: exact)*
- PERICARDIAL DISEASE NEC *(type: exact)*
- Unspecified circulatory system disorder *(type: exact)*
- [X]Cardiovascular disease, unspecified *(type: exact)*
- [X]Cardiovascular disease, unspecified (disorder) *(type: exact)*
- [X]Other forms of heart disease *(type: exact)*
- [X]Other forms of heart disease (disorder) *(type: exact)*
- [X]Other ill-defined heart diseases *(type: exact)*
- [X]Other ill-defined heart diseases (disorder) *(type: exact)*
- [X]Other specified diseases of pericardium *(type: exact)*
- [X]Other specified diseases of pericardium (disorder) *(type: exact)*
- circulatory system disease *(type: exact)*
- disease of subdivision of hemolymphoid system *(type: exact)*

---

### MONDO:0005009 ↔ EFO:0000373

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005009`
- **Mondo Label**: congestive heart failure
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000373`
- **EFO Label**: congestive heart failure

**EFO Xrefs** (to verify in Mondo):

- `DOID:6000`
- `ICD9:428.0`
- `MedDRA:10010684`
- `NCIt:C3080`
- `SNOMEDCT:42343007`

**EFO Synonyms** (to verify in Mondo):

- CCF - Congestive cardiac failure *(type: exact)*
- CHF *(type: exact)*
- CHF - Congestive heart failure *(type: exact)*
- CHF NOS *(type: exact)*
- Cardiac Failure *(type: exact)*
- Cardiac Failure Congestive *(type: exact)*
- Congestive cardiac failure *(type: exact)*
- Congestive heart disease *(type: exact)*
- Congestive heart failure (disorder) *(type: exact)*
- Congestive heart failure, unspecified *(type: exact)*
- Congetive cardiac failure *(type: exact)*
- Decompensation, Heart *(type: exact)*
- FAILURE, CONGESTIVE HEART *(type: exact)*
- Heart Decompensation *(type: exact)*
- Heart Failure, Congestive *(type: exact)*
- Myocardial Failure *(type: exact)*

---

### MONDO:0005065 ↔ EFO:0000588

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005065`
- **Mondo Label**: mesothelioma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000588`
- **EFO Label**: mesothelioma

**EFO Xrefs** (to verify in Mondo):

- `EFO:0000588`
- `ICD10:C45`
- `MESH:D008654`
- `NCIT:C3234`
- `OMIM:156240`
- `UMLS:C0025500`

**EFO Synonyms** (to verify in Mondo):

- mesothelioma *(type: exact)*

---

### MONDO:0005089 ↔ EFO:0000691

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005089`
- **Mondo Label**: sarcoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000691`
- **EFO Label**: sarcoma

**EFO Xrefs** (to verify in Mondo):

- `DOID:1115`
- `EFO:0000691`
- `GARD:0012018`
- `ICD10:C49`
- `ICD9:171`
- `ICD9:171.0`
- `ICD9:171.2`
- `ICD9:171.3`
- `ICD9:171.4`
- `ICD9:171.5`
- `ICD9:171.6`
- `ICD9:171.7`
- `ICD9:171.8`
- `ICD9:171.9`
- `ICDO:8800/3`
- `MESH:D012509`
- `NCIT:C9118`
- `SCTID:424413001`

**EFO Synonyms** (to verify in Mondo):

- mesenchymal tumor, malignant *(type: exact)*
- sarcoma *(type: exact)*
- sarcoma of soft tissue and bone *(type: exact)*
- sarcoma of the soft tissue and bone *(type: exact)*
- sarcoma, malignant *(type: exact)*
- tumor of soft tissue and skeleton *(type: exact)*

---

### MONDO:0005093 ↔ EFO:0000701

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005093`
- **Mondo Label**: skin disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000701`
- **EFO Label**: skin disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:37`
- `ICD10:L08`
- `ICD10:L30`
- `ICD10:L53`
- `ICD10:L91`
- `ICD10:L98`
- `ICD10:R21`
- `NCIt:C3371`

**EFO Synonyms** (to verify in Mondo):

- Cutaneous Disorder *(type: exact)*
- SKIN AND SUBCUTANEOUS TISSUE DISORDERS *(type: exact)*
- Skin Diseases and Manifestations *(type: exact)*
- Skin Disorder *(type: exact)*

---

### MONDO:0005010 ↔ EFO:0001645

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005010`
- **Mondo Label**: coronary artery disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0001645`
- **EFO Label**: coronary artery disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:3393`
- `ICD10:I25`
- `ICD9:410-414.99`
- `ICD9:414.0`
- `MedDRA:10011078`
- `NCIt:C26732`
- `NCIt:C50625`
- `OMIM:608320`
- `OMIM:608901`
- `OMIM:610938`
- `OMIM:614466`
- `OMIM:617347`
- `SNOMEDCT:414545008`
- `SNOMEDCT:443502000`
- `SNOMEDCT:53741008`

**EFO Synonyms** (to verify in Mondo):

- Arterioscleroses, Coronary *(type: exact)*
- Arteriosclerosis, Coronary *(type: exact)*
- Artery Disease, Coronary *(type: exact)*
- Artery Diseases, Coronary *(type: exact)*
- Atheroscleroses, Coronary *(type: exact)*
- Atherosclerosis, Coronary *(type: exact)*
- CAD *(type: exact)*
- CHD *(type: exact)*
- CHD (coronary heart disease) *(type: exact)*
- CHD - Coronary heart disease *(type: exact)*
- CORONARY ARTERY DIS *(type: exact)*
- CORONARY DIS *(type: exact)*
- CORONARY HEART DIS *(type: exact)*
- Coronary Arterioscleroses *(type: exact)*
- Coronary Arteriosclerosis *(type: exact)*
- Coronary Artery Disease *(type: exact)*
- Coronary Artery Diseases *(type: exact)*
- Coronary Atheroscleroses *(type: exact)*
- Coronary Atherosclerosis *(type: exact)*
- Coronary Disease *(type: exact)*
- Coronary Diseases *(type: exact)*
- Coronary Heart Diseases *(type: exact)*
- Disease, Coronary *(type: exact)*
- Disease, Coronary Artery *(type: exact)*
- Disease, Coronary Heart *(type: exact)*
- Diseases, Coronary *(type: exact)*
- Diseases, Coronary Artery *(type: exact)*
- Diseases, Coronary Heart *(type: exact)*
- Heart Disease, Coronary *(type: exact)*
- Heart Diseases, Coronary *(type: exact)*
- coronary heart disease *(type: exact)*

---

### MONDO:0011057 ↔ EFO:0003763

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0011057`
- **Mondo Label**: cerebrovascular disorder
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003763`
- **EFO Label**: cerebrovascular disorder

**EFO Xrefs** (to verify in Mondo):

- `DOID:6713`
- `ICD10:I66`
- `ICD10:I67`
- `ICD10:I69`
- `ICD9:430-438.99`
- `MESH:D002561`
- `MedDRA:10008196`
- `MedDRA:10008200`
- `NCIt:C2938`
- `SNOMEDCT:62914000`

**EFO Synonyms** (to verify in Mondo):

- BRAIN VASCULAR DIS *(type: exact)*
- Brain Vascular Disorder *(type: exact)*
- Brain Vascular Disorders *(type: exact)*
- CEREBROVASCULAR DIS *(type: exact)*
- Cerebrovascular Disease *(type: exact)*
- Cerebrovascular Disorders *(type: exact)*
- Cerebrovascular Insufficiencies *(type: exact)*
- Cerebrovascular Insufficiency *(type: exact)*
- Cerebrovascular Occlusion *(type: exact)*
- Cerebrovascular Occlusions *(type: exact)*
- INTRACRANIAL VASCULAR DIS *(type: exact)*
- Insufficiencies, Cerebrovascular *(type: exact)*
- Insufficiency, Cerebrovascular *(type: exact)*
- Intracranial Vascular Disease *(type: exact)*
- Intracranial Vascular Diseases *(type: exact)*
- Intracranial Vascular Disorder *(type: exact)*
- Intracranial Vascular Disorders *(type: exact)*
- Occlusion, Cerebrovascular *(type: exact)*
- Occlusions, Cerebrovascular *(type: exact)*
- VASCULAR DIS INTRACRANIAL *(type: exact)*
- Vascular Disease, Intracranial *(type: exact)*
- Vascular Diseases, Intracranial *(type: exact)*
- Vascular Disorder, Brain *(type: exact)*
- Vascular Disorder, Intracranial *(type: exact)*
- Vascular Disorders, Brain *(type: exact)*
- Vascular Disorders, Intracranial *(type: exact)*

---

### MONDO:0005269 ↔ EFO:0003781

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005269`
- **Mondo Label**: carotid artery disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003781`
- **EFO Label**: carotid artery disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:3407`
- `MESH:D002340`
- `MedDRA:10061744`
- `NCIt:C84476`
- `SNOMEDCT:300920004`

**EFO Synonyms** (to verify in Mondo):

- ARTERIAL DIS CAROTID *(type: exact)*
- ARTERIAL DIS COMMON CAROTID *(type: exact)*
- ARTERIAL DIS EXTERNAL CAROTID *(type: exact)*
- ARTERIAL DIS INTERNAL CAROTID *(type: exact)*
- Arterial Disease, Carotid *(type: exact)*
- Arterial Diseases, Carotid *(type: exact)*
- Arterial Diseases, Common Carotid *(type: exact)*
- Arterial Diseases, External Carotid *(type: exact)*
- Arterial Diseases, Internal Carotid *(type: exact)*
- Artery Disease, Carotid *(type: exact)*
- Artery Diseases, Carotid *(type: exact)*
- Artery Disorder, Carotid *(type: exact)*
- Artery Disorders, Carotid *(type: exact)*
- CAROTID ARTERY DIS *(type: exact)*
- COMMON CAROTID ARTERY DIS *(type: exact)*
- Carotid Arterial Disease *(type: exact)*
- Carotid Arterial Diseases *(type: exact)*
- Carotid Artery Diseases *(type: exact)*
- Carotid Artery Disorder *(type: exact)*
- Carotid Artery Disorders *(type: exact)*
- Common Carotid Artery Diseases *(type: exact)*
- Disorders, Carotid Artery *(type: exact)*
- EXTERNAL CAROTID ARTERY DIS *(type: exact)*
- External Carotid Artery Diseases *(type: exact)*
- INTERNAL CAROTID ARTERY DIS *(type: exact)*
- Internal Carotid Artery Diseases *(type: exact)*
- disorder of carotid artery (disorder) *(type: exact)*

---

### MONDO:0005294 ↔ EFO:0003875

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005294`
- **Mondo Label**: peripheral vascular disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003875`
- **EFO Label**: peripheral vascular disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:341`
- `ICD10:I73`
- `MESH:D016491`
- `MedDRA:10034633`
- `MedDRA:10034635`
- `SNOMEDCT:400047006`

**EFO Synonyms** (to verify in Mondo):

- Angiopathies, Peripheral *(type: exact)*
- Angiopathy, Peripheral *(type: exact)*
- DIS PERIPHERAL VASCULAR *(type: exact)*
- Disease, Peripheral Vascular *(type: exact)*
- Diseases, Peripheral Vascular *(type: exact)*
- PERIPHERAL VASCULAR DIS *(type: exact)*
- Peripheral Angiopathies *(type: exact)*
- Peripheral Angiopathy *(type: exact)*
- Peripheral Vascular Diseases *(type: exact)*
- VASCULAR DIS PERIPHERAL *(type: exact)*
- Vascular Disease, Peripheral *(type: exact)*
- Vascular Diseases, Peripheral *(type: exact)*

---

### MONDO:0005308 ↔ EFO:0003900

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005308`
- **Mondo Label**: ciliopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003900`
- **EFO Label**: ciliopathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:0060340`
- `MESH:D002925`
- `OMIM:244400`
- `SNOMEDCT:86204009`

**EFO Synonyms** (to verify in Mondo):

- CILIARY MOTILITY DIS *(type: exact)*
- Cilia Syndrome, Immotile *(type: exact)*
- Cilia Syndromes, Immotile *(type: exact)*
- Ciliary Dyskinesia *(type: exact)*
- Ciliary Dyskinesias *(type: exact)*
- Ciliary Motility Disorder *(type: exact)*
- Ciliary Motility Disorders *(type: exact)*
- Disorder, Ciliary Motility *(type: exact)*
- Disorders, Ciliary Motility *(type: exact)*
- Dyskinesia, Ciliary *(type: exact)*
- Dyskinesias, Ciliary *(type: exact)*
- Immotile Cilia Syndrome *(type: exact)*
- Immotile Cilia Syndromes *(type: exact)*
- Syndrome, Immotile Cilia *(type: exact)*
- Syndromes, Immotile Cilia *(type: exact)*

---

### MONDO:0005311 ↔ EFO:0003914

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005311`
- **Mondo Label**: atherosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003914`
- **EFO Label**: atherosclerosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:1936`
- `ICD10:I70`
- `ICD9:440`
- `MESH:D050197`
- `MONDO:0005311`
- `MedDRA:10003601`
- `NCIt:C35768`
- `SNOMEDCT:38716007`

**EFO Synonyms** (to verify in Mondo):

- Atherogenesis *(type: exact)*
- Atheroscleroses *(type: exact)*

---

### MONDO:0005381 ↔ EFO:0004260

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005381`
- **Mondo Label**: bone disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004260`
- **EFO Label**: bone disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:0080001`
- `ICD10:M46`
- `ICD10:M48`
- `ICD10:M49`
- `ICD10:M84`
- `ICD10:M89`
- `ICD10:M90`

---

### MONDO:0005384 ↔ EFO:0004263

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005384`
- **Mondo Label**: partial epilepsy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004263`
- **EFO Label**: partial epilepsy

**EFO Xrefs** (to verify in Mondo):

- `DOID:2234`
- `MESH:D004828`
- `MedDRA:10034058`
- `MedDRA:10034059`
- `MedDRA:10034060`
- `MedDRA:10034061`
- `MedDRA:10034062`
- `MedDRA:10034063`
- `MedDRA:10034064`
- `MedDRA:10065336`

**EFO Synonyms** (to verify in Mondo):

- epilepsies, partial *(type: exact)*
- focal epilepsy *(type: exact)*
- partial epilepsies *(type: exact)*

---

### MONDO:0005394 ↔ EFO:0004277

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005394`
- **Mondo Label**: brain infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004277`
- **EFO Label**: brain infarction

**EFO Xrefs** (to verify in Mondo):

- `DOID:3454`
- `ICD10:I63`
- `MESH:D020520`
- `MedDRA:10072154`
- `SNOMEDCT:230693009`
- `SNOMEDCT:230698000`

**EFO Synonyms** (to verify in Mondo):

- ANTERIOR CEREBRAL CIRC INFARCT *(type: exact)*
- ANTERIOR CIRC BRAIN INFARCT *(type: exact)*
- ANTERIOR CIRC INFARCT BRAIN *(type: exact)*
- Anterior Cerebral Circulation Infarction *(type: exact)*
- Anterior Circulation Brain Infarction *(type: exact)*
- Anterior Circulation Infarction, Brain *(type: exact)*
- BRAIN INFARCT *(type: exact)*
- BRAIN INFARCT ANTERIOR CIRC *(type: exact)*
- BRAIN INFARCT POSTERIOR CIRC *(type: exact)*
- BRAIN INFARCT VENOUS *(type: exact)*
- Brain Infarction *(type: exact)*
- Brain Infarction, Anterior Circulation *(type: exact)*
- Brain Infarction, Posterior Circulation *(type: exact)*
- Brain Infarction, Venous *(type: exact)*
- Brain Infarctions *(type: exact)*
- Brain Infarctions, Venous *(type: exact)*
- Brain Venous Infarction *(type: exact)*
- Brain Venous Infarctions *(type: exact)*
- INFARCT ANTERIOR CEREBRAL CIRC *(type: exact)*
- INFARCT ANTERIOR CIRC BRAIN *(type: exact)*
- INFARCT BRAIN ANTERIOR CIRC *(type: exact)*
- INFARCT BRAIN POSTERIOR CIRC *(type: exact)*
- INFARCT LACUNAR *(type: exact)*
- INFARCT POSTERIOR CIRC BRAIN *(type: exact)*
- Infarction, Anterior Cerebral Circulation *(type: exact)*
- Infarction, Anterior Circulation, Brain *(type: exact)*
- Infarction, Brain *(type: exact)*
- Infarction, Brain Venous *(type: exact)*
- Infarction, Brain, Anterior Circulation *(type: exact)*
- Infarction, Brain, Posterior Circulation *(type: exact)*
- Infarction, Lacunar *(type: exact)*
- Infarction, Posterior Circulation, Brain *(type: exact)*
- Infarction, Venous Brain *(type: exact)*
- Infarctions, Brain *(type: exact)*
- Infarctions, Brain Venous *(type: exact)*
- Infarctions, Lacunar *(type: exact)*
- Infarctions, Venous Brain *(type: exact)*
- Lacunar Infarction *(type: exact)*
- Lacunar Infarctions *(type: exact)*
- POSTERIOR CIRC BRAIN INFARCT *(type: exact)*
- POSTERIOR CIRC INFARCT BRAIN *(type: exact)*
- Posterior Circulation Brain Infarction *(type: exact)*
- Posterior Circulation Infarction, Brain *(type: exact)*
- VENOUS INFARCT BRAIN *(type: exact)*
- Venous Brain Infarction *(type: exact)*
- Venous Brain Infarctions *(type: exact)*
- Venous Infarction, Brain *(type: exact)*
- Venous Infarctions, Brain *(type: exact)*

---

### MONDO:0005509 ↔ EFO:0005561

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005509`
- **Mondo Label**: histiocytoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005561`
- **EFO Label**: histiocytoma

**EFO Xrefs** (to verify in Mondo):

- `DOID:4231`
- `EFO:0005561`
- `ICDO:8831/0`
- `MESH:D051642`
- `NCIT:C35765`
- `OMIM:612160`
- `SCTID_2010_1_31:128741006`
- `SCTID_2010_1_31:154614002`
- `SCTID_2010_1_31:189773000`
- `SCTID_2010_1_31:302843004`
- `SCTID_2010_1_31:72079004`
- `UMLS:C1509147`

**EFO Synonyms** (to verify in Mondo):

- histiocytoma *(type: exact)*

---

### MONDO:0005560 ↔ EFO:0005774

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005560`
- **Mondo Label**: brain disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005774`
- **EFO Label**: brain disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:936`
- `ICD10:G93`

---

### MONDO:0005561 ↔ EFO:0005775

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005561`
- **Mondo Label**: aortic disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005775`
- **EFO Label**: aortic disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:520`

---

### MONDO:0005976 ↔ EFO:0007504

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005976`
- **Mondo Label**: syphilis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0007504`
- **EFO Label**: syphilis

**EFO Xrefs** (to verify in Mondo):

- `DOID:4166`
- `ICD10:A51`
- `ICD10:A53`
- `MESH:D013587`
- `MedDRA:10042894`
- `MedDRA:10042895`
- `MedDRA:10042896`
- `MedDRA:10042901`
- `MedDRA:10062120`
- `NCIt:C35055`
- `SNOMEDCT:76272004`

---

### MONDO:0006026 ↔ EFO:1000018

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006026`
- **Mondo Label**: bladder disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000018`
- **EFO Label**: bladder disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:365`
- `ICD10:N32`
- `NCIt:C2900`
- `UMLS:C0005686`

**EFO Synonyms** (to verify in Mondo):

- bladder disorder *(type: exact)*
- urinary bladder disorder *(type: exact)*

---

### MONDO:0006642 ↔ EFO:1000800

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006642`
- **Mondo Label**: alcohol withdrawal delirium
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000800`
- **EFO Label**: alcohol withdrawal delirium

**EFO Xrefs** (to verify in Mondo):

- `DOID:8639`
- `ICD9:291.0`
- `MESH:D000430`
- `MedDRA:10001610`
- `SNOMEDCT:8635005`

**EFO Synonyms** (to verify in Mondo):

- Alcohol Withdrawal Delirium *(type: exact)*
- Alcohol withdrawal delirium (disorder) *(type: exact)*
- Alcoholic delirium *(type: exact)*
- Delirium tremens *(type: exact)*
- Mental and behavioral disorder due to use of alcohol: withdrawal state with delirium (disorder) *(type: exact)*
- delirium tremens *(type: exact)*

---

### MONDO:0006643 ↔ EFO:1000801

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006643`
- **Mondo Label**: alcoholic cardiomyopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000801`
- **EFO Label**: alcoholic cardiomyopathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:12935`
- `ICD10:I42.6`
- `MESH:D002310`
- `MedDRA:10001616`
- `NCIt:C53653`
- `SNOMEDCT:83521008`

**EFO Synonyms** (to verify in Mondo):

- Alcohol-induced heart muscle disease *(type: exact)*
- Alcoholic cardiomyopathy *(type: exact)*
- Cardiomyopathy, Alcoholic *(type: exact)*
- Dilated cardiomyopathy secondary to alcohol (disorder) *(type: exact)*

---

### MONDO:0006645 ↔ EFO:1000803

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006645`
- **Mondo Label**: alcoholic neuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000803`
- **EFO Label**: alcoholic neuropathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:14183`
- `MESH:D020269`

**EFO Synonyms** (to verify in Mondo):

- Alcohol-related polyneuropathy *(type: exact)*
- Alcoholic Neuropathy *(type: exact)*
- Alcoholic polyneuropathy *(type: exact)*

---

### MONDO:0011782 ↔ EFO:1000805

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0011782`
- **Mondo Label**: angioid streaks
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000805`
- **EFO Label**: angioid streaks

**EFO Xrefs** (to verify in Mondo):

- `DOID:13401`
- `MESH:D000793`
- `MedDRA:10066191`
- `SNOMEDCT:86103006`

**EFO Synonyms** (to verify in Mondo):

- Angioid Streaks *(type: exact)*
- Angioid streaks of choroid *(type: exact)*

---

### MONDO:0006647 ↔ EFO:1000807

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006647`
- **Mondo Label**: anterior cerebral artery infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000807`
- **EFO Label**: anterior cerebral artery infarction

**EFO Xrefs** (to verify in Mondo):

- `DOID:3528`
- `MESH:D020243`

**EFO Synonyms** (to verify in Mondo):

- Infarction, Anterior Cerebral Artery *(type: exact)*

---

### MONDO:0006648 ↔ EFO:1000808

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006648`
- **Mondo Label**: anterior compartment syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000808`
- **EFO Label**: anterior compartment syndrome

**EFO Xrefs** (to verify in Mondo):

- `DOID:3933`
- `MESH:D000868`
- `NCIt:C118422`
- `SNOMEDCT:12694001`

**EFO Synonyms** (to verify in Mondo):

- Anterior Compartment Syndrome *(type: exact)*
- Anterior compartment syndrome *(type: exact)*

---

### MONDO:0006650 ↔ EFO:1000810

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006650`
- **Mondo Label**: anterior spinal artery syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000810`
- **EFO Label**: anterior spinal artery syndrome

**EFO Xrefs** (to verify in Mondo):

- `DOID:6712`
- `MESH:D020759`
- `MedDRA:10002703`
- `SNOMEDCT:14363008`

**EFO Synonyms** (to verify in Mondo):

- Anterior Spinal Artery Syndrome *(type: exact)*
- Anterior spinal artery occlusion syndrome (disorder) *(type: exact)*

---

### MONDO:0006652 ↔ EFO:1000812

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006652`
- **Mondo Label**: anterolateral myocardial infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000812`
- **EFO Label**: anterolateral myocardial infarction

**EFO Xrefs** (to verify in Mondo):

- `DOID:5845`
- `MESH:D056988`
- `MedDRA:10068109`

**EFO Synonyms** (to verify in Mondo):

- Anterior Wall Myocardial Infarction *(type: exact)*

---

### MONDO:0006653 ↔ EFO:1000813

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006653`
- **Mondo Label**: anthracosilicosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000813`
- **EFO Label**: anthracosilicosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:10324`
- `MESH:D000874`
- `MedDRA:10050363`
- `NCIt:C34389`
- `SNOMEDCT:33548005`

**EFO Synonyms** (to verify in Mondo):

- Anthracosilicosis *(type: exact)*

---

### MONDO:0006654 ↔ EFO:1000814

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006654`
- **Mondo Label**: anthracosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000814`
- **EFO Label**: anthracosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:10327`
- `ICD10:J60`
- `MESH:D055008`
- `MedDRA:10073051`
- `NCIt:C34390`
- `SNOMEDCT:29422001`

**EFO Synonyms** (to verify in Mondo):

- Anthracosis *(type: exact)*
- Coal Miner&apos;s Pneumoconiosis *(type: exact)*
- Coal workers&apos; lung *(type: exact)*
- Coal workers&apos; pneumoconiosis *(type: exact)*
- Melanoedema *(type: exact)*
- black lung *(type: exact)*

---

### MONDO:0006656 ↔ EFO:1000816

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006656`
- **Mondo Label**: aortitis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000816`
- **EFO Label**: aortitis

**EFO Xrefs** (to verify in Mondo):

- `DOID:519`
- `MESH:D001025`
- `MedDRA:10002921`
- `NCIt:C97085`
- `SNOMEDCT:70933002`

**EFO Synonyms** (to verify in Mondo):

- Aortitis *(type: exact)*
- Aortitis (disorder) *(type: exact)*
- Aortitis NOS *(type: exact)*

---

### MONDO:0006658 ↔ EFO:1000819

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006658`
- **Mondo Label**: arteriolosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000819`
- **EFO Label**: arteriolosclerosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:5162`
- `MESH:D050379`
- `MONDO:0006658`
- `NCIt:C35543`
- `SNOMEDCT:17941002`
- `UMLS:C0878486`

**EFO Synonyms** (to verify in Mondo):

- Arteriolosclerosis *(type: exact)*
- Arteriolosclerosis (morphologic abnormality) *(type: exact)*

---

### MONDO:0006659 ↔ EFO:1000820

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006659`
- **Mondo Label**: arteriosclerosis obliterans
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000820`
- **EFO Label**: arteriosclerosis obliterans

**EFO Xrefs** (to verify in Mondo):

- `DOID:5160`
- `MESH:D001162`
- `MedDRA:10065418`
- `SNOMEDCT:361133006`

**EFO Synonyms** (to verify in Mondo):

- Arteriosclerosis Obliterans *(type: exact)*
- Arteriosclerosis obliterans (disorder) *(type: exact)*
- Arteriosclerosis obliterans (disorder) [Ambiguous] *(type: exact)*

---

### MONDO:0006666 ↔ EFO:1000827

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006666`
- **Mondo Label**: atrophy of thyroid
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000827`
- **EFO Label**: atrophy of thyroid

**EFO Xrefs** (to verify in Mondo):

- `DOID:2853`
- `ICD10:E03.4`
- `MESH:D050033`
- `MedDRA:10043693`

**EFO Synonyms** (to verify in Mondo):

- Hypoplasia of thyroid (disorder) *(type: exact)*
- Hypoplasia of thyroid (disorder) [Ambiguous] *(type: exact)*
- Thyroid Atrophy *(type: exact)*
- Thyroid Dysgenesis *(type: exact)*
- Thyroid atrophy (disorder) *(type: exact)*

---

### MONDO:0020322 ↔ EFO:1000828

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0020322`
- **Mondo Label**: b- and T-cell mixed leukemia
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000828`
- **EFO Label**: B- and T-cell mixed leukemia

**EFO Xrefs** (to verify in Mondo):

- `DOID:9953`
- `EFO:1000828`
- `ICD10:C95.0`
- `ICD9:207.80`
- `ICDO:9805/3`
- `MESH:D015456`
- `MedDRA:10067399`
- `NCIT:C4673`
- `Orphanet:98837`
- `SCTID:278453007`
- `UMLS:C0023464`

**EFO Synonyms** (to verify in Mondo):

- B- and T-cell mixed leukemia *(type: exact)*
- acute biphenotypic leukemia *(type: exact)*

---

### MONDO:0006671 ↔ EFO:1000832

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006671`
- **Mondo Label**: Bacteroides infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000832`
- **EFO Label**: Bacteroides infectious disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:4641`
- `MESH:D001442`

**EFO Synonyms** (to verify in Mondo):

- Bacteroides Infections *(type: exact)*

---

### MONDO:0006676 ↔ EFO:1000837

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006676`
- **Mondo Label**: beriberi
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000837`
- **EFO Label**: beriberi

**EFO Xrefs** (to verify in Mondo):

- `DOID:13725`
- `ICD10:E51.1`
- `MESH:D001602`
- `MedDRA:10004482`
- `SNOMEDCT:36656008`

**EFO Synonyms** (to verify in Mondo):

- Beriberi *(type: exact)*

---

### MONDO:0006677 ↔ EFO:1000838

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006677`
- **Mondo Label**: bile reflux
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000838`
- **EFO Label**: bile reflux

**EFO Xrefs** (to verify in Mondo):

- `DOID:12237`
- `MESH:D001655`

**EFO Synonyms** (to verify in Mondo):

- Bile Reflux *(type: exact)*

---

### MONDO:0006678 ↔ EFO:1000839

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006678`
- **Mondo Label**: bladder calculus
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000839`
- **EFO Label**: bladder calculus

**EFO Xrefs** (to verify in Mondo):

- `DOID:11355`
- `MESH:D001744`
- `MedDRA:10005001`
- `NCIt:C26707`
- `SNOMEDCT:70650003`

**EFO Synonyms** (to verify in Mondo):

- Urinary Bladder Calculi *(type: exact)*
- bladder stone *(type: exact)*
- bladder stones *(type: exact)*
- cystoliths *(type: exact)*
- vesical calculi *(type: exact)*

---

### MONDO:0006680 ↔ EFO:1000841

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006680`
- **Mondo Label**: blue nevus
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000841`
- **EFO Label**: blue nevus

**EFO Xrefs** (to verify in Mondo):

- `EFO:1000841`
- `GARD:0008452`
- `ICDO:8780/0`
- `MESH:D018329`
- `MedDRA:10062788`
- `NCIT:C3803`
- `SCTID:254806009`

**EFO Synonyms** (to verify in Mondo):

- Jadassohn-TiC(che nevus *(type: related)*
- Jadassohn-TiC(che syndrome *(type: related)*
- Jadassohn-Tièche nevus *(type: related)*
- Jadassohn-Tièche syndrome *(type: related)*
- Tièche-Jadassohn nevus *(type: related)*
- benign mesenchymal melanoma *(type: related)*
- blue Nevus of skin *(type: exact)*
- blue Nevus of the skin *(type: exact)*
- blue neuronevus *(type: related)*
- blue nevus *(type: exact)*
- blue skin Nevus *(type: exact)*

---

### MONDO:0006681 ↔ EFO:1000842

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006681`
- **Mondo Label**: Borrelia infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000842`
- **EFO Label**: Borrelia infectious disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:11730`
- `MESH:D001899`
- `MedDRA:10061591`

**EFO Synonyms** (to verify in Mondo):

- Borrelia Infections *(type: exact)*
- Borreliosis (disorder) *(type: exact)*
- Borreliosis, NOS *(type: exact)*
- borreliosis *(type: exact)*

---

### MONDO:0006682 ↔ EFO:1000843

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006682`
- **Mondo Label**: brachial plexus neuritis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000843`
- **EFO Label**: brachial plexus neuritis

**EFO Xrefs** (to verify in Mondo):

- `DOID:3689`
- `MESH:D020968`
- `MedDRA:10073002`
- `NCIt:C84600`

**EFO Synonyms** (to verify in Mondo):

- Brachial Plexus Neuritis *(type: exact)*
- Brachial neuritis *(type: exact)*
- Brachial neuritis (disorder) *(type: exact)*
- Parsonage-Aldren-Turner syndrome *(type: exact)*

---

### MONDO:0006683 ↔ EFO:1000844

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006683`
- **Mondo Label**: brachial plexus neuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000844`
- **EFO Label**: brachial plexus neuropathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:3690`
- `MESH:D020516`

**EFO Synonyms** (to verify in Mondo):

- Brachial Plexus Neuropathies *(type: exact)*
- Brachial plexus disorder *(type: exact)*
- brachial plexopathy *(type: exact)*

---

### MONDO:0006684 ↔ EFO:1000845

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006684`
- **Mondo Label**: brain edema
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000845`
- **EFO Label**: brain edema

**EFO Xrefs** (to verify in Mondo):

- `DOID:4724`
- `MESH:D001929`
- `MedDRA:10006121`

**EFO Synonyms** (to verify in Mondo):

- Brain Edema *(type: exact)*
- intracranial swelling *(type: exact)*
- wet brain *(type: exact)*

---

### MONDO:0006688 ↔ EFO:1000851

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006688`
- **Mondo Label**: byssinosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000851`
- **EFO Label**: byssinosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:10323`
- `ICD10:J66.0`
- `MESH:D002095`
- `MedDRA:10006822`
- `NCIt:C84605`
- `SNOMEDCT:85761009`

**EFO Synonyms** (to verify in Mondo):

- Byssinosis *(type: exact)*
- Byssinosis (disorder) *(type: exact)*
- Flax-dressers&apos; disease *(type: exact)*
- Stripper&apos;s asthma *(type: exact)*
- cotton mill fever *(type: exact)*

---

### MONDO:0006690 ↔ EFO:1000853

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006690`
- **Mondo Label**: carotid artery thrombosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000853`
- **EFO Label**: carotid artery thrombosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:3410`
- `MESH:D002341`
- `MedDRA:10007688`
- `SNOMEDCT:86003009`

**EFO Synonyms** (to verify in Mondo):

- Carotid Artery Thrombosis *(type: exact)*
- Carotid artery thrombosis *(type: exact)*
- Carotid artery thrombosis (disorder) *(type: exact)*

---

### MONDO:0006692 ↔ EFO:1000857

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006692`
- **Mondo Label**: central pontine myelinolysis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000857`
- **EFO Label**: central pontine myelinolysis

**EFO Xrefs** (to verify in Mondo):

- `DOID:636`
- `ICD10:G37.2`
- `MESH:D017590`
- `MedDRA:10007968`
- `NCIt:C84623`
- `SNOMEDCT:6807001`

**EFO Synonyms** (to verify in Mondo):

- Myelinolysis, Central Pontine *(type: exact)*
- central pontine myelinolysis (disorder) *(type: exact)*
- central pontine myelinosis *(type: exact)*

---

### MONDO:0006694 ↔ EFO:1000860

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006694`
- **Mondo Label**: cerebral atherosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000860`
- **EFO Label**: cerebral atherosclerosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:12720`
- `ICD10:I67.2`
- `MESH:D002537`
- `MedDRA:10008095`
- `MedDRA:1008095`
- `NCIt:C34459`
- `SNOMEDCT:55382008`

**EFO Synonyms** (to verify in Mondo):

- Cerebral atherosclerosis *(type: exact)*
- Cerebral atherosclerosis (disorder) *(type: exact)*
- Intracranial Arteriosclerosis *(type: exact)*

---

### MONDO:0021697 ↔ EFO:1000863

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0021697`
- **Mondo Label**: chlamydia infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000863`
- **EFO Label**: Chlamydophila infectious disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:11264`
- `MESH:D023521`

**EFO Synonyms** (to verify in Mondo):

- Chlamydophila Infections *(type: exact)*

---

### MONDO:0006698 ↔ EFO:1000864

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006698`
- **Mondo Label**: cholecystolithiasis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000864`
- **EFO Label**: cholecystolithiasis

**EFO Xrefs** (to verify in Mondo):

- `DOID:11151`
- `MESH:D041761`
- `MedDRA:10049890`

**EFO Synonyms** (to verify in Mondo):

- Cholecystolithiasis *(type: exact)*

---

### MONDO:0006700 ↔ EFO:1000866

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006700`
- **Mondo Label**: choroid cancer
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000866`
- **EFO Label**: choroid cancer

**EFO Xrefs** (to verify in Mondo):

- `DOID:12759`
- `MESH:D002830`
- `MedDRA:10057405`

**EFO Synonyms** (to verify in Mondo):

- malignant tumor of choroid (disorder) *(type: exact)*
- malignant tumor of the Choroid *(type: exact)*

---

### MONDO:0006702 ↔ EFO:1000868

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006702`
- **Mondo Label**: chronic inflammatory demyelinating polyradiculoneuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000868`
- **EFO Label**: chronic inflammatory demyelinating polyradiculoneuropathy

**EFO Xrefs** (to verify in Mondo):

- `DOID:5213`
- `MESH:D020277`
- `MedDRA:10057645`
- `MedDRA:10072650`
- `SNOMEDCT:128209004`

**EFO Synonyms** (to verify in Mondo):

- Polyradiculoneuropathy, Chronic Inflammatory Demyelinating *(type: exact)*
- chronic inflammatory demyelinating polyradiculoneuropathy (disorder) *(type: exact)*

---

### MONDO:0024388 ↔ EFO:1000874

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0024388`
- **Mondo Label**: Clostridium infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000874`
- **EFO Label**: commensal Clostridium infectious disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:3584`
- `MESH:D003015`

**EFO Synonyms** (to verify in Mondo):

- Clostridium Infections *(type: exact)*
- clostridial infection *(type: exact)*

---

### MONDO:0006708 ↔ EFO:1000875

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006708`
- **Mondo Label**: commensal Desulfovibrionaceae infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000875`
- **EFO Label**: commensal Desulfovibrionaceae infectious disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:3636`
- `MESH:D045824`

**EFO Synonyms** (to verify in Mondo):

- Desulfovibrionaceae Infections *(type: exact)*

---

### MONDO:0006710 ↔ EFO:1000877

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006710`
- **Mondo Label**: complex partial epilepsy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000877`
- **EFO Label**: complex partial epilepsy

**EFO Xrefs** (to verify in Mondo):

- `DOID:12382`
- `MESH:D017029`

**EFO Synonyms** (to verify in Mondo):

- Complex partial epileptic seizure *(type: exact)*
- Epilepsy, Complex Partial *(type: exact)*
- Psychomotor epilepsy *(type: exact)*
- Psychomotor epilepsy (disorder) *(type: exact)*
- epilepsy, psychomotor *(type: exact)*
- psychomotor epilepsy *(type: exact)*

---

### MONDO:0006714 ↔ EFO:1000881

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006714`
- **Mondo Label**: coronary aneurysm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000881`
- **EFO Label**: coronary aneurysm

**EFO Xrefs** (to verify in Mondo):

- `DOID:3362`
- `ICD10:I25.4`
- `ICD9:414.11`
- `MESH:D003323`
- `MedDRA:10002348`
- `SNOMEDCT:50570003`

**EFO Synonyms** (to verify in Mondo):

- Aneurysm of coronary vessels *(type: exact)*
- Aneurysmal lesion of coronary artery *(type: exact)*
- Arteriovenous aneurysm of coronary vessels *(type: exact)*
- Coronary Aneurysm *(type: exact)*

---

### MONDO:0006716 ↔ EFO:1000883

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006716`
- **Mondo Label**: coronary thrombosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000883`
- **EFO Label**: coronary thrombosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:11847`
- `MESH:D003328`
- `MedDRA:10011108`
- `SNOMEDCT:398274000`

**EFO Synonyms** (to verify in Mondo):

- Coronary Thrombosis *(type: exact)*
- Coronary artery thrombosis (disorder) *(type: exact)*

---

### MONDO:0006717 ↔ EFO:1000885

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006717`
- **Mondo Label**: cutaneous fibrous histiocytoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000885`
- **EFO Label**: cutaneous fibrous histiocytoma

**EFO Xrefs** (to verify in Mondo):

- `DOID:4418`
- `EFO:1000885`
- `ICDO:8832/0`
- `NCIT:C6801`
- `ONCOTREE:DF`
- `SCTID:448015002`
- `UMLS:C0002991`
- `UMLS:C0346049`

**EFO Synonyms** (to verify in Mondo):

- DF *(type: related)*
- benign cutaneous fibrous histiocytoma *(type: exact)*
- benign fibrous cutaneous histiocytoma *(type: exact)*
- benign fibrous histiocytoma of skin *(type: exact)*
- benign fibrous histiocytoma of the skin *(type: exact)*
- benign skin fibrous histiocytoma *(type: exact)*
- cutaneous fibrous histiocytoma *(type: exact)*
- dermatofibroma *(type: exact)*
- dermatofibroma, no ICD-O subtype *(type: exact)*
- dermatofibroma, no ICD-O subtype (morphologic abnormality) *(type: exact)*
- fibrohistiocytic neoplasm *(type: exact)*
- fibrohistiocytic tumor *(type: exact)*
- fibrous histiocytoma of skin *(type: exact)*
- fibrous histiocytoma of the skin *(type: exact)*
- fibrous xanthoma of skin *(type: exact)*
- pleomorphic fibroma *(type: exact)*
- sclerosing angioma *(type: exact)*
- sclerosing angioma (morphologic abnormality) *(type: exact)*
- sclerosing angioma of skin *(type: exact)*

---

### MONDO:0006720 ↔ EFO:1000889

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006720`
- **Mondo Label**: cystic, mucinous, and serous neoplasm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000889`
- **EFO Label**: cystic, mucinous, and serous neoplasm

**EFO Xrefs** (to verify in Mondo):

- `EFO:1000889`
- `MESH:D018297`

**EFO Synonyms** (to verify in Mondo):

- cystic, mucinous, and serous neoplasm *(type: exact)*

---

### MONDO:0009072 ↔ EFO:1000890

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0009072`
- **Mondo Label**: Dandy-Walker syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000890`
- **EFO Label**: Dandy-Walker syndrome

**EFO Xrefs** (to verify in Mondo):

- `DOID:2785`
- `MESH:D003616`
- `MedDRA:10048411`
- `SNOMEDCT:14447001`

**EFO Synonyms** (to verify in Mondo):

- (Atresia of foramina of Magendie + Luschka) or (Dandy - Walker syndrome) *(type: exact)*
- Atresia of foramina of Magendie and Luschka *(type: exact)*
- Dandy-Walker Syndrome *(type: exact)*
- Dandy-Walker syndrome (disorder) *(type: exact)*

---

### MONDO:0006721 ↔ EFO:1000891

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006721`
- **Mondo Label**: de Quervain disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000891`
- **EFO Label**: De Quervain disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:14107`
- `MESH:D053684`

**EFO Synonyms** (to verify in Mondo):

- De Quervain Disease *(type: exact)*
- Radial styloid tenosynovitis *(type: exact)*
- Tenosynovitis, de Quervain&apos;s *(type: exact)*

---

### MONDO:0019373 ↔ EFO:1000895

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0019373`
- **Mondo Label**: desmoplastic small round cell tumor
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000895`
- **EFO Label**: desmoplastic small round cell tumor

**EFO Xrefs** (to verify in Mondo):

- `EFO:1000895`
- `GARD:0006265`
- `HGNC:12796`
- `ICD10:C48.2`
- `ICDO:8806/3`
- `MESH:D058405`
- `MedDRA:10064581`
- `MedDRA:10064587`
- `NCIT:C8300`
- `ONCOTREE:DSRCT`
- `Orphanet:83469`
- `UMLS:C0281508`

**EFO Synonyms** (to verify in Mondo):

- DSRCT *(type: exact)*
- Desmoplas. small round cell tumor *(type: exact)*
- Desmoplastic small round cell tumor *(type: exact)*
- Desmoplastic small round-cell neoplasm *(type: exact)*
- Desmoplastic small round-cell tumor *(type: exact)*
- Polyphenotypic small round cell tumor *(type: exact)*
- desmoplastic small round cell tumor *(type: exact)*
- desmoplastic small-round-cell tumor *(type: related)*

---

### MONDO:0012819 ↔ EFO:1000897

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0012819`
- **Mondo Label**: diabetic ketoacidosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000897`
- **EFO Label**: diabetic ketoacidosis

**EFO Xrefs** (to verify in Mondo):

- `DOID:1837`
- `MESH:D016883`
- `MedDRA:10012671`
- `MedDRA:10023392`
- `NCIt:C50530`
- `SNOMEDCT:420422005`

**EFO Synonyms** (to verify in Mondo):

- DIABETES MELLITUS, KETOSIS-PRONE *(type: exact)*
- Diabetic Ketoacidosis *(type: exact)*
- ketosis-prone diabetes mellitus *(type: exact)*

---

### MONDO:0006727 ↔ EFO:1000899

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006727`
- **Mondo Label**: diastolic heart failure
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000899`
- **EFO Label**: diastolic heart failure

**EFO Xrefs** (to verify in Mondo):

- `DOID:9775`
- `ICD10:I50.3`
- `ICD9:428.3`
- `MESH:D054144`
- `MedDRA:10069211`
- `SNOMEDCT:418304008`

**EFO Synonyms** (to verify in Mondo):

- Heart Failure, Diastolic *(type: exact)*

---

### MONDO:0006873 ↔ EFO:1001067

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006873`
- **Mondo Label**: nutritional deficiency disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1001067`
- **EFO Label**: nutritional deficiency disease

**EFO Xrefs** (to verify in Mondo):

- `DOID:5113`
- `ICD10:E63`
- `MESH:D003677`
- `MedDRA:10046058`
- `SNOMEDCT:70241007`

---

## Terms Without Additional Metadata

The following EFO terms have no xrefs or synonyms defined:

- MONDO:0004989 ↔ EFO:0000305 (breast carcinoma)
- MONDO:0005039 ↔ EFO:0000512 (reproductive system disease)
- MONDO:0005071 ↔ EFO:0000618 (nervous system disease)
- MONDO:0005154 ↔ EFO:0001421 (liver disease)
- MONDO:0005155 ↔ EFO:0001422 (cirrhosis of liver)
- MONDO:0005267 ↔ EFO:0003777 (heart disease)
- MONDO:0005281 ↔ EFO:0003832 (gallbladder disease)
- MONDO:0005328 ↔ EFO:0003966 (eye disease)
- MONDO:0005401 ↔ EFO:0004288 (colonic neoplasm)
- MONDO:0005559 ↔ EFO:0005772 (neurodegenerative disease)
- MONDO:0006030 ↔ EFO:1000023 (chronic cystitis)
- MONDO:0006373 ↔ EFO:1000478 (Pituitary Gland Adenoma)
- MONDO:0006644 ↔ EFO:1000802 (alcoholic liver cirrhosis)
- MONDO:0006649 ↔ EFO:1000809 (anterior ischemic optic neuropathy)
- MONDO:0006655 ↔ EFO:1000815 (aortic valve prolapse)
- MONDO:0007150 ↔ EFO:1000818 (arcus senilis)
- MONDO:0006672 ↔ EFO:1000833 (balanitis)
- MONDO:0006679 ↔ EFO:1000840 (bladder neck obstruction)
- MONDO:0006686 ↔ EFO:1000847 (brain stem infarction)
- MONDO:0006687 ↔ EFO:1000850 (burning mouth syndrome)
- MONDO:0006693 ↔ EFO:1000859 (cerebral arterial disease)
- MONDO:0006696 ↔ EFO:1000862 (cervix erosion)
- MONDO:0006699 ↔ EFO:1000865 (choledocholithiasis)
- MONDO:0006701 ↔ EFO:1000867 (chromophobe adenoma)
- MONDO:0006704 ↔ EFO:1000870 (CNS demyelinating autoimmune disease)
- MONDO:0006709 ↔ EFO:1000876 (common bile duct neoplasm)
- MONDO:0006712 ↔ EFO:1000879 (corneal edema)
- MONDO:0006713 ↔ EFO:1000880 (corneal neovascularization)
- MONDO:0006718 ↔ EFO:1000887 (cutaneous syphilis)
- MONDO:0009761 ↔ EFO:1000888 (cystic lymphangioma)
- MONDO:0006722 ↔ EFO:1000892 (dental fluorosis)
- MONDO:0006723 ↔ EFO:1000893 (denture stomatitis)
- MONDO:0006999 ↔ EFO:1001216 (tooth disease)

---

*This report was generated as part of the Mondo-EFO mapping migration task (partial work on first 100 terms).*
*Note: This report documents EFO metadata only. Manual verification against Mondo is required.*