# EFO Agent System - Overview

This directory contains the specifications for three specialized agents that work together to manage the Experimental Factor Ontology (EFO).

## Agent Architecture

###  Three-Agent System

```
                    ┌─────────────────┐
                    │  User Request   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ EFO-ontologist  │ ◄─── Orchestrator
                    │  (Integrator)   │
                    └────┬───────┬────┘
                         │       │
              ┌──────────▼─┐   ┌─▼──────────┐
              │EFO-curator │   │EFO-importer│
              │(Researcher)│   │  (Import)  │
              └────────────┘   └────────────┘
```

## The Agents

### 1. EFO-ontologist (Orchestrator)
**File**: `EFO-ontologist.md`

**Role**: Main orchestrator and integration specialist
- First point of contact for all term requests
- Makes architectural decisions (EFO vs external ontologies)
- Coordinates curator and importer agents
- Handles OWL/XML editing and term integration
- Manages obsoletion and simple edits directly

**When to invoke**: 
- Any new term request
- Term edits or obsoletions
- Architectural questions
- General ontology work

**Key capabilities**:
- Triage and workflow routing
- OWL/XML formatting
- Git workflow (branches, commits, PRs)
- Quality assurance
- Cross-ontology decisions

### 2. EFO-curator (The Researcher)
**File**: `EFO-curator.md`

**Role**: Literature research and validation specialist
- Deep literature searches using artl-mcp
- Validates all term components (label, definition, xrefs, parent)
- Generates comprehensive validation reports
- Recommends appropriate ontology placement
- Domain-specific expertise (diseases, measurements, cells, etc.)

**When to invoke** (by ontologist):
- New term with missing information
- New term needing validation
- Definition changes requiring literature support
- Unclear parent term relationships
- Ontology placement questions

**Key capabilities**:
- Europe PMC literature search
- Full-text analysis
- Citation validation
- Domain expertise
- Evidence-based recommendations

### 3. EFO-importer (The Connector)
**File**: `EFO-importer.md`

**Role**: External ontology term importer
- Searches OLS for terms in external ontologies
- Bidirectional verification of term identity
- Adds IRIs to dependency files
- Updates mirrors and regenerates imports

**When to invoke** (by ontologist):
- Parent term exists in external ontology
- Need to import related terms
- Cross-ontology relationships needed

**Key capabilities**:
- OLS search (mcp_ols4)
- IRI validation
- Dependency file management
- Import generation (VS Code only)

## Handoff Protocol

**File**: `HANDOFF-PROTOCOL.md`

Defines:
- Communication patterns between agents
- Request/response formats
- Multi-agent workflows
- Error handling
- State tracking

**Key patterns**:
1. **New term (minimal info)**: Ontologist → Curator → Ontologist
2. **New term (complete info)**: Ontologist → Curator (verify) → Ontologist
3. **Import needed**: Ontologist → Importer → Ontologist
4. **External ontology**: Ontologist → Curator → User (no integration)
5. **Simple edit**: Ontologist only

## Quick Start

### For New Term Requests

As a user, you only need to interact with **EFO-ontologist**:

```markdown
@EFO-ontologist

Please add a new term:
- Label: [term name]
- Definition: [if you have one]
- Parent: [if you know it]
- References: [if you have any]
```

The ontologist will:
1. Assess what you've provided
2. Call curator to fill gaps or validate
3. Call importer if external terms needed
4. Integrate into EFO or recommend external ontology
5. Create a PR for review

### For Editing Existing Terms

```markdown
@EFO-ontologist

Please edit [term name] (EFO:XXXXXXX):
- [Describe the change needed]
```

### For Obsoleting Terms

```markdown
@EFO-ontologist

Please obsolete [term name] (EFO:XXXXXXX)
Replacement: [term name] (EFO:YYYYYYY)
Reason: [why obsoleting]
```

## Agent Capabilities Matrix

| Capability | Ontologist | Curator | Importer |
|-----------|-----------|---------|----------|
| Literature search | ❌ | ✅ | ❌ |
| OWL/XML editing | ✅ | ❌ | ❌ |
| OLS search | ✅ | ✅ | ✅ |
| Definition validation | ❌ | ✅ | ❌ |
| Parent term import | ❌ | ❌ | ✅ |
| Ontology placement decision | ✅ | Advisory | ❌ |
| Git workflow | ✅ | ❌ | ❌ |
| Term integration | ✅ | ❌ | ❌ |

## Tools Used

### artl-mcp (Literature Research)
Used by: **Curator**
- `search_europepmc_papers`: Find papers by keywords
- `get_europepmc_paper_by_id`: Get metadata for specific papers
- `get_all_identifiers_from_europepmc`: Get PMIDs, DOIs, PMCIDs
- `get_europepmc_full_text`: Get full text as Markdown
- `get_europepmc_pdf_as_markdown`: Convert PDF to Markdown

### ols4-mcp (Ontology Lookup)
Used by: **All agents**
- `mcp_ols4_search`: Search all ontologies
- `mcp_ols4_searchClasses`: Search specific ontology
- `mcp_ols4_fetch`: Get term details
- `mcp_ols4_getAncestors`: Get term hierarchy
- `mcp_ols4_getDescendants`: Get child terms

### Standard Tools
- `grep_search`, `file_search`: Find terms in files
- `read_file`, `replace_string_in_file`: Edit ontology
- `run_in_terminal`: Execute make commands
- `manage_todo_list`: Track multi-step workflows

## Workflow Examples

### Example 1: Minimal Information
```
User: "Add term: ATAC-seq"
    ↓
Ontologist: Triage → Call curator
    ↓
Curator: Research literature → Generate report
    ↓ 
Ontologist: Review → Parent needs import → Call importer
    ↓
Importer: Import parent from OBI
    ↓
Ontologist: Integrate term → Create PR
```

### Example 2: Complete Information
```
User: "Add cardiac measurement with definition, PMID, parent"
    ↓
Ontologist: Triage → Call curator (verify)
    ↓
Curator: Verify citations → Validate parent → Confirm
    ↓
Ontologist: Integrate term → Create PR
```

### Example 3: Should Be External
```
User: "Add general disease term"
    ↓
Ontologist: Triage → Call curator
    ↓
Curator: Research → Recommend MONDO
    ↓
Ontologist: Acknowledge → Inform user
    ↓
User: Submit to MONDO with curator's report
```

## Decision Trees

### Should I create one agent or two?

**Two agents is better because**:
✅ Separation of concerns (research vs integration)
✅ Curator can be called for external submissions too
✅ Different expertise required (literature vs OWL/XML)
✅ Easier to maintain and improve each
✅ Clear handoff points

### Which agent do I call?

```
Are you a user? → @EFO-ontologist
Are you the ontologist needing validation? → @EFO-curator  
Are you the ontologist needing imports? → @EFO-importer
Are you the curator? → Response to @EFO-ontologist
Are you the importer? → Response to @EFO-ontologist
```

## File Structure

```
.github/agents/
├── EFO-ontologist.md      ← Main orchestrator agent
├── EFO-curator.md         ← Research & validation agent
├── EFO-importer.md        ← Import specialist agent (existing)
└── HANDOFF-PROTOCOL.md    ← Communication protocols
```

## Maintenance

### Updating Agent Specifications

When updating an agent:
1. Edit the relevant agent's `.md` file
2. Update `HANDOFF-PROTOCOL.md` if communication patterns change
3. Update this README if capabilities change
4. Test the workflow with a sample issue

### Adding New Capabilities

When adding new tools or workflows:
1. Determine which agent should handle it
2. Update that agent's specification
3. Update handoff protocol if involves multiple agents
4. Add to capabilities matrix in this README

### Common Issues

**Agent not finding terms**:
- Check OLS is accessible
- Verify term exists in expected ontology
- Try alternative search terms

**Literature search returns nothing**:
- Try broader search terms
- Search for related concepts
- Check alternative spellings/synonyms

**Import fails**:
- Verify term exists in source ontology
- Check IRI format
- Ensure mirrors are up to date

## Best Practices

### For Users
- Provide as much information as you have
- Include relevant PMIDs or papers if known
- Mention domain context (disease, measurement, etc.)
- Reference related existing terms if applicable

### For Agent Development
- Keep agents focused on their core competency
- Use structured communication formats
- Always validate before integrating
- Document decisions in commit messages and PRs
- Use TODO lists for multi-step workflows

### For Ontology Curation
- Always require literature support
- Verify parent relationships make sense
- Check for existing terms before creating new ones
- Consider external ontologies for general concepts
- Maintain consistency with existing patterns

## Testing the System

To test the agent system:

1. **Simple test**: "Add synonym 'XYZ' to term ABC"
   - Should: Ontologist only

2. **Medium test**: "Add new term: [label only]"
   - Should: Ontologist → Curator → (maybe Importer) → Ontologist

3. **Complex test**: "Add new measurement with is_about relationship"
   - Should: All three agents, full validation, logical definition

4. **Edge test**: "Add general anatomical term"
   - Should: Ontologist → Curator → Recommend UBERON

## Support

For questions about:
- **Agent behavior**: See individual agent `.md` files
- **Communication**: See `HANDOFF-PROTOCOL.md`
- **Ontology editing**: See main `copilot-instructions.md`
- **Import process**: See `docs/Import_terms_from_another_ontology.md`

## Version History

- **v1.0** (2025-01-06): Initial three-agent system
  - EFO-ontologist (orchestrator)
  - EFO-curator (researcher)
  - EFO-importer (existing, connector)
  - Handoff protocol established
