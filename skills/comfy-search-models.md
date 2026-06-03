Search for ComfyUI models available on Comfy Cloud: $ARGUMENTS

Use `search_models` to find models matching the user's query. If they didn't specify filters, search by text. If they mentioned a type (checkpoint, lora, vae, controlnet, upscaler), filter by type. If they mentioned a base model (SD 1.5, SDXL, Flux), filter by base_model.

Present the results in a clean table format:

- Model name
- Type
- Base model (if available)
- Source (huggingface/civitai)

If there are many results, show the top 10 and mention the total count.
