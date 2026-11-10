---
name: remove-background
description: Remove or replace the background of an image on Comfy Cloud. Use when the user asks to cut out a subject, make a background transparent, erase a backdrop, or drop a person or product onto a new background.
---

# Remove a background

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`). The user signs in with that connector's OAuth flow. There is no API key to collect in chat, and there is no local ComfyUI install to start.

The built-in `remove-background` prompt and the tool descriptions own the call arguments. Discover the current template and nodes. Do not pin a remover by a remembered class name.

## What to do

1. Ask for a source image if they have not attached one. `upload_file` it and use the returned name.
2. `search_templates` for background removal or a transparent background. When one fits, `get_template_schema` and `run_template`.
3. If none fits, `search_nodes` for removal, matting, or segmentation, then build a short graph: the uploaded image in, the remover, and a save node that keeps transparency (a PNG or the alpha-capable format that node documents). Give every node a `_meta.title`.
4. To replace the background, composite the cutout over the new plate in the same graph, or run a second step after the cutout. Re-upload an output before using it as an input in a later job. The save directory and the load directory are not the same store.
5. Wait with `wait_for_job`, then `get_output`. In chat, show the image or the signed URL. When a download command exists and this session has a shell, run it unchanged. Leave the signed query string as returned.
6. When they asked for a workflow they can reopen, `save_workflow` and return `get_workflow_canvas_url`.
7. When they ask for a different strength or model (another removal model, or a different mask threshold) and the change only touches inputs, rerun with `submit_workflow`, `from_prompt_id` of the run being adjusted, and `input_overrides` of only the changed inputs. Do not rebuild the workflow in that case. If the requested model needs a different node or connections, discover it with `search_nodes`, edit the workflow, and submit the edited workflow instead. Either way, do not re-upload the source. If you need the workflow or a node id, call `get_job_status` with `include_workflow: true` on that prompt id first.

A job with no save node succeeds and returns nothing. Discovery does not spend generation credits. A generation needs an active Comfy Cloud subscription. If a run is refused, check `get_billing_status` and report what it says.
