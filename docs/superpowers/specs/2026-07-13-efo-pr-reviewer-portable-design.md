# EFO PR-review capability, portable across Claude / Copilot / Codex

**Issue:** [#2746](https://github.com/EBISPOT/efo/issues/2746)
**Date:** 2026-07-13
**Status:** Approved design — ready for implementation planning

## Problem

A generic, read-only ontology PR-review capability (the user-level `review-pr`
skill + `ontology-pr-reviewer` subagent) currently lives at the **user level**
(`~/.claude/`). It works across ontology repos (UBERON, EFO, CL, MONDO) but only
helps contributors who have that personal Claude Code setup installed.

We want an **EFO-specific** review capability that **ships with this repo** —
like the existing `efo-curator` / `efo-importer` / `efo-ontologist` agents (which
already exist as a Claude/Copilot pair) — so any contributor gets PR-review
support out of the box, regardless of which coding agent they use:

1. **Claude Code** (reference/default implementation)
2. **GitHub Copilot**
3. **Codex** (OpenAI Codex CLI)

Some contributors don't have Claude access, so the reviewer must not be
Claude-exclusive.

## Key design decision — separate two concerns

"Separate files per platform" conflates two independent decisions:

1. **Platform wrappers** (invocation glue: frontmatter, tool declarations,
   trigger mechanism). These *must* be separate — Claude, Copilot, and Codex
   each have different mechanisms. The existing `efo-*` agent pairs already prove
   this pattern.
2. **The review checklist itself** (the substance: hierarchy, xrefs/PMIDs,
   synonym typing, obsoletion safety, temp-ID handling). This is **identical**
   across all three platforms. Duplicating it three times is the #1 drift risk
   the ticket flags.

**Resolution (approved):** a **two-layer** design — one canonical checklist doc
as the single source of truth, and thin per-platform wrappers that **reference**
it rather than restating the rules. All three agents can read repo files at
runtime, so referencing (not duplicating) is feasible.

## Architecture

### Layer 1 — canonical checklist (single source of truth)

`docs/agents-documentation/efo-pr-review-checklist.md`

EFO-specialized; **no OBO-vs-OWL branching** (unlike the generic source). Contains
the review substance and the output contract:

- **Hierarchy & parents** — parents non-obsolete; genus–differentia logical defs
  mirror the text definition; every term has ≥1 asserted-or-implicit superclass;
  no cycles.
- **Definitions & references** — every new/edited term has a definition with
  **≥2 PMIDs**, embedded as nested `oboInOwl:hasDbXref` inside `obo:IAO_0000115`;
  PMIDs are real and support the assertion (flag, don't assert, when unverifiable).
- **Synonyms** — typed (`hasRelatedSynonym` for abbreviations/acronyms,
  `hasNarrowSynonym` for brand/narrow, `hasExactSynonym`, `hasBroadSynonym`); each
  carries a source `hasDbXref` encoded as a reified `owl:Axiom` on the synonym
  assertion. Bare synonyms flagged 🟡 for the author to confirm.
- **Obsoletion safety** — `obsolete_` label prefix, `owl:deprecated=true`,
  `efo:obsoleted_in_version`, `efo:reason_for_obsolescence`, `obo:IAO_0100001`
  (replaced-by) when a replacement exists; obsolete terms carry no logical axioms;
  **no remaining reference points at the obsoleted term** (including the "Type
  (is-a)" column of `src/templates/subclasses.csv`).
- **Temporary IDs** — `EFO_099xxxx` is the marker of an agent-generated temporary
  ID (replaced by automation after merge). A non-`EFO_099xxxx` ID is permanent and
  must not be relabeled temporary or renumbered.
- **Signing** — authored terms signed `obo:IAO_0000117` = `AI agent` (no `@`);
  `term_tracker_item` links the issue where appropriate.
- **Domain expectations** — disease terms → `has_disease_location` (may be
  inherited; flag if absent); measurement terms → `is_about` the measured entity.
- **Imports** — never hand-edited under `src/ontology/imports/`; only
  `iri_dependencies/*.txt` + regeneration; cross-ontology `SubClassOf` via
  `subclasses.csv`.
- **Output contract** — severity legend (🔴 CRITICAL / 🟡 IMPORTANT /
  🔵 SUGGESTION), a tick-box checklist, and a single
  **REQUEST CHANGES / APPROVE** recommendation.

### Layer 2 — thin per-platform wrappers

Each wrapper is glue only: it establishes the target, read-only constraints, and
the output expectation, then instructs the agent to **read the canonical
checklist and apply it**. No wrapper restates the rules.

| Platform | File(s) | Notes |
|---|---|---|
| **Claude** | `.claude/agents/efo-pr-reviewer.md` (read-only subagent) + `.claude/skills/efo-pr-review/SKILL.md` (driver) | Agent tools: `Bash, Read, Grep, Glob, WebFetch, WebSearch` — **no Edit/Write**. Skill determines target and owns the only GitHub-write step. |
| **Copilot** | `.github/agents/EFO-pr-reviewer.md` | Mirrors existing `EFO-*.md` frontmatter/style (`model: Gemini 3 Pro (Preview)`); read-only by explicit instruction. |
| **Codex** | `AGENTS.md` (new, slim, one-line pointer) + `docs/agents-documentation/efo-pr-review-codex.md` (on-demand reviewer) | `AGENTS.md` stays lean so unrelated Codex sessions aren't polluted; the pointer directs Codex to the on-demand doc, which in turn applies the canonical checklist. |

## Behavior (identical across platforms)

Derived from the source `review-pr` skill / `ontology-pr-reviewer` agent:

- **Target resolution:**
  - PR number argument → that PR (`gh pr diff <N>`, `gh pr view <N> --json …`).
  - No argument → current branch vs default branch (`git diff <base>...HEAD`);
    works even with no open PR (local-branch case). Default branch via
    `git symbolic-ref --quiet refs/remotes/origin/HEAD`, else `master`.
  - No diff vs base and no PR → nothing to review; stop.
- **Edit file is hard-coded** to `src/ontology/efo-edit.owl` (the generic
  version's OBO/OWL detection is removed).
- **Read-only by construction:** returns a structured markdown report; never
  edits, stages, commits, pushes, or opens/edits PRs.
- **Publish only on explicit request:** `gh pr comment <N> --body-file <file>`
  (non-blocking). Never `gh pr review --approve/--request-changes` (this is a
  local advisory review, not the CI gate). No PR yet → tell the user to open one.

## Read-only guarantees

- **Claude:** enforced structurally — the subagent has no Edit/Write tools; the
  driver skill owns the single GitHub-write step under explicit user control.
- **Copilot & Codex:** enforced by explicit prose constraints (these platforms
  cannot hard-restrict tools the way a Claude subagent can).

## Docs / registration

- `.github/copilot-instructions.md` — add `EFO-pr-reviewer` to the agent roster
  and the Multi-Agent Coordination section.
- `docs/agents-documentation/README.md` and `QUICK-REFERENCE.md` — document the
  reviewer and its per-platform invocation.
- `CLAUDE.md` — one line noting the review skill exists (parity touch).

## Non-goals

- No automatic/CI-triggered reviews — manually invoked, local tool only.
- No automatic PR comments or approvals.

## Verification

This is docs + config, not runtime code.

- **Structural:** each wrapper's frontmatter is valid; its reference path to the
  canonical checklist resolves; the read-only constraint is present in all four
  wrappers.
- **Smoke test (Claude path, executable in-session):** dispatch `efo-pr-reviewer`
  against a recent real PR/branch; confirm it produces a sane structured report
  and modifies nothing.
- **Copilot / Codex:** cannot be executed in this session → verified
  structurally, with a manual smoke-test note left in the PR.

## Open questions (resolved)

- Shared checklist vs duplicated per platform → **one canonical doc, wrappers
  reference it.**
- Codex invocation UX → **slim `AGENTS.md` pointer + dedicated on-demand prompt
  doc** (`efo-pr-review-codex.md`).
