These notes are for the EDITORS of efo

This project was created using the [ontology starter kit](https://github.com/cmungall/ontology-starter-kit). See the site for details.

## Editors Version

The editors version is [efo-edit.owl](efo-edit.owl)

** DO NOT EDIT efo.obo OR efo.owl in the top level directory **

[../../efo.owl](../../efo.owl) is the release version

To edit, open the file in Protege. First make sure you have the repository cloned, see [the GitHub project](https://github.com/EBISPOT/efo) for details.

## Update release notes and e-mail announcement to users

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

k. Copy the file to your directory for the external (SourceForge) repository) update both in the internal and external (SourceForge) SVN:

    .../ExperimentalFactorOntology/ReleaseDocs/"ExFactor Ontology release notes.txt" (internal repository)
    .../efo/trunk/docs/releasedocs/"ExFactor Ontology release notes.txt" (external (SourceForge) repository)

l. Finally, announce the new release by mailing:

    arrayexpress-atlas@ebi.ac.uk
    efo-users@lists.sourceforge.net
    efo-users@ebi.ac.uk
    
NOTE THAT SOURCEFORGE MAILING LIST WILL NO LONGER BE IN USE FROM MID 2018.

## Release Manager notes

You should only attempt to make a release AFTER the edit version is
committed and pushed.

to release:

    cd src/ontology
    make

If this looks good type:

    make release

This generates derived files such as efo.owl and efo.obo and places
them in the top level (../..). The versionIRI will be added.

Commit and push these files.

    git commit -a

And type a brief description of the release in the editor window

Finally type

    git push origin master

IMMEDIATELY AFTERWARDS (do *not* make further modifications) go here:

 * https://github.com/EBISPOT/efo/releases
 * https://github.com/EBISPOT/efo/releases/new

The value of the "Tag version" field MUST be

    vYYYY-MM-DD

The initial lowercase "v" is REQUIRED. The YYYY-MM-DD *must* match
what is in the versionIRI of the derived efo.owl (data-version in
efo.obo).

Release title should be YYYY-MM-DD, optionally followed by a title (e.g. "january release")

Then click "publish release"

__IMPORTANT__: NO MORE THAN ONE RELEASE PER DAY.

The PURLs are already configured to pull from github. This means that
BOTH ontology purls and versioned ontology purls will resolve to the
correct ontologies. Try it!

 * http://purl.obolibrary.org/obo/efo.owl <-- current ontology PURL
 * http://purl.obolibrary.org/obo/efo/releases/YYYY-MM-DD.owl <-- change to the release you just made

For questions on this contact Chris Mungall or email obo-admin AT obofoundry.org

