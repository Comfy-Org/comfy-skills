---
name: generate-3d
description: Generate a 3D model on Comfy Cloud. Use when the user asks for a mesh, a GLB or OBJ, text-to-3D, or image-to-3D from a photo or drawing.
---

# Generate a 3D model

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`). The user signs in with that connector's OAuth flow. Use the signed-in account. There is no API key to collect in chat, and there is no local ComfyUI install to start.

The server's tool descriptions and the built-in `generate-3d` prompt own the arguments. The catalog of 3D templates and nodes moves, so discover it. Do not invent a model or node name.

## What to do

1. Image-to-3D is the common case. When the user supplies a reference image, `upload_file` it first and use the returned name as the image input in whichever route runs below (`partner_generate` media inputs, a template input, or a loader node). When the user names a 3D provider, `search_nodes` in the partner 3D category. Try `partner_generate` with the 3D type that tool documents and your best-guess model slug. Its description names providers, not model ids. A wrong slug is rejected before the job is queued, and the error names the closest real slugs (`Did you mean`). Re-call once, and only when a suggestion keeps the provider prefix of the slug you guessed. If the bounce names a `params.model` tier, send that tier with the slug. A tier-shaped guess belongs in `params.model`; re-calling the bare slug runs that entry's default tier at a different price. Say which slug you switched to. If that re-call bounces too, stop. If no suggestion keeps your guess's provider prefix, do not re-call — that call queues and charges — and ask which model to use. If the tool says "unknown model" with no close match, "not yet implemented", or that it does not serve 3D, continue with a template. That fall-through still runs on Comfy Cloud. If they asked to build a workflow, skip the shortcut and wire the partner node in.
2. Search `search_templates` for image-to-3D or a broader 3D query, using the tool's tag filter when a text search is noisy. Clone a fit with `get_template_schema` and `run_template` before hand-building.
3. If no template fits, `search_nodes` with typed filters for a 3D file or mesh output, a 3D category, and image input when they supplied a picture. Use `search_models` for checkpoints those nodes require.
4. The graph needs the uploaded image (or a text prompt) and a 3D save or output node. Give every node a `_meta.title`.
5. 3D jobs are often slower than images. Wait with `wait_for_job`, then `get_output`. Tell the user which files came back (mesh, texture, preview). In chat, share the returned links. When a download command exists and this session has a shell, run it unchanged.
6. When they asked for a workflow they can reopen, `save_workflow` and return `get_workflow_canvas_url`. Say the layout is auto-generated.
7. When they ask to adjust this result (seed, prompt wording, or a different reference image) rather than a new subject, do not rebuild the graph and do not re-send the JSON. Call `submit_workflow` with `from_prompt_id` set to the run being adjusted and `input_overrides` holding only the changed inputs (`{nodeId: {inputName: value}}`). If you do not know the node id, call `get_job_status` with `include_workflow: true` on that prompt id first. A new reference still goes through `upload_file`; override the loader input with the returned name. If that result came from `partner_generate`, there is no workflow to rerun: call `partner_generate` again with the changed fields. If they want this exact mesh edited (keep the mesh, change the texture) rather than the workflow's inputs changed, use `use_previous_output` or `partner_generate` media inputs.

If a step fails, search again for a current alternative. Discovery does not spend generation credits. A generation needs an active Comfy Cloud subscription. If a run is refused, check `get_billing_status` and report what it says.
