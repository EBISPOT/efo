---
description: Take an EFO GitHub issue end-to-end — research, import, edit, and open a PR
argument-hint: <issue-number>
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite, mcp__OLS-MCP__search, mcp__OLS-MCP__searchClasses, mcp__OLS-MCP__fetch
---

You are the **EFO orchestrator** (see `CLAUDE.md`). Take issue **#$1** all the way from ticket to reviewable PR. Do not stop halfway; the only reasons to pause are a genuine blocker or a decision that needs the user/issue author.

Work through these steps, tracking them with a todo list:

1. **Read the ticket.** Run `gh issue view $1`. Read any linked issues. Extract every PMID/DOI in the title or body — they must be read during curation.
2. **Triage** using the Routing table in `CLAUDE.md`. State your plan (which subagents, in what order) before acting.
3. **OLS pre-check** (new terms): confirm the concept isn't already in an imported ontology. If it is, treat it as an import.
4. **Create the branch from an up-to-date `master`.** Always start the issue branch from the latest `origin/master` so it never builds on stale or unrelated work:
   ```bash
   git fetch origin master
   git checkout -b issue-$1 origin/master   # branches directly from fresh remote master
   ```
   Branching from `origin/master` guarantees freshness regardless of your current branch or local state. If you keep a local `master`, fast-forward it too: `git checkout master && git merge --ff-only origin/master`. Ensure the working tree is clean first (`git status`) — commit or stash unrelated changes before branching. If a branch/PR for this issue already exists, check it out and continue instead of starting over (rebase it onto the latest `origin/master` if it has fallen behind).
5. **Dispatch the specialist subagents in sequence** via the Task tool, using the handoff template from `CLAUDE.md`:
   - `efo-curator` for research/validation (new terms, or definitions needing citations)
   - `efo-importer` for ANY external term (never import yourself)
   - `efo-ontologist` to edit `efo-edit.owl`
   Review each report; re-dispatch with specific feedback if incomplete. Enforce: ≥2 PMIDs per new term, typed synonyms, non-obsolete verified parents.
6. **Verify** from `src/ontology`: `make normalize_src`, and `robot reason -i efo-edit.owl -r ELK`. Fix or report failures honestly.
7. **Commit & open the PR** yourself (subagents never touch git):
   - `git add -A && git commit -m "<action>: <desc> (refs #$1)"`
   - `git push -u origin issue-$1`
   - `gh pr create` with the summary template from `CLAUDE.md` (Summary, Changes table, References, Checks, Notes, `Closes #$1`).
8. **Report back** the PR URL, a one-paragraph summary, and any open questions or PR comments left for the reviewer.

If at any step you are not confident how to proceed, stop and ask — comment on the issue with `gh issue comment $1` and/or ask the user. Never guess PMIDs, ontology IDs, or parent terms.
