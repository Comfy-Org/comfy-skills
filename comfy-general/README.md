# Comfy General

General-purpose personal automation slash commands for Claude Code. Installs independently from the `comfy-cloud` plugin in the same `comfy-skills` marketplace, so people who don't need it don't see it in their command palette.

## What's inside

| Command | One-liner |
|---------|-----------|
| `/comfy-general:action-items` | Build a classified action-items to-do list from someone's recent Slack and Notion activity and append it to a Notion page. |

The command is fully generic: the person to digest and the target Notion page are passed as arguments, nothing is hardcoded.

## Install (Claude Code)

```
/plugin marketplace add Comfy-Org/comfy-skills
/plugin install comfy-general@comfy-skills
```

Commands are namespaced under the plugin, e.g. `/comfy-general:action-items`.

## Requirements

The `action-items` command needs the Slack and Notion MCP tools connected. It loads them on demand if they are not already available.

## Usage

```
/comfy-general:action-items someone@example.com https://www.notion.so/<page-id>
/comfy-general:action-items someone@example.com <notion-page-id> 6h
```

Pass the person (email or Slack handle), the Notion page (URL or ID), and an optional lookback window (defaults to ~3 hours).
