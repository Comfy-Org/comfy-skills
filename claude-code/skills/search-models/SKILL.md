---
name: search-models
description: Search Comfy Cloud's model catalog. Use when the user asks which checkpoints, LoRAs, VAEs, ControlNets, or upscalers exist, or asks for a model by style, base family, or source.
---

# Search models

Use the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`), signed in with OAuth. Catalog search does not need a generation subscription and does not take an API key.

Call `search_models`. The tool description is the filter list. Use a text query when they did not name a type. When they name a kind (checkpoint, LoRA, VAE, ControlNet, upscaler) or a base family, set the matching filter the tool documents. Do not answer from memory, and do not add models the tool did not return.

Show the rows it returned: name, type, base model, and source when those fields are present. If the tool returns more than you should paste, show the first page it gave you and say how many more it reported. If the result is empty, broaden the query once, then say nothing matched.
