# Comfy Skills

Home of **Comfy Cloud skills and plugins for AI coding agents** — the slash commands and MCP connection that let an agent generate images, video, audio, and 3D, search models and nodes, and run ComfyUI workflows through [Comfy Cloud](https://cloud.comfy.org).

For internal Comfy engineering conventions, see [comfy-conventions](https://github.com/Comfy-Org/comfy-conventions) instead.

## Install (Claude Code)

The **`comfy-cloud`** plugin bundles the Comfy Cloud MCP connection **and** the slash commands in one step:

```
/plugin marketplace add Comfy-Org/comfy-skills
/plugin install comfy-cloud@comfy-skills
```

Then run `/mcp` to sign in (OAuth). That's it — the plugin registers the hosted MCP server (`https://cloud.comfy.org/mcp`) and adds the commands.

Commands are namespaced under the plugin, e.g. `/comfy-cloud:generate-image`, `/comfy-cloud:search-models`, `/comfy-cloud:help`.

> **Other clients** (Claude Desktop, etc.) don't use Claude Code plugins — they connect to the same hosted MCP server through their own config. Full per-client setup lives in the docs: **https://docs.comfy.org/cloud/mcp**

## Commands

| Command | What it does |
|---|---|
| `/comfy-cloud:generate-image` | Generate, edit, or modify an image |
| `/comfy-cloud:generate-video` | Generate, edit, or extend a video |
| `/comfy-cloud:generate-audio` | Generate audio |
| `/comfy-cloud:generate-3d` | Generate a 3D model |
| `/comfy-cloud:remove-background` | Remove the background from an image |
| `/comfy-cloud:upscale-image` | Upscale an image |
| `/comfy-cloud:search-models` | Search available models |
| `/comfy-cloud:search-nodes` | Search available nodes |
| `/comfy-cloud:search-templates` | Search workflow templates |
| `/comfy-cloud:help` | Show what the Comfy Cloud tools can do |
| `/comfy-cloud:combine-people` | Composite a user's photo with another person |
| `/comfy-cloud:rickroll` | Exactly what it sounds like |

## Repo layout

- **`claude-code/`** — the `comfy-cloud` Claude Code plugin: `commands/` (the slash commands) plus `.claude-plugin/plugin.json` (metadata + the bundled MCP server). **Edit commands here.**
- **`.claude-plugin/marketplace.json`** — the marketplace manifest so `/plugin marketplace add Comfy-Org/comfy-skills` resolves the plugin.
- **`skills/`** — *legacy* flat command files for the deprecated `comfy-cloud-mcp` curl installer. Frozen; will be removed once that installer fully retires.

## Authoring rule: steer the approach, defer the specifics

A command installed on a user's machine is **frozen at install time**. So it must never hard-code facts that change -- which templates exist, which model names are live, which nodes are available. Those rot, and a user who installed in spring is then following guidance written in winter.

Write commands in two layers:

1. **Stable steering** (safe to freeze): the approach. For example, "look for a template first, clone it, swap the input, then submit; prefer structured discovery over guessing."
2. **Live specifics** (never freeze): tell the agent to *discover* current options at run time via the tools, rather than listing them inline. For example, use `search_templates` with the `tag` filter, or `search_nodes` with its typed `output_type` / `category` params, instead of pasting today's template names or node lists into the command.

If you find yourself writing a literal model name, template name, or node id into a command, stop and point the agent at the tool that returns the current set instead. That keeps the command correct as the catalog moves, and it keeps the agent from going off on a tangent before it engages the right tool.

## Contributing

Commands are plain markdown with a short YAML frontmatter `description`. Add or edit a file under `claude-code/commands/`, keep it thin per the rule above, and open a PR. Run `claude plugin validate ./claude-code` before pushing. Keep prose clear and free of emoji.

## Status

`comfy-cloud` is the canonical Claude Code plugin (MCP + commands). The legacy `skills/` flat layout remains only for the deprecated `comfy-cloud-mcp` installer and will be removed once that retires. Cursor / Codex support can be added later as sibling folders.
