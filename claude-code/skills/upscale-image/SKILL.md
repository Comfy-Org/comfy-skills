---
name: upscale-image
description: Upscale an image on Comfy Cloud. Use when the user asks to enlarge a photo or illustration, increase resolution, or run super-resolution on an image they provide.
---

# Upscale an image

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`). The user signs in with that connector's OAuth flow. There is no API key to collect in chat, and there is no local ComfyUI install to start.

The built-in `upscale-image` prompt and the tool descriptions own the arguments. Which upscale models exist changes, so search for them. Do not recommend a model by a name you remember unless that search just returned it.

## What to do

1. Ask for the image if they have not attached one. `upload_file` it.
2. `search_templates` for upscale or super-resolution. When one fits the medium (photo, illustration, anime), `get_template_schema` and `run_template`.
3. If none fits, `search_models` for an upscale model that matches the picture and the scale they asked for, then `search_nodes` for the loader and apply nodes. Wire load, upscale, and save. Give every node a `_meta.title`.
4. A second pass that repaints detail is optional. Offer it when they asked for sharpness, and keep the denoise low enough that identity survives. Confirm the denoise control on the node you actually fetched.
5. Wait with `wait_for_job`, then `get_output`. In chat, show the image or the signed URL. When a download command exists and this session has a shell, run it unchanged.
6. When they asked for a workflow they can reopen, `save_workflow` and return `get_workflow_canvas_url`.
7. When they ask for a different strength or model (another upscaler, or a different scale factor), rerun with `submit_workflow`, `from_prompt_id` of the run being adjusted, and `input_overrides` of only the changed inputs. Do not re-upload the source and do not rebuild the workflow. If you do not know the node id, call `get_job_status` with `include_workflow: true` on that prompt id first.

Discovery does not spend generation credits. A generation needs an active Comfy Cloud subscription. If a run is refused, check `get_billing_status` and report what it says.
