# Comfy Cloud

Generate and edit images, video, audio, and 3D with ComfyUI on [Comfy Cloud](https://cloud.comfy.org), straight from Claude. The plugin connects Claude to the hosted Comfy Cloud MCP server and adds slash commands for common tasks: run templates and workflows, search models, nodes, and templates, estimate credits, upload inputs, and manage jobs and outputs.

## What you need

- A Comfy account. You sign in with OAuth the first time Claude uses the server.
- Browsing and searching the catalog works with just an account. Generating media uses Comfy Cloud credits and needs an active subscription.

This plugin drives Comfy Cloud only. It does not connect to a local ComfyUI install.

## Install (Claude Code)

```
/plugin marketplace add Comfy-Org/comfy-skills
/plugin install comfy-cloud@comfy-skills
```

Then run `/mcp` and sign in to Comfy Cloud.

## Commands

| Command | What it does |
|---|---|
| `/comfy-cloud:generate-image` | Generate, edit, or modify an image |
| `/comfy-cloud:generate-video` | Generate, edit, or extend a video |
| `/comfy-cloud:generate-audio` | Generate speech or sound effects |
| `/comfy-cloud:clone-voice` | Clone a voice from a reference recording and speak text with it |
| `/comfy-cloud:generate-3d` | Generate a 3D model |
| `/comfy-cloud:remove-background` | Remove the background from an image |
| `/comfy-cloud:upscale-image` | Upscale an image |
| `/comfy-cloud:combine-people` | Composite multiple people into one image |
| `/comfy-cloud:search-models` | Search the model catalog |
| `/comfy-cloud:search-nodes` | Search nodes, with wiring hints |
| `/comfy-cloud:search-templates` | Find pre-built workflow templates |
| `/comfy-cloud:help` | Show what the Comfy Cloud tools can do |
| `/comfy-cloud:rickroll` | Exactly what it sounds like |

## What the plugin runs and sends

- The plugin contains only Markdown commands and a manifest. It runs no local code, scripts, or hooks.
- It declares one remote MCP server, `https://cloud.comfy.org/mcp` (HTTP). Prompts, workflow definitions, and any files you choose to upload are sent to that server so Comfy Cloud can run them. Generated outputs are stored in your Comfy Cloud account.
- Some generations run on third-party model providers (partner APIs) through Comfy Cloud. Comfy Cloud makes those calls; the plugin does not contact them directly.

## Links

- Documentation: https://docs.comfy.org/cloud/mcp
- Privacy policy: https://comfy.org/privacy-policy/
- Terms of service: https://comfy.org/terms-of-service/
- Support: support@comfy.org

## License

MIT. See [LICENSE](LICENSE).
