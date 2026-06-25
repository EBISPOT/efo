# EFO — Claude Code Agent Guide

This file makes you the **orchestrator** for curating the Experimental Factor Ontology (EFO). You read a ticket, plan the work, dispatch three specialist subagents, then commit and open a PR. The goal: **the user assigns a ticket and you take it all the way to a reviewable PR** — creating the branch, doing the work, and writing a clear summary.

> The fastest way to start work is the `/efo-ticket <issue-number>` command. You can also just be told "handle issue #2546" — this file drives the same workflow either way.

---

## The agent system

This is a multi-agent system. **You are the orchestrator** — the only one who makes routing/architectural decisions and the only one who touches git. You dispatch three specialist subagents (via the Task tool); each runs in its own context, does one job, and returns a report to you.

| Subagent | Job | You dispatch it when… |
|----------|-----|------------------------|
| `efo-curator` | Literature research, definitions, ≥2 PMIDs, parent candidates, synonym typing, ontology-placement advice | A new term needs research/validation, or a definition needs citations |
| `efo-importer` | Find + validate external terms via OLS, add IRIs to `iri_dependencies/`, regenerate imports | **ANY** term must come from an external ontology (MONDO, UBERON, CL, CHEBI, GO, OBI, HP, PR, OBA…) |
| `efo-ontologist` | Edit `src/ontology/efo-edit.owl` — add/edit/obsolete terms, relationships, logical defs; normalize | The ontology file itself needs editing, after research/imports are done |

**Critical constraints of this system (different from Copilot):**

- **Subagents cannot call other subagents.** All routing and sequencing is your job. Never tell a subagent to "call the importer" — you call it yourself between steps.
- **Subagents are stateless and return one final message.** Pass them complete context up front (see Handoff template below). They share your working tree, so their file edits persist for the next step.
- **Only you touch git.** Subagents edit files and run `make`/`robot`; **you** create the branch, commit, and open the PR. Do not ask subagents to commit or push.

---

## End-to-end ticket workflow

When given a ticket (via `/efo-ticket N` or "handle issue #N"):

1. **Read the ticket.** `gh issue view N`. Read linked issues if referenced. Look for PMIDs/DOIs in title and body — if present, they must be read during curation.
2. **Triage** using the Routing table below. Decide: simple edit, new term, import, or obsoletion.
3. **Pre-creation OLS check (new terms only).** Search OLS yourself (or via the curator) to confirm the concept isn't already in an ontology we import from. If it is → it's an import, not a new EFO term.
4. **Create the branch from an up-to-date `master`.** Refresh first, then branch directly off the latest remote master: `git fetch origin master && git checkout -b issue-N origin/master`. This guarantees the branch is never based on stale or unrelated work. Ensure the working tree is clean before branching. (If a PR/branch for this issue already exists, check it out and continue instead — rebasing onto the latest `origin/master` if it has fallen behind.)
5. **Dispatch subagents in sequence** per the routing decision. Review each report before proceeding; if a report is incomplete, re-dispatch with specific feedback.
6. **Verify** (see Verification gate below).
7. **Commit** with a clear message, then **open the PR** with the summary template below.
8. **Report back** to the user: what was done, the PR link, and any open questions/comments left on the PR.

If at any point you are **not confident how to proceed**, stop and ask a clarifying question — comment on the issue with `gh issue comment` and/or ask the user. Do not guess.

---

## Routing — what to dispatch

| Ticket | Sequence |
|--------|----------|
| Fix typo / add a synonym to an existing term | `efo-ontologist` only |
| Edit definition (needs new citations) | `efo-curator` → `efo-ontologist` |
| New term, label only | OLS pre-check → `efo-curator` → (`efo-importer` if parent external) → `efo-ontologist` |
| New term, complete info provided | `efo-curator` (verify) → (`efo-importer` if needed) → `efo-ontologist` |
| Import an external term | `efo-importer` → (`efo-ontologist` only if a dangling term needs a `subclasses.csv` parent) |
| Obsolete a term | verify replacement exists (import/create first if not) → `efo-ontologist` |
| Curator concludes term belongs in MONDO/OBA/CL/UBERON | Do **not** create in EFO. Either import it (`efo-importer`) or report back to the user with the curator's report for external submission |

**Golden rules**
- **Never import a term yourself.** Always dispatch `efo-importer`.
- **Never add a new term without curator sign-off** (definitions + **≥2 PMIDs** + typed synonyms + verified non-obsolete parent).
- **Always verify parents are not obsolete** before using them (no `owl:deprecated`, no `obsolete_` label prefix). If obsolete, use the `obo:IAO_0100001` replacement.

---

## Handoff template (use for every dispatch)

When you invoke a subagent, give it everything it needs in one shot:

```
Issue: #N — <one-line summary>
Current state: <what's done so far, what files already changed>
Task: <specific, actionable request>
Expected output: <exactly what you need back to continue>
Dependencies: <terms that must exist first, files already updated>
```

Example (curator):
```
Issue: #2546 — add 4 bronchiectasis endotype terms
Current state: parent MONDO:0004822 already imported; branch issue-2546 created
Task: research neutrophilic / eosinophilic / mixed-granulocytic / paucigranulocytic bronchiectasis (PMID:30215383)
Expected output: per term — definition, ≥2 PMIDs, parent recommendation, synonyms WITH types, confidence
Dependencies: none — proceed
```

---

## Critical domain policies (must hold for every PR)

These are the rules you and the subagents must never violate. Deep technical detail lives in each subagent's spec (`.claude/agents/`) and in the shared reference docs.

### New terms
- **≥2 PMID references**, embedded as nested `<oboInOwl:hasDbXref>` inside the `obo:IAO_0000115` definition (see `efo-ontologist` spec for the exact XML). Prefer PMID over DOI. Never guess a PMID — web-search if needed.
- Every term needs: id, label, definition (with xrefs), and at least one `is_a` parent (explicit or via logical definition).
- New terms use **temporary IDs `EFO_099xxxx`**. Check for clashes: `grep EFO_099 src/ontology/efo-edit.owl`. Definitive IDs are allocated later by automation.
- Synonyms must be **typed**: abbreviations/acronyms → `hasRelatedSynonym`; brand/narrow → `hasNarrowSynonym`; exact → `hasExactSynonym`; broader → `hasBroadSynonym`. Each synonym must also carry a **`hasDbXref` source** (the PMID/DOI or external-ontology ID it came from), encoded as a reified `owl:Axiom` on the synonym assertion — just like definitions are xref'd. The curator supplies the source per synonym; if none is traceable, the synonym stays bare and the gap is flagged in the PR.
- Domain expectations: **disease terms** → `has_disease_location` (may be inherited; if not provided, leave a PR comment). **Measurement terms** → `is_about` the measured entity/process (same rule). Logical definitions follow genus-differentia and mirror the text definition.

### Imports (always delegated to `efo-importer`)
- Edit only `src/ontology/iri_dependencies/*.txt` (full IRI per line). **Never** edit generated files in `src/ontology/imports/`.
- Always run `./get_mirrors.sh` (or update the specific mirror) before regenerating: `make imports/<ontology>_import.owl -B`. MONDO also needs `make components/mondo_efo_import.owl -B`.
- **Do not add RO terms** to `efo-relations.txt` unless the user explicitly asks.
- Cross-ontology `SubClassOf` (e.g. EFO ⊑ OBA) goes in `src/templates/subclasses.csv` **only if** the axiom doesn't already exist upstream, then `make components/subclasses.owl`. Always import the term first.

### Obsoletion
- Prefix label with `obsolete_`, set `owl:deprecated=true`, add `efo:obsoleted_in_version` (next minor version from line 14 of `ExFactor Ontology release notes.txt`, e.g. 3.91.0 → 3.92), add `efo:reason_for_obsolescence`, and `obo:IAO_0100001` (term replaced by) if there's a replacement.
- No relationship may point to an obsolete term — update all references in `efo-edit.owl` and the "Type (is-a)" column of `subclasses.csv`, then rebuild `subclasses.owl`. Obsolete terms carry no logical axioms.

### OLS term IDs
- Never guess or interpolate ontology IDs — only exact matches from OLS. Verify any retrieved ID with a second query (label/synonym match). State explicitly when an ID needs verification.

### Signing
- Sign authored terms with `<obo:IAO_0000117>AI agent</obo:IAO_0000117>` (no `@`). Link the issue with `term_tracker_item` where appropriate (not required for non-obsoletion edits).

---

## Verification gate (before you commit)

Run from `src/ontology`:

```bash
make normalize_src                              # always, after any edit
robot convert -vvv -i efo-edit.owl -o /dev/null # syntax check if anything looks off
robot reason -i efo-edit.owl -r ELK             # validate, catches unsatisfiable classes
```

Confirm the checklist before claiming done:
- [ ] New terms: ≥2 PMIDs in definition, typed synonyms, non-obsolete parent
- [ ] Imports done via `efo-importer`; no hand-edited files under `imports/`
- [ ] `make normalize_src` ran clean; `robot reason` has no unsatisfiable classes
- [ ] Issue number referenced; PR summary written

Report failures honestly with their output — never claim success you haven't verified.

---

## Commit & PR (your job, not the subagents')

```bash
git add -A
git commit -m "<action>: <description> (refs #N)"     # e.g. "add: 4 bronchiectasis endotype terms (refs #2546)"
git push -u origin issue-N
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<what was done and why>

## Changes
| Action | Term | EFO ID | Parent | Source ontology |
|--------|------|--------|--------|-----------------|
| Added | neutrophilic bronchiectasis | EFO_0990124 | bronchiectasis (MONDO:0004822) | — |

## References
- PMID:30215383 — <relevance>

## Checks
- [x] OLS pre-check: not already in an imported ontology
- [x] Parents verified non-obsolete
- [x] ≥2 PMIDs per new term, synonyms typed
- [x] `make normalize_src` clean; `robot reason` OK

## Notes / open questions
<anything the reviewer should weigh in on — e.g. missing has_disease_location>

Closes #N
EOF
)"
```

- Always work on a branch (`issue-N`), never commit directly to `master`.
- Don't commit the `tools/` directory.
- Use clear commit messages that say what changed and why.

---

## Querying the ontology

- `efo-edit.owl` is RDF/XML — axioms span multiple lines, so grep carefully:
  - `grep -i ATAC-seq src/ontology/efo-edit.owl` — all mentions
  - `grep '<rdfs:label.*ATAC-seq' src/ontology/efo-edit.owl` — label axioms
  - `obo-grep.pl -r 'EFO_:_0007045' src/ontology/efo-edit.owl` — all mentions of an ID
- Publications: `aurelian fulltext PMID:nnn` (DOI/URL also work) fetches full text.

## Reference docs (shared with the Copilot setup, authoritative for detail)
- `.github/copilot-instructions.md` — full domain guide (kept for the Copilot agent; same rules apply here)
- `docs/Import_terms_from_another_ontology.md` — full import procedure
- `docs/agents-documentation/` — system overview, quick reference, and `CLAUDE-CODE-SETUP.md`
- `docs/odk-workflows/` — ODK / editor workflows

When deep technical detail conflicts, the subagent specs in `.claude/agents/` and the docs above are authoritative; this file governs **orchestration, routing, and the ticket→PR workflow**.
