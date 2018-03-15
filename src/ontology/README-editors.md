These notes are for the EDITORS of efo

For the full description of the release process including the internal-link specific information, please make sure that you see https://www.ebi.ac.uk/seqdb/confluence/display/FGPTO/EFO+Release+Process !!!! This is vital if you are the EFO developer in charge of monthly release.

This project was created using the [ontology starter kit](https://github.com/cmungall/ontology-starter-kit). See the site for details.

## Editors Version

The editors version is [efo-edit.owl](efo-edit.owl)

** DO NOT EDIT efo.obo OR efo.owl in the top level directory **

[../../efo.owl](../../efo.owl) is the release version

To edit, open the file in Protege. First make sure you have the repository cloned, see [the GitHub project](https://github.com/EBISPOT/efo) for details.


## Release Manager notes

You should only attempt to make a release AFTER the edit version is
committed and pushed.

to release:
First, update the version number in the /efo/src/ontology/version.txt. This is usually an increment of +1 in the monthly release version.
You can do this with vi or other text editing program. Make sure to push this version.txt file before you do the release in the next step.



    cd src/ontology
    make

This step generates efo.obo, efo.owl and its derivatives in /src/ontology. We need to manually fix efo.obo before it gets released to the top level. 

## Edit OBO version

A few manual hacks are required to get this to parse in OBO however.

As of EFO 2.91, the OBO generator still creates duplicate subsetdefs. This is non-critical in most cases but it appears to break EnsEMBL process. Manual clean-up is required by deleting the following duplicate lines from efo.obo at the top level. A ticket has been filed for this error in the release script.

Open ../../efo.obo

Remove the following "duplicate" line (please make sure there is one of each duplicates remain in the file)

    subsetdef: efo_slim "efo slim"
    subsetdef: grouping_class "grouping class"
    subsetdef: organ_slim "organ slim"
    subsetdef: uberon_slim "uberon slim"
    subsetdef: vertebrate_core "vertebrate core"


Now, add EFO root class and top relationship

    Add EFO root for class:
---

[Term] 

id: EFO:0000001

name: experimental factor

def: "An experimental factor in Array Express which are essentially the variable aspects of an experiment design which can be used to describe an experiment, or set of experiments, in an increasingly detailed manner. This upper level class is really used to give a root class from which applications can rely on and not be tied to upper ontology classses which do change." []

created_by: James Malone

---

    Add top relationship:

---

[Typedef]

id: EFO:0000824

name: relationship

---
 

At this point, all files should be ready to be copied over to the top-level directory.

If there are no errors after you make the file, and you have edited efo.obo, type:

make release


    make release

This generates derived files such as efo.owl and efo.obo and places
them in the top level (../..). The versionIRI will be added.

At this point, please check your local copy of the top-level efo.owl and see if everything looks ok (e.g. the version is updated and reflecting the current to-be-released version, the date is correct).



## Update release notes

Release notes detailing major changes between releases are produced to aid users awareness.

You will modify the release notes file:

    https://github.com/EBISPOT/efo/blob/master/ExFactor%20Ontology%20release%20notes.txt

The sections you will need to replace or modify should be obvious. To write the release notes use the Bubastis tool  http://www.ebi.ac.uk/efo/bubastis

Historically, Bubastis used to be able to process the diff between the penultimate release (non-inferred, merged efo.owl) and the latest release. This function, however, has stopped working. Alternately, you will download the previous release onto your machine and run Bubastis by uploading files from your local machine as followed:

a. Get the files of the latest and penultimate release (non-inferred) OWL files on Github history of the released EFO (top-most level efo.owl) at https://github.com/EBISPOT/efo/commits/master/efo.owl. 

b. Point Bubastis to these 2 files in your local machine. Important: 'Ontology 1' in Bubastis must be the old version, 'Ontology 2' must be the new version! Leave all the 'diff options' turned on.

c. Copy the "Classes modified" section of the diff into the Section 4 ("4. Change log") of the release notes file

d. Copy the "New classes" section of the diff into the Section 2 ("2. New to EFO") of the release notes file

e. Copy the "Deleted classes" section of the diff into the Section 3 ("3. Obsolete Classes") of the release notes file

f. If any URIs are deprecated and there is a replacement URI to use (e.g. one of a pair of duplicate classes was made obsolete), document these in "Section 1. Changes to URIs". Include the old URI, old name, new URI and new name (and optionally a comment). Also, inform (by email) the ArrayExpress / Atlas database curators! Note - there is no way to know this from the diff itelf, only from your own records of the edits made !

g. Update the total number of classes included in this release in "Summary" (available through Protege 'Window->Views->Ontology views->Ontology metrics')

h. Set the release version number correctly

i. Set the date correctly

j. Add a short paragraph to "Summary:" summarising any major activity that has occurred over the previous month

k. Save the file.


Commit and push these files.

    git commit -a

And type a brief description of the release in the editor window

Finally type

    git push origin master

IMMEDIATELY AFTERWARDS (do *not* make further modifications) go here:
 * https://github.com/EBISPOT/efo/releases/new
Click "Edit" and make change to reflect THIS release you are working on (the one you've just pushed to master branch in the previous step).

The value of the "Tag version" field MUST be

vYYYY-MM-DD

The initial lowercase "v" is REQUIRED. The YYYY-MM-DD must match what is in the versionIRI of the derived efo.owl (data-version in efo.obo).

Release title should be YYYY-MM-DD, optionally followed by a title (e.g. "2017-12-15 EFO 2.91")

Then click "publish release"

__IMPORTANT: NO MORE THAN ONE RELEASE PER DAY.__

On https://github.com/EBISPOT/efo/tags  - you should see the tag you have just added appear as the new tag on there.

Now if you go to https://github.com/EBISPOT/efo/releases/ - you will see the tag you have just added to Github. Use this link to edit the description should you wish to.

 

The PURLs are already configured to pull from github. This means that BOTH ontology purls and versioned ontology purls will resolve to the correct ontologies. Try it!

    http://www.ebi.ac.uk/efo/efo.owl <-- current ontology PURL
    http://www.ebi.ac.uk/efo/releases/vYYYY-MM-DD/efo.owl <-- change to the release you just made
    
## Run 'Build EFO Web' Bamboo plan

    go to http://gromit.ebi.ac.uk:10001/browse/EFO
    click on the plan 'Build EFO Web'
    If the run is successful, manually go into the plan and promote it to wwwdev (staging), and www (prod) respectively.

## Finally, announce the new release by mailing:

    arrayexpress-atlas@ebi.ac.uk
    efo-users@lists.sourceforge.net
    efo-users@ebi.ac.uk
    
NOTE THAT SOURCEFORGE MAILING LIST WILL NO LONGER BE IN USE FROM MID 2018.

---

** Note: Should you need to delete a release/tag, follow these step and re-tag / re-release:
Delete release (https://help.github.com/articles/editing-and-deleting-releases/):

    On GitHub, navigate to the main page of the repository.
    Under your repository name, click Releases.
    On the Release page, click the name of the release you wish to delete.
    In the upper-right corner of the page, click Delete.

Delete tag:

    Do a git pull to retrieve the tag you have created on Github

    git tag -d tagName

    git push --delete origin tagName

********************NOW GO BACK TO FIX WHAT NEEDS TO BE FIXED AND COMMIT/PUSH/RE-TAG***************************
