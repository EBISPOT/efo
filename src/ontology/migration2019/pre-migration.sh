#This script is only to be run once on 30th September 2019
set -e
git checkout master ../efo-edit.owl
java -jar ../../../bin/efo-fixer.jar ../efo-edit.owl efo-edit-fixed.owl
robot diff -l ../efo-edit.owl -r efo-edit-fixed.owl -o efo-edit-diff.txt
#At this point, manually copy the import statements from import-statements.owl to efo-edit-fixed.owl
#The reason for this is that using ROBOT causes too many problems with the default namespace
#cd ..
#robot merge --catalog catalog-v001.xml --collapse-import-closure false -i ./migration2019/import-statements.owl -i ./migration2019/efo-edit-fixed.owl -o ./migration2019/efo-edit-imports.owl
#cd ./migration2019
sed -i '' '/- AnnotationAssertion.*HPO[:]skoehler.*/d' efo-edit-diff.txt
sed -i '' '/- AnnotationAssertion.*HPO[:]probinson.*/d' efo-edit-diff.txt
sed -i '' '/- AnnotationAssertion.*patterns#createdBy>.*/d' efo-edit-diff.txt
sed -i '' '/- AnnotationAssertion.*bioportal_provenance>.*>.*/d' efo-edit-diff.txt
sed -i '' '/- AnnotationAssertion.*alternative_term>.*/d' efo-edit-diff.txt
sed -i '' '/- AnnotationAssertion.*_definition_citation>.*/d' efo-edit-diff.txt
echo "Pre-migration done. IMPORTANT: Please manually add the import statements from import-statements.owl to efo-edit-fixed.owl!"