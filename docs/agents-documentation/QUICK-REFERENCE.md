# EFO Agent System - Quick Reference Guide

## 🎯 The Three-Agent System at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                       USER REQUEST                          │
│              "Please add term: [name]"                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │           EFO-ONTOLOGIST               │
        │      The Architect & Orchestrator      │
        │                                        │
        │  • Receives all user requests          │
        │  • Makes architectural decisions       │
        │  • Coordinates other agents            │
        │  • Integrates into efo-edit.owl        │
        │  • Creates PRs                         │
        └──────────┬──────────────────┬──────────┘
                   │                  │
         ┌─────────▼─────────┐   ┌────▼───────────┐
         │    EFO-CURATOR    │   │  EFO-IMPORTER. │
         │   The Researcher  │   │ The Connector  │
         │                   │   │                │
         │ • Literature      │   │ • OLS search   │
         │   search (artl)   │   │ • Term import  │
         │ • Validate        │   │ • IRI deps     │
         │   definitions     │   │ • Mirrors      │
         │ • Find citations  │   │                │
         │ • Recommend       │   │                │
         │   ontology        │   │                │
         └───────────────────┘   └────────────────┘
```

## 📋 Decision Matrix: What Happens When?

| User Request | Ontologist Action | Curator Called? | Importer Called? |
|--------------|-------------------|-----------------|------------------|
| New term (label only) | Triage → delegate | ✅ YES (research) | Maybe (if parent external) |
| New term (complete info) | Triage → delegate | ✅ YES (verify) | Maybe (if parent external) |
| Edit definition | Assess | ✅ YES (if needs citations) | ❌ NO |
| Fix typo | Edit directly | ❌ NO | ❌ NO |
| Obsolete term | Handle directly | ❌ NO | Maybe (if replacement external) |
| Add synonym | Edit directly | Only if validation needed | ❌ NO |

## 🔄 Common Workflows

### Workflow A: Minimal Info → Full Integration
```
User: "Add term: ATAC-seq"

1. 🎭 Ontologist: "Need full validation"
   ↓
2. 📚 Curator: Research literature
   - Search Europe PMC
   - Find definition: "Assay for Transposase-Accessible Chromatin..."
   - Locate PMIDs: 24097267, others
   - Identify parent: "chromatin accessibility assay"
   - Report: "Ready for EFO"
   ↓
3. 🎭 Ontologist: "Parent not in EFO, need to import from OBI"
   ↓
4. 🔗 Importer: Search OLS
   - Find: OBI:0002039
   - Add to obi_terms.txt
   - Confirm: "Import complete"
   ↓
5. 🎭 Ontologist: Integration
   - Generate EFO_0920XXX
   - Create OWL/XML entry
   - Add SubClassOf OBI:0002039
   - Normalize
   - Commit → PR
   ↓
Done ✅
```

### Workflow B: Complete Info → Quick Verify
```
User: "Add cardiac troponin measurement"
      Definition: [provided]
      PMID: 12345678
      Parent: blood measurement

1. 🎭 Ontologist: "Verify provided info"
   ↓
2. 📚 Curator: Validate
   - Check PMID ✅ relevant
   - Verify definition ✅ accurate
   - Confirm parent ✅ appropriate
   - Note: needs "is_about cardiac troponin"
   - Report: "Ready for EFO, import PR:000000058"
   ↓
3. 🔗 Importer: Import cardiac troponin from PR
   ↓
4. 🎭 Ontologist: Integration with logical definition
   ↓
Done ✅
```

### Workflow C: External Ontology Recommendation
```
User: "Add Alzheimer's disease"

1. 🎭 Ontologist: "This looks like MONDO territory"
   ↓
2. 📚 Curator: Research
   - Search literature ✅
   - Find definition ✅
   - Check MONDO: ✅ MONDO:0004975 exists!
   - Report: "DO NOT create in EFO, import from MONDO"
   ↓
3. 🎭 Ontologist: "Acknowledged"
   ↓
4. 🔗 Importer: Import MONDO:0004975
   ↓
Done ✅ (imported, not created)
```

### Workflow D: Should Be in OBA
```
User: "Add western blot assay"

1. 🎭 Ontologist: "Looks like measurement/assay"
   ↓
2. 📚 Curator: Research
   - Search literature ✅
   - Find definition ✅
   - Analyze domain: general assay technique
   - Report: "Create in OBA, not EFO"
   - Provide full validation report
   ↓
3. 🎭 Ontologist → User:
   "This should be created in OBA because it's a general
    assay technique. Here's the complete validation report
    to submit to OBA..."
   ↓
Done 🚫 (no EFO integration, user submits to OBA)
```

## 🎨 Agent Personalities

### 🎭 EFO-Ontologist: The Decisive Architect
- **Mindset**: "Where should this go? Who needs to validate?"
- **Strengths**: Quick triage, knows ontology landscape
- **Limitations**: Doesn't do deep literature research
- **Says**: 
  - "Let me check if this belongs in EFO"
  - "Calling curator to validate..."
  - "This needs a parent import first"

### 📚 EFO-Curator: The Diligent Researcher
- **Mindset**: "What does the literature say? Is this accurate?"
- **Strengths**: Deep research, evidence-based, thorough
- **Limitations**: No knowledge of OWL/XML editing
- **Says**:
  - "Found 15 papers mentioning this concept"
  - "Definition supported by PMID:12345678"
  - "This actually belongs in OBA based on usage patterns"

### 🔗 EFO-Importer: The Efficient Connector
- **Mindset**: "Where is this term? Is this the right one?"
- **Strengths**: Fast OLS lookups, precise verification
- **Limitations**: Only handles imports, not integration
- **Says**:
  - "Found in CL as CL:1000348"
  - "Import complete, ready to use"
  - "Term not found, trying alternative ontology"

## 📊 Capabilities Comparison

| Task | Ontologist | Curator | Importer |
|------|-----------|---------|----------|
| **Literature Search** | | | |
| Europe PMC search | ❌ | ✅ Full | ❌ |
| Full text analysis | ❌ | ✅ Yes | ❌ |
| Citation validation | ❌ | ✅ Yes | ❌ |
| **Ontology Work** | | | |
| OWL/XML editing | ✅ Expert | ❌ | ❌ |
| OLS search | ✅ Basic | ✅ Basic | ✅ Expert |
| Import terms | ❌ | ❌ | ✅ Yes |
| Logical definitions | ✅ Yes | ❌ | ❌ |
| **Decision Making** | | | |
| Triage requests | ✅ Yes | ❌ | ❌ |
| Ontology placement | ✅ Decides | ✅ Advises | ❌ |
| Parent selection | ✅ Decides | ✅ Researches | ✅ Finds |
| **Git Workflow** | | | |
| Branches | ✅ Yes | ❌ | ❌ |
| Commits | ✅ Yes | ❌ | ❌ |
| PRs | ✅ Yes | ❌ | ❌ |

## 🔧 When to Use Which Agent

### Use @EFO-ontologist when:
- ✅ You're a user with any request
- ✅ Need architectural decision
- ✅ Need term integration
- ✅ Need obsoletion
- ✅ Coordinating multiple agents

### Use @EFO-curator when:
- ⚠️ (Called by ontologist)
- ✅ Need literature research
- ✅ Need definition validation
- ✅ Unclear what ontology is appropriate
- ✅ Missing metadata

### Use @EFO-importer when:
- ⚠️ (Called by ontologist)
- ✅ Need external term imported
- ✅ Parent is in another ontology
- ✅ Need to check if term exists elsewhere

## 💡 Pro Tips

### For Users
1. **Start with ontologist**: Always `@EFO-ontologist` for requests
2. **Provide what you have**: Even partial info is helpful
3. **Trust the process**: Agents will coordinate automatically
4. **Don't worry about ontology choice**: Curator will recommend

### For Ontologist
1. **Always validate**: Even complete requests should go to curator
2. **Think cross-ontology**: Consider MONDO, OBA, CL, UBERON first
3. **Don't skip importer**: Always import parents if they are from a different ontology, never copy-paste
4. **Document decisions**: Explain non-obvious choices in PRs

### For Curator
1. **Be thorough**: More evidence is better than less
2. **Flag uncertainties**: Explicitly state confidence levels
3. **Think domain**: Consider measurement vs disease vs cell type
4. **Recommend boldly**: Don't hesitate to suggest external ontologies

### For Importer
1. **Verify bidirectionally**: Always fetch after search to confirm
2. **Note environment**: GitHub vs VS Code matters
3. **Suggest alternatives**: If term not found, help find it elsewhere

## 🎯 Success Metrics

### A Good Curator Report Has:
- ✅ Clear definition with 2-3 literature sources
- ✅ Validated parent term with justification
- ✅ PMIDs and DOIs (both when available)
- ✅ Synonyms with sources
- ✅ Clear ontology recommendation
- ✅ Confidence levels stated

### A Good Ontologist Integration Has:
- ✅ All required components (label, def, xref, parent)
- ✅ Proper OWL/XML formatting
- ✅ Logical definitions when appropriate
- ✅ Normalized without errors
- ✅ Clear commit message
- ✅ Complete PR description

### A Good Importer Job Has:
- ✅ Correct term found in correct ontology
- ✅ Bidirectional verification passed
- ✅ IRI added to correct dependency file
- ✅ Ready to use in efo-edit.owl

## 🚨 Red Flags

### Curator Should Flag:
- 🚩 No literature support found
- 🚩 Conflicting definitions in papers
- 🚩 Term seems to belong in another ontology
- 🚩 Parent term doesn't make sense
- 🚩 Provided citations don't support definition

### Ontologist Should Flag:
- 🚩 Curator has low confidence
- 🚩 Parent term needs importing but not found
- 🚩 Logical definition doesn't match text definition
- 🚩 Term already exists in EFO or imports
- 🚩 Obsoletion would break many relationships

### Importer Should Flag:
- 🚩 Term not found in expected ontology
- 🚩 Multiple candidate terms (ambiguous)
- 🚩 Term doesn't match description
- 🚩 Ontology mirror is stale

## 📚 Documentation Structure

```
docs/agents-documentation/
│
├── README.md                  ← Overview & quick start
└── QUICK-REFERENCE.md         ← This file (visual guide)

.github/agents/
│
├── EFO-ontologist.md          ← Full ontologist spec
├── EFO-curator.md             ← Full curator spec
├── EFO-importer.md            ← Full importer spec
└── HANDOFF-PROTOCOL.md        ← Communication protocols
```

**Read this first**: `README.md`
**Need details**: Individual agent `.md` files
**Understanding communication**: `HANDOFF-PROTOCOL.md`
**Quick lookup**: This file (`QUICK-REFERENCE.md`)

## 🔗 Related Documentation

- **Main guide**: `.github/copilot-instructions.md`
- **Import workflow**: `docs/Import_terms_from_another_ontology.md`
- **Editor workflow**: `docs/odk-workflows/EditorsWorkflow.md`
- **ODK docs**: `docs/odk-workflows/`

## ❓ Common Questions

**Q: Why three agents instead of one?**
A: Separation of concerns. Research skills ≠ Integration skills. Each agent is expert at one thing.

**Q: Can I call curator directly?**
A: Technically yes, but better to go through ontologist who orchestrates the full workflow.

**Q: What if curator says "should be in OBA"?**
A: Ontologist acknowledges and provides report to user for OBA submission. No EFO integration.

**Q: Do I need to know OWL/XML?**
A: No! Just tell ontologist what you want. They handle all the technical details.

**Q: How long does curation take?**
A: Depends on literature availability. Simple terms: fast. Novel concepts: may take research time.

**Q: What if a term exists in multiple ontologies?**
A: Curator researches which is authoritative. Ontologist decides whether to import or create.

**Q: Can I update an agent?**
A: Yes! Edit the `.md` file, update handoff protocol if needed, test with a sample issue.


---

Last updated: 2025-01-06
Version: 1.0
