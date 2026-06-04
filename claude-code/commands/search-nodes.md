---
description: Search Comfy Cloud's nodes with wiring hints
---

Search for ComfyUI nodes available on Comfy Cloud: $ARGUMENTS

Use `search_nodes` to find nodes matching the user's query. If they asked about a category (image processing, sampling, conditioning), filter by category. If they asked about I/O types (IMAGE, LATENT, MODEL), filter by input_type or output_type.

Present the results clearly:

- Node name and display name
- Category
- Pack (which custom node pack it belongs to, or "core" for built-in)
- Inputs and outputs

If they're looking for nodes to accomplish a specific task, suggest which nodes to use together and how to wire them up.
