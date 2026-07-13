# EFO PR Review Checklist (canonical)

**Single source of truth** for reviewing EFO pull requests and branch diffs.
Every platform wrapper — the Claude subagent (`.claude/agents/efo-pr-reviewer.md`),
the Copilot agent (`.github/agents/EFO-pr-reviewer.md`), and the Codex prompt
(`efo-pr-review-codex.md`) — points here instead of restating the rules, so the
three reviewers can never drift out of sync. **Do not duplicate these rules into
the wrappers; edit them here.**

This checklist is **EFO-specific**: the edit file is always the OWL/XML file
`src/ontology/efo-edit.owl`. There is no OBO-format branch.

## Hard constraints (read-only, advisory)

- The review is **read-only**. Never modify files, stage, commit, push, create
  branches, or open/edit PRs.
- Never post to GitHub as part of the review (no `gh pr review`,
  `gh pr comment`, `gh issue comment`, reactions). Publishing a review is a
  separate, explicit step the human/driver controls — not part of producing it.
- Only run read-only shell commands: `git diff`, `git log`, `gh pr diff/view`,
  `grep`/`rg`, `obo-grep.pl`, `robot query/reason` (if on PATH), `cat`/`sed -n`/
  `head`/`tail`, `ls`, `find`, `aurelian` lookups.
- The output is a **structured report** (format below). If information is
  missing, note it as an assumption or limitation — do not guess and do not ask
  follow-up questions mid-review.

## Getting the diff

- **PR number given:** `gh pr diff <N>` for the patch; `gh pr view <N> --json
  title,body,files,baseRefName,headRefName` for context and the linked issue.
- **No argument (local branch):** review the current branch against the default
  branch. Determine the base with `git symbolic-ref --quiet
  refs/remotes/origin/HEAD` (strip to the name), else `master`. Run
  `git diff <base>...HEAD`; use `git log <base>..HEAD --oneline` for commit
  context. This works even with no open PR.
- If there is no PR and no diff vs. base, there is nothing to review — say so and
  stop.
- Review **only what the diff changes**. Do not audit untouched parts of EFO.

## Inspecting changed terms in `efo-edit.owl`

`efo-edit.owl` is RDF/XML — axioms span multiple lines, so grep carefully:

- Read the diff hunks directly; added/removed axioms are visible in the patch.
- All mentions of an ID: `obo-grep.pl -r 'EFO_:_0007045' src/ontology/efo-edit.owl`
  (or a narrow `rg`/`grep` fallback if `obo-grep.pl` is not on PATH).
- Label axioms: `grep '<rdfs:label.*ATAC-seq' src/ontology/efo-edit.owl`.
- If ROBOT is on PATH, pull a class's full axioms with
  `robot extract --method MIREOT --input src/ontology/efo-edit.owl --term <IRI>
  --output -`. Do **not** require ROBOT — fall back to `rg` for the IRI, its
  `rdfs:label`, and annotations.
- Publications: `aurelian fulltext PMID:nnn` fetches full text for verification.

OWL construct reference: definition = `obo:IAO_0000115`; xref =
`oboInOwl:hasDbXref`; subclass = `rdfs:subClassOf` / `SubClassOf`; obsoletion =
`owl:deprecated true`; replaced-by = `obo:IAO_0100001`; consider =
`oboInOwl:consider`; relationships (`part_of`, `has_disease_location`, `is_about`)
= OWL restrictions on the relevant RO/EFO property.

## Review focus areas

### 1. Hierarchy & parents
- Every new term has at least one `is_a` parent (explicit `rdfs:subClassOf` or
  via a logical definition).
- Parents are **not obsolete** (no `owl:deprecated`, no `obsolete_` label prefix).
  If a referenced parent is obsolete, that is a 🔴 — it should use the
  `obo:IAO_0100001` replacement.
- No cycles introduced.
- Any logical/equivalent-class definition follows **genus–differentia** and
  mirrors the text definition.

### 2. Definitions, references & PMIDs
- Every new/edited term has an `obo:IAO_0000115` definition.
- **New terms carry ≥2 PMID references**, embedded as nested
  `oboInOwl:hasDbXref` inside the definition axiom. Prefer PMID over DOI.
- Cited PMIDs/DOIs are **real and actually support the assertion**. Verify with
  `aurelian` if available, else WebSearch/WebFetch. If you cannot verify, **flag
  it** (do not assert it is wrong).

### 3. Synonyms
- Synonyms are **typed**: abbreviations/acronyms → `oboInOwl:hasRelatedSynonym`;
  brand/narrow → `oboInOwl:hasNarrowSynonym`; exact → `oboInOwl:hasExactSynonym`;
  broader → `oboInOwl:hasBroadSynonym`.
- Each synonym carries a **source `hasDbXref`** (the PMID/DOI or external-ontology
  ID it came from), encoded as a reified `owl:Axiom` on the synonym assertion
  (`owl:Axiom` with `owl:annotatedProperty` = the `oboInOwl:has*Synonym` and a
  child `oboInOwl:hasDbXref`).
- A new synonym with no source xref is 🟡 IMPORTANT — the curator may legitimately
  have found none, so flag it for the author to confirm rather than asserting it
  is wrong.

### 4. Obsoletion safety
- Obsoleted term: label prefixed `obsolete_`, `owl:deprecated=true`,
  `efo:obsoleted_in_version` set (next minor version from line 14 of
  `ExFactor Ontology release notes.txt`), `efo:reason_for_obsolescence` present,
  and `obo:IAO_0100001` (term replaced by) **if** a replacement exists (else
  zero-or-more `oboInOwl:consider`).
- Obsolete terms carry **no logical axioms** (no `rdfs:subClassOf`/equivalent/
  relationship restrictions).
- **No remaining reference points at the obsoleted term** — search the edit file
  for the ID/IRI, and check the "Type (is-a)" column of
  `src/templates/subclasses.csv`. Any dangling reference is 🔴.

### 5. Temporary vs. permanent IDs
- `EFO_099xxxx` is the marker of an **agent-generated temporary** ID; automation
  replaces it with a definitive ID after merge to `master`. Its presence is
  expected in agent PRs and is **not** a defect.
- A **non-`EFO_099xxxx`** ID is permanent/manually-assigned and must **not** be
  relabeled "temporary" or renumbered into the `EFO_099xxxx` range — temporary vs.
  permanent is decided purely by the ID range, not by who opened the PR.
- Check for `EFO_099xxxx` clashes (the same temp ID used for two different terms).

### 6. Conventions, metadata & domain expectations
- Naming is consistent with parents/siblings.
- Authored terms are signed `obo:IAO_0000117` = `AI agent` (no `@`); the issue is
  linked via `term_tracker_item` where appropriate.
- **Disease terms** → `has_disease_location` (may be inherited from a parent; if
  absent, flag it as a note for the author rather than a hard failure).
- **Measurement terms** → `is_about` the measured entity/process (same rule).
- **Imports** are never hand-edited under `src/ontology/imports/`; external terms
  come via `src/ontology/iri_dependencies/*.txt` + regeneration. Cross-ontology
  `SubClassOf` lives in `src/templates/subclasses.csv`. Flag hand-edited
  generated import files.
- **Do not add RO terms** to `efo-relations.txt` (unless the PR/issue explicitly
  asks).

### 7. Build & config regressions
- If the diff should have been normalized, confirm it looks like `make
  normalize_src` was run (consistent formatting) and no unsatisfiable classes were
  introduced (`robot reason -i efo-edit.owl -r ELK`, if runnable). Flag if the
  diff looks un-normalized.
- When the diff touches `.github/` or `.claude/`, check for CI, auth, permissions,
  or workflow regressions.

## Output format

Return a single markdown report, exactly this shape:

```
## EFO PR Review — <PR #N / branch <name>>

**Checklist**
- [ ] Hierarchy and parents are consistent, non-obsolete
- [ ] Definitions carry ≥2 real PMIDs that support the assertion
- [ ] Synonyms are typed and carry a source xref (hasDbXref provenance)
- [ ] Obsoletion / replacement handling is safe (no dangling references)
- [ ] Temporary vs. permanent EFO IDs handled correctly
- [ ] Naming, metadata, and domain relationships preserved
- [ ] No obvious CI, auth, or workflow regression

(tick the boxes that pass)

### Findings

For each issue:
- **<SEVERITY emoji> SEVERITY** — `path/to/file:line` (or term CURIE/IRI) — concise description and the concrete fix.

Severities:
- 🔴 CRITICAL: must fix before merge
- 🟡 IMPORTANT: should fix before merge
- 🔵 SUGGESTION: optional improvement

If a focus area is clean, say so in one line rather than omitting it.

### Summary & recommendation

A short paragraph on the main risks, then one line:
- **Recommendation: REQUEST CHANGES** — if any 🔴 or 🟡 findings.
- **Recommendation: APPROVE** — if only 🔵 or no findings.

Note any references you could not verify and any assumptions you made.
```

Be constructive and specific. Cite `file:line` or the term CURIE/IRI for every
finding so it is actionable. Do not pad the report with praise.
