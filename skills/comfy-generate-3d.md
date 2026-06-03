Generate a 3D model using Comfy Cloud based on the user's description: $ARGUMENTS

Approach: prefer a ready-made template over hand-building, and discover the current options with the tools rather than assuming a fixed catalog. Model, node, and template availability changes over time, so let the tools tell you what exists right now.

**Step 0 - Partner-API shortcut.** If the user named a provider or capability (Meshy, Tripo, Rodin, Tencent, and so on), find the matching node with `search_nodes` filtered by `category: "api node/3d"` (optionally add a `q` for the provider name). If a matching `api node/3d/...` node exists, try `partner_generate` first with `type: "3d"` and that provider's model slug, plus `prompt` and any optional fields (`seed`, `medias[]`). On success, return the artifact URL(s) and stop. If it returns "unknown model" or "not yet implemented", continue below.

1. **Look for a template first.** Call `search_templates` with `tag: "Image to 3D"` (image-to-3D is the common case), and/or `q: "3d"` for the broader set. If a suitable template comes back, clone it as your base workflow: swap in the user's input (such as the reference image) and adjust settings instead of building from scratch. Cloning a template is almost always faster than hand-wiring nodes, so spend real effort here before falling through to step 2.

2. **If no template fits, discover nodes structurally - do not free-text guess.** Use `search_nodes` with its typed filters, which match against the live catalog:
   - `output_type: "FILE_3D_GLB"` (also `MESH`, `FILE_3D_OBJ`) to find nodes that produce a 3D file.
   - `category: "3d"` or `category: "api node/3d"` to browse the 3D nodes.
   - `input_type: "IMAGE"` to find what accepts an image, for image-to-3D.

   Use `search_models` for any checkpoints the chosen nodes require. Do not paste in remembered model or node names - query for them, because the set changes.

3. If the user provides a reference image (image-to-3D), `upload_file` it first.

4. Build a ComfyUI API-format workflow JSON, or edit the cloned template. A 3D workflow generally chains an input, a 3D generation or reconstruction node, and a 3D save/output node.

5. **Validate inputs and outputs before submitting.** Confirm the workflow has:
   - at least one input node carrying the user's intent (a text prompt node, or LoadImage for image-to-3D), and
   - at least one save/output node wired to the final mesh. If you are unsure of the exact node, find it with `search_nodes output_type: "FILE_3D_GLB"`.

   API and partner nodes often produce an output but include no save node by default. Add and wire one, or the job runs and produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow`. 3D generation can take longer than image generation.

7. Poll `get_job_status` every 5 seconds until completed, showing brief status updates while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the result. Pass a short `description` (for example "red sports car 3d model") so the saved file gets a descriptive name.

9. Tell the user where the files were saved. 3D outputs may include mesh files (.obj, .glb), textures, or rendered preview images.

If a step fails, show the error clearly and use the search tools to find a current alternative rather than assuming none exists.
