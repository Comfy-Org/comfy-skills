# Comfy Skills

The single source of truth for **Comfy Cloud product skills** -- the slash commands that let an AI agent generate images, video, audio, and 3D, search models and nodes, and run ComfyUI workflows through [Comfy Cloud](https://cloud.comfy.org).

These are end-user skills (for people using Comfy Cloud via Claude Code, Claude Desktop, and other MCP clients). For internal Comfy engineering conventions, see [comfy-conventions](https://github.com/Comfy-Org/comfy-conventions) instead.

## Skills

| Skill | What it does |
|---|---|
| `comfy-generate-image` | Generate, edit, or modify an image |
| `comfy-generate-video` | Generate, edit, or extend a video |
| `comfy-generate-audio` | Generate audio |
| `comfy-generate-3d` | Generate a 3D model |
| `comfy-remove-background` | Remove the background from an image |
| `comfy-upscale-image` | Upscale an image |
| `comfy-search-models` | Search available models |
| `comfy-search-nodes` | Search available nodes |
| `comfy-search-templates` | Search workflow templates |
| `comfy-help` | Show what the Comfy Cloud tools can do |
| `technique-combine-people` | Composite a user's photo with another person |
| `comfy-rickroll` | Exactly what it sounds like |

## How these are used

This repo is the **one place** the skills are authored. Everything else consumes from here, so the guidance never drifts across surfaces:

- **Installers** (the Comfy Cloud MCP installer) pull these skill files and install them as local slash commands on the user's machine.
- **The MCP server** bundles them at build time so the same guidance is available as server-side prompts.

One source, many delivery surfaces. Do not hand-edit copies elsewhere -- change them here.

## Authoring rule: steer the approach, defer the specifics

A skill installed on a user's machine is **frozen at install time**. So a skill must never hard-code facts that change -- which templates exist, which model names are live, which nodes are available. Those rot, and a user who installed in spring is then following guidance written in winter.

Write skills in two layers:

1. **Stable steering** (safe to freeze): the approach. For example, "look for a template first, clone it, swap the input, then submit; prefer structured discovery over guessing."
2. **Live specifics** (never freeze): tell the agent to *discover* current options at run time via the tools, rather than listing them inline. For example, use `search_templates` with the `tag` filter, or `search_nodes` with its typed `output_type` / `category` params, instead of pasting today's template names or node lists into the skill.

If you find yourself writing a literal model name, template name, or node id into a skill, stop and point the agent at the tool that returns the current set instead. That keeps the skill correct as the catalog moves, and it keeps the agent from going off on a tangent before it engages the right tool.

## Contributing

Skills are plain markdown. Add or edit a file under `skills/`, keep it thin per the rule above, and open a PR. Keep prose clear and free of emoji.

## Status

Being consolidated as the canonical home for Comfy Cloud product skills (previously duplicated across the MCP server and installer repos). Consumer wiring (installer pull + server build-time bundling) is in progress.
