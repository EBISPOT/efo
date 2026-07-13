# AGENTS.md — EFO (Codex)

Guidance for coding agents (e.g. Codex CLI) working in the Experimental Factor
Ontology repository. Kept intentionally lean so it does not bloat unrelated
sessions.

## Orientation

- The ontology edit file is `src/ontology/efo-edit.owl` (OWL/XML). Generated
  imports under `src/ontology/imports/` are **never** hand-edited.
- The authoritative curation workflow, routing, and domain rules live in
  **`.github/copilot-instructions.md`** (full guide) and **`CLAUDE.md`**
  (orchestration). Read the relevant one before making ontology changes.
- Specialist agent specs (research, import, editing) are in `.github/agents/` and
  `.claude/agents/`.

## Reviewing a pull request or branch

To review an EFO PR or the current branch **read-only** (no edits, no posting),
follow **`docs/agents-documentation/efo-pr-review-codex.md`**. It applies the
canonical review checklist at
`docs/agents-documentation/efo-pr-review-checklist.md`, which is shared with the
Claude and Copilot reviewers so all three stay in sync.
