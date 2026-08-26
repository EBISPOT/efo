[![Build Status](https://github.com/EBISPOT/efo/actions/workflows/qc.yml/badge.svg)](https://github.com/EBISPOT/efo/actions/workflows/qc.yml)

# EFO

![alt text](efo.gif?raw=true)

The Experimental Factor Ontology (EFO) provides a systematic description of many experimental variables available in EBI databases, and for projects such as the [NHGRI-EBI GWAS catalog](https://www.ebi.ac.uk/gwas/). It combines parts of several biological ontologies, such as [UBERON anatomy](http://uberon.github.io/), [ChEBI chemical compounds](https://www.ebi.ac.uk/chebi/), [Cell Ontology](https://github.com/obophenotype/cell-ontology) and the [Monarch Disease Ontology (MONDO)](http://obofoundry.org/ontology/mondo.html). The scope of EFO is to support the annotation, analysis and visualization of data handled by many groups at the EBI and as the core ontology for [Open Targets](http://www.opentargets.org/). EFO is developed by the [EMBL-EBI Samples, Phenotypes and Ontologies Team](http://www.ebi.ac.uk/about/spot-team) (SPOT). We also add terms for external users when requested.

The latest version of the ontology can always be found attached to each EFO 3 release, found here: [https://github.com/EBISPOT/efo/releases](https://github.com/EBISPOT/efo/releases)

You can explore EFO in the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols4/ontologies/efo)

# Term requests and contact

Submit new terms or report bugs using our [issue tracker](https://github.com/EBISPOT/efo/issues), or join [EFO mailing list](https://listserver.ebi.ac.uk/mailman/listinfo/efo-users) for announcement and monthly update.

# Editing EFO

Editors of this ontology should use the edit version,
[`src/ontology/efo-edit.owl`](https://github.com/EBISPOT/efo/blob/master/src/ontology/efo-edit.owl).

EFO is built using [owlmake](https://github.com/EBISPOT/owlmake). To build the
release files, first install owlmake and make sure it is on your `PATH`. For
example, on an Apple silicon Mac:

```bash
mkdir -p ~/.local/bin
curl -fsSL https://github.com/EBISPOT/owlmake/releases/latest/download/om-macos-arm64 \
  -o ~/.local/bin/om
chmod +x ~/.local/bin/om
```

Then run `om` from the repository root to build the default targets, or run
`om make gh_actions` to execute the same build and QC target as EFO's GitHub
workflow.
