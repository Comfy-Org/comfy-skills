# AGENTS.md

Comfy Cloud skills and plugins for AI coding agents: the Agent Skills, slash
commands, and MCP connection that let an agent generate images, video, audio,
and 3D, search models/nodes/templates, and run ComfyUI workflows through the
hosted [Comfy Cloud](https://cloud.comfy.org) service. Everything here is plain
Markdown (command/skill files plus JSON manifests) — there is no application
code, build step, or compiled artifact.

## Commands

This repo has no package manifest, test suite, or lint config. The one check the
project runs is Claude Code's plugin-manifest validator (README "Contributing"):

```bash
claude plugin validate ./claude-code       # comfy-cloud
claude plugin validate ./claude-code-sdk   # comfy-sdk
```

Run them from the repo root. `comfy-cloud` points agents at the hosted MCP
server (`https://cloud.comfy.org/mcp`); it does not run a server. `comfy-sdk`
ships no MCP server.

## Directory map

- `claude-code/` — the `comfy-cloud` plugin for chat, Cowork, and Claude Code.
  **Edit the plugin here.**
  - `claude-code/skills/<name>/SKILL.md` — Agent Skills. `name` matches the
    folder. Descriptions are triggers. Bodies add guidance on top of the MCP
    server's tools and prompts. They must not assume a local install or an API
    key in chat.
  - `claude-code/commands/` — slash commands for Cowork and Claude Code. In
    chat, command files also load as skills, so do not put jokes or
    shell-only pranks here. `rickroll` is not in this folder.
  - `claude-code/.mcp.json` — hosted connector (`https://cloud.comfy.org/mcp`),
    kept in sync with `mcpServers` in `plugin.json`.
  - `claude-code/.claude-plugin/plugin.json` — plugin metadata. `name` stays
    `comfy-cloud`.
- `claude-code-sdk/` — the `comfy-sdk` plugin: one `skills/comfy-sdk/SKILL.md`
  and metadata only. Keep it a single file. Do not add an MCP server here.
- `.claude-plugin/marketplace.json` — marketplace manifest so
  `/plugin marketplace add Comfy-Org/comfy-skills` resolves both plugins.
- `skills/` — **legacy** flat files for the deprecated `comfy-cloud-mcp` curl
  installer. Frozen. Also the snapshot source for Comfy Cloud MCP prompts
  (`refresh-skills` mirrors `skills/*.md`). Do not add `SKILL.md` trees here
  and do not edit these files when changing the plugin.
- There is no `techniques/` directory on `main`. Recipe files that exist today
  are `skills/technique-*.md`. The MCP server serves them through its technique
  tool. Do not copy those recipes into the plugin. `combine-people` is a slash
  command only, not a second skill.
- `openclaw/comfy/SKILL.md` — the OpenClaw-format skill for the hosted MCP.
- `assets/` — static assets (the README logo).
- `.github/workflows/` — CI (see below).

## Conventions and gotchas

- **Authoring rule — steer the approach, defer the specifics** (README has the
  full version). A skill or command is frozen on the user's machine at install
  time, so it must never hard-code facts that rot: template names, live model
  names, node ids.
  Write stable *steering* (the approach) and tell the agent to *discover* current
  options at run time via the tools (`search_templates` with `tag`,
  `search_nodes` with typed params) instead of pasting today's catalog inline. If
  you catch yourself typing a literal model/template/node name into a command,
  point the agent at the tool that returns the current set instead.
- **Skills and commands are thin Markdown.** Skills use `name` and `description`
  frontmatter under `claude-code/skills/<name>/SKILL.md`. Commands use a short
  `description` under `claude-code/commands/`. Keep prose clear, and avoid emoji.
- **`claude-code/` is canonical; `skills/` is frozen.** Prefer editing the plugin
  under `claude-code/`. Don't build new work on the legacy `skills/` layout, and
  don't rewrite it — production MCP prompts are rendered from those files.
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
- `.github/workflows/sdk-skill-smoke.yml` runs on pull requests. It checks that
  `claude-code-sdk/skills/comfy-sdk/SKILL.md` still matches the published SDKs.
  Leave that file's code samples valid. `claude plugin validate` above is still
  the manual pre-push check for both plugins.

## Deeper docs

- `README.md` — install, command table, repo layout, the full authoring rule.
- Per-client MCP setup: <https://docs.comfy.org/cloud/mcp>
- Comfy Cloud: <https://cloud.comfy.org>
