---
name: consistent-characters
description: Keep one or more characters visually consistent across images or video on Comfy Cloud. Use when the user wants the same person, mascot, or character to match across scenes, a turnaround, a storyboard, or a sequence of shots.
---

# Consistent characters

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`), signed in with OAuth. There is no API key to collect, and there is no local ComfyUI install to start.

The live recipe is on the server, not in this skill. Call `get_creative_technique` the way that tool's description says to request the consistent-characters technique, and read a `comfy://guides/techniques/` resource when the server lists one for this task. Follow that text. It is refreshed from the catalog. Do not type node class names, model ids, or slot paths from memory. If the tool returns nothing for this technique, say so, then use the rules below and discover nodes with `search_nodes` and `get_node`.

## Rules that stay true as the catalog moves

- One reference set per character. Generate or upload each character in its own run so traits do not bleed. `upload_file` anything the next job must load. A saved output is not automatically a loadable input.
- Reuse those same reference files on every shot. A previous shot can guide lighting. It is a poor identity reference, because drift compounds.
- One image per reference slot. Copy slot names from `get_node` for the node you selected. A flat array is not a substitute when the schema is a list of slots.
- The prompt names which slot is which character, with a few traits that must survive, and it states how many people are in the frame.
- For motion, `search_templates` for reference-to-video and wire the same references. Do not pick a video family by memory.

Show a couple of seeds and let them choose. Regenerate the shots that drifted, with the same references. Discovery does not spend generation credits. A generation needs an active Comfy Cloud subscription.
