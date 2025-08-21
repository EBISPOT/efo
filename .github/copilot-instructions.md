# Experimental Factor Ontology Project Guide

This includes instructions for editing the efo ontology. 

## Project Layout
- Main development file is `src/ontology/efo-edit.owl` (OWL/XML syntax)
- ODK and ontology documentation can be found in `/docs/`

## Querying ontology

- Use grep/rg to find terms, but be aware that in RDF/XML files like efo-edit.owl, axioms may span multiple lines.
    - `grep -i ATAC-seq src/ontology/efo-edit.owl` - all axioms that mention ATAC-seq
    - `grep '<rdfs:label.*ATAC-seq' src/ontology/efo-edit.owl` - all label axioms that mention ATAC-seq
- All mentions of an ID
    - `obo-grep.pl -r 'EFO_:_0007045' src/ontology/efo-edit.owl`
- Only search over `src/ontology/efo-edit.owl`
- DO NOT bother doing your own greps over the file, or looking for other files, unless otherwise asked, you will just waste time.
- ONLY use the methods above for searching the ontology

## Before making edits
- Read the request carefully and make a plan, especially if there is nuance
- If related issues are mentioned read them: `gh issue view GITHUB-ISSUE-NUMBER`
- Try identify if there are PMID or doi either in the title or in the body of the issue
- if a PMID or doi is mentioned in the issue, ALWAYS try and read it
- ALWAYS check proposed parent terms for consistency

## Editors guide
- When you are finished editing the efo-edit.owl file, please normalize by running:

```bash
cd src/ontology #If you are not in the ontology folder
make normalize_src
```

- For any edition that does not involve obsoleting terms, there is no need to add a 'term tracker item' pointing to the GitHub issue
- For importing new terms, please read carefully the doumentation in `/docs/Import_terms_from_another_ontology.md`
- Only add subclass axioms in subclasses.csv when linking terms from different ontologies (e.g., EFO ⊑ OBA), and never if the axiom already exists in EFO or its imports. If the ticket asks for a parent term that is already in the imported ontology, do NOT add the relationship in the `subclasses.csv` file
  - ALWAYS first import the term before adding it to `subclasses.csv`
  - Check in the owl file of the ontology that is being updated if the relationship already exist

## OBO Guidelines
- Term ID format: EFO_NNNNNNN (7-digit number)
- Handling New Term Requests (NTRs):
  - New terms start  EFO_092xxxx
  - Do `grep EFO_092 src/ontology/efo-edit.owl` to check for clashes
- Each term requires: id, name, definition with references
- Never guess EFO IDs, or ontology term IDs, use search tools above to determine actual term
- Never guess PMIDs for references, do a web search if needed
- Use standard relationship types: is_a, part_of, realizes, etc.
- Follow existing term patterns for consistency

## Publications
- Run the command `aurelian fulltext <PMID:nnn>` to fetch full text for a publication. A doi or URL can also be used
- You should cite publications appropriately, e.g. `def: "...." [PMID:nnnn, doi:mmmm]

## GitHub Contribution Process
- Most requests from users should follow one of two patterns:
    - You are not confident how to proceed, in which case end with asking a clarifying question (via `gh`)
    - you are confident how to proceed, you make changes, commit on a branch, and open a PR for the user to review
- Check existing terms before adding new ones
- For new terms: provide name, definition, place in hierarchy, and references
- Include PMIDs for all assertions
- Follow naming conventions from parent terms
- Always commit in a branch, e.g. issue-NNN
- Don't commit the tools directory or anything from it
- If there is an existing PR which you started then checkout that branch and continue, rather than starting a new PR (unless you explicitly want to abandon the original PR, e.g. it was on completely the wrong tracks)
- Always make clear detailed commit messages, saying what you did and why
- Always sign your commits `@dragon-ai-agent`
- Create PRs using `gh pr create ...`
- File PRs with clear descriptions, and sign your PR

## Handling GitHub issues and requests
- Use `gh` to read and write issues/PRs
- Sign all commits and PRs as `@dragon-ai-agent`

## TROUBLESHOOTING

- If your obo file has syntax errors, you can use `robot convert -vvv` to see full trace
- Use `robot reason` to validate

## How to Obsolete a Term in EFO
### Overview
This guide describes the steps to obsolete an existing EFO term in the ontology. Obsoleting a term ensures that it is no longer used in annotation while preserving its historical context and mapping to replacement terms when appropriate.
obsolete terms should have no logical axioms (e.g. SubClassOf, EquivalentClasses) on them. Obsolete terms may be replaced by a single term (so-called obsoletion with exact replacement), or by zero to many `consider` tags.

### Steps
1. Locate the term to be obsoleted

	- Search for the term in the efo-edit.owl file.
	- Confirm the term’s IRI (e.g., http://www.ebi.ac.uk/efo/EFO_1000022).

2. Update the term

	- Prefix the label with obsolete_.
	- Mark the term as deprecated.
	- Add efo:obsoleted_in_version with the next ontology release version.
		- If the current EFO version is X.YY.Z, set efo:obsoleted_in_version to X.(YY+1)
			Example: 3.80.0 → 3.81
		- The release version can be found in the 'ExFactor Ontology release notes.txt' file, in line 14 (example: Experimental Factor Ontology version 3.80.0).
        - Update the ontology version only when a term is newly obsoleted.
        - If you are editing a term that is already obsoleted (e.g., changing its term_replaced_by target or other metadata), do not update the version.
	- If the obsolete term has a direct replacement, add the annotation property obo:IAO_0100001 (term replaced by) with the full IRI of the replacement term.
	- Add efo:reason_for_obsolescence describing the reason and replacement that you will find in the GitHub ticket.
	- Synonyms and xrefs can be migrated judiciously.

3. Example

```
    <!-- http://www.ebi.ac.uk/efo/EFO_1000022 -->

    <owl:Class rdf:about="http://www.ebi.ac.uk/efo/EFO_1000022">
        <obo:IAO_0000117>Catherine Leroy</obo:IAO_0000117>
        <obo:IAO_0100001>http://www.ebi.ac.uk/efo/EFO_1000172</obo:IAO_0100001>
        <efo:obsoleted_in_version>2.65</efo:obsoleted_in_version>
        <efo:reason_for_obsolescence>use : EFO_1000172 label : cervicals quamous cell carcinoma</efo:reason_for_obsolescence>
        <rdfs:label>obsolete_cervical squamous cell carcinoma</rdfs:label>
        <owl:deprecated rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</owl:deprecated>
    </owl:Class>
```
4. Update subclasses of the obsolete term. No relationship should point to an obsolete term:
	- Search for usage of the obsolete term in:
		- efo-edit.owl — Replace all occurrences of the full IRI of the obsolete term in other classes (maintain IRI as it is in the obsoleted term) with the full IRI of the replacement term.
		- src/templates/subclasses.csv — Check the column "Type (is-a)". If the obsolete term’s ID (e.g., EFO:XXXXXXX) appears in this column, replace it with the replacement term’s ID.
			- Rebuild the 'sublasses.owl' component:

```bash
cd src/ontology #If you are not in the ontology folder
make components/subclasses.owl      
```


5. Commit changes

	- Commit to the repository with a message such as:
		Obsoleted EFO_1000022; replaced with EFO_1000172


## Other metadata

- Link back to the issue you are dealing with using the `term_tracker_item`
- All terms should have definitions, with at least one definition xref, ideally a PMID
- You can sign terms as `<obo:IAO_0000117>dragon-ai-agent</obo:IAO_0000117>` (without the @ symbol)

## Relationships

**All terms** must have at least one `is_a` (SubClassOf to a named class). This can be explicit or implicit via a logical definition.  
- Many terms in this ontology have `part_of` relationships to UBERON terms where applicable.  

### Additional domain-specific expectations 
- **Disease terms** should have a `has_disease_location` relationship to an appropriate anatomical entity.  
  - This relationship may be inherited from a parent or ancestor term; explicit addition is not required if inherited.  
  - If the issue is not providing this relationship, **make a comment in the PR**.  
- **Measurement terms** should have an `is_about` relationship to the entity or process being measured  
  (e.g., `sleep measurement` → `is_about` some `sleep`).  
  - If the issue is not providing this relationship, **make a comment in the PR**. 

## Logical definitions

These should follow genus-differentia form, and the text definition should mirror the logical definition. Example:

```
    <!-- http://www.ebi.ac.uk/efo/EFO_0020865 -->

    <owl:Class rdf:about="http://www.ebi.ac.uk/efo/EFO_0020865">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.ebi.ac.uk/efo/EFO_0001444"/>
                    <owl:Class>
                        <owl:unionOf rdf:parseType="Collection">
                            <owl:Restriction>
                                <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/BFO_0000050"/>
                                <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/UBERON_0000947"/>
                            </owl:Restriction>
                            <owl:Restriction>
                                <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/IAO_0000136"/>
                                <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/UBERON_0000947"/>
                            </owl:Restriction>
                        </owl:unionOf>
                    </owl:Class>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
        <rdfs:subClassOf rdf:resource="http://www.ebi.ac.uk/efo/EFO_0004298"/>
        <obo:IAO_0000115>Measurement of some parts of the aorta, including ascending aorta distensibility and area.</obo:IAO_0000115>
        <obo:IAO_0000117>Annalisa Buniello</obo:IAO_0000117>
        <dc:creator>Zoe May Pendlington</dc:creator>
        <dc:date rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2022-02-14T09:22:02Z</dc:date>
        <oboInOwl:hasExactSynonym>aortic diagnostic technique</oboInOwl:hasExactSynonym>
        <rdfs:label xml:lang="en">aortic measurement</rdfs:label>
    </owl:Class>
```

The reasoner can find the most specific `is_a`, so it's OK to leave this off.

