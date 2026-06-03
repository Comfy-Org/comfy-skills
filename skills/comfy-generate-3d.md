Generate a 3D model using Comfy Cloud based on the user's description: $ARGUMENTS

Follow these steps exactly:

**Step 0 — Route partner-API requests directly.** If the user named a provider, model, or capability (e.g. "Meshy", "Tripo", "Rodin", "Tencent 3D"), do one `search_nodes` lookup with the named term. If the matching node's category starts with `api node/`, try `partner_generate` first — see its tool description for the currently-wired model ids. Pass `type: "3d"` plus the partner's model slug, `prompt`, and any optional fields (`seed`/`medias[]`). On success, return the artifact URL(s) and **stop** — do NOT continue with the workflow steps below. If `partner_generate` returns "unknown model" or "not yet implemented", or the matching node has no `api node/` prefix (OSS model), continue to Step 1.

1. Use `search_templates` with queries like "3D generation", "image to 3D", "text to 3D", or "mesh generation" to find a pre-built 3D workflow template. If a good template exists, use it as the base workflow instead of building from scratch.

2. If no suitable template was found, use `search_nodes` to find 3D-related nodes. Search for "3D", "mesh", or "Hunyuan3D" to discover available 3D generation nodes. Use `search_models` to find 3D models (e.g. Hunyuan3D, TripoSR, InstantMesh).

3. If the user provides a reference image (for image-to-3D), use `upload_file` to upload it first. Many 3D generation workflows take an image as input to create a 3D model from it.

4. Build a ComfyUI API-format workflow JSON with the appropriate 3D nodes. 3D workflows typically involve specialized loader nodes, 3D generation/reconstruction nodes, and 3D output nodes. If using a template, modify the prompt and settings as needed.

5. **Validate the workflow has inputs and outputs before submitting.** Confirm the JSON contains:
   - At least one **input node** carrying the user's intent (text prompt node, LoadImage for image-to-3D, etc.).
   - At least one **output/save node** wired to the final mesh/output (e.g. `SaveGLB`, `Hunyuan3DSaveMesh`, `SaveImage` for preview renders, or the partner node's own save output).

   API-backed partner nodes often produce an output tensor but **do not include a save node by default** — you must add one and wire it to their output. Without it the job runs successfully but produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow` with the workflow JSON. Note: 3D generation can take longer than image generation.

7. Poll `get_job_status` every 5 seconds until the job is completed. Show the user a brief status update while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the generated 3D output. Pass a short `description` parameter (e.g. "red sports car 3d model") so the saved file gets a descriptive name.

9. Tell the user where the 3D output files were saved. 3D outputs may include mesh files (.obj, .glb), textures, or rendered preview images.

If any step fails, show the error clearly. 3D generation support in ComfyUI is actively evolving — fewer templates and models may be available compared to image generation.
