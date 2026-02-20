# Repository structure

The main kinds of files in the repository:

1. Release files
2. Imports
3. [Components](#components)

## Release files
Release file are the file that are considered part of the official ontology release and to be used by the community. A detailed description of the release artefacts can be found [here](https://github.com/INCATools/ontology-development-kit/blob/master/docs/ReleaseArtefacts.md).

## Imports
Imports are subsets of external ontologies that contain terms and axioms you would like to re-use in your ontology. These are considered "external", like dependencies in software development, and are not included in your "base" product, which is the [release artefact](https://github.com/INCATools/ontology-development-kit/blob/master/docs/ReleaseArtefacts.md) which contains only those axioms that you personally maintain.

These are the current imports in EFO

| Import | URL | Type |
| ------ | --- | ---- |
| uberon | http://purl.obolibrary.org/obo/uberon/uberon-base.owl | slme |
| hp | http://purl.obolibrary.org/obo/hp/hp-base.owl | slme |
| chebi | http://purl.obolibrary.org/obo/chebi/chebi-base.owl | slme |
| pr | http://purl.obolibrary.org/obo/pr/pr-base.owl | slme |
| ecto | http://purl.obolibrary.org/obo/ecto/ecto-base.owl | slme |
| cl | http://purl.obolibrary.org/obo/cl/cl-base.owl | slme |
| gsso | http://purl.obolibrary.org/obo/gsso.owl | slme |
| hancestro | https://raw.githubusercontent.com/EBISPOT/hancestro/main/hancestro.owl | slme |
| fbbt | http://purl.obolibrary.org/obo/fbbt/fbbt-base.owl | slme |
| obi | http://purl.obolibrary.org/obo/obi/obi-base.owl | slme |
| oba | http://purl.obolibrary.org/obo/oba/oba-base.owl | slme |
| fbbi | http://purl.obolibrary.org/obo/fbbi/fbbi-base.owl | slme |
| go | http://purl.obolibrary.org/obo/go/go-base.owl | slme |
## Components
Components, in contrast to imports, are considered full members of the ontology. This means that any axiom in a component is also included in the ontology base - which means it is considered _native_ to the ontology. While this sounds complicated, consider this: conceptually, no component should be part of more than one ontology. If that seems to be the case, we are most likely talking about an import. Components are often not needed for ontologies, but there are some use cases:

1. There is an automated process that generates and re-generates a part of the ontology
2. A part of the ontology is managed in ROBOT templates
3. The expressivity of the component is higher than the format of the edit file. For example, people still choose to manage their ontology in OBO format (they should not) missing out on a lot of owl features. They may choose to manage logic that is beyond OBO in a specific OWL component.

These are the components in EFO

| Filename | URL |
| -------- | --- |
| subclasses.owl | None |
| import_replaced_by.owl | None |
| anatomagram_lung.owl | None |
| anatomagram_kidney.owl | None |
| anatomagram_pancreas.owl | None |
| anatomagram_liver.owl | None |
| anatomagram_placenta.owl | None |
| gwas_import.owl | None |
| mondo_efo_import.owl | None |
| efo_equivalent_class_axioms.owl | None |
