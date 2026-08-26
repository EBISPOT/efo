# Refreshing Imports in EFO

This document describes how to refresh terms imported from external ontologies
such as UBERON, MONDO, and CL. EFO's import pipelines and mirror sources are
recorded in `owlmake.yaml` and are executed by [owlmake](https://github.com/EBISPOT/owlmake).
Run the commands below from the repository root.

## Files to edit

- `src/ontology/iri_dependencies/` contains the curated term lists. Each
  ontology has a plain-text file such as `mondo_terms.txt`,
  `uberon_terms.txt`, or `cl_terms.txt`. Put one full term IRI on each line.
- `src/ontology/imports/` contains generated OWL modules and backup copies of
  the term lists. **Never edit files in this directory by hand.**
- `src/ontology/mirror/` contains local source-ontology mirrors. Mirror URLs
  come from `owlmake.yaml`; they do not need to be copied into commands.

## Refresh one import

1. Edit the relevant dependency file, for example:

   ```text
   src/ontology/iri_dependencies/uberon_terms.txt
   ```

2. Refresh the mirror and rebuild the import from it:

   ```bash
   om make imports/uberon_import.owl --rebuild mirrors,imports
   ```

   Replace `uberon` with the required import ID. The `--rebuild` flags are
   required: mirrors and imports sit in refresh groups the plan keeps by
   default, and a kept target is reused even when named explicitly (`-B` does
   not override a kept group — it only forces targets whose rules are in
   play). `--rebuild mirrors,imports` puts both groups' rules back in play and
   rebuilds only the mirror and import in the requested target's closure.

3. Verify that the requested term is present:

   ```bash
   om ogrep UBERON:0000948 -i src/ontology/imports/uberon_import.owl
   ```

4. Review the generated changes with `git diff`. A normal import refresh may
   update both the OWL module and its backup term list.

## Refresh all imports

To refresh every mirror and regenerate every import module:

```bash
om make all_imports --rebuild mirrors,imports
```

This is more expensive than rebuilding one import and should be used only when
the full import set needs refreshing.

## What the import target does

For `imports/<ontology>_import.owl`, owlmake:

1. reads `src/ontology/iri_dependencies/<ontology>_terms.txt` and any shared
   seed lists declared by the plan;
2. obtains the source ontology from the corresponding mirror target;
3. extracts the configured locality module and applies any import-specific
   cleanup steps;
4. writes `src/ontology/imports/<ontology>_import.owl`; and
5. writes the backup term list under `src/ontology/imports/`.

The generated import may contain more entities than the explicit seed list
because it includes axioms required to preserve the extracted module.

## MONDO imports

MONDO follows the same workflow as the other imports:

```bash
om make imports/mondo_import.owl --rebuild mirrors,imports
```

The MONDO pipeline also detects referenced HGNC terms and adds them to
`src/ontology/iri_dependencies/mondo_exclude.txt` before writing the final
module. `mondo_import.owl` is gitignored because it is large; owlmake builds it
automatically when a requested target needs it and it is absent.

There is no separate `mondo_efo_import.owl` rebuild step. The release build
consumes `imports/mondo_import.owl` directly.

## Fixing dangling imported terms

An imported term can appear directly below `owl:Thing` when its source parent
is outside the extracted module. First check the source ontology: do not add a
local assertion when the intended relationship already exists upstream and can
be preserved by importing the required parent.

When EFO genuinely needs a cross-ontology parent assertion:

1. Ensure both terms have already been imported.
2. Add a row to `src/templates/subclasses.csv`:

   ```text
   ID_OF_IMPORTED_TERM,ID_OF_PARENT_TERM
   ```

   For example:

   ```text
   MONDO:0042489,BFO:0000019
   ```

3. Rebuild the generated component:

   ```bash
   om make components/subclasses.owl
   ```

4. Verify the resulting assertion and run the relevant QC target.

Do not repair dangling terms by editing an import OWL file in Protégé or a text
editor; generated imports will be overwritten on the next refresh.

## Troubleshooting

- Use `-B` when a target or one of its inputs has changed but timestamps would
  otherwise allow reuse. `-B` does not override the kept mirrors/imports
  groups — use `--rebuild mirrors,imports` for those.
- Use `om make --list-targets` to confirm the exact target name.
- Use `om ogrep <CURIE-or-label> -i <file>` to inspect a term and axioms that
  refer to it.
- Use `om convert -vvv` for detailed parser errors and `om reason` for ontology
  validation.
