---
description: Show what you can do with your local ComfyUI
---

Show the user what they can do with the local comfy-mcp tools.

Explain in a friendly, concise way:

**What you can do:**

- Generate images for free, straight from a text prompt, on your own GPU
- Generate video, image, audio, or other output from the built-in template gallery, or a hand-built workflow
- Run PAID partner models (Flux Pro, Kling, Nano Banana, DALL-E, …) when you want hosted quality or speed instead of local compute — always asks before spending
- Search the built-in template gallery, and the models and nodes your OWN install actually has — model and node search is live against your install; template search is the bundled gallery
- Validate a workflow against your live ComfyUI before running it, and get a normalized diagnosis when one fails
- Manage your local ComfyUI: launch, stop, restart, check GPU/VRAM, tail logs, install a missing custom node pack, update ComfyUI, or switch versions
- Upload input files, download models, and fetch a job's output files

**Quick examples to try:**

- "Generate a photo of a mountain lake at golden hour"
- "Is my ComfyUI running? What GPU does it see?"
- "Find me a text-to-video template"
- "What nodes take an IMAGE and produce a LATENT?"
- "Validate this workflow before I run it"
- "Search my install for SDXL checkpoints"

**How it works:**
comfy-mcp runs as a local process (started via `uvx comfy-mcp`) and drives `comfy-cli` against the ComfyUI on THIS machine — no cloud GPU, and no charge for local generation. Call `server_info` any time something seems off; it reports whether ComfyUI is reachable, your hardware, and whether comfy-cli or ComfyUI itself is out of date.

**Tips:**

- Templates without partner/API nodes and `generate_image` never ask for spend confirmation; a gallery template that contains a partner/API node spends credits like any partner model and always asks first — say yes only when you actually want to pay
- If a workflow won't run, `validate_workflow` usually says exactly what's missing (a model, a node, an input)
- A missing custom node? `workflow_deps` maps it to the pack, then `install_node` + `restart_comfyui` picks it up
- Point `COMFY_PROJECT` at a directory to anchor relative paths, or check `/comfy-local:project-status`
