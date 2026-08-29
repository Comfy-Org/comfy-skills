---
description: Generate, edit, or modify an image with your local ComfyUI
---

Generate, edit, or modify an image on the user's own ComfyUI based on their description: $ARGUMENTS

Follow these steps:

0. Call `server_info` first to confirm a local ComfyUI is reachable, and check `hardware`/`freshness`/`compatibility`. If it isn't running, offer `launch_comfyui`. If `freshness` reports the core or a pack outdated, say so before concluding the catalog lacks something — update first.

1. Route by intent:
   - Plain text-to-image with no specific model/style: use `generate_image` directly — free, local, and the fastest path. Don't fetch a template for this case.
   - A specific style, checkpoint, or template-shaped request (img2img, inpainting, a named pipeline): use `search_templates` to find a match, inspect with `get_template` (read its `local_check`), then `fetch_template` to write the runnable JSON.
   - A named PARTNER model (Flux Pro, Nano Banana, DALL-E, Ideogram, Recraft, …): confirm the alias and its params with `list_partner_models` / `partner_model_schema`. Two ways to run it, offer whichever fits: `partner_generate` runs entirely on the partner's infrastructure and ALWAYS spends credits; `emit_partner_workflow` writes a local workflow using the partner's node (only five aliases map to one — flux-2, flux-pro, kling-i2v, nano-banana, seedance) that you then run locally with `run_workflow` — still billed when it runs, just executed as a normal workflow.

2. If the user supplies an input image, stage it with `upload_file` first, then reference the returned path in the workflow (a LoadImage node, or the model's binary-type param).

3. Before running a template or hand-authored workflow, make sure it's been checked against the LIVE install — either trust `get_template`/`fetch_template`'s own `local_check`, or call `validate_workflow` directly. Don't run a workflow whose check reports it won't run; surface the specific gap (missing model, missing node) instead of guessing.

4. Spend consent: `generate_image` is always free. Anything that reaches a PARTNER model (`partner_generate`, or `run_workflow`/`run_template` on a workflow carrying a partner-API node) may spend credits. Only pass `confirm_spend=True` after the user has actually agreed — never set it just to clear an error, and never assume consent from an ambiguous request.

5. Submit:
   - `generate_image(prompt, wait=True)` for the free on-ramp.
   - `run_workflow(workflow_path, wait=True, confirm_spend=...)` for a fetched or hand-built workflow.
   - `run_template(name, params, confirm_spend=...)` as the one-call alternative to fetch-then-run when no local edits are needed.
   For a run likely to take a while, prefer `wait=False` and poll with `job(action="wait", prompt_id=...)`, or stream progress with `job(action="watch", prompt_id=...)`. Use `job(action="status")` / `job(action="error")` to inspect afterward, `job(action="cancel")` if the user asks to stop.

6. Report the result — the saved output path(s) from the tool's own response, or `fetch_outputs` if the job was submitted async. Offer to open the file.

If a step fails, show the actual error (comfy-cli's message usually explains it) and suggest the concrete next step: `workflow_deps` -> `install_node` -> `restart_comfyui` for a missing node, `search_models` -> `download_model` for a missing checkpoint, or a comfy-cli upgrade for a version-gated tool.
