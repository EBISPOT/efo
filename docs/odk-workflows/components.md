# Adding components

For details on what components are, please see the component section of the
[repository file structure document](../odk-workflows/RepositoryFileStructure.md).

Components are ontology modules that live in `src/ontology/components/` and are
imported by `efo-edit.owl`. Each generated component is declared as a rule in
`owlmake.yaml`, which is the single description of the build.

To add a new component:

1) Add a rule to `owlmake.yaml` under `prerequisites:` with the component file
   as its `target`, listing its inputs under `needs:` and the operations that
   produce it under `steps:` (existing component rules such as
   `src/ontology/components/subclasses.owl` are good templates). A component
   derived from a template table uses an `op: template` step over a TSV in
   `src/templates/`; a component fetched from a remote resource uses an
   `op: fetch` step.

2) Make `efo-edit.owl` import the component's IRI
   (`http://www.ebi.ac.uk/efo/components/your-component-name.owl`), and add a
   line to `src/ontology/catalog-v001.xml` redirecting that IRI to the file in
   `src/ontology/components/`, so the component is found when the edit file is
   loaded (by `om`, Protégé, or anything else reading the catalog).

3) Build it with `om make components/your-component-name.owl` and check it is
   reachable from the targets that should include it (`all_components` groups
   the generated components).

Because the rule is part of `owlmake.yaml`, the change shows up as a plan diff
in review — adding a component is a change to what the build does, and the plan
is where that is recorded.
