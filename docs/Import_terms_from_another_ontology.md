# Refreshing Imports in EFO

This document describes how to refresh imported ontology terms in the Experimental Factor Ontology (EFO). The import system ensures that external terms (e.g., from UBERON, MONDO, CL) are correctly maintained and safely integrated into the EFO ontology.

## Folder Structure Overview

- `src/ontology/imports/`  
  **Do not edit this folder directly.** This folder is automatically generated and contains:
  - `.owl` import files (e.g., `uberon_import.owl`)
  - Copies of the imported term lists as a safeguard against term disappearance

- `src/ontology/iri_dependencies/`  
  **This is where you should make changes.** This folder contains plain-text files, each corresponding to an imported ontology. Each file contains a list of IRIs to be imported:
  - `mondo_terms.txt`
  - `uberon_terms.txt`
  - `cl_terms.txt`
  - etc.

Each line in these files should contain one full IRI of a term to be imported.

## Step-by-Step: How to Refresh Imports

### 1. Update Ontology Mirrors

Before updating the imports, ensure that the local ontology mirrors are up to date. These mirrors are used to resolve IRIs when generating import files.

```bash
./get_mirrors.sh
```

This script will download or update local copies of external ontologies used in the import process.

### 2. Edit the Term Lists (if needed)

To add or remove imported terms:

1. Navigate to:
   ```bash
   src/ontology/iri_dependencies/
   ```
2. Open the relevant file (e.g., `uberon_terms.txt`) in a text editor.
3. Add or remove full IRIs of the terms you want to import, one per line.

**Note:** Do not edit anything in the `src/ontology/imports/` directory manually. All edits must go through the IRI dependency files.

### 3. Run the Import for a Specific Ontology

To regenerate the import file for a single ontology, run:

```bash
cd src/ontology
make [ontology]_import.owl
```

For example, to update UBERON:

```bash
make uberon_import.owl
```

If you encounter issues (e.g., caching, stale builds), you can force the rebuild:

```bash
make uberon_import.owl -B
```

### 4. Refresh All Imports (Optional)

To regenerate all import files at once:

```bash
cd src/ontology
make all_imports -B
```

## What Happens When You Run `make`

Running `make [ontology]_import.owl` will:

1. Read the list of IRIs from `iri_dependencies/[ontology]_terms.txt`
2. Resolve those IRIs using the updated mirrors
3. Generate:
   - An `.owl` file in `src/ontology/imports/` (e.g., `uberon_import.owl`)
   - A backup copy of the term list in `src/ontology/imports/` for safety

This system ensures reproducibility, traceability, and prevents accidental loss of imported terms.

## Notes and Best Practices

- Always run `./get_mirrors.sh` before running `make`, especially if terms may have changed upstream.
- Only edit the `.txt` files in `src/ontology/iri_dependencies/`.
- Do not directly modify any `.owl` files or `.txt` backups in the `imports` folder.
- Use `-B` with `make` if the system appears not to be updating the files.
- Review changes using `git diff` to ensure that the intended terms were updated.

## Example Workflow

```bash
# Step 1: Update local mirrors
./get_mirrors.sh

# Step 2: Edit IRIs (if needed)
nano src/ontology/iri_dependencies/uberon_terms.txt #Or use a text editor such as VSC

# Step 3: Run the import
cd src/ontology
make uberon_import.owl
```

To update all imports:

```bash
cd src/ontology
make all_imports -B
```

## Fixing Dangling Imported Terms

Sometimes, after importing a term, it may appear as a "dangling class"—that is, attached only to `owl:Thing` with no asserted superclass. This typically happens when the imported term does not include a parent in the original ontology, or when ROBOT's import process prunes axioms not explicitly included.

This can lead to quality control (QC) failures or unwanted structural issues in the ontology.

### Solution: Use `subclasses.csv` to Assert Parentage

To manually assert a parent class for an imported term, use the `subclasses.csv` template file located in:

```
src/templates/subclasses.csv
```

This file allows you to declare subclass relationships between imported terms and existing EFO terms.

#### Instructions

1. Open `src/templates/subclasses.csv`.

2. Add a new row with the following format:

```
ID_OF_IMPORTED_TERM,ID_OF_PARENT_TERM_IN_EFO
```

For example:

```
MONDO:0042489,BFO:0000019
```

3. Save the file.

4. Rebuild the ontology:

```bash
cd src/ontology #If you are not in the ontology folder
make components/subclasses.owl      
```

This will ensure the imported term is attached to the correct location in the EFO hierarchy and prevent it from hanging under `owl:Thing`.

### Summary

- Dangling terms occur when ROBOT excludes axioms linking to a parent class.
- To fix this, use `subclasses.csv` to manually define the parent.
- Avoid editing OWL files directly in Protege or the imports folder.
- Always use the templating system to ensure consistency and reproducibility.

