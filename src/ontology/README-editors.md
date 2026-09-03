# EFO editor workflow

EFO's ontology build is defined by the repository-root `owlmake.yaml`. The old
ODK/Makefile and EFO2-to-EFO3 migration instructions are no longer applicable.
Run build commands from the repository root.

After editing `src/ontology/efo-edit.owl`, normalize and reason over it:

```bash
om make normalize_src
om reason -i src/ontology/efo-edit.owl -r hermit
```

Run the ontology quality checks with:

```bash
om make qc
```

Run `om` to build the default targets, including the release artefacts, or use
`om make release` when only the release target is required. To reproduce the
GitHub Actions build and QC path, run:

```bash
om make gh_actions
```

See the following maintained documentation for the rest of the workflow:

- [`../../README.md`](../../README.md) for setup and build entry points.
- [`../../CLAUDE.md`](../../CLAUDE.md) and
  [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) for
  curation and verification rules.
- [`../../docs/Import_terms_from_another_ontology.md`](../../docs/Import_terms_from_another_ontology.md)
  for import updates.
- [`../../docs/odk-workflows/EditorsWorkflow.md`](../../docs/odk-workflows/EditorsWorkflow.md)
  for the general editing workflow.

Use `om make --list-targets` to inspect all translated legacy targets, including
`all_diffs`, `edit_diff`, and the import-maintenance targets.
