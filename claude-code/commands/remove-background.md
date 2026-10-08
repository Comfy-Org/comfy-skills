---
description: Remove the background from an image with Comfy Cloud
---

Remove the background from an image using Comfy Cloud: $ARGUMENTS

Follow these steps exactly:

1. Use `search_templates` with queries like "remove background", "background removal", or "transparent background" to find a pre-built background removal workflow template. If a good template exists, use it as the base workflow instead of building from scratch.

2. If no suitable template was found, use `search_nodes` to find background removal nodes. Search for "RMBG", "background removal", "SAM", or "segment". Common nodes: RMBG (fast automatic removal), SAM (segment anything for precise masks), BiRefNet (high-quality matting).

3. The user must provide an input image. Use `upload_file` to upload it to Comfy Cloud. Use the returned filename in a LoadImage node.

4. Build a ComfyUI API-format workflow JSON for background removal. A typical workflow uses: LoadImage → background removal node (e.g. RMBG) → SaveImage (with PNG format to preserve transparency). If the user wants to replace the background rather than make it transparent, add a second image and composite them. Give EVERY node a `_meta.title` that names its role in plain words (e.g. "Load driving video", "Remove background", "Overlay graphic 1", "Save video"). The canvas shows these titles; without them the user sees only class names.

5. **Validate the workflow has inputs and outputs before submitting.** Confirm the JSON contains:
   - At least one **input node** (`LoadImage` for the source image).
   - At least one **output/save node** wired to the final image (`SaveImage` with PNG format to preserve transparency).

   Without an output node the job runs successfully but produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow` with the workflow JSON.

7. Poll `get_job_status` every 3 seconds until the job is completed. Show the user a brief status update while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the result. Pass a short `description` parameter (e.g. "transparent-portrait") so the suggested filename is descriptive, then run the returned curl command in the user's shell to download the file.

9. Display the result to the user. Note that the output is a PNG with transparency if background was removed (not replaced).

10. If the user asked to BUILD or CREATE a workflow (not just for an output), after the run completes call `save_workflow` with the same JSON and a descriptive `name`, then `get_workflow_canvas_url` with the returned workflow id, and give the user that link. Mention that the saved layout is auto-generated and may need tidying. If you ran a subgraph template instead, tell the user the canvas shows one collapsed subgraph node and how to open it (double-click the node body, not its title, to step inside it, or right-click it and choose Unpack Subgraph to flatten it onto the canvas).

If any step fails, show the error clearly. If background removal nodes aren't available, suggest using an inpainting approach as a fallback.
