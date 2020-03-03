These notes are for the EDITORS of efo

For the full description of the release process including the internal-link specific information, please make sure that you see https://www.ebi.ac.uk/seqdb/confluence/display/FGPTO/EFO+Release+Process !!!! This is vital if you are the EFO developer in charge of monthly release.

This project was created using the [ontology starter kit](https://github.com/cmungall/ontology-starter-kit). See the site for details.

## Editors Version

- We currently use EFO 2 (located in our efo2 branch) to update EFO 3, therefore any edits required to EFO 3 should be done through the efo-edit.owl procedure (pushing to GitHub), or through MONDO by submitting an issue or a pull request.
- Once ready to update EFO 3, perform a `git pull` as usual in the efo2 branch (where you edit EFO 2) to get the latest version of efo and efo-edit.owl
- To switch to the master branch: `git checkout master`
- As you are now in the master branch (this can be checked with `git status`!), you can perform a `git pull` to ensure the EFO 3 master branch is up to date.
- Before performing the following steps, make sure you switch to the `src/ontology` directory if you are not there already:

   `cd src/ontology`
- If you require any new mappings to be added, this should be done now by adding to the `mondo_efo_mappings.tsv` and the `mondo_terms.txt` files accordingly.
- To update the efo-edit.owl file in the master branch with the latest version from efo2 and ensure the latest copy of mondo.owl, uberon.owl and OTAR therapeutic areas file is in the mirror folder:
     `./get_mirrors.sh`
     - You may have to make `get_mirrors.sh` executable if it will not run in this way using `chmod a+x get_mirrors.sh`.
     - Alternatively, you can run with `bash get_mirrors.sh`
- You then should run `make`
     - During `make``, the efo-fixer.jar makes all of the changes, such as ensuring all definitions are using IAO_00000115 rather than the prior efo:definition and all alternative_terms are now has_exact_synonym.
Mondo-id-switcher.jar uses the tsv template of all mapped terms, mondo_efo_mappings.tsv, and switches all MONDO URIs to EFO URIs ready for import.
- **NOTE:** When generating EFO 3 for the first time, you may encounter a warning (WARN  org.obolibrary.robot.IOHelper - Catalog imports/catalog-v001.xml does not exist. Loading ontology without catalog) when first running the make command. It is necessary for this make command to be run despite potentially resulting in failure (make: *** [efo-3-edit.owl] Error 1) as it will generate the mondo_efo_import.owl file.
     - To resolve this error, open the mondo_efo_import.owl and efo-upper.owl files in Protege.
     - This creates catalog-v001.xml files used by the import process to combine MONDO and EFO.
     - The make process can then be restarted with `make -B`
          - `-B` forces the make command to run rebuild everything from the beginning, not just files that have yet to be generated etc.
     - To push changes to GitHub, follow the same procedure as with EFO 2 but ensure that, when running a git status, you are in efo3 not master.
     - When performing a git push, use `git push origin master`.

If you would like to switch back to editing EFO version 2 after pushing EFO 3 changes or running the EFO 3 pipeline, use `git checkout efo2`. If this does not work, try `git stash` then `git checkout efo2`.


## Release Manager notes

You should only attempt to make a release AFTER EFO2 has been committed and pushed.

- `git checkout master`
- `git pull`
- Edit the version.txt one increment  e.g. 3.0.0 -> 3.1.0
- `./get_mirrors.sh``
- `make`
- Once complete, check the build/efo.owl file has the correct date, correct version number and reasons well.
- You will need to clone the Bubastis source code to run locally for the EFO3 release notes. This can be found here: https://github.com/EBISPOT/bubastis. Note: Clone into a different repo, not your EFO repo!
     - `git clone git@github.com:EBISPOT/bubastis.git`
     - In your bubastis top level directory: mvn clean package
     - Go to Run → Edit configurations… or use the drop down in the top right to edit configurations.
     - Edit the config to where program arguments contains:  -ontology1 "https://github.com/EBISPOT/efo/releases/download/current/efo.owl" -ontology2 "PATH TO YOUR VERSION OF EFO 3 IN THE BUILD FOLDER" -output PATH/MONTH2019bubastisdiff.txt
     - You can now copy over the diffs to the release notes, change the version, date, no. of classes and add a new summary etc.
     - Save and exit.
- `git status`
- `git add -u`
- `git status`
- `git commit -m “EFO release 3.x.x”`
- `git push origin master`
- Go to https://github.com/EBISPOT/efo/releases/new
     - Tag version is v.3.x.x (where 3.x.x is the version e.g. v.3.0.0 or v.3.1.0)
     - Title is 2018-10-15 EFO 3.x.x
     - Attach the build/efo.owl file as an asset (you can drag from your folder to the box)
     - Write a summary of the release in the description - see previous releases for some inspiration.
- Go to [current tag](https://github.com/EBISPOT/efo/releases/tag/current) and update the assets to the latest versions
- Build EFO web through Bamboo
     - Push to staging and check the wwwdev site, if all looks good then push to production
- Inform our efo-users@ebi.ac.uk and arrayexpress-atlas@ebi.ac.uk mailing lists of the new release.


# EFO Migration steps (30. September 2019)

1. `cd src/ontology/migration2019`
1. `bash ./pre-migration.sh`
1. Manually copying the import statements from import-stamentens.owl to efo-edit.owl
1. `bash ./migration.sh`

# Step-by-step guide to create a dynamic import

1. The first thing we need is a list of all terms from the the new ontologies as they are used in efo-edit.owl. Use a custom sparql query to get a terms list (analogous to say `src/sparql/hp_terms.sparql`), using `make xyz_terms_in_src`. The make goal is already present with a wildcard - you dont need to add anything. Example: `make hp_terms_in_src`
1. Download a mirror of the ontology that is supposed to be integrated. Usually we just add the ontology to the src/ontology/mirror directory. Add a respective command to `get_mirrors.sh`.
1. Determine which axioms to preserve:
   1. Create a new CONSTRUCT sparql query, for example by duplicating `../sparql/preserve_hp_axioms.sparql` (to, for example: `../sparql/preserve_cl_axioms.sparql`). This query needs to capture all axioms you want to preserve which contain classes from the namespace you are about to remove.
   1. Once the query is done and in the correct place, you can run the full migration pipeline using `make dump_xyz`, e.g. `make dump_hp`
1. Review the efo-edit.owl diff now and undo unintended changes.
   1. LOGICAL DEFINITIONS ARE CURRENTLY NOT REMOVED! For HP, these had to be removed (semi) manually using ROBOT remove equivalent.
	 1. I would recommend to run build/efo-edit-functional.owl and search equivalentclass axioms in Atom with a query such as `EquivalentClasses[(]obo:CL`
	 1. In the last meeting (Zoe, Nico) we decided to preserve logical axioms by default, due to the major effort an reviewing them all individually (it is impossible to tell which ones come from which context)
1. Add relevant import redirect to catalog.xml
1. Add ontology to the list of imports `IMPORTS = mondo hancestro uberon hp`
1. Add the `imports/hp_terms.txt` and `imports/hp_import.owl` goals as specified for your specific ontology import ONLY if you need to customise it. By default, if you dont add anything, the module that is extracted contains only those terms that are specified in `iri_dependencies/%_terms.txt` and relations in `iri_dependencies/efo_relations.txt`.
1. Add ontology import statement to efo-edit.owl
1. Run release
1. Run `make all_diffs` and make sure all is in order (entity diff and axiom diff ROBOT most importantly)


