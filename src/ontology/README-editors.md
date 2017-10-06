These notes are for the EDITORS of efo

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

    cd src/ontology
    make

If this looks good type:

    make prepare_release

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

