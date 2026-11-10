---
name: search-nodes
description: Search Comfy Cloud's nodes and how to wire them. Use when the user asks which node does a job, what inputs a node takes, or how to connect nodes for a ComfyUI workflow.
---

# Search nodes

Use the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`), signed in with OAuth. Node search does not need a generation subscription and does not take an API key.

Call `search_nodes`. Prefer its typed filters (category, input type, output type) when they asked a structural question, and a text query when they named a feature. Read `get_node` before quoting slot names or option lists. Deprecated nodes are often hidden from search. Use a class the search returned.

For each hit, show the name, display name, category, and pack when the tool includes them, plus the inputs and outputs that matter for the question. When they want a pipeline, suggest a wiring only from those returned slots. If search is empty, drop a filter and try once more, then say the catalog had no match.
