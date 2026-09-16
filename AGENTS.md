# AGENTS.md

Comfy Cloud skills and plugins for AI coding agents: the slash commands and MCP
connection that let an agent generate images, video, audio, and 3D, search
models/nodes/templates, and run ComfyUI workflows through the hosted
[Comfy Cloud](https://cloud.comfy.org) service. Everything here is plain Markdown
(command/skill files plus JSON manifests) — there is no application code, build
step, or compiled artifact.

## Commands

This repo has no package manifest, test suite, or lint config. The one check the
project runs is Claude Code's plugin-manifest validator (README "Contributing"):

```bash
claude plugin validate ./claude-code   # validate the comfy-cloud plugin before pushing
```

Run it from the repo root; it validates `claude-code/.claude-plugin/plugin.json`.
There is nothing to install, build, or run locally — the plugin points agents at
the hosted MCP server (`https://cloud.comfy.org/mcp`), it does not run a server.

## Directory map

- `claude-code/` — the `comfy-cloud` Claude Code plugin. **Edit commands here.**
  - `claude-code/commands/` — the slash-command Markdown files (`generate-image`,
    `generate-video`, `search-templates`, `help`, …).
  - `claude-code/.claude-plugin/plugin.json` — plugin metadata + the bundled
    `comfy-cloud` HTTP MCP server declaration.
- `.claude-plugin/marketplace.json` — marketplace manifest so
  `/plugin marketplace add Comfy-Org/comfy-skills` resolves the plugin.
- `skills/` — **legacy** flat command files for the deprecated `comfy-cloud-mcp`
  curl installer. Frozen; slated for removal once that installer retires.
- `openclaw/comfy/SKILL.md` — the OpenClaw-format skill for the hosted MCP.
- `assets/` — static assets (the README logo).
- `.github/workflows/` — CI (see below).

## Conventions and gotchas

- **Authoring rule — steer the approach, defer the specifics** (README has the
  full version). A command is frozen on the user's machine at install time, so it
  must never hard-code facts that rot: template names, live model names, node ids.
  Write stable *steering* (the approach) and tell the agent to *discover* current
  options at run time via the tools (`search_templates` with `tag`,
  `search_nodes` with typed params) instead of pasting today's catalog inline. If
  you catch yourself typing a literal model/template/node name into a command,
  point the agent at the tool that returns the current set instead.
- **Commands are thin Markdown** with a short YAML frontmatter `description`. Add
  or edit under `claude-code/commands/`, keep prose clear, and avoid emoji.
- **`claude-code/` is canonical; `skills/` is frozen.** Prefer editing the plugin
  under `claude-code/`. Don't build new work on the legacy `skills/` layout.
- **comfy-cli skills live elsewhere.** The `comfy`, `comfy-debug`, `comfy-build`,
  etc. agent skills are no longer in this repo — they ship bundled inside
  [comfy-cli](https://github.com/Comfy-Org/comfy-cli) (`comfy_cli/skills/`) and
  install via `comfy skills install`. Don't re-add them here.
- **Commit style — Conventional Commits with an optional scope**, matching the
  git history: `feat(generate-video): …`, `fix(generate-audio): …`,
  `chore: …`, `docs(openclaw): …`. Land changes via pull request.
- **Public repo.** This repository is public; keep everything committed here fit
  for a world-readable audience (no secrets, no private internal detail).

## CI

- `.github/workflows/detect-unreviewed-merge.yml` runs on every push to `main`:
  a SOC 2 compliance check that flags merges landing without an approving review
  (it calls a reusable workflow in `Comfy-Org/github-workflows` and opens a
  tracking issue). It is **not** a build/test/lint gate — it does not validate
  the plugin or block PRs — so it stays green regardless of content changes.
  There is no automated test or lint workflow; `claude plugin validate` above is
  the manual pre-push check.

## Deeper docs

- `README.md` — install, command table, repo layout, the full authoring rule.
- Per-client MCP setup: <https://docs.comfy.org/cloud/mcp>
- Comfy Cloud: <https://cloud.comfy.org>
