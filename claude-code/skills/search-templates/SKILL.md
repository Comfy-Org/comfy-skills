---
name: search-templates
description: Find a pre-built Comfy Cloud workflow template. Use when the user asks for a template, a starting workflow, or which ready-made graph matches a task, a tag, or a model family.
---

# Search templates

Use the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`), signed in with OAuth. Template search does not need a generation subscription and does not take an API key.

Call `search_templates`. Use a text query for a task they described, a tag filter when they named a category, and a model filter when they named a family. The tool description lists the current arguments. Do not invent template names.

Show title, the first sentence of the description, tags, and models used, when the tool returns them, plus a link to view the template if one is present. If many rows come back, show the first page and the total. If none match, relax the filter once.

When they want it run, not just listed, read `get_template_schema` and use `run_template`. That hand-off is the generation skill for the media type.
