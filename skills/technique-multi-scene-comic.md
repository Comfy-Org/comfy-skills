Create a multi-scene comic, manga or storyboard (漫画 / 漫剧) with the same characters drawn consistently across every panel, optionally animated into video: $ARGUMENTS

Follow these steps exactly:

No single template produces a finished multi-panel comic. Build it panel by panel: one character sheet per character, then one image job per scene that is given those sheets as references. The template names and image-input counts below were current when this was written. `get_template_schema` is the source of truth: if it says a template is gone, use `search_templates` with the same query instead of guessing a replacement, and if its LoadImage count differs from the one listed here, go by the schema.

Every LoadImage in a template is live. An input you do not override is sent with the template's demo picture, and that picture ends up in your panel. So every template you run in this recipe must have each of its LoadImage inputs filled with an image you chose. Pick a template whose input count matches what you have, or fill the spare inputs as described below. Never leave one at its default.

## Step 1: Plan the script

Ask for (or draft and confirm) a scene list: N panels, each with location, characters present, action, camera and dialogue/caption. Fix the art style as one short style string and reuse it verbatim in every prompt (e.g. "clean-line shoujo manga, screentone shading, black and white").

## Step 2: Make a character sheet for each character

If the user uploaded a reference for a character, `upload_file` it. Otherwise generate one front-facing reference from text first with a text-to-image `partner_generate` call (for example `bfl/flux-2-pro`), prompting with the style string and the character description. Do not use a reference-image template for this: with no reference to give it, its image inputs would run with demo pictures.

Then turn that reference into a sheet. Feed the generated reference into the sheet template's LoadImage input with `use_previous_output` on its `prompt_id`. If `partner_generate` instead returned a direct-dispatch `job_id` and says its output is not in the asset library, `use_previous_output` cannot read it: download its URL exactly as returned, `upload_file` it, and put the returned filename in the LoadImage input. The same applies wherever a `partner_generate` image is reused later in this recipe. Use `search_templates` (query `character reference` or `turnaround`). `api_google_nano_banana_create_turnaround_sheet` takes one LoadImage reference and returns front/side/back views. `template_3x3_contact_sheet` returns pose and angle variations of the same character and outfit, but it has three LoadImage inputs; use it only when you have three images of that character to fill them. Call `get_template_schema` first to learn the overridable slots. A character the user uploaded a reference for keeps that upload; generate a reference only for the characters without one. With two or more references to generate, make them as ONE `submit_batch` of `partner_generate` items and `wait_for_batch` it; one reference to generate is one `partner_generate`. With two or more characters, make the sheets as a second `submit_batch` of `run_template` items, each with its own character's uploaded or generated reference in the LoadImage slot, and `wait_for_batch` that too: the sheets wait for the references, and each batch is otherwise independent. Whenever you `wait_for_batch`, call it again while it returns `timed_out: true`, until every job is terminal, and re-submit any item whose job failed before you use that batch's outputs. A batch holds at most 50 items; above that, split across several `submit_batch` calls and state each batch's total. A single character is one sheet: one `run_template` + `wait_for_job`. Keep each character's job id: it is the identity anchor for every later panel.

## Step 3: Generate each scene panel

For each panel, run a multi-reference image template with the sheets of ALL characters in that panel attached, plus the scene prompt (location, action, camera, style string). Pick the template whose LoadImage count equals the number of references for that panel (one sheet per character). Candidates, with their LoadImage counts:

- `api_flux2` (FLUX.2 Pro): 4 slots, multi-reference consistency
- `api_bfl_flux_1_kontext_multiple_images_input` (Flux.1 Kontext Multiple Image Input): 3 slots
- `api_nano_banana_pro` (Nano Banana Pro): 2 slots
- `api_kling_o3_image` (Kling O3): 2 slots
- `flux_kontext_dev_basic`: 1 slot

So a scene with 1 to 4 characters always has an exact fit. Use `get_template_schema` to confirm the LoadImage inputs before you submit, and override every one of them.

A scene with no characters (an establishing shot, an empty room) has no references to give, so do not run a reference template for it. Generate it with a text-to-image `partner_generate` call, as in Step 2, prompting with the scene and the style string.

With more than four characters, pack the sheets into grids with `utility_image_stitch` (Image Stitch 2x2 Grid, exactly 4 LoadImage inputs). Run each grid with `run_template`, then `wait_for_job` before you reuse its output. Each grid takes four sheets and counts as one reference. Make grids until the grids plus the sheets left over add up to four or fewer references, then pick the template that fits that count exactly (5 characters: 1 grid + 1 sheet = 2 references; 8 characters: 2 grids = 2 references). A grid with fewer than four sheets still needs all four inputs filled: put the front-facing reference from Step 2 of a character already in that grid in each empty quadrant, never the demo picture. For each grid, say in the prompt which quadrant shows which character. Past 16 characters, split the scene. Feed each sheet (or grid) in with `use_previous_output` (job id + output index → the returned filename goes in the LoadImage slot). That chains the output straight in, with no download and re-upload. Keep the seed fixed across panels where the template exposes one.

Prompt rule: say which reference is which ("Reference 1 is Mira: silver hair, burn scar on right cheek, red school blazer …"), and demand exact reproduction of face, hair and outfit from the references.

Every panel is its own job, and a scene drawn as several panels is several jobs. With two or more panels that have characters, submit them together as ONE `submit_batch` of `run_template` items, then `wait_for_batch` until every job is terminal, as in Step 2. Panels without characters are `partner_generate` jobs: two or more of them go together in a separate `submit_batch` of `partner_generate` items, waited the same way. A batch holds at most 50 items; past 50 panels, split across several `submit_batch` calls in page order and state each batch's total. Note which panel each item's job id belongs to, because Step 4 fetches panels by job id. A single panel with characters is one `run_template` + `wait_for_job`; a single panel without characters is one `partner_generate`.

## Step 4: Review and fix drift

Fetch each panel with `get_output` (or all of a batch at once with `get_batch_output`), and match it to its panel by job id. If a character drifted (face, hair, outfit), re-run only that panel with the same full set of references it was first made with (every character sheet or grid, in the same slots) and a stronger identity sentence for the character that drifted. Two or more drifted panels go together in one `submit_batch`, split at 50 items like the first pass, with each job id noted against its panel. Do not re-run the whole batch or the drifted panel's whole scene.

## Step 5 (optional): Animate it (漫剧 / motion comic)

Warn first: partner-API video templates use credits for every clip.

- `templates-6-key-frames` (Multi-Keyframe Video Stitching, Wan 2.2): exactly 6 panels as keyframes in one video (it has 6 LoadImage inputs). With fewer than six panels, use the clip-per-pair templates below instead. With more than six, run it once per consecutive group of six in scene order, then animate any leftover panels with the clip-per-pair templates, starting from the last panel of the final group so the clips join up
- `api_kling_v3_flf2v` / `api_seedance2_0_flf2v`: one clip per consecutive panel pair (first frame → last frame); two or more clips likewise go together in one `submit_batch`, split at 50 items, with each job id noted against its panel pair
- `video_ltx2_3_ia2v`: one panel + a dialogue audio file → lip-synced clip
- `template_seedance2_storyboard_to_video`: animates a storyboard image with Seedance 2.0. It also draws a stick-figure storyboard from its text prompt, but the video is built from the storyboard image in its own LoadImage input, not from that drawing. It has two LoadImage inputs, so fill both: the storyboard input with a page stitched from your Step 3 panels (see Step 6) or the user's own board, and the character input with that character's sheet from Step 2. Override both of its prompts with your scene too, or it animates its demo scene. Check `get_template_schema` for which input is which.

Pass panel images into the video templates with `use_previous_output`, the same way as in Step 3, and fill every image input there too.

## Step 6: Deliver

Each `get_output` result carries an `/api/s/<id>` Download link and View link plus a ready-to-run download command. The links expire in about 5 minutes; re-run `get_output` for fresh ones. If you have a working shell, run that download command for each panel and clip as soon as it is ready, and give the user the saved files in scene order, each with its scene caption. If you do not, give the user only the `/api/s/<id>` Download and View links from `get_output`, in scene order with their captions, and tell them to save the files now, because the links expire. Those are the only links the user gets. The signed inline-view URL in a `get_output` result and the signed storage URLs that `get_batch_output` returns are for your own downloads only; never paste them to the user. For panels that came back through `get_batch_output`, and for any clip whose `get_output` result has no `/api/s/<id>` link (video and audio usually do not get one), run the emitted download command yourself or hand the user that command to run, never the URL. Do not make a page layout unless asked. If the user wants a page, `utility_image_stitch` (Image Stitch 2x2 Grid) combines four panels into one 2x2 page image, also fed with `use_previous_output`. It does not draw speech balloons or custom panel borders, and longer comics need one page per four panels. If the last page has fewer than four panels, list those panels on their own instead of stitching them, so no demo picture fills the empty quadrants. Say that plainly; do not promise a layout tool that does not exist.
