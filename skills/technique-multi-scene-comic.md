Create a multi-scene comic, manga or storyboard (漫画 / 漫剧) with the same characters drawn consistently across every panel, optionally animated into video: $ARGUMENTS

Follow these steps exactly:

No single template produces a finished multi-panel comic. Build it panel by panel: one character sheet per character, then one image job per scene that is given those sheets as references. The template names and image-input counts below were current when this was written. `get_template_schema` is the source of truth: if it says a template is gone, use `search_templates` with the same query instead of guessing a replacement, and if its LoadImage count differs from the one listed here, go by the schema.

Every LoadImage in a template is live. An input you do not override is sent with the template's demo picture, and that picture ends up in your panel. So every template you run in this recipe must have each of its LoadImage inputs filled with an image you chose. Pick a template whose input count matches what you have, or fill the spare inputs as described below. Never leave one at its default.

## Step 1: Plan the script

Ask for (or draft and confirm) a scene list: N panels, each with location, characters present, action, camera and dialogue/caption. Fix the art style as one short style string and reuse it verbatim in every prompt (e.g. "clean-line shoujo manga, screentone shading, black and white").

## Step 2: Make a character sheet for each character

If the user uploaded a reference for a character, `upload_file` it. Otherwise generate one front-facing reference from text first with `partner_generate` (text-to-image, no image inputs, e.g. `bfl/flux-2-pro`), prompting with the style string and the character description. Do not use a reference-image template for this: with no reference to give it, its image inputs would run with demo pictures.

Then turn that reference into a sheet. Use `search_templates` (query `character reference` or `turnaround`). `api_google_nano_banana_create_turnaround_sheet` takes one LoadImage reference and returns front/side/back views. `template_3x3_contact_sheet` returns pose and angle variations of the same character and outfit, but it has three LoadImage inputs; use it only when you have three images of that character to fill them. Call `get_template_schema` first to learn the overridable slots, `run_template`, then `wait_for_job`. Keep each character's job id: it is the identity anchor for every later panel.

## Step 3: Generate each scene panel

For each scene, run a multi-reference image template with the sheets of ALL characters in that scene attached, plus the scene prompt (location, action, camera, style string). Pick the template whose LoadImage count equals the number of references for the scene (one sheet per character). Candidates, with their LoadImage counts:

- `api_flux2` (FLUX.2 Pro): 4 slots, multi-reference consistency
- `api_bfl_flux_1_kontext_multiple_images_input` (Flux.1 Kontext Multiple Image Input): 3 slots
- `api_nano_banana_pro` (Nano Banana Pro): 2 slots
- `api_kling_o3_image` (Kling O3): 2 slots
- `flux_kontext_dev_basic`: 1 slot

So a scene with 1 to 4 characters always has an exact fit. Use `get_template_schema` to confirm the LoadImage inputs before you submit, and override every one of them.

With more than four characters, pack the sheets into grids with `utility_image_stitch` (Image Stitch 2x2 Grid, exactly 4 LoadImage inputs). Each grid takes four sheets and counts as one reference. Make grids until the grids plus the sheets left over add up to four or fewer references, then pick the template that fits that count exactly (5 characters: 1 grid + 1 sheet = 2 references; 8 characters: 2 grids = 2 references). A grid with fewer than four sheets still needs all four inputs filled: put the front-facing reference from Step 2 of a character already in that grid in each empty quadrant, never the demo picture. For each grid, say in the prompt which quadrant shows which character. Past 16 characters, split the scene. Feed each sheet (or grid) in with `use_previous_output` (job id + output index → the returned filename goes in the LoadImage slot). That chains the output straight in, with no download and re-upload. Keep the seed fixed across panels where the template exposes one.

Prompt rule: say which reference is which ("Reference 1 is Mira: silver hair, burn scar on right cheek, red school blazer …"), and demand exact reproduction of face, hair and outfit from the references.

With more than three scenes, submit them together with `submit_batch`, then `wait_for_batch` until every job has finished. Note which scene each item's job id belongs to, because Step 4 fetches panels by scene. Otherwise run one `run_template` + `wait_for_job` per scene.

## Step 4: Review and fix drift

Fetch each panel with `get_output` (or all of a batch at once with `get_batch_output`), and match it to its scene by job id. If a character drifted (face, hair, outfit), re-run only that scene with the sheet attached again and a stronger identity sentence. Do not re-run the whole batch.

## Step 5 (optional): Animate it (漫剧 / motion comic)

Warn first: partner-API video templates use credits for every clip.

- `templates-6-key-frames` (Multi-Keyframe Video Stitching, Wan 2.2): exactly 6 panels as keyframes in one video (it has 6 LoadImage inputs; with fewer panels, use the clip-per-pair templates below)
- `api_kling_v3_flf2v` / `api_seedance2_0_flf2v`: one clip per consecutive panel pair (first frame → last frame)
- `video_ltx2_3_ia2v`: one panel + a dialogue audio file → lip-synced clip
- `template_seedance2_storyboard_to_video`: draws its OWN 8-panel storyboard from a text prompt, then animates it with Seedance 2.0. Use it for a fresh short from the script, with the character sheet as the character image. It does not take the panels from Step 3. It has two LoadImage inputs; check `get_template_schema` and fill both.

Pass panel images into the video templates with `use_previous_output`, the same way as in Step 3, and fill every image input there too.

## Step 6: Deliver

List every panel (and clip) URL in scene order, each with its scene caption. Do not make a page layout unless asked. If the user wants a page, `utility_image_stitch` (Image Stitch 2x2 Grid) combines four panels into one 2x2 page image, also fed with `use_previous_output`. It does not draw speech balloons or custom panel borders, and longer comics need one page per four panels. If the last page has fewer than four panels, list those panels on their own instead of stitching them, so no demo picture fills the empty quadrants. Say that plainly; do not promise a layout tool that does not exist.
