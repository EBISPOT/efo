# Mondo-EFO Mapping Analysis Report

This report documents the migration status and metadata comparison for the first 100 EFO disease terms being replaced with their Mondo equivalents.

## Migration Status

✅ **All 100 Mondo terms are imported** in EFO (present in `iri_dependencies/mondo_terms.txt`)

✅ **All 100 EFO terms have been obsoleted** with:
- Label prefixed with `obsolete_`
- `owl:deprecated true`
- `efo:obsoleted_in_version "3.85"`
- `obo:IAO_0100001` (term_replaced_by) pointing to the Mondo IRI
- `efo:reason_for_obsolescence` explaining the migration

## Metadata Comparison Summary

- **Total terms analyzed**: 100
- **Xrefs already in Mondo**: 297
- **Xrefs missing from Mondo**: 248 (across 77 terms)
- **Synonyms already in Mondo**: 152
- **Synonyms missing from Mondo**: 463 (across 69 terms)

## Detailed Analysis

### MONDO:0004960 ↔ EFO:0000203

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004960`
- **Mondo Label**: monoclonal gammopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000203`
- **EFO Label**: monoclonal gammopathy

**Xrefs already in Mondo** (1):

- ✅ `NCIt:C35548`

**Xrefs missing from Mondo** (6):

- ❌ `DOID:7442`
- ❌ `MESH:D008998`
- ❌ `MedDRA:10060880`
- ❌ `SNOMEDCT:277577000`
- ❌ `SNOMEDCT:35601003`
- ❌ `SNOMEDCT:58648008`

**Synonyms missing from Mondo** (11):

- ❌ Benign Monoclonal Gammopathy *(type: exact)*
- ❌ MGUS *(type: exact)*
- ❌ MGUS - Monoclonal gammopathy of uncertain significance *(type: exact)*
- ❌ Monoclonal Gammopathy Of Undetermined Significance (MGUS) *(type: exact)*
- ❌ Monoclonal Gammopathy of Unknown Significance *(type: exact)*
- ❌ Monoclonal gammopathy of uncertain significance *(type: exact)*
- ❌ Monoclonal gammopathy of uncertain significance (disorder) *(type: exact)*
- ❌ Monoclonal gammopathy of undetermined significance *(type: exact)*
- ❌ Monoclonal gammopathy of undetermined significance (morphologic abnormality) *(type: exact)*
- ❌ Paraproteinaemia *(type: exact)*
- ❌ Paraproteinemia *(type: exact)*

---

### MONDO:0004972 ↔ EFO:0000232

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004972`
- **Mondo Label**: adenoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000232`
- **EFO Label**: adenoma

**Xrefs already in Mondo** (7):

- ✅ `DOID:657`
- ✅ `EFO:0000232`
- ✅ `ICDO:8140/0`
- ✅ `MESH:D000236`
- ✅ `NCIT:C2855`
- ✅ `SCTID:443416007`
- ✅ `UMLS:C0001430`

**Synonyms already in Mondo** (6):

- ✅ acinar cell adenoma *(type: exact)*
- ✅ acinar cell adenoma (morphologic abnormality) *(type: exact)*
- ✅ acinic cell adenoma *(type: exact)*
- ✅ adenoma *(type: exact)*
- ✅ adenoma, benign *(type: narrow)*
- ✅ adenomas *(type: exact)*

---

### MONDO:0004989 ↔ EFO:0000305

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004989`
- **Mondo Label**: breast carcinoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000305`
- **EFO Label**: breast carcinoma

**Xrefs missing from Mondo** (7):

- ❌ `DOID:3459`
- ❌ `EFO:0000305`
- ❌ `NCIT:C4872`
- ❌ `OMIM:114480`
- ❌ `OMIM:615554`
- ❌ `SCTID:254838004`
- ❌ `UMLS:C0678222`

**Synonyms missing from Mondo** (9):

- ❌ breast cancer *(type: broad)*
- ❌ breast cancer, NOS *(type: broad)*
- ❌ breast carcinoma *(type: exact)*
- ❌ cancer of breast *(type: broad)*
- ❌ cancer of the breast *(type: broad)*
- ❌ cancer, breast *(type: broad)*
- ❌ carcinoma of breast *(type: exact)*
- ❌ carcinoma of the breast *(type: exact)*
- ❌ mammary carcinoma *(type: exact)*

---

### MONDO:0004994 ↔ EFO:0000318

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004994`
- **Mondo Label**: cardiomyopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000318`
- **EFO Label**: cardiomyopathy

**Xrefs already in Mondo** (6):

- ✅ `DOID:0050700`
- ✅ `ICD9:425`
- ✅ `MESH:D009202`
- ✅ `MedDRA:10007636`
- ✅ `NCIt:C34830`
- ✅ `SNOMEDCT:85898001`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:I42`

**Synonyms already in Mondo** (1):

- ✅ Cardiomyopathies *(type: exact)*

**Synonyms missing from Mondo** (22):

- ❌ CARDIOMYOPATH IN OTH DIS *(type: exact)*
- ❌ CARDIOMYOPATHIES SECOND *(type: exact)*
- ❌ Cardiomyopathies, Primary *(type: exact)*
- ❌ Cardiomyopathies, Secondary *(type: exact)*
- ❌ Cardiomyopathy (disorder) *(type: exact)*
- ❌ Cardiomyopathy NOS *(type: exact)*
- ❌ Cardiomyopathy NOS (disorder) *(type: exact)*
- ❌ Cardiomyopathy in other diseases classified elsewhere *(type: exact)*
- ❌ Cardiomyopathy, NOS *(type: exact)*
- ❌ Cardiomyopathy, Primary *(type: exact)*
- ❌ Cardiomyopathy, Secondary *(type: exact)*
- ❌ Other primary cardiomyopathies *(type: exact)*
- ❌ Other primary cardiomyopathies (disorder) *(type: exact)*
- ❌ Other primary cardiomyopathy NOS *(type: exact)*
- ❌ Other primary cardiomyopathy NOS (disorder) *(type: exact)*
- ❌ PRIM CARDIOMYOPATHY NEC *(type: exact)*
- ❌ Primary Cardiomyopathies *(type: exact)*
- ❌ Primary Cardiomyopathy *(type: exact)*
- ❌ Secondary Cardiomyopathies *(type: exact)*
- ❌ Secondary Cardiomyopathy *(type: exact)*
- ❌ [X]Cardiomyopathy in other diseases classified elsewhere *(type: exact)*
- ❌ [X]Cardiomyopathy in other diseases classified elsewhere (disorder) *(type: exact)*

---

### MONDO:0004995 ↔ EFO:0000319

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0004995`
- **Mondo Label**: cardiovascular disorder
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000319`
- **EFO Label**: cardiovascular disease

**Xrefs already in Mondo** (14):

- ✅ `DOID:1287`
- ✅ `ICD9:423`
- ✅ `ICD9:423.8`
- ✅ `ICD9:424`
- ✅ `ICD9:429`
- ✅ `ICD9:429.2`
- ✅ `ICD9:429.7`
- ✅ `ICD9:429.8`
- ✅ `ICD9:429.81`
- ✅ `ICD9:429.89`
- ✅ `ICD9:459.9`
- ✅ `MESH:D002318`
- ✅ `NCIt:C2931`
- ✅ `SNOMEDCT:49601007`

**Xrefs missing from Mondo** (6):

- ❌ `ICD10:I98`
- ❌ `ICD10:I99`
- ❌ `ICD9:390-459.99`
- ❌ `ICD9:420-429.99`
- ❌ `MedDRA:10007648`
- ❌ `SNOMEDCT:105980002`

**Synonyms already in Mondo** (7):

- ✅ Cardiovascular Disease (CVD) *(type: exact)*
- ✅ Cardiovascular Disorder *(type: exact)*
- ✅ Cardiovascular system disease *(type: exact)*
- ✅ Disease of cardiovascular system *(type: exact)*
- ✅ Disorder of cardiovascular system *(type: exact)*
- ✅ circulatory system disease *(type: exact)*
- ✅ disease of subdivision of hemolymphoid system *(type: exact)*

**Synonyms missing from Mondo** (61):

- ❌ ASCVD *(type: exact)*
- ❌ CARDIOVASC DIS *(type: exact)*
- ❌ CIRCULATORY DISEASE NOS *(type: exact)*
- ❌ CVD *(type: exact)*
- ❌ CVD, NOS *(type: exact)*
- ❌ CVS disease *(type: exact)*
- ❌ Cardiovascular Diseases *(type: exact)*
- ❌ Cardiovascular Disorders *(type: exact)*
- ❌ Cardiovascular disease, NOS *(type: exact)*
- ❌ Cardiovascular disease, unspecified *(type: exact)*
- ❌ Cardiovascular disorder, NOS *(type: exact)*
- ❌ Certain sequelae of myocardial infarction, not elsewhere classified *(type: exact)*
- ❌ Circulatory system disease NOS *(type: exact)*
- ❌ Circulatory system disease NOS (disorder) *(type: exact)*
- ❌ DISEASES OF THE CIRCULATORY SYSTEM *(type: exact)*
- ❌ Disease affecting entire cardiovascular system *(type: exact)*
- ❌ Disease affecting entire cardiovascular system (disorder) *(type: exact)*
- ❌ Disease of cardiovascular system (disorder) *(type: exact)*
- ❌ Disease of cardiovascular system, NOS *(type: exact)*
- ❌ Disease, Cardiovascular *(type: exact)*
- ❌ Diseases, Cardiovascular *(type: exact)*
- ❌ Disorder of cardiovascular system (disorder) *(type: exact)*
- ❌ Disorder of circulatory system *(type: exact)*
- ❌ Disorder of circulatory system, NOS *(type: exact)*
- ❌ Disorder of the circulatory system *(type: exact)*
- ❌ ILL-DEFINED HRT DIS NEC *(type: exact)*
- ❌ Ill-defined descriptions and complications of heart disease *(type: exact)*
- ❌ OTHER SEQUELAE OF MI NEC *(type: exact)*
- ❌ Other diseases of endocardium *(type: exact)*
- ❌ Other diseases of endocardium (disorder) *(type: exact)*
- ❌ Other diseases of pericardium *(type: exact)*
- ❌ Other diseases of pericardium (disorder) *(type: exact)*
- ❌ Other disorders of papillary muscle *(type: exact)*
- ❌ Other forms of heart disease *(type: exact)*
- ❌ Other forms of heart disease (disorder) *(type: exact)*
- ❌ Other heart disease *(type: exact)*
- ❌ Other heart disease (disorder) *(type: exact)*
- ❌ Other heart disease NOS *(type: exact)*
- ❌ Other heart disease NOS (disorder) *(type: exact)*
- ❌ Other ill-defined heart disease *(type: exact)*
- ❌ Other ill-defined heart disease (disorder) *(type: exact)*
- ❌ Other ill-defined heart disease NOS *(type: exact)*
- ❌ Other ill-defined heart disease NOS (disorder) *(type: exact)*
- ❌ Other ill-defined heart diseases *(type: exact)*
- ❌ Other pericardial disease NOS *(type: exact)*
- ❌ Other pericardial disease NOS (disorder) *(type: exact)*
- ❌ Other sequelae of myocardial infarction, not elsewhere classified *(type: exact)*
- ❌ Other specified diseases of pericardium *(type: exact)*
- ❌ Other specified pericardial disease NOS *(type: exact)*
- ❌ Other specified pericardial disease NOS (disorder) *(type: exact)*
- ❌ PAPILLARY MUSCLE DIS NEC *(type: exact)*
- ❌ PERICARDIAL DISEASE NEC *(type: exact)*
- ❌ Unspecified circulatory system disorder *(type: exact)*
- ❌ [X]Cardiovascular disease, unspecified *(type: exact)*
- ❌ [X]Cardiovascular disease, unspecified (disorder) *(type: exact)*
- ❌ [X]Other forms of heart disease *(type: exact)*
- ❌ [X]Other forms of heart disease (disorder) *(type: exact)*
- ❌ [X]Other ill-defined heart diseases *(type: exact)*
- ❌ [X]Other ill-defined heart diseases (disorder) *(type: exact)*
- ❌ [X]Other specified diseases of pericardium *(type: exact)*
- ❌ [X]Other specified diseases of pericardium (disorder) *(type: exact)*

---

### MONDO:0005009 ↔ EFO:0000373

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005009`
- **Mondo Label**: congestive heart failure
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000373`
- **EFO Label**: congestive heart failure

**Xrefs already in Mondo** (4):

- ✅ `DOID:6000`
- ✅ `ICD9:428.0`
- ✅ `NCIt:C3080`
- ✅ `SNOMEDCT:42343007`

**Xrefs missing from Mondo** (1):

- ❌ `MedDRA:10010684`

**Synonyms already in Mondo** (4):

- ✅ CHF *(type: exact)*
- ✅ Congestive heart disease *(type: exact)*
- ✅ FAILURE, CONGESTIVE HEART *(type: exact)*
- ✅ Heart Failure, Congestive *(type: exact)*

**Synonyms missing from Mondo** (12):

- ❌ CCF - Congestive cardiac failure *(type: exact)*
- ❌ CHF - Congestive heart failure *(type: exact)*
- ❌ CHF NOS *(type: exact)*
- ❌ Cardiac Failure *(type: exact)*
- ❌ Cardiac Failure Congestive *(type: exact)*
- ❌ Congestive cardiac failure *(type: exact)*
- ❌ Congestive heart failure (disorder) *(type: exact)*
- ❌ Congestive heart failure, unspecified *(type: exact)*
- ❌ Congetive cardiac failure *(type: exact)*
- ❌ Decompensation, Heart *(type: exact)*
- ❌ Heart Decompensation *(type: exact)*
- ❌ Myocardial Failure *(type: exact)*

---

### MONDO:0005039 ↔ EFO:0000512

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005039`
- **Mondo Label**: reproductive system disorder
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000512`
- **EFO Label**: reproductive system disease

**Xrefs already in Mondo** (3):

- ✅ `DOID:15`
- ✅ `SNOMEDCT:362968007`
- ✅ `Wikipedia:Reproductive_system_disease`

**Synonyms already in Mondo** (2):

- ✅ Disorder of reproductive system *(type: exact)*
- ✅ genital system disease *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Disorder of reproductive system (disorder) *(type: exact)*
- ❌ Non-neoplastic Reproductive system disease *(type: exact)*

---

### MONDO:0005065 ↔ EFO:0000588

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005065`
- **Mondo Label**: mesothelioma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000588`
- **EFO Label**: mesothelioma

**Xrefs already in Mondo** (4):

- ✅ `EFO:0000588`
- ✅ `MESH:D008654`
- ✅ `NCIT:C3234`
- ✅ `UMLS:C0025500`

**Xrefs missing from Mondo** (2):

- ❌ `ICD10:C45`
- ❌ `OMIM:156240`

**Synonyms already in Mondo** (1):

- ✅ mesothelioma *(type: exact)*

---

### MONDO:0005071 ↔ EFO:0000618

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005071`
- **Mondo Label**: nervous system disorder
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000618`
- **EFO Label**: nervous system disease

*No xrefs or synonyms in EFO term.*

---

### MONDO:0005089 ↔ EFO:0000691

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005089`
- **Mondo Label**: sarcoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000691`
- **EFO Label**: sarcoma

**Xrefs already in Mondo** (16):

- ✅ `DOID:1115`
- ✅ `EFO:0000691`
- ✅ `ICD9:171`
- ✅ `ICD9:171.0`
- ✅ `ICD9:171.2`
- ✅ `ICD9:171.3`
- ✅ `ICD9:171.4`
- ✅ `ICD9:171.5`
- ✅ `ICD9:171.6`
- ✅ `ICD9:171.7`
- ✅ `ICD9:171.8`
- ✅ `ICD9:171.9`
- ✅ `ICDO:8800/3`
- ✅ `MESH:D012509`
- ✅ `NCIT:C9118`
- ✅ `SCTID:424413001`

**Xrefs missing from Mondo** (2):

- ❌ `GARD:0012018`
- ❌ `ICD10:C49`

**Synonyms already in Mondo** (6):

- ✅ mesenchymal tumor, malignant *(type: exact)*
- ✅ sarcoma *(type: exact)*
- ✅ sarcoma of soft tissue and bone *(type: exact)*
- ✅ sarcoma of the soft tissue and bone *(type: exact)*
- ✅ sarcoma, malignant *(type: exact)*
- ✅ tumor of soft tissue and skeleton *(type: exact)*

---

### MONDO:0005093 ↔ EFO:0000701

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005093`
- **Mondo Label**: skin disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0000701`
- **EFO Label**: skin disease

**Xrefs missing from Mondo** (8):

- ❌ `DOID:37`
- ❌ `ICD10:L08`
- ❌ `ICD10:L30`
- ❌ `ICD10:L53`
- ❌ `ICD10:L91`
- ❌ `ICD10:L98`
- ❌ `ICD10:R21`
- ❌ `NCIt:C3371`

**Synonyms missing from Mondo** (4):

- ❌ Cutaneous Disorder *(type: exact)*
- ❌ SKIN AND SUBCUTANEOUS TISSUE DISORDERS *(type: exact)*
- ❌ Skin Diseases and Manifestations *(type: exact)*
- ❌ Skin Disorder *(type: exact)*

---

### MONDO:0005154 ↔ EFO:0001421

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005154`
- **Mondo Label**: liver disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0001421`
- **EFO Label**: liver disease

**Xrefs missing from Mondo** (10):

- ❌ `DOID:409`
- ❌ `ICD10:K75`
- ❌ `ICD10:K76`
- ❌ `ICD9:573.9`
- ❌ `MESH:D008107`
- ❌ `NCIt:C3196`
- ❌ `NCIt:C50634`
- ❌ `SNOMEDCT:15230009`
- ❌ `SNOMEDCT:199117000`
- ❌ `SNOMEDCT:235856003`

**Synonyms missing from Mondo** (32):

- ❌ Disease of liver *(type: exact)*
- ❌ Disease, Liver *(type: exact)*
- ❌ Diseases, Liver *(type: exact)*
- ❌ Disorder of liver *(type: exact)*
- ❌ Dysfunction, Liver *(type: exact)*
- ❌ Dysfunctions, Liver *(type: exact)*
- ❌ Hepatopathy *(type: exact)*
- ❌ LD - Liver disease *(type: exact)*
- ❌ LIVER DIS *(type: exact)*
- ❌ Liver Diseases *(type: exact)*
- ❌ Liver Disorder *(type: exact)*
- ❌ Liver Dysfunction *(type: exact)*
- ❌ Liver Dysfunctions *(type: exact)*
- ❌ Liver and Intrahepatic Bile Duct Disorder *(type: exact)*
- ❌ Liver disorder NOS *(type: exact)*
- ❌ Liver disorder NOS (disorder) *(type: exact)*
- ❌ Liver disorder in pregnancy *(type: exact)*
- ❌ Liver disorder in pregnancy (disorder) *(type: exact)*
- ❌ Liver disorder in pregnancy - delivered (disorder) *(type: exact)*
- ❌ Liver disorder in pregnancy NOS (disorder) *(type: exact)*
- ❌ Liver disorder in pregnancy unspecified (disorder) *(type: exact)*
- ❌ Liver disorder in pregnancy, unspecified as to episode of care *(type: exact)*
- ❌ Liver disorder in pregnancy, with delivery *(type: exact)*
- ❌ Unspecified disorder of liver *(type: exact)*
- ❌ [X]Diseases of the liver *(type: exact)*
- ❌ [X]Diseases of the liver (disorder) *(type: exact)*
- ❌ disease of liver [Ambiguous] *(type: exact)*
- ❌ disease of the liver (disorder) *(type: exact)*
- ❌ disorder of liver (disorder) *(type: exact)*
- ❌ hepatic disorder *(type: exact)*
- ❌ liver disorder antepartum *(type: exact)*
- ❌ liver disorder in pregnancy - delivered *(type: exact)*

---

### MONDO:0005155 ↔ EFO:0001422

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005155`
- **Mondo Label**: cirrhosis of liver
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0001422`
- **EFO Label**: cirrhosis of liver

*No xrefs or synonyms in EFO term.*

---

### MONDO:0005010 ↔ EFO:0001645

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005010`
- **Mondo Label**: coronary artery disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0001645`
- **EFO Label**: coronary artery disease

**Xrefs missing from Mondo** (15):

- ❌ `DOID:3393`
- ❌ `ICD10:I25`
- ❌ `ICD9:410-414.99`
- ❌ `ICD9:414.0`
- ❌ `MedDRA:10011078`
- ❌ `NCIt:C26732`
- ❌ `NCIt:C50625`
- ❌ `OMIM:608320`
- ❌ `OMIM:608901`
- ❌ `OMIM:610938`
- ❌ `OMIM:614466`
- ❌ `OMIM:617347`
- ❌ `SNOMEDCT:414545008`
- ❌ `SNOMEDCT:443502000`
- ❌ `SNOMEDCT:53741008`

**Synonyms missing from Mondo** (31):

- ❌ Arterioscleroses, Coronary *(type: exact)*
- ❌ Arteriosclerosis, Coronary *(type: exact)*
- ❌ Artery Disease, Coronary *(type: exact)*
- ❌ Artery Diseases, Coronary *(type: exact)*
- ❌ Atheroscleroses, Coronary *(type: exact)*
- ❌ Atherosclerosis, Coronary *(type: exact)*
- ❌ CAD *(type: exact)*
- ❌ CHD *(type: exact)*
- ❌ CHD (coronary heart disease) *(type: exact)*
- ❌ CHD - Coronary heart disease *(type: exact)*
- ❌ CORONARY ARTERY DIS *(type: exact)*
- ❌ CORONARY DIS *(type: exact)*
- ❌ CORONARY HEART DIS *(type: exact)*
- ❌ Coronary Arterioscleroses *(type: exact)*
- ❌ Coronary Arteriosclerosis *(type: exact)*
- ❌ Coronary Artery Disease *(type: exact)*
- ❌ Coronary Artery Diseases *(type: exact)*
- ❌ Coronary Atheroscleroses *(type: exact)*
- ❌ Coronary Atherosclerosis *(type: exact)*
- ❌ Coronary Disease *(type: exact)*
- ❌ Coronary Diseases *(type: exact)*
- ❌ Coronary Heart Diseases *(type: exact)*
- ❌ Disease, Coronary *(type: exact)*
- ❌ Disease, Coronary Artery *(type: exact)*
- ❌ Disease, Coronary Heart *(type: exact)*
- ❌ Diseases, Coronary *(type: exact)*
- ❌ Diseases, Coronary Artery *(type: exact)*
- ❌ Diseases, Coronary Heart *(type: exact)*
- ❌ Heart Disease, Coronary *(type: exact)*
- ❌ Heart Diseases, Coronary *(type: exact)*
- ❌ coronary heart disease *(type: exact)*

---

### MONDO:0011057 ↔ EFO:0003763

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0011057`
- **Mondo Label**: cerebrovascular disorder
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003763`
- **EFO Label**: cerebrovascular disorder

**Xrefs already in Mondo** (4):

- ✅ `DOID:6713`
- ✅ `MESH:D002561`
- ✅ `NCIt:C2938`
- ✅ `SNOMEDCT:62914000`

**Xrefs missing from Mondo** (6):

- ❌ `ICD10:I66`
- ❌ `ICD10:I67`
- ❌ `ICD10:I69`
- ❌ `ICD9:430-438.99`
- ❌ `MedDRA:10008196`
- ❌ `MedDRA:10008200`

**Synonyms already in Mondo** (1):

- ✅ Cerebrovascular Disease *(type: exact)*

**Synonyms missing from Mondo** (25):

- ❌ BRAIN VASCULAR DIS *(type: exact)*
- ❌ Brain Vascular Disorder *(type: exact)*
- ❌ Brain Vascular Disorders *(type: exact)*
- ❌ CEREBROVASCULAR DIS *(type: exact)*
- ❌ Cerebrovascular Disorders *(type: exact)*
- ❌ Cerebrovascular Insufficiencies *(type: exact)*
- ❌ Cerebrovascular Insufficiency *(type: exact)*
- ❌ Cerebrovascular Occlusion *(type: exact)*
- ❌ Cerebrovascular Occlusions *(type: exact)*
- ❌ INTRACRANIAL VASCULAR DIS *(type: exact)*
- ❌ Insufficiencies, Cerebrovascular *(type: exact)*
- ❌ Insufficiency, Cerebrovascular *(type: exact)*
- ❌ Intracranial Vascular Disease *(type: exact)*
- ❌ Intracranial Vascular Diseases *(type: exact)*
- ❌ Intracranial Vascular Disorder *(type: exact)*
- ❌ Intracranial Vascular Disorders *(type: exact)*
- ❌ Occlusion, Cerebrovascular *(type: exact)*
- ❌ Occlusions, Cerebrovascular *(type: exact)*
- ❌ VASCULAR DIS INTRACRANIAL *(type: exact)*
- ❌ Vascular Disease, Intracranial *(type: exact)*
- ❌ Vascular Diseases, Intracranial *(type: exact)*
- ❌ Vascular Disorder, Brain *(type: exact)*
- ❌ Vascular Disorder, Intracranial *(type: exact)*
- ❌ Vascular Disorders, Brain *(type: exact)*
- ❌ Vascular Disorders, Intracranial *(type: exact)*

---

### MONDO:0005267 ↔ EFO:0003777

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005267`
- **Mondo Label**: heart disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003777`
- **EFO Label**: heart disease

**Xrefs missing from Mondo** (6):

- ❌ `DOID:114`
- ❌ `ICD10:I24`
- ❌ `ICD10:I51`
- ❌ `MESH:D006331`
- ❌ `MedDRA:10019276`
- ❌ `SNOMEDCT:56265001`

**Synonyms missing from Mondo** (9):

- ❌ CARDIAC DIS *(type: exact)*
- ❌ Cardiac Disease *(type: exact)*
- ❌ Cardiac Diseases *(type: exact)*
- ❌ Disease, Cardiac *(type: exact)*
- ❌ Disease, Heart *(type: exact)*
- ❌ Diseases, Cardiac *(type: exact)*
- ❌ Diseases, Heart *(type: exact)*
- ❌ HEART DIS *(type: exact)*
- ❌ Heart Diseases *(type: exact)*

---

### MONDO:0005269 ↔ EFO:0003781

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005269`
- **Mondo Label**: carotid artery disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003781`
- **EFO Label**: carotid artery disease

**Xrefs missing from Mondo** (5):

- ❌ `DOID:3407`
- ❌ `MESH:D002340`
- ❌ `MedDRA:10061744`
- ❌ `NCIt:C84476`
- ❌ `SNOMEDCT:300920004`

**Synonyms missing from Mondo** (27):

- ❌ ARTERIAL DIS CAROTID *(type: exact)*
- ❌ ARTERIAL DIS COMMON CAROTID *(type: exact)*
- ❌ ARTERIAL DIS EXTERNAL CAROTID *(type: exact)*
- ❌ ARTERIAL DIS INTERNAL CAROTID *(type: exact)*
- ❌ Arterial Disease, Carotid *(type: exact)*
- ❌ Arterial Diseases, Carotid *(type: exact)*
- ❌ Arterial Diseases, Common Carotid *(type: exact)*
- ❌ Arterial Diseases, External Carotid *(type: exact)*
- ❌ Arterial Diseases, Internal Carotid *(type: exact)*
- ❌ Artery Disease, Carotid *(type: exact)*
- ❌ Artery Diseases, Carotid *(type: exact)*
- ❌ Artery Disorder, Carotid *(type: exact)*
- ❌ Artery Disorders, Carotid *(type: exact)*
- ❌ CAROTID ARTERY DIS *(type: exact)*
- ❌ COMMON CAROTID ARTERY DIS *(type: exact)*
- ❌ Carotid Arterial Disease *(type: exact)*
- ❌ Carotid Arterial Diseases *(type: exact)*
- ❌ Carotid Artery Diseases *(type: exact)*
- ❌ Carotid Artery Disorder *(type: exact)*
- ❌ Carotid Artery Disorders *(type: exact)*
- ❌ Common Carotid Artery Diseases *(type: exact)*
- ❌ Disorders, Carotid Artery *(type: exact)*
- ❌ EXTERNAL CAROTID ARTERY DIS *(type: exact)*
- ❌ External Carotid Artery Diseases *(type: exact)*
- ❌ INTERNAL CAROTID ARTERY DIS *(type: exact)*
- ❌ Internal Carotid Artery Diseases *(type: exact)*
- ❌ disorder of carotid artery (disorder) *(type: exact)*

---

### MONDO:0005281 ↔ EFO:0003832

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005281`
- **Mondo Label**: gallbladder disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003832`
- **EFO Label**: gallbladder disease

**Xrefs missing from Mondo** (5):

- ❌ `DOID:0060262`
- ❌ `ICD10:K82`
- ❌ `MESH:D005705`
- ❌ `MedDRA:10017641`
- ❌ `OMIM:609919`

**Synonyms missing from Mondo** (12):

- ❌ Bladder Disease, Gall *(type: exact)*
- ❌ Bladder Diseases, Gall *(type: exact)*
- ❌ Disease, Gall Bladder *(type: exact)*
- ❌ Disease, Gallbladder *(type: exact)*
- ❌ Diseases, Gall Bladder *(type: exact)*
- ❌ Diseases, Gallbladder *(type: exact)*
- ❌ GALL BLADDER DIS *(type: exact)*
- ❌ GALLBLADDER DIS *(type: exact)*
- ❌ Gall Bladder Diseases *(type: exact)*
- ❌ Gallbladder Disease *(type: exact)*
- ❌ Gallbladder Diseases *(type: exact)*
- ❌ gall bladder disease *(type: exact)*

---

### MONDO:0005294 ↔ EFO:0003875

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005294`
- **Mondo Label**: peripheral vascular disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003875`
- **EFO Label**: peripheral vascular disease

**Xrefs already in Mondo** (2):

- ✅ `DOID:341`
- ✅ `MESH:D016491`

**Xrefs missing from Mondo** (4):

- ❌ `ICD10:I73`
- ❌ `MedDRA:10034633`
- ❌ `MedDRA:10034635`
- ❌ `SNOMEDCT:400047006`

**Synonyms already in Mondo** (2):

- ✅ Disease, Peripheral Vascular *(type: exact)*
- ✅ Vascular Disease, Peripheral *(type: exact)*

**Synonyms missing from Mondo** (10):

- ❌ Angiopathies, Peripheral *(type: exact)*
- ❌ Angiopathy, Peripheral *(type: exact)*
- ❌ DIS PERIPHERAL VASCULAR *(type: exact)*
- ❌ Diseases, Peripheral Vascular *(type: exact)*
- ❌ PERIPHERAL VASCULAR DIS *(type: exact)*
- ❌ Peripheral Angiopathies *(type: exact)*
- ❌ Peripheral Angiopathy *(type: exact)*
- ❌ Peripheral Vascular Diseases *(type: exact)*
- ❌ VASCULAR DIS PERIPHERAL *(type: exact)*
- ❌ Vascular Diseases, Peripheral *(type: exact)*

---

### MONDO:0005308 ↔ EFO:0003900

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005308`
- **Mondo Label**: ciliopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003900`
- **EFO Label**: ciliopathy

**Xrefs missing from Mondo** (4):

- ❌ `DOID:0060340`
- ❌ `MESH:D002925`
- ❌ `OMIM:244400`
- ❌ `SNOMEDCT:86204009`

**Synonyms missing from Mondo** (15):

- ❌ CILIARY MOTILITY DIS *(type: exact)*
- ❌ Cilia Syndrome, Immotile *(type: exact)*
- ❌ Cilia Syndromes, Immotile *(type: exact)*
- ❌ Ciliary Dyskinesia *(type: exact)*
- ❌ Ciliary Dyskinesias *(type: exact)*
- ❌ Ciliary Motility Disorder *(type: exact)*
- ❌ Ciliary Motility Disorders *(type: exact)*
- ❌ Disorder, Ciliary Motility *(type: exact)*
- ❌ Disorders, Ciliary Motility *(type: exact)*
- ❌ Dyskinesia, Ciliary *(type: exact)*
- ❌ Dyskinesias, Ciliary *(type: exact)*
- ❌ Immotile Cilia Syndrome *(type: exact)*
- ❌ Immotile Cilia Syndromes *(type: exact)*
- ❌ Syndrome, Immotile Cilia *(type: exact)*
- ❌ Syndromes, Immotile Cilia *(type: exact)*

---

### MONDO:0005311 ↔ EFO:0003914

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005311`
- **Mondo Label**: atherosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003914`
- **EFO Label**: atherosclerosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:1936`
- ✅ `ICD9:440`
- ✅ `MESH:D050197`
- ✅ `NCIt:C35768`

**Xrefs missing from Mondo** (4):

- ❌ `ICD10:I70`
- ❌ `MONDO:0005311`
- ❌ `MedDRA:10003601`
- ❌ `SNOMEDCT:38716007`

**Synonyms missing from Mondo** (2):

- ❌ Atherogenesis *(type: exact)*
- ❌ Atheroscleroses *(type: exact)*

---

### MONDO:0005328 ↔ EFO:0003966

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005328`
- **Mondo Label**: eye disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0003966`
- **EFO Label**: eye disease

**Xrefs missing from Mondo** (6):

- ❌ `DOID:5614`
- ❌ `ICD10:H44`
- ❌ `MESH:D005128`
- ❌ `NCIt:C26767`
- ❌ `UMLS:C0015397`
- ❌ `Wikipedia:Eye_disease`

**Synonyms missing from Mondo** (1):

- ❌ eye disorder *(type: exact)*

---

### MONDO:0005381 ↔ EFO:0004260

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005381`
- **Mondo Label**: bone disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004260`
- **EFO Label**: bone disease

**Xrefs missing from Mondo** (7):

- ❌ `DOID:0080001`
- ❌ `ICD10:M46`
- ❌ `ICD10:M48`
- ❌ `ICD10:M49`
- ❌ `ICD10:M84`
- ❌ `ICD10:M89`
- ❌ `ICD10:M90`

---

### MONDO:0005384 ↔ EFO:0004263

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005384`
- **Mondo Label**: focal epilepsy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004263`
- **EFO Label**: partial epilepsy

**Xrefs already in Mondo** (2):

- ✅ `DOID:2234`
- ✅ `MESH:D004828`

**Xrefs missing from Mondo** (8):

- ❌ `MedDRA:10034058`
- ❌ `MedDRA:10034059`
- ❌ `MedDRA:10034060`
- ❌ `MedDRA:10034061`
- ❌ `MedDRA:10034062`
- ❌ `MedDRA:10034063`
- ❌ `MedDRA:10034064`
- ❌ `MedDRA:10065336`

**Synonyms already in Mondo** (1):

- ✅ focal epilepsy *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ epilepsies, partial *(type: exact)*
- ❌ partial epilepsies *(type: exact)*

---

### MONDO:0005394 ↔ EFO:0004277

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005394`
- **Mondo Label**: brain infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004277`
- **EFO Label**: brain infarction

**Xrefs already in Mondo** (2):

- ✅ `DOID:3454`
- ✅ `MESH:D020520`

**Xrefs missing from Mondo** (4):

- ❌ `ICD10:I63`
- ❌ `MedDRA:10072154`
- ❌ `SNOMEDCT:230693009`
- ❌ `SNOMEDCT:230698000`

**Synonyms already in Mondo** (1):

- ✅ Brain Infarction *(type: exact)*

**Synonyms missing from Mondo** (47):

- ❌ ANTERIOR CEREBRAL CIRC INFARCT *(type: exact)*
- ❌ ANTERIOR CIRC BRAIN INFARCT *(type: exact)*
- ❌ ANTERIOR CIRC INFARCT BRAIN *(type: exact)*
- ❌ Anterior Cerebral Circulation Infarction *(type: exact)*
- ❌ Anterior Circulation Brain Infarction *(type: exact)*
- ❌ Anterior Circulation Infarction, Brain *(type: exact)*
- ❌ BRAIN INFARCT *(type: exact)*
- ❌ BRAIN INFARCT ANTERIOR CIRC *(type: exact)*
- ❌ BRAIN INFARCT POSTERIOR CIRC *(type: exact)*
- ❌ BRAIN INFARCT VENOUS *(type: exact)*
- ❌ Brain Infarction, Anterior Circulation *(type: exact)*
- ❌ Brain Infarction, Posterior Circulation *(type: exact)*
- ❌ Brain Infarction, Venous *(type: exact)*
- ❌ Brain Infarctions *(type: exact)*
- ❌ Brain Infarctions, Venous *(type: exact)*
- ❌ Brain Venous Infarction *(type: exact)*
- ❌ Brain Venous Infarctions *(type: exact)*
- ❌ INFARCT ANTERIOR CEREBRAL CIRC *(type: exact)*
- ❌ INFARCT ANTERIOR CIRC BRAIN *(type: exact)*
- ❌ INFARCT BRAIN ANTERIOR CIRC *(type: exact)*
- ❌ INFARCT BRAIN POSTERIOR CIRC *(type: exact)*
- ❌ INFARCT LACUNAR *(type: exact)*
- ❌ INFARCT POSTERIOR CIRC BRAIN *(type: exact)*
- ❌ Infarction, Anterior Cerebral Circulation *(type: exact)*
- ❌ Infarction, Anterior Circulation, Brain *(type: exact)*
- ❌ Infarction, Brain *(type: exact)*
- ❌ Infarction, Brain Venous *(type: exact)*
- ❌ Infarction, Brain, Anterior Circulation *(type: exact)*
- ❌ Infarction, Brain, Posterior Circulation *(type: exact)*
- ❌ Infarction, Lacunar *(type: exact)*
- ❌ Infarction, Posterior Circulation, Brain *(type: exact)*
- ❌ Infarction, Venous Brain *(type: exact)*
- ❌ Infarctions, Brain *(type: exact)*
- ❌ Infarctions, Brain Venous *(type: exact)*
- ❌ Infarctions, Lacunar *(type: exact)*
- ❌ Infarctions, Venous Brain *(type: exact)*
- ❌ Lacunar Infarction *(type: exact)*
- ❌ Lacunar Infarctions *(type: exact)*
- ❌ POSTERIOR CIRC BRAIN INFARCT *(type: exact)*
- ❌ POSTERIOR CIRC INFARCT BRAIN *(type: exact)*
- ❌ Posterior Circulation Brain Infarction *(type: exact)*
- ❌ Posterior Circulation Infarction, Brain *(type: exact)*
- ❌ VENOUS INFARCT BRAIN *(type: exact)*
- ❌ Venous Brain Infarction *(type: exact)*
- ❌ Venous Brain Infarctions *(type: exact)*
- ❌ Venous Infarction, Brain *(type: exact)*
- ❌ Venous Infarctions, Brain *(type: exact)*

---

### MONDO:0005401 ↔ EFO:0004288

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005401`
- **Mondo Label**: colonic neoplasm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0004288`
- **EFO Label**: colonic neoplasm

**Xrefs missing from Mondo** (4):

- ❌ `EFO:0004288`
- ❌ `MESH:D003110`
- ❌ `NCIT:C2953`
- ❌ `UMLS:C0009375`

**Synonyms missing from Mondo** (9):

- ❌ colon neoplasm *(type: exact)*
- ❌ colon neoplasm (disease) *(type: exact)*
- ❌ colon tumor *(type: exact)*
- ❌ colonic neoplasm *(type: exact)*
- ❌ colonic tumor *(type: exact)*
- ❌ neoplasm of colon *(type: exact)*
- ❌ neoplasm of the colon *(type: exact)*
- ❌ tumor of colon *(type: exact)*
- ❌ tumor of the colon *(type: exact)*

---

### MONDO:0005509 ↔ EFO:0005561

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005509`
- **Mondo Label**: histiocytoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005561`
- **EFO Label**: histiocytoma

**Xrefs already in Mondo** (6):

- ✅ `DOID:4231`
- ✅ `EFO:0005561`
- ✅ `ICDO:8831/0`
- ✅ `MESH:D051642`
- ✅ `NCIT:C35765`
- ✅ `UMLS:C1509147`

**Xrefs missing from Mondo** (6):

- ❌ `OMIM:612160`
- ❌ `SCTID_2010_1_31:128741006`
- ❌ `SCTID_2010_1_31:154614002`
- ❌ `SCTID_2010_1_31:189773000`
- ❌ `SCTID_2010_1_31:302843004`
- ❌ `SCTID_2010_1_31:72079004`

**Synonyms already in Mondo** (1):

- ✅ histiocytoma *(type: exact)*

---

### MONDO:0005559 ↔ EFO:0005772

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005559`
- **Mondo Label**: neurodegenerative disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005772`
- **EFO Label**: neurodegenerative disease

**Xrefs already in Mondo** (3):

- ✅ `DOID:1289`
- ✅ `MESH:D019636`
- ✅ `NCIt:C4802`

**Xrefs missing from Mondo** (3):

- ❌ `SNOMEDCT:362975008`
- ❌ `UMLS:C0524851`
- ❌ `UMLS:C1285162`

**Synonyms already in Mondo** (1):

- ✅ central nervous system degenerative disorder *(type: exact)*

**Synonyms missing from Mondo** (3):

- ❌ Neurodegenerative Diseases *(type: exact)*
- ❌ neurodegenerative disorder *(type: exact)*
- ❌ neurodegenerative disorders *(type: exact)*

---

### MONDO:0005560 ↔ EFO:0005774

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005560`
- **Mondo Label**: brain disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005774`
- **EFO Label**: brain disease

**Xrefs missing from Mondo** (2):

- ❌ `DOID:936`
- ❌ `ICD10:G93`

---

### MONDO:0005561 ↔ EFO:0005775

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005561`
- **Mondo Label**: aortic disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0005775`
- **EFO Label**: aortic disease

**Xrefs missing from Mondo** (1):

- ❌ `DOID:520`

---

### MONDO:0005976 ↔ EFO:0007504

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0005976`
- **Mondo Label**: syphilis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_0007504`
- **EFO Label**: syphilis

**Xrefs already in Mondo** (5):

- ✅ `DOID:4166`
- ✅ `MESH:D013587`
- ✅ `MedDRA:10062120`
- ✅ `NCIt:C35055`
- ✅ `SNOMEDCT:76272004`

**Xrefs missing from Mondo** (6):

- ❌ `ICD10:A51`
- ❌ `ICD10:A53`
- ❌ `MedDRA:10042894`
- ❌ `MedDRA:10042895`
- ❌ `MedDRA:10042896`
- ❌ `MedDRA:10042901`

---

### MONDO:0006026 ↔ EFO:1000018

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006026`
- **Mondo Label**: bladder disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000018`
- **EFO Label**: bladder disease

**Xrefs missing from Mondo** (4):

- ❌ `DOID:365`
- ❌ `ICD10:N32`
- ❌ `NCIt:C2900`
- ❌ `UMLS:C0005686`

**Synonyms missing from Mondo** (2):

- ❌ bladder disorder *(type: exact)*
- ❌ urinary bladder disorder *(type: exact)*

---

### MONDO:0006030 ↔ EFO:1000023

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006030`
- **Mondo Label**: chronic cystitis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000023`
- **EFO Label**: chronic cystitis

**Xrefs already in Mondo** (4):

- ✅ `DOID:1680`
- ✅ `NCIt:C27008`
- ✅ `SNOMEDCT:33655002`
- ✅ `UMLS:C0221763`

**Xrefs missing from Mondo** (2):

- ❌ `ICD9CM:595.2`
- ❌ `MedDRA:10008852`

**Synonyms missing from Mondo** (1):

- ❌ Other chronic cystitis *(type: exact)*

---

### MONDO:0006373 ↔ EFO:1000478

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006373`
- **Mondo Label**: pituitary gland adenoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000478`
- **EFO Label**: Pituitary Gland Adenoma

**Xrefs missing from Mondo** (12):

- ❌ `DOID:3829`
- ❌ `EFO:1000478`
- ❌ `ICD10:D35.2`
- ❌ `ICDO:8272/0`
- ❌ `MedDRA:10035079`
- ❌ `NCIT:C3329`
- ❌ `OMIM:617540`
- ❌ `OMIM:617686`
- ❌ `ONCOTREE:PTAD`
- ❌ `Orphanet:99408`
- ❌ `SCTID:254956000`
- ❌ `UMLS:C0032000`

**Synonyms missing from Mondo** (8):

- ❌ PTAD *(type: related)*
- ❌ adenoma of pituitary *(type: exact)*
- ❌ adenoma of pituitary gland *(type: exact)*
- ❌ adenoma of the pituitary *(type: exact)*
- ❌ adenoma of the pituitary gland *(type: exact)*
- ❌ adenoma, anterior lobe pituitary gland, benign *(type: exact)*
- ❌ pituitary adenoma *(type: exact)*
- ❌ pituitary gland adenoma *(type: exact)*

---

### MONDO:0006642 ↔ EFO:1000800

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006642`
- **Mondo Label**: alcohol withdrawal delirium
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000800`
- **EFO Label**: alcohol withdrawal delirium

**Xrefs already in Mondo** (4):

- ✅ `ICD9:291.0`
- ✅ `MESH:D000430`
- ✅ `MedDRA:10001610`
- ✅ `SNOMEDCT:8635005`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:8639`

**Synonyms already in Mondo** (2):

- ✅ Alcohol Withdrawal Delirium *(type: exact)*
- ✅ delirium tremens *(type: exact)*

**Synonyms missing from Mondo** (3):

- ❌ Alcohol withdrawal delirium (disorder) *(type: exact)*
- ❌ Alcoholic delirium *(type: exact)*
- ❌ Mental and behavioral disorder due to use of alcohol: withdrawal state with delirium (disorder) *(type: exact)*

---

### MONDO:0006643 ↔ EFO:1000801

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006643`
- **Mondo Label**: alcoholic cardiomyopathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000801`
- **EFO Label**: alcoholic cardiomyopathy

**Xrefs already in Mondo** (5):

- ✅ `DOID:12935`
- ✅ `MESH:D002310`
- ✅ `MedDRA:10001616`
- ✅ `NCIt:C53653`
- ✅ `SNOMEDCT:83521008`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:I42.6`

**Synonyms already in Mondo** (2):

- ✅ Alcohol-induced heart muscle disease *(type: exact)*
- ✅ Alcoholic cardiomyopathy *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Cardiomyopathy, Alcoholic *(type: exact)*
- ❌ Dilated cardiomyopathy secondary to alcohol (disorder) *(type: exact)*

---

### MONDO:0006644 ↔ EFO:1000802

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006644`
- **Mondo Label**: alcoholic liver cirrhosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000802`
- **EFO Label**: alcoholic liver cirrhosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:14018`
- ✅ `MESH:D008104`
- ✅ `MedDRA:10001618`
- ✅ `NCIt:C34782`

**Xrefs missing from Mondo** (2):

- ❌ `ICD10:K70.3`
- ❌ `SNOMEDCT:420054005`

**Synonyms already in Mondo** (5):

- ✅ Alcoholic Cirrhosis *(type: exact)*
- ✅ Alcoholic cirrhosis of liver *(type: exact)*
- ✅ Laennec&apos;s cirrhosis *(type: exact)*
- ✅ Laennec&apos;s cirrhosis, alcoholic *(type: exact)*
- ✅ Portal cirrhosis *(type: exact)*

**Synonyms missing from Mondo** (5):

- ❌ Alcoholic cirrhosis of liver (disorder) *(type: exact)*
- ❌ Alcoholic cirrhosis of liver (disorder) [Ambiguous] *(type: exact)*
- ❌ Liver Cirrhosis, Alcoholic *(type: exact)*
- ❌ Portal cirrhosis (disorder) *(type: exact)*
- ❌ Portal cirrhosis unspecified (disorder) *(type: exact)*

---

### MONDO:0006645 ↔ EFO:1000803

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006645`
- **Mondo Label**: alcoholic polyneuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000803`
- **EFO Label**: alcoholic neuropathy

**Xrefs already in Mondo** (2):

- ✅ `DOID:14183`
- ✅ `MESH:D020269`

**Synonyms already in Mondo** (3):

- ✅ Alcohol-related polyneuropathy *(type: exact)*
- ✅ Alcoholic Neuropathy *(type: exact)*
- ✅ Alcoholic polyneuropathy *(type: exact)*

---

### MONDO:0011782 ↔ EFO:1000805

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0011782`
- **Mondo Label**: angioid streaks
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000805`
- **EFO Label**: angioid streaks

**Xrefs already in Mondo** (3):

- ✅ `DOID:13401`
- ✅ `MESH:D000793`
- ✅ `MedDRA:10066191`

**Xrefs missing from Mondo** (1):

- ❌ `SNOMEDCT:86103006`

**Synonyms already in Mondo** (1):

- ✅ Angioid Streaks *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Angioid streaks of choroid *(type: exact)*

---

### MONDO:0006647 ↔ EFO:1000807

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006647`
- **Mondo Label**: anterior cerebral artery infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000807`
- **EFO Label**: anterior cerebral artery infarction

**Xrefs already in Mondo** (2):

- ✅ `DOID:3528`
- ✅ `MESH:D020243`

**Synonyms missing from Mondo** (1):

- ❌ Infarction, Anterior Cerebral Artery *(type: exact)*

---

### MONDO:0006648 ↔ EFO:1000808

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006648`
- **Mondo Label**: anterior compartment of tibia syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000808`
- **EFO Label**: anterior compartment syndrome

**Xrefs already in Mondo** (3):

- ✅ `DOID:3933`
- ✅ `MESH:D000868`
- ✅ `SNOMEDCT:12694001`

**Xrefs missing from Mondo** (1):

- ❌ `NCIt:C118422`

**Synonyms already in Mondo** (1):

- ✅ Anterior compartment syndrome *(type: exact)*

---

### MONDO:0006649 ↔ EFO:1000809

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006649`
- **Mondo Label**: anterior ischemic optic neuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000809`
- **EFO Label**: anterior ischemic optic neuropathy

**Xrefs already in Mondo** (4):

- ✅ `DOID:12010`
- ✅ `MESH:D018917`
- ✅ `MedDRA:10068250`
- ✅ `SNOMEDCT:404659001`

**Synonyms already in Mondo** (1):

- ✅ Ischemic optic neuropathy *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Optic Neuropathy, Ischemic *(type: exact)*

---

### MONDO:0006650 ↔ EFO:1000810

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006650`
- **Mondo Label**: anterior spinal artery syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000810`
- **EFO Label**: anterior spinal artery syndrome

**Xrefs missing from Mondo** (4):

- ❌ `DOID:6712`
- ❌ `MESH:D020759`
- ❌ `MedDRA:10002703`
- ❌ `SNOMEDCT:14363008`

**Synonyms missing from Mondo** (2):

- ❌ Anterior Spinal Artery Syndrome *(type: exact)*
- ❌ Anterior spinal artery occlusion syndrome (disorder) *(type: exact)*

---

### MONDO:0006652 ↔ EFO:1000812

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006652`
- **Mondo Label**: anterolateral myocardial infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000812`
- **EFO Label**: anterolateral myocardial infarction

**Xrefs already in Mondo** (3):

- ✅ `DOID:5845`
- ✅ `MESH:D056988`
- ✅ `MedDRA:10068109`

**Synonyms missing from Mondo** (1):

- ❌ Anterior Wall Myocardial Infarction *(type: exact)*

---

### MONDO:0006653 ↔ EFO:1000813

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006653`
- **Mondo Label**: anthracosilicosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000813`
- **EFO Label**: anthracosilicosis

**Xrefs already in Mondo** (5):

- ✅ `DOID:10324`
- ✅ `MESH:D000874`
- ✅ `MedDRA:10050363`
- ✅ `NCIt:C34389`
- ✅ `SNOMEDCT:33548005`

**Synonyms already in Mondo** (1):

- ✅ Anthracosilicosis *(type: exact)*

---

### MONDO:0006654 ↔ EFO:1000814

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006654`
- **Mondo Label**: anthracosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000814`
- **EFO Label**: anthracosis

**Xrefs already in Mondo** (5):

- ✅ `DOID:10327`
- ✅ `MESH:D055008`
- ✅ `MedDRA:10073051`
- ✅ `NCIt:C34390`
- ✅ `SNOMEDCT:29422001`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:J60`

**Synonyms already in Mondo** (6):

- ✅ Anthracosis *(type: exact)*
- ✅ Coal Miner&apos;s Pneumoconiosis *(type: exact)*
- ✅ Coal workers&apos; lung *(type: exact)*
- ✅ Coal workers&apos; pneumoconiosis *(type: exact)*
- ✅ Melanoedema *(type: exact)*
- ✅ black lung *(type: exact)*

---

### MONDO:0006655 ↔ EFO:1000815

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006655`
- **Mondo Label**: aortic valve prolapse
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000815`
- **EFO Label**: aortic valve prolapse

**Xrefs already in Mondo** (3):

- ✅ `DOID:5232`
- ✅ `MESH:D001023`
- ✅ `MedDRA:10057454`

**Synonyms already in Mondo** (1):

- ✅ Aortic Valve Prolapse *(type: exact)*

---

### MONDO:0006656 ↔ EFO:1000816

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006656`
- **Mondo Label**: aortitis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000816`
- **EFO Label**: aortitis

**Xrefs missing from Mondo** (5):

- ❌ `DOID:519`
- ❌ `MESH:D001025`
- ❌ `MedDRA:10002921`
- ❌ `NCIt:C97085`
- ❌ `SNOMEDCT:70933002`

**Synonyms missing from Mondo** (3):

- ❌ Aortitis *(type: exact)*
- ❌ Aortitis (disorder) *(type: exact)*
- ❌ Aortitis NOS *(type: exact)*

---

### MONDO:0007150 ↔ EFO:1000818

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0007150`
- **Mondo Label**: arcus senilis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000818`
- **EFO Label**: arcus senilis

**Xrefs already in Mondo** (3):

- ✅ `DOID:11342`
- ✅ `MESH:D001112`
- ✅ `MedDRA:10003082`

**Xrefs missing from Mondo** (1):

- ❌ `SNOMEDCT:111522004`

**Synonyms already in Mondo** (2):

- ✅ Arcus Senilis *(type: exact)*
- ✅ corneal arcus *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Arcus of cornea (disorder) *(type: exact)*

---

### MONDO:0006658 ↔ EFO:1000819

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006658`
- **Mondo Label**: arteriolosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000819`
- **EFO Label**: arteriolosclerosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:5162`
- ✅ `MESH:D050379`
- ✅ `NCIt:C35543`
- ✅ `UMLS:C0878486`

**Xrefs missing from Mondo** (2):

- ❌ `MONDO:0006658`
- ❌ `SNOMEDCT:17941002`

**Synonyms already in Mondo** (2):

- ✅ Arteriolosclerosis *(type: exact)*
- ✅ Arteriolosclerosis (morphologic abnormality) *(type: exact)*

---

### MONDO:0006659 ↔ EFO:1000820

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006659`
- **Mondo Label**: arteriosclerosis obliterans
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000820`
- **EFO Label**: arteriosclerosis obliterans

**Xrefs already in Mondo** (4):

- ✅ `DOID:5160`
- ✅ `MESH:D001162`
- ✅ `MedDRA:10065418`
- ✅ `SNOMEDCT:361133006`

**Synonyms already in Mondo** (2):

- ✅ Arteriosclerosis Obliterans *(type: exact)*
- ✅ Arteriosclerosis obliterans (disorder) [Ambiguous] *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Arteriosclerosis obliterans (disorder) *(type: exact)*

---

### MONDO:0006666 ↔ EFO:1000827

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006666`
- **Mondo Label**: atrophy of thyroid
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000827`
- **EFO Label**: atrophy of thyroid

**Xrefs already in Mondo** (1):

- ✅ `MedDRA:10043693`

**Xrefs missing from Mondo** (3):

- ❌ `DOID:2853`
- ❌ `ICD10:E03.4`
- ❌ `MESH:D050033`

**Synonyms already in Mondo** (1):

- ✅ Thyroid Atrophy *(type: exact)*

**Synonyms missing from Mondo** (4):

- ❌ Hypoplasia of thyroid (disorder) *(type: exact)*
- ❌ Hypoplasia of thyroid (disorder) [Ambiguous] *(type: exact)*
- ❌ Thyroid Dysgenesis *(type: exact)*
- ❌ Thyroid atrophy (disorder) *(type: exact)*

---

### MONDO:0020322 ↔ EFO:1000828

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0020322`
- **Mondo Label**: acute biphenotypic leukemia
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000828`
- **EFO Label**: B- and T-cell mixed leukemia

**Xrefs already in Mondo** (10):

- ✅ `DOID:9953`
- ✅ `EFO:1000828`
- ✅ `ICD9:207.80`
- ✅ `ICDO:9805/3`
- ✅ `MESH:D015456`
- ✅ `MedDRA:10067399`
- ✅ `NCIT:C4673`
- ✅ `Orphanet:98837`
- ✅ `SCTID:278453007`
- ✅ `UMLS:C0023464`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:C95.0`

**Synonyms already in Mondo** (2):

- ✅ B- and T-cell mixed leukemia *(type: exact)*
- ✅ acute biphenotypic leukemia *(type: exact)*

---

### MONDO:0006671 ↔ EFO:1000832

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006671`
- **Mondo Label**: Bacteroides infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000832`
- **EFO Label**: Bacteroides infectious disease

**Xrefs already in Mondo** (1):

- ✅ `MESH:D001442`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:4641`

**Synonyms missing from Mondo** (1):

- ❌ Bacteroides Infections *(type: exact)*

---

### MONDO:0006672 ↔ EFO:1000833

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006672`
- **Mondo Label**: balanitis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000833`
- **EFO Label**: balanitis

**Xrefs missing from Mondo** (5):

- ❌ `DOID:13033`
- ❌ `MESH:D001446`
- ❌ `MedDRA:10004073`
- ❌ `NCIt:C26705`
- ❌ `SNOMEDCT:44882003`

**Synonyms missing from Mondo** (3):

- ❌ Balanitis *(type: exact)*
- ❌ Balanitis (disorder) *(type: exact)*
- ❌ Balanitis [Ambiguous] *(type: exact)*

---

### MONDO:0006676 ↔ EFO:1000837

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006676`
- **Mondo Label**: beriberi
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000837`
- **EFO Label**: beriberi

**Xrefs already in Mondo** (4):

- ✅ `DOID:13725`
- ✅ `MESH:D001602`
- ✅ `MedDRA:10004482`
- ✅ `SNOMEDCT:36656008`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:E51.1`

**Synonyms already in Mondo** (1):

- ✅ Beriberi *(type: exact)*

---

### MONDO:0006677 ↔ EFO:1000838

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006677`
- **Mondo Label**: bile reflux
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000838`
- **EFO Label**: bile reflux

**Xrefs already in Mondo** (2):

- ✅ `DOID:12237`
- ✅ `MESH:D001655`

**Synonyms already in Mondo** (1):

- ✅ Bile Reflux *(type: exact)*

---

### MONDO:0006678 ↔ EFO:1000839

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006678`
- **Mondo Label**: bladder calculus
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000839`
- **EFO Label**: bladder calculus

**Xrefs already in Mondo** (4):

- ✅ `DOID:11355`
- ✅ `MESH:D001744`
- ✅ `MedDRA:10005001`
- ✅ `SNOMEDCT:70650003`

**Xrefs missing from Mondo** (1):

- ❌ `NCIt:C26707`

**Synonyms missing from Mondo** (5):

- ❌ Urinary Bladder Calculi *(type: exact)*
- ❌ bladder stone *(type: exact)*
- ❌ bladder stones *(type: exact)*
- ❌ cystoliths *(type: exact)*
- ❌ vesical calculi *(type: exact)*

---

### MONDO:0006679 ↔ EFO:1000840

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006679`
- **Mondo Label**: bladder neck obstruction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000840`
- **EFO Label**: bladder neck obstruction

**Xrefs already in Mondo** (4):

- ✅ `DOID:13948`
- ✅ `MESH:D001748`
- ✅ `MedDRA:10005053`
- ✅ `SNOMEDCT:399072004`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:N35`

**Synonyms already in Mondo** (1):

- ✅ Obstruction of bladder neck or vesicourethral orifice *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Urinary Bladder Neck Obstruction *(type: exact)*
- ❌ bladder neck obstruction (disorder) *(type: exact)*

---

### MONDO:0006680 ↔ EFO:1000841

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006680`
- **Mondo Label**: blue nevus
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000841`
- **EFO Label**: blue nevus

**Xrefs already in Mondo** (6):

- ✅ `EFO:1000841`
- ✅ `ICDO:8780/0`
- ✅ `MESH:D018329`
- ✅ `MedDRA:10062788`
- ✅ `NCIT:C3803`
- ✅ `SCTID:254806009`

**Xrefs missing from Mondo** (1):

- ❌ `GARD:0008452`

**Synonyms already in Mondo** (11):

- ✅ Jadassohn-TiC(che nevus *(type: related)*
- ✅ Jadassohn-TiC(che syndrome *(type: related)*
- ✅ Jadassohn-Tièche nevus *(type: related)*
- ✅ Jadassohn-Tièche syndrome *(type: related)*
- ✅ Tièche-Jadassohn nevus *(type: related)*
- ✅ benign mesenchymal melanoma *(type: related)*
- ✅ blue Nevus of skin *(type: exact)*
- ✅ blue Nevus of the skin *(type: exact)*
- ✅ blue neuronevus *(type: related)*
- ✅ blue nevus *(type: exact)*
- ✅ blue skin Nevus *(type: exact)*

---

### MONDO:0006681 ↔ EFO:1000842

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006681`
- **Mondo Label**: Borrelia infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000842`
- **EFO Label**: Borrelia infectious disease

**Xrefs already in Mondo** (2):

- ✅ `MESH:D001899`
- ✅ `MedDRA:10061591`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:11730`

**Synonyms missing from Mondo** (4):

- ❌ Borrelia Infections *(type: exact)*
- ❌ Borreliosis (disorder) *(type: exact)*
- ❌ Borreliosis, NOS *(type: exact)*
- ❌ borreliosis *(type: exact)*

---

### MONDO:0006682 ↔ EFO:1000843

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006682`
- **Mondo Label**: brachial plexus neuritis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000843`
- **EFO Label**: brachial plexus neuritis

**Xrefs missing from Mondo** (4):

- ❌ `DOID:3689`
- ❌ `MESH:D020968`
- ❌ `MedDRA:10073002`
- ❌ `NCIt:C84600`

**Synonyms missing from Mondo** (4):

- ❌ Brachial Plexus Neuritis *(type: exact)*
- ❌ Brachial neuritis *(type: exact)*
- ❌ Brachial neuritis (disorder) *(type: exact)*
- ❌ Parsonage-Aldren-Turner syndrome *(type: exact)*

---

### MONDO:0006683 ↔ EFO:1000844

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006683`
- **Mondo Label**: brachial plexus neuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000844`
- **EFO Label**: brachial plexus neuropathy

**Xrefs missing from Mondo** (2):

- ❌ `DOID:3690`
- ❌ `MESH:D020516`

**Synonyms missing from Mondo** (3):

- ❌ Brachial Plexus Neuropathies *(type: exact)*
- ❌ Brachial plexus disorder *(type: exact)*
- ❌ brachial plexopathy *(type: exact)*

---

### MONDO:0006684 ↔ EFO:1000845

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006684`
- **Mondo Label**: brain edema
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000845`
- **EFO Label**: brain edema

**Xrefs already in Mondo** (3):

- ✅ `DOID:4724`
- ✅ `MESH:D001929`
- ✅ `MedDRA:10006121`

**Synonyms already in Mondo** (3):

- ✅ Brain Edema *(type: exact)*
- ✅ intracranial swelling *(type: exact)*
- ✅ wet brain *(type: exact)*

---

### MONDO:0006686 ↔ EFO:1000847

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006686`
- **Mondo Label**: brain stem infarction
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000847`
- **EFO Label**: brain stem infarction

**Xrefs missing from Mondo** (3):

- ❌ `DOID:3523`
- ❌ `MESH:D020526`
- ❌ `MedDRA:10006147`

**Synonyms missing from Mondo** (5):

- ❌ Brain Stem Infarctions *(type: exact)*
- ❌ Brainstem infarction *(type: exact)*
- ❌ Brainstem infarction NOS *(type: exact)*
- ❌ Brainstem infarction NOS (disorder) *(type: exact)*
- ❌ brain stem infarction (disorder) *(type: exact)*

---

### MONDO:0006687 ↔ EFO:1000850

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006687`
- **Mondo Label**: burning mouth syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000850`
- **EFO Label**: burning mouth syndrome

**Xrefs already in Mondo** (5):

- ✅ `DOID:4331`
- ✅ `MESH:D002054`
- ✅ `MedDRA:10068065`
- ✅ `NCIt:C62545`
- ✅ `SNOMEDCT:399165002`

**Synonyms already in Mondo** (3):

- ✅ Burning Mouth Syndrome *(type: exact)*
- ✅ Orodynia *(type: exact)*
- ✅ Stomatopyrosis *(type: exact)*

---

### MONDO:0006688 ↔ EFO:1000851

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006688`
- **Mondo Label**: byssinosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000851`
- **EFO Label**: byssinosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:10323`
- ✅ `MESH:D002095`
- ✅ `MedDRA:10006822`
- ✅ `NCIt:C84605`

**Xrefs missing from Mondo** (2):

- ❌ `ICD10:J66.0`
- ❌ `SNOMEDCT:85761009`

**Synonyms already in Mondo** (4):

- ✅ Byssinosis *(type: exact)*
- ✅ Flax-dressers&apos; disease *(type: exact)*
- ✅ Stripper&apos;s asthma *(type: exact)*
- ✅ cotton mill fever *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Byssinosis (disorder) *(type: exact)*

---

### MONDO:0006690 ↔ EFO:1000853

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006690`
- **Mondo Label**: carotid artery thrombosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000853`
- **EFO Label**: carotid artery thrombosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:3410`
- ✅ `MESH:D002341`
- ✅ `MedDRA:10007688`
- ✅ `SNOMEDCT:86003009`

**Synonyms already in Mondo** (1):

- ✅ Carotid artery thrombosis *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Carotid artery thrombosis (disorder) *(type: exact)*

---

### MONDO:0006692 ↔ EFO:1000857

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006692`
- **Mondo Label**: central pontine myelinolysis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000857`
- **EFO Label**: central pontine myelinolysis

**Xrefs already in Mondo** (5):

- ✅ `DOID:636`
- ✅ `MESH:D017590`
- ✅ `MedDRA:10007968`
- ✅ `NCIt:C84623`
- ✅ `SNOMEDCT:6807001`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:G37.2`

**Synonyms missing from Mondo** (3):

- ❌ Myelinolysis, Central Pontine *(type: exact)*
- ❌ central pontine myelinolysis (disorder) *(type: exact)*
- ❌ central pontine myelinosis *(type: exact)*

---

### MONDO:0006693 ↔ EFO:1000859

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006693`
- **Mondo Label**: cerebral arterial disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000859`
- **EFO Label**: cerebral arterial disease

**Xrefs already in Mondo** (2):

- ✅ `DOID:3527`
- ✅ `MESH:D002539`

**Synonyms missing from Mondo** (1):

- ❌ Cerebral Arterial Diseases *(type: exact)*

---

### MONDO:0006694 ↔ EFO:1000860

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006694`
- **Mondo Label**: cerebral atherosclerosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000860`
- **EFO Label**: cerebral atherosclerosis

**Xrefs already in Mondo** (5):

- ✅ `DOID:12720`
- ✅ `MESH:D002537`
- ✅ `MedDRA:1008095`
- ✅ `NCIt:C34459`
- ✅ `SNOMEDCT:55382008`

**Xrefs missing from Mondo** (2):

- ❌ `ICD10:I67.2`
- ❌ `MedDRA:10008095`

**Synonyms already in Mondo** (1):

- ✅ Cerebral atherosclerosis *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Cerebral atherosclerosis (disorder) *(type: exact)*
- ❌ Intracranial Arteriosclerosis *(type: exact)*

---

### MONDO:0006696 ↔ EFO:1000862

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006696`
- **Mondo Label**: cervix erosion
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000862`
- **EFO Label**: cervix erosion

**Xrefs already in Mondo** (4):

- ✅ `DOID:3456`
- ✅ `MESH:D002579`
- ✅ `MedDRA:10015128`
- ✅ `SNOMEDCT:61253004`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:N86`

**Synonyms already in Mondo** (1):

- ✅ Erosion of cervix *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Erosion of cervix (disorder) *(type: exact)*
- ❌ Uterine Cervical Erosion *(type: exact)*

---

### MONDO:0021697 ↔ EFO:1000863

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0021697`
- **Mondo Label**: chlamydia infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000863`
- **EFO Label**: Chlamydophila infectious disease

**Xrefs already in Mondo** (1):

- ✅ `MESH:D023521`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:11264`

**Synonyms missing from Mondo** (1):

- ❌ Chlamydophila Infections *(type: exact)*

---

### MONDO:0006698 ↔ EFO:1000864

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006698`
- **Mondo Label**: cholecystolithiasis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000864`
- **EFO Label**: cholecystolithiasis

**Xrefs already in Mondo** (3):

- ✅ `DOID:11151`
- ✅ `MESH:D041761`
- ✅ `MedDRA:10049890`

**Synonyms already in Mondo** (1):

- ✅ Cholecystolithiasis *(type: exact)*

---

### MONDO:0006699 ↔ EFO:1000865

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006699`
- **Mondo Label**: choledocholithiasis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000865`
- **EFO Label**: choledocholithiasis

**Xrefs missing from Mondo** (3):

- ❌ `DOID:11755`
- ❌ `MESH:D042883`
- ❌ `MedDRA:10049891`

**Synonyms missing from Mondo** (1):

- ❌ Choledocholithiasis *(type: exact)*

---

### MONDO:0006700 ↔ EFO:1000866

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006700`
- **Mondo Label**: choroid cancer
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000866`
- **EFO Label**: choroid cancer

**Xrefs missing from Mondo** (3):

- ❌ `DOID:12759`
- ❌ `MESH:D002830`
- ❌ `MedDRA:10057405`

**Synonyms missing from Mondo** (2):

- ❌ malignant tumor of choroid (disorder) *(type: exact)*
- ❌ malignant tumor of the Choroid *(type: exact)*

---

### MONDO:0006701 ↔ EFO:1000867

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006701`
- **Mondo Label**: chromophobe adenoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000867`
- **EFO Label**: chromophobe adenoma

**Xrefs already in Mondo** (6):

- ✅ `DOID:3828`
- ✅ `EFO:1000867`
- ✅ `ICDO:8270/0`
- ✅ `MESH:D000238`
- ✅ `NCIT:C2857`
- ✅ `UMLS:C0001432`

**Synonyms already in Mondo** (5):

- ✅ chromophobe adenoma *(type: exact)*
- ✅ chromophobe adenoma of pituitary gland *(type: exact)*
- ✅ chromophobe adenoma of the pituitary gland *(type: exact)*
- ✅ pituitary chromophobe adenoma *(type: exact)*
- ✅ pituitary gland chromophobe adenoma *(type: exact)*

---

### MONDO:0006702 ↔ EFO:1000868

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006702`
- **Mondo Label**: chronic inflammatory demyelinating polyradiculoneuropathy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000868`
- **EFO Label**: chronic inflammatory demyelinating polyradiculoneuropathy

**Xrefs already in Mondo** (4):

- ✅ `DOID:5213`
- ✅ `MESH:D020277`
- ✅ `MedDRA:10057645`
- ✅ `SNOMEDCT:128209004`

**Xrefs missing from Mondo** (1):

- ❌ `MedDRA:10072650`

**Synonyms missing from Mondo** (2):

- ❌ Polyradiculoneuropathy, Chronic Inflammatory Demyelinating *(type: exact)*
- ❌ chronic inflammatory demyelinating polyradiculoneuropathy (disorder) *(type: exact)*

---

### MONDO:0006704 ↔ EFO:1000870

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006704`
- **Mondo Label**: CNS demyelinating autoimmune disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000870`
- **EFO Label**: CNS demyelinating autoimmune disease

**Xrefs already in Mondo** (1):

- ✅ `MESH:D020278`

**Xrefs missing from Mondo** (2):

- ❌ `DOID:641`
- ❌ `ICD10:G37`

**Synonyms missing from Mondo** (1):

- ❌ Demyelinating Autoimmune Diseases, CNS *(type: exact)*

---

### MONDO:0024388 ↔ EFO:1000874

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0024388`
- **Mondo Label**: Clostridium infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000874`
- **EFO Label**: commensal Clostridium infectious disease

**Xrefs already in Mondo** (1):

- ✅ `MESH:D003015`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:3584`

**Synonyms missing from Mondo** (2):

- ❌ Clostridium Infections *(type: exact)*
- ❌ clostridial infection *(type: exact)*

---

### MONDO:0006708 ↔ EFO:1000875

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006708`
- **Mondo Label**: Desulfovibrionaceae infectious disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000875`
- **EFO Label**: commensal Desulfovibrionaceae infectious disease

**Xrefs already in Mondo** (1):

- ✅ `MESH:D045824`

**Xrefs missing from Mondo** (1):

- ❌ `DOID:3636`

**Synonyms missing from Mondo** (1):

- ❌ Desulfovibrionaceae Infections *(type: exact)*

---

### MONDO:0006709 ↔ EFO:1000876

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006709`
- **Mondo Label**: common bile duct neoplasm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000876`
- **EFO Label**: common bile duct neoplasm

**Xrefs missing from Mondo** (5):

- ❌ `DOID:4608`
- ❌ `EFO:1000876`
- ❌ `MESH:D003138`
- ❌ `SCTID:126857009`
- ❌ `UMLS:C0009442`

**Synonyms missing from Mondo** (5):

- ❌ common bile duct neoplasm *(type: exact)*
- ❌ common bile duct neoplasm (disease) *(type: exact)*
- ❌ common bile duct tumor *(type: exact)*
- ❌ neoplasm of common bile duct *(type: exact)*
- ❌ tumor of common bile duct *(type: exact)*

---

### MONDO:0006710 ↔ EFO:1000877

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006710`
- **Mondo Label**: complex partial epilepsy
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000877`
- **EFO Label**: complex partial epilepsy

**Xrefs already in Mondo** (2):

- ✅ `DOID:12382`
- ✅ `MESH:D017029`

**Synonyms already in Mondo** (3):

- ✅ Complex partial epileptic seizure *(type: exact)*
- ✅ epilepsy, psychomotor *(type: exact)*
- ✅ psychomotor epilepsy *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ Epilepsy, Complex Partial *(type: exact)*
- ❌ Psychomotor epilepsy (disorder) *(type: exact)*

---

### MONDO:0006712 ↔ EFO:1000879

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006712`
- **Mondo Label**: corneal edema
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000879`
- **EFO Label**: corneal edema

**Xrefs already in Mondo** (5):

- ✅ `DOID:11030`
- ✅ `ICD9:371.2`
- ✅ `MESH:D015715`
- ✅ `MedDRA:10011007`
- ✅ `SNOMEDCT:27194006`

**Xrefs missing from Mondo** (3):

- ❌ `MedDRA:1001MedDRA:1007`
- ❌ `MedDRA:1001MedDRA:1009`
- ❌ `NCIt:C50508`

**Synonyms already in Mondo** (1):

- ✅ Corneal Edema *(type: exact)*

**Synonyms missing from Mondo** (7):

- ❌ Corneal edema (disorder) *(type: exact)*
- ❌ Corneal edema NOS (disorder) *(type: exact)*
- ❌ Corneal edema, unspecified *(type: exact)*
- ❌ Corneal oedema *(type: exact)*
- ❌ Corneal oedema [Ambiguous] *(type: exact)*
- ❌ Unspecified corneal edema (disorder) *(type: exact)*
- ❌ cornea edema *(type: exact)*

---

### MONDO:0006713 ↔ EFO:1000880

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006713`
- **Mondo Label**: corneal neovascularization
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000880`
- **EFO Label**: corneal neovascularization

**Xrefs already in Mondo** (5):

- ✅ `DOID:11382`
- ✅ `ICD9:370.6`
- ✅ `MESH:D016510`
- ✅ `MedDRA:10011031`
- ✅ `SNOMEDCT:19161004`

**Xrefs missing from Mondo** (1):

- ❌ `MedDRA:10011032`

**Synonyms already in Mondo** (1):

- ✅ Corneal neovascularization *(type: exact)*

**Synonyms missing from Mondo** (4):

- ❌ Corneal neovascularization (disorder) *(type: exact)*
- ❌ Corneal neovascularization NOS (disorder) *(type: exact)*
- ❌ Corneal neovascularization, unspecified *(type: exact)*
- ❌ Unspecified corneal neovascularization (disorder) *(type: exact)*

---

### MONDO:0006714 ↔ EFO:1000881

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006714`
- **Mondo Label**: coronary aneurysm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000881`
- **EFO Label**: coronary aneurysm

**Xrefs already in Mondo** (5):

- ✅ `DOID:3362`
- ✅ `ICD9:414.11`
- ✅ `MESH:D003323`
- ✅ `MedDRA:10002348`
- ✅ `SNOMEDCT:50570003`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:I25.4`

**Synonyms already in Mondo** (4):

- ✅ Aneurysm of coronary vessels *(type: exact)*
- ✅ Aneurysmal lesion of coronary artery *(type: exact)*
- ✅ Arteriovenous aneurysm of coronary vessels *(type: exact)*
- ✅ Coronary Aneurysm *(type: exact)*

---

### MONDO:0006716 ↔ EFO:1000883

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006716`
- **Mondo Label**: coronary thrombosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000883`
- **EFO Label**: coronary thrombosis

**Xrefs missing from Mondo** (4):

- ❌ `DOID:11847`
- ❌ `MESH:D003328`
- ❌ `MedDRA:10011108`
- ❌ `SNOMEDCT:398274000`

**Synonyms missing from Mondo** (2):

- ❌ Coronary Thrombosis *(type: exact)*
- ❌ Coronary artery thrombosis (disorder) *(type: exact)*

---

### MONDO:0006717 ↔ EFO:1000885

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006717`
- **Mondo Label**: cutaneous fibrous histiocytoma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000885`
- **EFO Label**: cutaneous fibrous histiocytoma

**Xrefs already in Mondo** (7):

- ✅ `DOID:4418`
- ✅ `EFO:1000885`
- ✅ `ICDO:8832/0`
- ✅ `NCIT:C6801`
- ✅ `ONCOTREE:DF`
- ✅ `SCTID:448015002`
- ✅ `UMLS:C0002991`

**Xrefs missing from Mondo** (1):

- ❌ `UMLS:C0346049`

**Synonyms already in Mondo** (19):

- ✅ DF *(type: related)*
- ✅ benign cutaneous fibrous histiocytoma *(type: exact)*
- ✅ benign fibrous cutaneous histiocytoma *(type: exact)*
- ✅ benign fibrous histiocytoma of skin *(type: exact)*
- ✅ benign fibrous histiocytoma of the skin *(type: exact)*
- ✅ benign skin fibrous histiocytoma *(type: exact)*
- ✅ cutaneous fibrous histiocytoma *(type: exact)*
- ✅ dermatofibroma *(type: exact)*
- ✅ dermatofibroma, no ICD-O subtype *(type: exact)*
- ✅ dermatofibroma, no ICD-O subtype (morphologic abnormality) *(type: exact)*
- ✅ fibrohistiocytic neoplasm *(type: exact)*
- ✅ fibrohistiocytic tumor *(type: exact)*
- ✅ fibrous histiocytoma of skin *(type: exact)*
- ✅ fibrous histiocytoma of the skin *(type: exact)*
- ✅ fibrous xanthoma of skin *(type: exact)*
- ✅ pleomorphic fibroma *(type: exact)*
- ✅ sclerosing angioma *(type: exact)*
- ✅ sclerosing angioma (morphologic abnormality) *(type: exact)*
- ✅ sclerosing angioma of skin *(type: exact)*

---

### MONDO:0006718 ↔ EFO:1000887

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006718`
- **Mondo Label**: cutaneous syphilis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000887`
- **EFO Label**: cutaneous syphilis

**Xrefs already in Mondo** (1):

- ✅ `MESH:D013591`

**Xrefs missing from Mondo** (2):

- ❌ `DOID:5000`
- ❌ `ICD10:A50.06`

**Synonyms missing from Mondo** (2):

- ❌ Syphilis, Cutaneous *(type: exact)*
- ❌ Syphilitic skin disorder *(type: exact)*

---

### MONDO:0009761 ↔ EFO:1000888

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0009761`
- **Mondo Label**: cystic hygroma
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000888`
- **EFO Label**: cystic lymphangioma

**Xrefs already in Mondo** (9):

- ✅ `DOID:3081`
- ✅ `EFO:1000888`
- ✅ `ICDO:9173/0`
- ✅ `MESH:D018191`
- ✅ `MedDRA:10058949`
- ✅ `NCIT:C3724`
- ✅ `OMIM:257350`
- ✅ `Orphanet:79486`
- ✅ `SCTID:399882002`

**Xrefs missing from Mondo** (2):

- ❌ `GARD:0006234`
- ❌ `ICD10:D18.1`

**Synonyms already in Mondo** (6):

- ✅ cystic hygroma *(type: exact)*
- ✅ cystic hygroma, fetal *(type: related)*
- ✅ cystic lymphangioma *(type: exact)*
- ✅ hygroma *(type: exact)*
- ✅ macrocystic lymphatic malformation *(type: related)*
- ✅ nuchal bleb, familial *(type: related)*

---

### MONDO:0006720 ↔ EFO:1000889

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006720`
- **Mondo Label**: cystic, mucinous, and serous neoplasm
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000889`
- **EFO Label**: cystic, mucinous, and serous neoplasm

**Xrefs already in Mondo** (2):

- ✅ `EFO:1000889`
- ✅ `MESH:D018297`

**Synonyms already in Mondo** (1):

- ✅ cystic, mucinous, and serous neoplasm *(type: exact)*

---

### MONDO:0009072 ↔ EFO:1000890

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0009072`
- **Mondo Label**: Dandy-Walker syndrome
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000890`
- **EFO Label**: Dandy-Walker syndrome

**Xrefs already in Mondo** (4):

- ✅ `DOID:2785`
- ✅ `MESH:D003616`
- ✅ `MedDRA:10048411`
- ✅ `SNOMEDCT:14447001`

**Synonyms already in Mondo** (2):

- ✅ Atresia of foramina of Magendie and Luschka *(type: exact)*
- ✅ Dandy-Walker Syndrome *(type: exact)*

**Synonyms missing from Mondo** (2):

- ❌ (Atresia of foramina of Magendie + Luschka) or (Dandy - Walker syndrome) *(type: exact)*
- ❌ Dandy-Walker syndrome (disorder) *(type: exact)*

---

### MONDO:0006721 ↔ EFO:1000891

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006721`
- **Mondo Label**: de Quervain disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000891`
- **EFO Label**: De Quervain disease

**Xrefs already in Mondo** (2):

- ✅ `DOID:14107`
- ✅ `MESH:D053684`

**Synonyms already in Mondo** (3):

- ✅ De Quervain Disease *(type: exact)*
- ✅ Radial styloid tenosynovitis *(type: exact)*
- ✅ Tenosynovitis, de Quervain&apos;s *(type: exact)*

---

### MONDO:0006722 ↔ EFO:1000892

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006722`
- **Mondo Label**: dental fluorosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000892`
- **EFO Label**: dental fluorosis

**Xrefs already in Mondo** (5):

- ✅ `DOID:13711`
- ✅ `MESH:D009050`
- ✅ `MedDRA:10016819`
- ✅ `NCIt:C85059`
- ✅ `SNOMEDCT:30265004`

**Synonyms already in Mondo** (3):

- ✅ Intrinsic enamel discolouration of fluorosis *(type: exact)*
- ✅ Mottled teeth *(type: exact)*
- ✅ Mottling of enamel *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ Fluorosis, Dental *(type: exact)*

---

### MONDO:0006723 ↔ EFO:1000893

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006723`
- **Mondo Label**: denture stomatitis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000893`
- **EFO Label**: denture stomatitis

**Xrefs already in Mondo** (3):

- ✅ `DOID:11875`
- ✅ `MESH:D013282`
- ✅ `SNOMEDCT:69254008`

**Xrefs missing from Mondo** (1):

- ❌ `MedDRA:10080528`

**Synonyms already in Mondo** (1):

- ✅ Denture sore mouth *(type: exact)*

**Synonyms missing from Mondo** (3):

- ❌ Denture stomatitis (disorder) *(type: exact)*
- ❌ Denture stomatitis [Ambiguous] *(type: exact)*
- ❌ Stomatitis, Denture *(type: exact)*

---

### MONDO:0019373 ↔ EFO:1000895

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0019373`
- **Mondo Label**: desmoplastic small round cell tumor
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000895`
- **EFO Label**: desmoplastic small round cell tumor

**Xrefs already in Mondo** (10):

- ✅ `EFO:1000895`
- ✅ `HGNC:12796`
- ✅ `ICDO:8806/3`
- ✅ `MESH:D058405`
- ✅ `MedDRA:10064581`
- ✅ `MedDRA:10064587`
- ✅ `NCIT:C8300`
- ✅ `ONCOTREE:DSRCT`
- ✅ `Orphanet:83469`
- ✅ `UMLS:C0281508`

**Xrefs missing from Mondo** (2):

- ❌ `GARD:0006265`
- ❌ `ICD10:C48.2`

**Synonyms already in Mondo** (7):

- ✅ DSRCT *(type: exact)*
- ✅ Desmoplas. small round cell tumor *(type: exact)*
- ✅ Desmoplastic small round-cell neoplasm *(type: exact)*
- ✅ Desmoplastic small round-cell tumor *(type: exact)*
- ✅ Polyphenotypic small round cell tumor *(type: exact)*
- ✅ desmoplastic small round cell tumor *(type: exact)*
- ✅ desmoplastic small-round-cell tumor *(type: related)*

---

### MONDO:0012819 ↔ EFO:1000897

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0012819`
- **Mondo Label**: diabetic ketoacidosis
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000897`
- **EFO Label**: diabetic ketoacidosis

**Xrefs already in Mondo** (4):

- ✅ `DOID:1837`
- ✅ `MESH:D016883`
- ✅ `MedDRA:10012671`
- ✅ `SNOMEDCT:420422005`

**Xrefs missing from Mondo** (2):

- ❌ `MedDRA:10023392`
- ❌ `NCIt:C50530`

**Synonyms already in Mondo** (2):

- ✅ Diabetic Ketoacidosis *(type: exact)*
- ✅ ketosis-prone diabetes mellitus *(type: exact)*

**Synonyms missing from Mondo** (1):

- ❌ DIABETES MELLITUS, KETOSIS-PRONE *(type: exact)*

---

### MONDO:0006727 ↔ EFO:1000899

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006727`
- **Mondo Label**: diastolic heart failure
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1000899`
- **EFO Label**: diastolic heart failure

**Xrefs already in Mondo** (5):

- ✅ `DOID:9775`
- ✅ `ICD9:428.3`
- ✅ `MESH:D054144`
- ✅ `MedDRA:10069211`
- ✅ `SNOMEDCT:418304008`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:I50.3`

**Synonyms missing from Mondo** (1):

- ❌ Heart Failure, Diastolic *(type: exact)*

---

### MONDO:0006873 ↔ EFO:1001067

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006873`
- **Mondo Label**: nutritional deficiency disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1001067`
- **EFO Label**: nutritional deficiency disease

**Xrefs already in Mondo** (4):

- ✅ `DOID:5113`
- ✅ `MESH:D003677`
- ✅ `MedDRA:10046058`
- ✅ `SNOMEDCT:70241007`

**Xrefs missing from Mondo** (1):

- ❌ `ICD10:E63`

---

### MONDO:0006999 ↔ EFO:1001216

- **Mondo IRI**: `http://purl.obolibrary.org/obo/MONDO_0006999`
- **Mondo Label**: tooth disease
- **EFO IRI**: `http://www.ebi.ac.uk/efo/EFO_1001216`
- **EFO Label**: tooth disease

**Xrefs missing from Mondo** (4):

- ❌ `DOID:1091`
- ❌ `ICD10:K08`
- ❌ `MESH:DO14076`
- ❌ `SNOMEDCT:234947003`

**Synonyms missing from Mondo** (4):

- ❌ dental disease *(type: exact)*
- ❌ dental disorder *(type: exact)*
- ❌ disease of teeth *(type: exact)*
- ❌ tooth disorder *(type: exact)*

---

*This report was generated as part of the Mondo-EFO mapping migration task (partial work on first 100 terms).*