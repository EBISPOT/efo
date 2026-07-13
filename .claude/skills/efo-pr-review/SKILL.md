---
name: efo-pr-review
description: Use when asked to review an EFO pull request or the current branch's changes. Dispatches the read-only efo-pr-reviewer subagent, which reviews src/ontology/efo-edit.owl against the canonical EFO checklist (hierarchy, definitions, xrefs/PMIDs, synonym typing, obsoletion safety, temporary EFO_099xxxx ID handling), returns a structured report, and can optionally publish it as a PR comment on explicit request.
---

# Review EFO PR

On-demand, **local** PR/branch review for the Experimental Factor Ontology. It
never runs automatically and never posts to GitHub unless the user explicitly
asks. The edit file is always `src/ontology/efo-edit.owl`.

The heavy diff + ontology analysis runs in an isolated, **read-only** subagent
(`efo-pr-reviewer`) so it does not clutter the main conversation and cannot
accidentally modify or push anything. All review substance lives in the canonical
checklist `docs/agents-documentation/efo-pr-review-checklist.md`, which the
subagent reads.

## Step 1 — Determine the target

- **Argument given (a PR number):** target that PR. Confirm the repo with
  `gh repo view --json nameWithOwner -q .nameWithOwner`.
- **No argument:** review the **current branch** against the default branch (works
  even with no open PR):
  - default branch: `git symbolic-ref --quiet refs/remotes/origin/HEAD` (strip to
    the name), else `master`.
  - target = `git diff <base>...HEAD`.
- If there is no PR and the branch has no diff vs. base, tell the user there's
  nothing to review and stop.

## Step 2 — Dispatch the read-only reviewer

Dispatch the **`efo-pr-reviewer`** subagent (Agent tool,
`subagent_type: "efo-pr-reviewer"`). Hand it the concrete target, e.g.:

> Review **PR #1234** in repo `EBISPOT/efo`. Get the diff with `gh pr diff 1234`
> and context with `gh pr view 1234 --json title,body,files,baseRefName,headRefName`.
> Read the canonical checklist at
> `docs/agents-documentation/efo-pr-review-checklist.md` and return your structured
> report.

or, for a local branch:

> Review the **local branch `issue-123`** against base `master` in `EBISPOT/efo`.
> Get the diff with `git diff master...HEAD`. Read the canonical checklist at
> `docs/agents-documentation/efo-pr-review-checklist.md` and return your structured
> report.

The subagent is read-only: it produces a report and returns it — it does not
edit, commit, push, or post.

## Step 3 — Relay the report

Show the subagent's returned report to the user (it is already formatted as a
markdown review). Add a one-line note that nothing was posted to GitHub and that
you can publish it on request.

## Step 4 — Publish only if the user asks

This is an outward-facing action — do it **only** on an explicit request, and
confirm the PR number + repo first.

- Write the report to a temp file and post it as a **non-blocking comment**:
  `gh pr comment <N> --repo EBISPOT/efo --body-file <file>`
- Do **not** submit a formal `gh pr review --approve/--request-changes` unless the
  user explicitly asks — this is a local advisory review, not the CI review gate.
- If there is no PR yet (local-branch review), there is nothing to comment on;
  tell the user to open the PR first.

## Notes

- Read-only by construction: the reviewer has no Edit/Write tools and is
  instructed never to push or post. The only GitHub-writing step is Step 4, which
  lives here in the main thread under explicit user control.
- EFO-specialized and repo-checked-in: this skill and the `efo-pr-reviewer`
  subagent ship with the repo, so any contributor with Claude Code gets EFO PR
  review out of the box. Copilot and Codex have equivalent wrappers
  (`.github/agents/EFO-pr-reviewer.md`,
  `docs/agents-documentation/efo-pr-review-codex.md`) that reference the same
  canonical checklist.
