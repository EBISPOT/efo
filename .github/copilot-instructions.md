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

## Critical Pre-Creation Checks

### BEFORE Creating Any New Term:

1. **MANDATORY OLS Search for Existing Terms**
   - **ALWAYS search OLS MCP** to check if the term already exists in ontologies we import from (MONDO, UBERON, CL, CHEBI, GO, OBI, etc.)
    - If term exists in an imported ontology:
      - **DO NOT create a new EFO term**
      - Instead, add the term IRI to the appropriate file in `src/ontology/iri_dependencies/`
      - Call @EFO-importer to handle the import
     - **NO curation is needed** for imported terms
    - Only create new EFO terms if:
      - Term does not exist in any imported ontology
      - Term is EFO-specific (e.g., experimental factors, assays)

2. **Verify Parent Terms and Relationships Are Not Obsolete**
  - **ALWAYS check** that any term used for classification or relationships is NOT obsolete
  - Check for parent terms (SubClassOf relationships)
  - Check for any object property relationships (part_of, realizes, etc.)
  - Search for `owl:deprecated` or `obsolete_` prefix in the term's label
  - If parent/related term is obsolete:
    - Find the replacement term (check `obo:IAO_0100001` term_replaced_by annotation)
    - Use the replacement term instead
    - If no replacement exists, request clarification from the user

3. **RO Terms in efo-relations.txt**
  - **DO NOT add RO (Relation Ontology) terms** to `src/ontology/efo-relations.txt` unless explicitly specified by the user
  - RO terms should be imported via the standard import mechanism
  - Only add non-standard or EFO-specific relations to efo-relations.txt

4. **Search Before Adding New Terms**
  - **ALWAYS search for existing terms** before proposing any new term
  - Search for similar labels:
    - `grep -i "term_name" src/ontology/efo-edit.owl`
    - Search OLS for the concept using OLS MCP tools
  - Search for synonyms:
    - `grep -i "alternative_name" src/ontology/efo-edit.owl`
  - If similar terms exist:
    - Comment on the issue asking if new term is needed
    - Propose modifications to existing term instead
    - Wait for curator confirmation before creating new term
  - Check for related term issues:
    - Are there open issues about similar terms?
    - Are similar terms flagged as problematic?
  - Example search:
    ```bash
    grep -i "diffus.*capacity\|DLCO" src/ontology/efo-edit.owl
    ```

## Import Policy - CRITICAL

**ALL IMPORTS MUST BE DELEGATED TO @EFO-importer**

- **NEVER perform imports yourself** - always call @EFO-importer
- This applies to:
  - Parent terms from external ontologies (MONDO, UBERON, CL, etc.)
  - Terms needed for relationships (is_about, part_of, etc.)
  - Any term from outside EFO that needs to be referenced
- The EFO-importer agent has specialized knowledge of:
  - OLS search and verification
  - IRI dependency management
  - Mirror updates and import regeneration
  - Bidirectional term validation

**When you identify an import need:**
1. Stop your workflow
2. Call @EFO-importer with the term label/s and expected ontology
3. Wait for import confirmation
4. Then proceed with your task using the imported term

### Before answering import-related questions
1. REQUIRED: Delegate to @EFO-importer for actual import operations
2. You may read docs/Import_terms_from_another_ontology.md for context
3. Never execute import commands yourself

### Essential import workflow (for reference only - delegate to @EFO-importer)
The instructions below are for understanding the import process.
**DO NOT execute these yourself - always call @EFO-importer instead.**

- Edit the IRI dependency lists, never the generated imports:
  - Edit files in `src/ontology/iri_dependencies/` (e.g. `mondo_terms.txt`, `cl_terms.txt`).
  - Each line must be the full IRI of the term to import.
  - DO NOT edit anything in `src/ontology/imports/` (these are generated).
./get_mirrors.sh
```

- Regenerate a single import (from `src/ontology`):

```bash
cd src/ontology
make imports/[ontology]_import.owl -B
# example: make imports/uberon_import.owl
```

- Regenerate all imports (if needed):

```bash
make all_imports -B
```

- What the make target does:
  - Reads `iri_dependencies/[ontology]_terms.txt`, resolves IRIs using mirrors and writes a generated `.owl` into `src/ontology/imports/` and a backup copy of the term list.

- Fix dangling imported terms (no asserted parent):
  1. Add a row to `src/templates/subclasses.csv` with `ID_OF_IMPORTED_TERM,ID_OF_PARENT_TERM_IN_EFO`.
  2. Rebuild the component:
```bash
cd src/ontology
make components/subclasses.owl
```

Notes:
- Always run `./get_mirrors.sh` before `make` when updating imports.
- Do not edit generated `.owl` files directly. Make changes in the `iri_dependencies/` text files or `src/templates/subclasses.csv` as appropriate.

**REMINDER: The above workflow is for reference only. Always delegate actual import operations to @EFO-importer.**

### Minimal verification checklist (for @EFO-importer)
- Confirm the IRI you add is valid (correct prefix and IRI syntax).
- Verify the term exists in the local mirror (or OLS) after `./get_mirrors.sh`.
- When adding subclass assertions, ensure the parent exists in EFO or its imports and that the relationship is not already present upstream.

### Potential pitfalls (for @EFO-importer)
- Stale mirrors: forgetting `./get_mirrors.sh` causes unresolvable IRIs. Mitigation: always run mirrors update and include it in PR description when imports change.
- Editing generated files: modifying files under `src/ontology/imports/` will be overwritten and is discouraged. Mitigation: only edit `src/ontology/iri_dependencies/*.txt` or `src/templates/subclasses.csv`.
- Missing parent relationships: imported terms can become dangling. Mitigation: prefer using `subclasses.csv` to assert parentage and run `make components/subclasses.owl`.
- Caching/build issues: use `-B` to force rebuild when results look stale.
- Incorrect subclass assertions: do not add subclass axioms for relationships that already exist in the source ontology or in EFO imports; check source OWL first.

If you need the full, unabridged procedure, consult `docs/Import_terms_from_another_ontology.md` (this file must remain authoritative).

**CRITICAL: Do not perform imports yourself. Always call @EFO-importer for any import operation.**

- Only add subclass axioms in subclasses.csv when linking terms from different ontologies (e.g., EFO ⊑ OBA), and never if the axiom already exists in EFO or its imports. If the ticket asks for a parent term that is already in the imported ontology, do NOT add the relationship in the `subclasses.csv` file
  - ALWAYS first call @EFO-importer to import the term before adding it to `subclasses.csv`
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
- Include PMIDs for all assertions
- Follow naming conventions from parent terms
- Always commit in a branch, e.g. issue-NNN
- Don't commit the tools directory or anything from it
- If there is an existing PR which you started then checkout that branch and continue, rather than starting a new PR (unless you explicitly want to abandon the original PR, e.g. it was on completely the wrong tracks)
- Always make clear detailed commit messages, saying what you did and why
- Create PRs using `gh pr create ...`
- File PRs with clear descriptions

## Handling GitHub issues and requests
- Use `gh` to read and write issues/PRs

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
    - src/templates/subclasses.csv — Check the column "Type (is-a)". If the obsolete term's ID (e.g., EFO:XXXXXXX) appears in this column, replace it with the replacement term's ID.
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
- You can sign terms as `<obo:IAO_0000117>AI agent</obo:IAO_0000117>` (without the @ symbol)

### CRITICAL: Reference Requirements for New Terms

**MINIMUM 2 PMID REFERENCES REQUIRED**

- **All new terms MUST have at least 2 PMID cross-references**
- PMIDs should be attached **directly to the definition** using `<oboInOwl:hasDbXref>` within the definition annotation
- Prefer PMID over DOI for references
- Example format (see EFO:0700018):

```xml
<obo:IAO_0000115 rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Definition text here.
    <oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">PMID:12345678</oboInOwl:hasDbXref>
    <oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">PMID:87654321</oboInOwl:hasDbXref>
</obo:IAO_0000115>
```

- If EFO-curator provides PMIDs, use those
- If insufficient PMIDs provided, request additional literature search from EFO-curator
- **DO NOT proceed with term creation** if fewer than 2 PMIDs are available

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

## When using OLS MCP for term IDs
1. NEVER guess or interpolate IDs - only use exact matches from OLS
1. If you provide a term ID retrieved from a query, always verify with a second query
1. If uncertain about a term ID, explicitly state "This ID needs verification"
1. If you have retrieved multiple terms IDs to be imported, query all the IDs into OLS and check that the ID matches with the term you were looking (in label or synonym)



## Multi-Agent Coordination

This section describes how to coordinate work across the three specialized EFO agents. The workflow orchestration is managed by these instructions, not by individual agents.

### Agent Roles and Capabilities

#### EFO-curator
**Purpose**: Literature research, evidence gathering, and term validation  
**Calls when**: You need to analyze publications, extract definitions, validate scientific accuracy  
**Inputs to provide**: PMIDs/DOIs, issue context, specific questions  
**Outputs expected**: Curated definitions, parent term candidates, synonyms with categorization, cross-references (minimum 2 PMIDs/DOIs)

**Synonym Categorization by EFO-curator:**
- EFO-curator should categorize synonyms by type:
  - **Abbreviations/Acronyms** → Mark as `hasRelatedSynonym` (e.g., "5-ASA" for "5-aminosalicylic acid")
  - **Brand names/Narrow terms** → Mark as `hasNarrowSynonym` (e.g., "Asacol" for "mesalamine")
  - **Exact synonyms** → Mark as `hasExactSynonym`
  - **Broader terms** → Mark as `hasBroadSynonym`
- EFO-curator should provide this categorization in the curation report
- Example format:
  ```
  Synonyms:
  - 5-aminosalicylic acid (hasExactSynonym)
  - 5-ASA (hasRelatedSynonym - abbreviation)
  - mesalazine (hasExactSynonym)
  - Asacol (hasNarrowSynonym - brand name)
  - Pentasa (hasNarrowSynonym - brand name)
  ```

#### EFO-importer  
**Purpose**: External term imports and IRI management  
**Calls when**: **ALWAYS when ANY term needs importing from external ontologies** (MONDO, UBERON, CL, CHEBI, GO, OBI, etc.)  
**Critical**: ALL import operations MUST be delegated to this agent - never perform imports yourself  
**Inputs to provide**: Term names or IDs to import, target ontology  
**Outputs expected**: Updated iri_dependencies files, regenerated imports, verified IRIs

#### EFO-ontologist  
**Purpose**: Direct OWL/XML editing in efo-edit.owl  
**Calls when**: You need to add/edit/obsolete terms, add relationships, update metadata or search terms in efo-edit.owl
**Inputs to provide**: Complete term specifications (ID, label, definition with 2+ PMIDs, parent, synonym types, xrefs)  
**Outputs expected**: Updated efo-edit.owl, normalized file, git commits

**For detailed technical specifications**, see `.github/agents/EFO-ontologist.md`:
- How to implement synonym types (XML format for each type)
- How to embed PMIDs in definitions (nested oboInOwl:hasDbXref format)
- How to verify parents are not obsolete (grep patterns and replacement logic)
- RO terms restriction for efo-relations.txt
- OWL/XML formatting patterns
- Logical definition templates

### Common Workflow Patterns

#### Pattern 1: New Term Request (NTR) with PMID

```
Step 1: Call @EFO-curator
  Task: Analyze PMID:12345678 for issue #XXXX and extract new term details
  Extract: Definition, parent candidates, synonyms, related terms
  Context: [brief issue summary]
  
Step 2: Review curator output
  Validate: Definition quality, parent term appropriateness
  Decision: Accept, modify, or request clarification
  
Step 3a: If imports needed → ALWAYS call @EFO-importer
  Task: Import [list of terms] from [ontology]
  Verify: Terms exist in source, relationships are correct
  CRITICAL: Never skip this step - all imports must go through EFO-importer
  
Step 3b: If no imports → Skip to Step 4

Step 4: Call @EFO-ontologist
  Task: Add new term to efo-edit.owl
  Provide: Complete specification from Steps 1-3
  Include: ID (EFO_092xxxx), label, definition with xrefs, parent(s), synonyms
```

#### Pattern 2: Import-Only Request

```
Step 1: ALWAYS call @EFO-importer
  Task: Import MONDO:1234567 (disease name) for issue #XXXX
  Verify: Term exists, check if parent assertion needed
  CRITICAL: Never attempt to import yourself
  
Step 2: If dangling term → Call @EFO-ontologist
  Task: Add subclass assertion in subclasses.csv
  Specify: Imported term → EFO parent
  Note: Only if relationship doesn't exist upstream
```

#### Pattern 3: Obsolete Term with Replacement

```
Step 1: Verify replacement term exists
  Check: Use grep/obo-grep.pl in efo-edit.owl
  If missing: Follow Pattern 1 or 2 to add it first
  
Step 2: Call @EFO-ontologist
  Task: Obsolete EFO_XXXXXXX with replacement EFO_YYYYYYY
  Provide: Issue number, reason for obsolescence
  Ensure: All references updated (efo-edit.owl + subclasses.csv)
```

#### Pattern 4: Complex Curation (multiple PMIDs, conflicting sources)

```
Step 1: Call @EFO-curator
  Task: Reconcile conflicting definitions from PMID:AAA, PMID:BBB, PMID:CCC
  Request: Evidence-based recommendation with confidence assessment
  Context: [describe conflict]
  
Step 2: Review and decide
  Options: Accept curator recommendation, request additional research, consult user
  
Step 3-4: Follow Pattern 1 steps 3-4
```

### Handoff State Tracking

When delegating to an agent, always provide:

1. **Issue context**: GitHub issue number and brief summary
2. **Current state**: What's been done, what's pending
3. **Specific task**: Clear, actionable request
4. **Expected output**: What you need back to continue
5. **Dependencies**: Terms that must exist first, files that must be updated

Example handoff:
```
@EFO-curator Please analyze PMID:30215383 for issue #2546

Context: Adding bronchiectasis endotype terms
Current state: Parent term MONDO:0004822 exists in EFO
Task: Extract definitions and parent candidates for:
  - neutrophilic bronchiectasis
  - eosinophilic bronchiectasis
  - mixed granulocytic bronchiectasis
  - paucigranulocytic bronchiectasis

Expected output:
  - Definition for each term (with confidence)
  - Parent term recommendation (likely all → MONDO:0004822)
  - Synonyms and cross-references
  - Any additional PMIDs for validation

Dependencies: None, proceed with analysis
```

### Preconditions for Adding New Terms (MANDATORY)

Before requesting @EFO-ontologist to edit `src/ontology/efo-edit.owl` for **any new term**, the following must be present:

**Required from @EFO-curator:**
- Curator output attached: definitions, **minimum 2 PMIDs/DOIs**, synonyms **with type categorization** (exact/related/narrow/broad), suggested parent(s), and confidence assessment
- OR explicit curator sign-off: `@EFO-curator: SIGN-OFF`

**Required from @EFO-importer (if applicable):**
- Import completion confirmed for any external terms needed

**Required term specification:**
- Label
- Textual definition with **minimum 2 PMIDs embedded as xrefs**
- Parent term(s) - **VERIFIED as non-obsolete**
- Synonyms (if any) - **WITH type categorization** (exact/related/narrow/broad)
- Logical definitions and relationships (if applicable)

**EFO-ontologist MUST verify these preconditions.** If any are missing, refuse to proceed and respond with:

```
Cannot proceed: missing [specific items].
Please call @EFO-curator for [what's needed]
OR call @EFO-importer for [what import is needed]
```

**Example refusal:**
```
Cannot proceed: missing curator sign-off and definitions for new term 'ATAC-seq peak intensity'.
Please call @EFO-curator to research and validate this term first.
```

**For PRs adding new terms, include this checklist:**
```markdown
- [ ] Curator output attached or @EFO-curator sign-off provided
- [ ] @EFO-importer confirmed necessary imports (if any)
- [ ] Complete term spec provided (label, definition, parent(s), synonyms)
```

### Decision Points and Routing

**When to handle directly vs delegate:**

| Scenario | Action |
|----------|--------|
| Simple grep/search query | Handle directly with tools |
| Term exists, just needs minor edit | Call @EFO-ontologist |
| PMID mentioned but no definition provided | Call @EFO-curator first |
| **ANY import needed** | **ALWAYS call @EFO-importer** |
| **New term request** | **ALWAYS call @EFO-curator first, then @EFO-ontologist** |
| Complex multi-step workflow | Orchestrate sequence yourself |
| User asks "what should I do?" | Analyze and recommend, don't auto-execute |

**Quality checks before handing off:**

- [ ] Issue has been read (`gh issue view`)
- [ ] Related issues checked if referenced
- [ ] Existing terms searched (don't duplicate)
- [ ] PMIDs/DOIs identified and accessible
- [ ] Parent terms verified to exist
- [ ] Import dependencies identified

### Error Handling and Recovery

**If an agent returns incomplete output:**
1. Provide specific feedback on what's missing
2. Re-request with clarification
3. Don't proceed to next step until resolved

**If an agent can't complete the task:**
1. Review the constraint (e.g., import term doesn't exist)
2. Adjust plan (e.g., pick different term or add NTR)
3. Inform user if fundamental blocker

**If conflicts arise between agents:**
1. Curator says X, but ontologist finds Y already exists
2. Pause workflow
3. Reconcile with user input

### Multi-Step Workflow Example

**Complete NTR with import and curation:**

```bash
# Step 0: PRE-CHECK - Search OLS for existing terms
# ALWAYS do this BEFORE calling curator
mcp_ols4_search "bronchiectasis endotype"
# If found in imported ontology → call @EFO-importer instead
# If not found → proceed to curation

# Step 1: Understand request
gh issue view 2546
# Identified: Need 4 new bronchiectasis endotype terms, PMID:30215383

# Step 2: Delegate curation
@EFO-curator analyze PMID:30215383 for bronchiectasis endotypes
# Wait for: definitions, minimum 2 PMIDs per term, parents, synonyms WITH TYPES, confidence

# Step 3: Review curation output
# Verify: Each term has 2+ PMIDs, synonyms have types, definitions adequate
# Decision: Definitions look good, parent is MONDO:0004822

# Step 4: Verify parent is not obsolete
grep -A 5 "MONDO:0004822" src/ontology/efo-edit.owl | grep -E "(owl:deprecated|obsolete_)"
# Result: No obsolete flag found, parent is valid

# Step 5: Check if parent needs import
grep -i "MONDO:0004822" src/ontology/efo-edit.owl
# Result: Already imported, no action needed

# Step 6: Generate term IDs
grep "EFO_092" src/ontology/efo-edit.owl | tail -n 1
# Result: Last ID is EFO_0920123, use 0920124-0920127

# Step 7: Delegate OWL editing
@EFO-ontologist add 4 new terms:
  EFO_0920124 neutrophilic bronchiectasis
  EFO_0920125 eosinophilic bronchiectasis  
  EFO_0920126 mixed granulocytic bronchiectasis
  EFO_0920127 paucigranulocytic bronchiectasis
[provide full specifications from curator INCLUDING:
 - Definitions with 2+ embedded PMIDs
 - Synonyms with type annotations (exact/related/narrow/broad)
 - Verified non-obsolete parent term]

# Step 8: Create PR
git checkout -b issue-2546
# EFO-ontologist commits changes
gh pr create --title "Add bronchiectasis endotype terms" --body "Fixes #2546...

Pre-creation checks completed:
- OLS search confirmed terms not in imported ontologies
- Parent term MONDO:0004822 verified as non-obsolete
- All 4 terms include 2+ PMIDs embedded in definitions
- Synonyms categorized by type (exact/related/narrow/broad)"
```

### Notes on Agent Limitations

- **No agent orchestrates other agents** - that's the job of these instructions
- **Agents don't make architectural decisions** - escalate to user when unclear
- **Agents stay in their lane** - curator doesn't edit OWL, ontologist doesn't curate literature
- **Serial not parallel** - complete one agent's task fully before moving to next

This coordination model ensures clear separation of concerns while maintaining workflow coherence.
