# Comfy Cloud

Comfy Cloud generates and edits images, video, audio, and 3D from a Claude conversation. This plugin bundles Agent Skills for those workflows with a connector to the hosted Comfy Cloud MCP server, so Claude can search the live catalog and run workflows on your Comfy Cloud account. The same plugin loads in chat, Cowork, and Claude Code.

## Use it

Install the plugin from the Claude plugin directory, or from the Comfy Skills marketplace in Claude Code:

```
/plugin marketplace add Comfy-Org/comfy-skills
/plugin install comfy-cloud --marketplace Comfy-Org/comfy-skills
```

The second line is the one-step install on Claude Code 2.1.275 or later. In chat and Cowork, until the plugin is in the directory, add the marketplace from Customize, Plugins, Add, Add marketplace, Add from a repository (`Comfy-Org/comfy-skills`), then add `comfy-cloud` from Discover. Open the plugin's Connectors tab and sign in to Comfy Cloud. In Claude Code, run `/mcp` and authenticate the `comfy-cloud` server. Then ask in plain language: generate an image, extend a video, clone a voice, upscale a photo, remove a background, or find a template. You can also invoke a skill by name, such as `/comfy-cloud:generate-image`.

Sign in with the connector's OAuth flow. A chat does not need an API key, and it does not need a local ComfyUI install. Generation uses your Comfy Cloud subscription. Catalog search does not spend generation credits.

Slash commands in `commands/` remain for people who want to start a task by name in Claude Code or Cowork. The skills are what chat loads on its own when a request matches.

## Data

This plugin stores nothing and ships no credentials. When you connect `https://cloud.comfy.org/mcp`, Claude sends your prompts, any files you upload for a workflow, and the workflow parameters to Comfy Cloud on the account you signed in with. Comfy Cloud runs the job and returns outputs such as images, video, audio, 3D files, or short-lived download links. Catalog searches send the search text to that same host.

The Comfy privacy policy is at <https://comfy.org/privacy>. Setup and tool docs are at <https://docs.comfy.org/cloud/mcp>.
