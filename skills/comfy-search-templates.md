Search for ComfyUI workflow templates available on Comfy Cloud: $ARGUMENTS

Use `search_templates` to find pre-built workflow templates matching the user's query. Templates are ready-to-use workflows from comfy.org that can be deployed directly to Comfy Cloud.

Search strategies:

- If the user describes a task (e.g. "generate a video from an image"), search by text query
- If they mention a category (e.g. "text to image", "video"), filter by tag
- If they mention a specific model (e.g. "Flux", "LTX", "SDXL"), filter by model

Present the results in a clean format:

- Template title
- Description (first sentence)
- Tags
- Models used
- URL to view/deploy

If there are many results, show the top 10 and mention the total count.
