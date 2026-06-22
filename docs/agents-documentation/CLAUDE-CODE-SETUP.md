# EFO Agent System — Claude Code Setup

This repo's multi-agent EFO curation workflow runs in **both** GitHub Copilot and **Claude Code**. The Copilot files are unchanged; this document covers the Claude Code adaptation.

## How to use it

Assign a ticket and Claude takes it end-to-end — branch, research, imports, OWL edits, verification, and a PR with a summary table:

```
/efo-ticket 2546
```

Or just say: *"handle issue #2546"* — `CLAUDE.md` drives the same workflow.

You can also invoke a single specialist directly, e.g. *"use the efo-curator subagent to research ATAC-seq"*.

## What maps to what

| Copilot | Claude Code | Purpose |
|---------|-------------|---------|
| `.github/copilot-instructions.md` | `CLAUDE.md` | Orchestrator: routing, policy, ticket→PR workflow |
| `.github/agents/EFO-curator.md` | `.claude/agents/efo-curator.md` | Literature research & validation |
| `.github/agents/EFO-importer.md` | `.claude/agents/efo-importer.md` | External-ontology imports via OLS |
| `.github/agents/EFO-ontologist.md` | `.claude/agents/efo-ontologist.md` | OWL/XML editing of `efo-edit.owl` |
| `handoffs:` frontmatter | Orchestrator dispatches via the Task tool | Agent invocation |
| `.vscode/mcp.json` | `.mcp.json` | MCP servers (`OLS-MCP`, `artl-mcp`) |
| — | `.claude/commands/efo-ticket.md` | One-shot `/efo-ticket N` trigger |

## Key differences from the Copilot model

Claude Code subagents behave differently, and the design reflects that:

- **Subagents can't call each other.** All routing and sequencing lives in the orchestrator (`CLAUDE.md` / the command). The Copilot `handoffs:` blocks are replaced by the orchestrator dispatching each subagent in turn.
- **Subagents are stateless** and return a single report. The orchestrator passes full context up front (handoff template in `CLAUDE.md`). Subagents share the working tree, so their file edits persist for the next step.
- **Only the orchestrator touches git.** Subagents edit files, run `make`, and run `robot`; the orchestrator creates the branch, commits, and opens the PR. (In the Copilot setup the ontologist did its own commits.)
- **Tool scoping** is enforced via each subagent's `tools:` frontmatter — the curator is read-only (no Edit/Write), the importer/ontologist can edit but not commit.

## MCP servers

`.mcp.json` declares the two servers the agents need:
- **OLS-MCP** (`http://www.ebi.ac.uk/ols4/api/mcp`) — ontology lookup, used by curator, importer, ontologist.
- **artl-mcp** (`uvx artl-mcp`) — Europe PMC literature, used by the curator.

Tool names appear as `mcp__OLS-MCP__*` and `mcp__artl-mcp__*`. Approve the servers when Claude Code first prompts.

## Running in the cloud (later)

Today this runs in local Claude Code. `.github/workflows/copilot-setup-steps.yml` documents the environment EFO needs (ROBOT, obo-scripts, `uv`, aurelian) and remains the reference. To run Claude Code as a GitHub-triggered cloud agent, add a workflow using the official Claude Code GitHub Action that:
1. Reproduces those setup steps (ROBOT + obo-scripts on PATH, `uv` venv with `aurelian jinja2-cli`),
2. Provides an `ANTHROPIC_API_KEY` secret,
3. Invokes the equivalent of `/efo-ticket <number>` on issue assignment.

The `CLAUDE.md` + `.claude/` structures already work unchanged in that environment, since `.mcp.json` and the subagent specs are committed to the repo.
