# EFO Agent Handoff Protocol

This document defines the interaction patterns, communication protocols, and handoff procedures between the three EFO agents: **EFO-ontologist**, **EFO-curator**, and **EFO-importer**.

## Agent Roles Summary

| Agent | Primary Role | Input | Output |
|-------|-------------|-------|--------|
| **EFO-ontologist** | Orchestrator & integrator | User requests, term specifications | Integrated terms, PRs, or recommendations |
| **EFO-curator** | Researcher & validator | Term metadata (partial/complete) | Validation reports with literature evidence |
| **EFO-importer** | External term importer | Term labels, ontology hints | Imported IRIs in dependency files |

## Communication Protocol

### Agent Invocation Syntax

When one agent needs to call another:

```markdown
@[agent-name] [task description]

Required information:
- [parameter 1]: [value]
- [parameter 2]: [value]

Expected output:
- [what you need back]
```

### Response Format

Responding agents should structure replies as:

```markdown
@[calling-agent-name] - RESPONSE

[Summary of findings]

## Detailed Results
[Full response content]

## Status
✓ Complete / ⚠️ Partial / ✗ Failed

## Recommendations
[Next steps or additional actions needed]
```

## Handoff Patterns

### Pattern 1: Ontologist → Curator (New Term, Minimal Info)

**Scenario**: User provides only a label, or incomplete information

**Ontologist initiates**:
```markdown
@EFO-curator - VALIDATION REQUEST

Term: [label]
Source: Issue #NNNN

Provided information:
- Label: [term label]
- Definition: [if provided, otherwise MISSING]
- Parent: [if provided, otherwise MISSING]
- Xrefs: [if provided, otherwise MISSING]

Required actions:
- [ ] Research and validate/create definition
- [ ] Find authoritative citations (PMIDs/DOIs)
- [ ] Identify and validate parent term(s)
- [ ] Search for synonyms in literature
- [ ] Determine appropriate ontology placement

Expected output:
- Complete validation report
- Ontology placement recommendation (EFO vs external)
- Literature evidence for all claims
```

**Curator responds**:
```markdown
@EFO-ontologist - CURATION COMPLETE

## Status
✓ Validation complete

## Ontology Recommendation
[EFO / OBA / MONDO / CL / UBERON / other]

## Validated Components
- Label: [final label]
- Definition: [validated definition]
- Primary xref: PMID:XXXXXXX (DOI:10.xxxx/yyyy)
- Parent term: [term label] ([ONTOLOGY:ID])
- Synonyms: [list]

## Detailed Report
[Full markdown report as specified in EFO-curator.md]

## Next Steps for Ontologist
[Specific recommendations]
```

**Ontologist decision**:
- If curator recommends external ontology → Inform user, provide report
- If curator approves EFO → Check if parent needs importing → Proceed to integration

---

### Pattern 2: Ontologist → Curator (Validation Only)

**Scenario**: User provides complete information, but it needs verification

**Ontologist initiates**:
```markdown
@EFO-curator - VERIFICATION REQUEST

Term: [label]
Source: Issue #NNNN

Provided information (needs verification):
- Label: [term label]
- Definition: [provided definition]
- Parent: [suggested parent]
- Xrefs: [provided xrefs]
- Synonyms: [provided synonyms]

Required actions:
- [ ] Verify definition accuracy against literature
- [ ] Validate provided citations
- [ ] Confirm parent term appropriateness
- [ ] Validate synonyms
- [ ] Confirm ontology placement

Expected output:
- Verification report
- Corrections or confirmations for each component
```

**Curator responds**:
```markdown
@EFO-ontologist - VERIFICATION COMPLETE

## Status
✓ Verified with modifications / ✓ Verified as-is / ⚠️ Issues found

## Verification Results

### Label: ✓ Confirmed / ⚠️ Suggest change to: [alternative]

### Definition: 
Status: ✓ Accurate / ⚠️ Needs revision
Revised: [new definition if needed]
Supporting literature: PMID:XXXXXXX

### Parent term:
Status: ✓ Appropriate / ⚠️ Suggest alternative
Recommendation: [parent term] ([ONTOLOGY:ID])
Justification: [explanation]

### Cross-references:
Status: ✓ Valid / ⚠️ Issues found
- PMID:XXXXXXX - ✓ Relevant and accurate
- PMID:YYYYYYY - ⚠️ Not directly relevant, suggest removing

### Synonyms:
Status: ✓ Validated / ⚠️ Issues found
- [synonym 1] - ✓ Confirmed in PMID:XXXXXXX
- [synonym 2] - ⚠️ Not found in literature, suggest removing

## Ontology Recommendation
[EFO / external ontology]

## Confidence Level
High / Medium / Low - [explanation]
```

**Ontologist decision**:
- Apply corrections from curator
- Proceed with integration or recommend external ontology

---

### Pattern 3: Ontologist → Importer → Ontologist

**Scenario**: Parent term or related term needs importing from external ontology

**Ontologist initiates**:
```markdown
@EFO-importer - IMPORT REQUEST

Term to import: [term label]
Expected source ontology: [CL / MONDO / UBERON / ChEBI / GO / HP / OBI / other]
Reason: [parent term for EFO:XXXXXXX / relationship requirement]

Context:
[Why this import is needed]

Expected output:
- Confirmation of import
- IRI added to dependency file
- Import regenerated (if in VS Code)
```

**Importer responds**:
```markdown
@EFO-ontologist - IMPORT COMPLETE

## Status
✓ Import successful / ⚠️ Partial / ✗ Failed

## Imported Term
- Label: [term label]
- ID: [ONTOLOGY:ID]
- IRI: [full IRI]
- Added to: src/ontology/iri_dependencies/[ontology]_terms.txt

## Verification
✓ Bidirectional validation passed
✓ Term definition matches expectation

## Environment
[GitHub sandbox / VS Code]
Import status: [Generated / Will be generated on merge]

## Available for Use
Term can now be referenced in efo-edit.owl using IRI:
[full IRI]
```

**Ontologist proceeds**:
- Use the provided IRI in term relationships
- Check if subclasses.csv entry needed
- Continue with integration

---

### Pattern 4: Curator → Ontologist (Unsolicited Recommendation)

**Scenario**: During research, curator discovers term should be in external ontology

**Curator reports**:
```markdown
@EFO-ontologist - EXTERNAL ONTOLOGY DETECTED

## Alert
Term should NOT be created in EFO

## Recommendation
Create in: [ONTOLOGY NAME]
Reason: [detailed explanation]

## Curation Status
✓ Complete - ready for external submission

## Report
[Full validation report follows]
[User can use this to submit to external ontology]

## Suggested User Communication
"Thank you for your term request. Based on our research, this term 
would be more appropriately created in [ONTOLOGY] because [reason]. 
We've prepared a complete validation report below that you can use 
to submit a new term request to [ONTOLOGY]..."
```

**Ontologist responds**:
```markdown
@EFO-curator - ACKNOWLEDGED

✓ External ontology recommendation accepted
✓ Will inform user with your complete report
✓ Closing workflow without integration

Thank you for the thorough research.
```

---

### Pattern 5: Curator → Ontologist (Import Recommendation)

**Scenario**: Curator identifies that proposed parent term should be imported

**Curator reports**:
```markdown
@EFO-ontologist - IMPORT REQUIRED

## Curation Status
✓ Term validated for EFO integration

## Import Required
Term: [parent term label]
Source: [ontology]
Reason: Appropriate parent not in EFO, found in [ontology]

## Evidence
Found in: PMID:XXXXXXX
Definition: [definition]
Relationship: [proposed EFO term] SubClassOf [external term]

## Recommendation
1. Call @EFO-importer to import [external term]
2. Use as parent for [EFO term]
3. Proceed with integration

## Full Report
[Validation report follows]
```

**Ontologist proceeds**:
```markdown
@EFO-curator - ACKNOWLEDGED

✓ Will import required parent term
✓ Will proceed with integration after import

Calling @EFO-importer...
```

---

## Error Handling Protocols

### When Curator Cannot Find Evidence

**Curator reports**:
```markdown
@EFO-ontologist - INSUFFICIENT EVIDENCE

## Status
⚠️ Incomplete validation

## Issues
- [Component]: Could not find literature support
- [Component]: Conflicting definitions found

## Attempted Searches
- [Search strategy 1]: [results]
- [Search strategy 2]: [results]

## Recommendations
1. Request more information from user
2. Expand search scope to [alternative sources]
3. Consider if term is too specific/novel for current literature

## Partial Results
[Any validated components]

## Next Steps Needed
[What would help complete validation]
```

**Ontologist response**:
```markdown
@EFO-curator - ACKNOWLEDGED

Will request additional information from user via PR comment.

Specific questions to ask:
[List based on curator's gaps]
```

### When Importer Cannot Find Term

**Importer reports**:
```markdown
@EFO-ontologist - IMPORT FAILED

## Status
✗ Term not found

## Search Details
- Ontology searched: [ontology]
- Search terms used: [list]
- Results: No matches found

## Recommendations
1. Verify term name/label
2. Check if term exists in alternative ontology
3. Consider if term needs to be created in external ontology first

## Alternative Findings
[Any potentially related terms found]
```

**Ontologist responds**:
```markdown
@EFO-importer - ACKNOWLEDGED

Will [verify term name with user / search alternative ontologies / 
      recommend external term creation]
```

### When Ontologist Rejects Curator Recommendation

**Scenario**: Ontologist has additional context that changes decision

**Ontologist responds**:
```markdown
@EFO-curator - RECOMMENDATION OVERRIDE

## Decision
Proceeding with [alternative action] instead of recommended [action]

## Justification
[Detailed explanation of why override is appropriate]
[Additional context not available to curator]

## Acknowledgment
Thank you for the thorough research. Your report will be [used for X]

## Next Steps
[What will actually happen]
```

---

## Multi-Agent Workflows

### Complex New Term (All Three Agents)

```
User Request
    ↓
[EFO-ontologist] - Triage
    ↓
[EFO-ontologist] → @EFO-curator - "Validate this term"
    ↓
[EFO-curator] - Research & validate
    ↓
[EFO-curator] → @EFO-ontologist - "Ready for EFO, but needs parent import"
    ↓
[EFO-ontologist] → @EFO-importer - "Import parent term"
    ↓
[EFO-importer] - Import parent
    ↓
[EFO-importer] → @EFO-ontologist - "Import complete"
    ↓
[EFO-ontologist] - Integrate term
    ↓
[EFO-ontologist] - Create PR
    ↓
User Review
```

### External Ontology Recommendation

```
User Request
    ↓
[EFO-ontologist] - Triage
    ↓
[EFO-ontologist] → @EFO-curator - "Validate and recommend"
    ↓
[EFO-curator] - Research & validate
    ↓
[EFO-curator] → @EFO-ontologist - "Should be in OBA, here's full report"
    ↓
[EFO-ontologist] - Acknowledge
    ↓
[EFO-ontologist] → User - "Create in OBA with curator's report"
    ↓
Close Issue (no integration)
```

### Simple Edit (Single Agent)

```
User Request: "Fix typo in definition"
    ↓
[EFO-ontologist] - Assess (no validation needed)
    ↓
[EFO-ontologist] - Make edit directly
    ↓
[EFO-ontologist] - Create PR
    ↓
User Review
```

---

## State Tracking

### Using TODO Lists

Agents should use the `manage_todo_list` tool to track multi-step workflows:

**Ontologist example**:
```markdown
📋 TODO: New term integration - [term label] (issue #NNNN)

1. ✓ Initial triage complete
2. 🔄 Waiting for curator validation (@EFO-curator)
3. ⏳ Import parent term (after curator response)
4. ⏳ Integrate term into efo-edit.owl
5. ⏳ Run normalization
6. ⏳ Create PR
```

**Curator example**:
```markdown
📋 TODO: Validate [term label] for @EFO-ontologist

1. 🔄 Search literature for definition
2. ⏳ Validate cross-references
3. ⏳ Identify parent term
4. ⏳ Search for synonyms
5. ⏳ Generate validation report
```

### Status Communication

Use clear status markers:
- ✓ Complete
- 🔄 In progress
- ⏳ Pending (waiting for dependency)
- ⚠️ Issue/blocker
- ✗ Failed

---

## Best Practices

### For Ontologist (Orchestrator)
1. Always provide complete context when calling other agents
2. Make triage decisions quickly and clearly
3. Wait for complete responses before proceeding
4. Acknowledge all responses from other agents
5. Document override decisions clearly

### For Curator (Research Specialist)
1. Be thorough in literature search
2. Always provide evidence for claims
3. Flag uncertainties clearly
4. Recommend next steps explicitly
5. Don't hesitate to recommend external ontologies

### For Importer (Import Specialist)
1. Always perform bidirectional verification
2. Report both success and failure clearly
3. Provide exact IRIs in responses
4. Note environment limitations (GitHub vs VS Code)
5. Suggest alternatives when imports fail

### For All Agents
1. Use structured communication formats
2. Reference specific issue numbers
3. Use @ mentions when handing off
4. Provide actionable recommendations
5. Track state with TODO lists
6. Be explicit about what you need from others
7. Acknowledge receipt of handoffs

---

## Example Complete Workflow Transcript

```markdown
User: "Please add a new term: ATAC-seq peak intensity"

---

@EFO-ontologist:
TRIAGE COMPLETE
This is a new measurement term with minimal information.

@EFO-curator - VALIDATION REQUEST

Term: ATAC-seq peak intensity
Source: Issue #1234

Provided information:
- Label: ATAC-seq peak intensity
- Definition: MISSING
- Parent: MISSING
- Xrefs: MISSING

Required actions:
- [ ] Research definition from literature
- [ ] Find PMIDs/DOIs for citations
- [ ] Identify parent term (measurement hierarchy)
- [ ] Identify what is being measured (for is_about)
- [ ] Check if this belongs in OBA vs EFO

Expected output:
- Complete validation report
- Ontology placement recommendation

---

@EFO-curator:
RESEARCH IN PROGRESS

📋 TODO:
1. 🔄 Literature search for ATAC-seq peak intensity
2. ⏳ Validate definition
3. ⏳ Identify parent measurement class
4. ⏳ Determine is_about target
5. ⏳ Generate report

Searching Europe PMC...

---

@EFO-curator:
@EFO-ontologist - CURATION COMPLETE

## Status
✓ Validation complete

## Ontology Recommendation
✓ EFO (chromatin accessibility measurement in epigenomics experiments)

## Validated Components
- Label: ATAC-seq peak intensity
- Definition: A quantitative measurement of the signal intensity of peaks identified in ATAC-seq experiments, reflecting the degree of chromatin accessibility at specific genomic loci.
- Primary xref: PMID:24097267 (DOI:10.1038/nmeth.2688)
- Additional xref: PMID:29590004
- Parent term: ATAC-seq assay (EFO:0007045)
- is_about: chromatin accessibility (GO:0031490)
- Synonyms: ATAC peak intensity, chromatin accessibility peak intensity

## Import Required
⚠️ Need to import: chromatin accessibility
Suggested source: GO (Gene Ontology) GO:0031490

## Detailed Report
[Full validation report with all literature evidence]

## Confidence Level
High - well-established experimental measurement in epigenomics

---

@EFO-ontologist:
@EFO-curator - ACKNOWLEDGED

✓ Will import chromatin accessibility from GO
✓ Will proceed with EFO integration

@EFO-importer - IMPORT REQUEST

Term to import: chromatin accessibility
Expected source ontology: GO (Gene Ontology)
ID: GO:0031490
Reason: Need as is_about target for ATAC-seq peak intensity

Context:
New ATAC-seq measurement term needs to reference the biological process being measured

Expected output:
- IRI added to go_terms.txt
- Confirmation for use in efo-edit.owl

---

@EFO-importer:
@EFO-ontologist - IMPORT COMPLETE

## Status
✓ Import successful

## Imported Term
- Label: chromatin accessibility
- ID: GO:0031490
- IRI: http://purl.obolibrary.org/obo/GO_0031490
- Added to: src/ontology/iri_dependencies/go_terms.txt

## Verification
✓ Bidirectional validation passed
✓ Definition: "The extent to which nuclear DNA is available for binding by DNA-binding proteins"

## Environment
VS Code - import regenerated

## Available for Use
✓ Term ready to reference in efo-edit.owl

---

@EFO-ontologist:
INTEGRATION IN PROGRESS

📋 TODO:
1. ✓ Curation complete
2. ✓ Parent term imported
3. 🔄 Generate EFO ID (checking for clashes)
4. ⏳ Create OWL/XML entry
5. ⏳ Add logical definition with is_about
6. ⏳ Normalize
7. ⏳ Commit and PR

Generated ID: EFO_0920445 (checked - no clashes)

---

@EFO-ontologist:
INTEGRATION COMPLETE

✓ Added: ATAC-seq peak intensity (EFO:0920445)
✓ Parent: ATAC-seq assay (EFO:0007045)
✓ Logical definition: measurement AND is_about chromatin accessibility
✓ Definition: [as validated by curator]
✓ Xrefs: PMID:24097267, PMID:29590004
✓ Normalized successfully
✓ Branch: issue-1234
✓ PR: #2537

Ready for review.

Issue #1234 resolved.
```

---

## Quick Reference

### Agent Responsibilities
- **Ontologist**: Orchestrates, decides, integrates
- **Curator**: Researches, validates, reports
- **Importer**: Finds, verifies, imports

### Call This Agent When:
- **Ontologist**: Any user request, architectural decisions
- **Curator**: Need literature validation, missing metadata
- **Importer**: Need external term, parent from another ontology

### Expected Response Time:
- **Ontologist**: Immediate (orchestration)
- **Curator**: Variable (depends on literature complexity)
- **Importer**: Fast (OLS search + file edit)

### Always Include in Handoffs:
- Context (issue number, term name)
- What you need (specific tasks)
- What you have (current information)
- What's expected (output format)
