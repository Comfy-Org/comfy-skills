Remove the background from an image using Comfy Cloud: $ARGUMENTS

Follow these steps exactly:

1. Use `search_templates` with queries like "remove background", "background removal", or "transparent background" to find a pre-built background removal workflow template. If a good template exists, use it as the base workflow instead of building from scratch.

2. If no suitable template was found, use `search_nodes` to find background removal nodes. Search for "RMBG", "background removal", "SAM", or "segment". Common nodes: RMBG (fast automatic removal), SAM (segment anything for precise masks), BiRefNet (high-quality matting).

3. The user must provide an input image. Use `upload_file` to upload it to Comfy Cloud. Use the returned filename in a LoadImage node.

4. Build a ComfyUI API-format workflow JSON for background removal. A typical workflow uses: LoadImage → background removal node (e.g. RMBG) → SaveImage (with PNG format to preserve transparency). If the user wants to replace the background rather than make it transparent, add a second image and composite them.

5. **Validate the workflow has inputs and outputs before submitting.** Confirm the JSON contains:
   - At least one **input node** (`LoadImage` for the source image).
   - At least one **output/save node** wired to the final image (`SaveImage` with PNG format to preserve transparency).

   Without an output node the job runs successfully but produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow` with the workflow JSON.

7. Poll `get_job_status` every 3 seconds until the job is completed. Show the user a brief status update while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the result. Pass a short `description` parameter (e.g. "transparent-portrait") so the suggested filename is descriptive, then run the returned curl command in the user's shell to download the file.

9. Display the result to the user. Note that the output is a PNG with transparency if background was removed (not replaced).

If any step fails, show the error clearly. If background removal nodes aren't available, suggest using an inpainting approach as a fallback.
