---
description: Generate a 3D model with Comfy Cloud
---

Generate a 3D model using Comfy Cloud based on the user's description: $ARGUMENTS

Approach: prefer a ready-made template over hand-building, and discover the current options with the tools rather than assuming a fixed catalog. Model, node, and template availability changes over time, so let the tools tell you what exists right now.

**Step 0 - Partner-API shortcut.** If the user named a provider or capability (Meshy, Tripo, Rodin, Tencent, and so on), find the matching node with `search_nodes` filtered by `category: "partner/3d"` (optionally add a `q` for the provider name). `partner_generate` returns only the output, never a workflow: if the user asked to BUILD or CREATE a workflow (not just for an output), skip `partner_generate` and continue to Step 1, wiring the matching partner node into the workflow you build. If a matching `partner/3d/...` node exists, try `partner_generate` first with `type: "3d"` and that provider's model slug, plus `prompt` and any optional fields (`seed`, `medias[]`). On success, return the artifact URL(s) and stop. If it returns "unknown model" or "not yet implemented", or says it "does not serve type" (3D has no `partner_generate` persist path today), continue below — the template path in step 1 does generate 3D on Comfy Cloud.

1. **Look for a template first.** Call `search_templates` with `tag: "Image to 3D"` (image-to-3D is the common case), and/or `q: "3d"` for the broader set. If a suitable template comes back, clone it as your base workflow: swap in the user's input (such as the reference image) and adjust settings instead of building from scratch. Cloning a template is almost always faster than hand-wiring nodes, so spend real effort here before falling through to step 2.

2. **If no template fits, discover nodes structurally - do not free-text guess.** Use `search_nodes` with its typed filters, which match against the live catalog:
   - `output_type: "FILE_3D_GLB"` (also `MESH`, `FILE_3D_OBJ`) to find nodes that produce a 3D file.
   - `category: "3d"` or `category: "partner/3d"` to browse the 3D nodes.
   - `input_type: "IMAGE"` to find what accepts an image, for image-to-3D.

   Use `search_models` for any checkpoints the chosen nodes require. Do not paste in remembered model or node names - query for them, because the set changes.

3. If the user provides a reference image (image-to-3D), `upload_file` it first.

4. Build a ComfyUI API-format workflow JSON, or edit the cloned template. A 3D workflow generally chains an input, a 3D generation or reconstruction node, and a 3D save/output node. Give EVERY node a `_meta.title` that names its role in plain words (e.g. "Load driving video", "Remove background", "Overlay graphic 1", "Save video"). The canvas shows these titles; without them the user sees only class names.

5. **Validate inputs and outputs before submitting.** Confirm the workflow has:
   - at least one input node carrying the user's intent (a text prompt node, or LoadImage for image-to-3D), and
   - at least one save/output node wired to the final mesh. If you are unsure of the exact node, find it with `search_nodes output_type: "FILE_3D_GLB"`.

   API and partner nodes often produce an output but include no save node by default. Add and wire one, or the job runs and produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow`. 3D generation can take longer than image generation.

7. Poll `get_job_status` every 5 seconds until completed, showing brief status updates while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the result. Pass a short `description` (for example "red sports car 3d model") so the saved file gets a descriptive name.

9. Tell the user where the files were saved. 3D outputs may include mesh files (.obj, .glb), textures, or rendered preview images.

10. If the user asked to BUILD or CREATE a workflow (not just for an output), after the run completes call `save_workflow` with the same JSON, a descriptive `name`, and `overwrite: false` — on a name collision choose a new name rather than replacing the user's existing workflow. Then call `get_workflow_canvas_url` with the `workflow_id` from the save result; if the save result omits `workflow_id`, find it with `list_saved_workflows` — never pass the filename (`saved_workflow_filename` publishes a PUBLIC share snapshot). If you ran a template with `run_template`, call `get_template`, apply the same `input_overrides` you ran with to that body (same node ids or slot paths; inputs you did not override keep the template defaults), and `save_workflow` the result instead, so the canvas matches the run. If you adjusted the run with `submit_workflow` + `from_prompt_id` reruns, apply each rerun's `input_overrides` on top, in run order, to whichever JSON you save (the built workflow or the template body), so the saved workflow matches the latest run rather than the first one. Give the user the canvas link. Mention that the saved layout is auto-generated and may need tidying. If you ran a subgraph template instead, tell the user the canvas shows one collapsed subgraph node and how to open it (double-click the node body, not its title, to step inside it, or right-click it and choose Unpack Subgraph to flatten it onto the canvas).

11. **If the user asks to adjust the result** (different seed, prompt wording, steps/cfg, resolution, a different reference image) rather than a new subject: do NOT rebuild the workflow and do NOT re-send the JSON. Call `submit_workflow` with `from_prompt_id` set to the prompt_id of the run being adjusted and `input_overrides` holding ONLY the changed inputs ({nodeId: {inputName: value}}). If you do not know the node id, call `get_job_status` with `include_workflow: true` on that prompt_id first. A new reference image still goes through `upload_file` first; override the loader node's input with the returned filename. Then continue from step 7. A 3D result always came from a template or workflow (Step 0's `partner_generate` does not serve 3D), so `from_prompt_id` + `input_overrides` is the only rerun path. If the user wants the 3D MODEL itself edited (e.g. "keep this exact mesh, just retexture it") rather than the workflow's inputs changed, call `use_previous_output` with that prompt_id (pick the `output_index` of the mesh file), then feed the returned filename to a `Load3D` node — the simplest way is a mesh-input template. Search with the 3D tag and a page large enough to see past the generators, e.g. `search_templates({ tag: "3D", limit: 50 })`, and shortlist results whose `description` says they take an uploaded 3D model or mesh as INPUT (today these are mesh-processing templates: part splitting, retopology, UV unwrapping), not ones that generate a model from text or images. The list rows do not show node types, so before running one call `get_template_schema({ template_id })` and confirm a node with `class_type: "Load3D"` is present; its `model_file` input is the override to set via run_template `input_overrides` with the `use_previous_output` filename. If no such template performs the edit the user asked for (for example retexturing), build it as a workflow instead (step 2): `search_nodes` with `category: "partner/3d"` or `category: "3d"` plus a `q` for the edit (e.g. "texture"), pick a node whose inputs take a 3D model file, and wire `Load3D`'s `model_3d` output into it. Only if no node performs the edit, say so plainly instead of forcing one. `partner_generate` does not serve 3D (Step 0) and its `medias[]` accepts images only; `upload_file` does not accept .glb/.obj, so `use_previous_output` is the only in-band route for a generated mesh.

If a step fails, show the error clearly and use the search tools to find a current alternative rather than assuming none exists.
