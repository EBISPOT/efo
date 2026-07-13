# EFO PR Review — Codex prompt

On-demand instructions for reviewing an EFO pull request or branch diff with the
**Codex CLI**. Codex has no subagent mechanism, so this is a prompt you invoke
when you want a review: point Codex at this file (e.g. "Follow
`docs/agents-documentation/efo-pr-review-codex.md` to review PR #1234" / "…to
review the current branch"). `AGENTS.md` carries a one-line pointer here so it
does not bloat unrelated Codex sessions.

The edit file is always the OWL/XML file **`src/ontology/efo-edit.owl`**.

## The rules live in one place — read them

**All review substance and the exact output format are defined in the canonical
checklist: `docs/agents-documentation/efo-pr-review-checklist.md`.** Read that
file first, then apply it. It is the single source of truth, shared with the
Claude (`.claude/agents/efo-pr-reviewer.md`) and Copilot
(`.github/agents/EFO-pr-reviewer.md`) reviewers so the three stay in sync. Do not
work from a copy of the rules here — apply the checklist.

## Hard constraints (read-only)

- **Never** modify files, stage, commit, push, create branches, or open/edit PRs.
- **Never** post to GitHub (no `gh pr review`, `gh pr comment`, `gh issue
  comment`, reactions). Producing the review and publishing it are separate; the
  human decides whether to publish.
- Only run **read-only** shell commands: `git diff`, `git log`, `gh pr diff/view`,
  `grep`/`rg`, `obo-grep.pl`, `robot query/reason` (if available), `cat`/`sed`/
  `head`/`tail`, `ls`, `find`, `aurelian`.
- The output **is** the review report. Do not ask follow-up questions mid-review;
  note missing information as an assumption or limitation.

## Steps

1. **Read the canonical checklist** at
   `docs/agents-documentation/efo-pr-review-checklist.md`.
2. **Get the diff:**
   - PR number given → `gh pr diff <N>` plus `gh pr view <N> --json
     title,body,files,baseRefName,headRefName`.
   - No PR (local branch) → default branch via `git symbolic-ref --quiet
     refs/remotes/origin/HEAD` (strip to name, else `master`), then
     `git diff <base>...HEAD`. Works with no open PR.
   - No diff and no PR → nothing to review; say so and stop.
3. **Review** `src/ontology/efo-edit.owl` changes against every focus area in the
   checklist (hierarchy/parents, definitions & ≥2 PMIDs, synonym typing + source
   xrefs, obsoletion safety, temporary `EFO_099xxxx` ID handling,
   conventions/metadata, build/config regressions). Inspect terms with the
   grep/`obo-grep.pl`/`robot` techniques the checklist describes. Verify PMIDs
   where possible; flag what you cannot verify rather than asserting it is wrong.
4. **Return the report** in the exact format the checklist specifies — the
   `## EFO PR Review — …` block with the tick-box checklist, severity-tagged
   findings (🔴/🟡/🔵) cited to `file:line`/CURIE, and a single
   **REQUEST CHANGES / APPROVE** recommendation.

## Publishing

Codex does not publish the review. If you want it on the PR, run
`gh pr comment <N> --body-file <file>` yourself — a deliberate, non-blocking
comment, never a formal `gh pr review --approve/--request-changes`.
