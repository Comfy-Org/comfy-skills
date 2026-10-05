Create a multi-scene comic, manga or storyboard (漫画 / 漫剧) with the same characters drawn consistently across every panel, optionally animated into video: $ARGUMENTS

Follow these steps exactly:

No single template produces a finished multi-panel comic. Build it panel by panel: one character sheet per character, then one image job per scene that is given those sheets as references. The template names below were current when this was written; if `get_template_schema` says one is gone, use `search_templates` with the same query instead of guessing a replacement.

## Step 1: Plan the script

Ask for (or draft and confirm) a scene list: N panels, each with location, characters present, action, camera and dialogue/caption. Fix the art style as one short style string and reuse it verbatim in every prompt (e.g. "clean-line shoujo manga, screentone shading, black and white").

## Step 2: Make a character sheet for each character

If the user uploaded a reference for a character, `upload_file` it. Otherwise generate one front-facing reference first with `run_template` on a reference-capable image template (`api_nano_banana_pro`), prompting with the style string and the character description.

Then turn that reference into a sheet. Use `search_templates` (query `character reference` or `turnaround`). `api_google_nano_banana_create_turnaround_sheet` takes one LoadImage reference and returns front/side/back views. `template_3x3_contact_sheet` returns pose and angle variations of the same character and outfit. Call `get_template_schema` first to learn the overridable slots, `run_template`, then `wait_for_job`. Keep each character's job id: it is the identity anchor for every later panel.

## Step 3: Generate each scene panel

For each scene, run a multi-reference image template with the sheets of ALL characters in that scene attached, plus the scene prompt (location, action, camera, style string). Candidates:

- `api_google_nano_banana2_image_edit` / `api_nano_banana_pro`: Nano Banana, reference-consistent edit
- `api_kling_omni_image`: Kling O1, up to 10 reference images
- `flux_kontext_dev_basic`: keeps a character consistent (single reference)
- `image_qwen_image_edit_2509`: multi-image input

Use `get_template_schema` to find the LoadImage slots, then feed each sheet in with `use_previous_output` (sheet job id + output index → the returned filename goes in the LoadImage slot). That chains the output straight in, with no download and re-upload. Keep the seed fixed across panels where the template exposes one.

Prompt rule: say which reference is which ("Reference 1 is Mira: silver hair, burn scar on right cheek, red school blazer …"), and demand exact reproduction of face, hair and outfit from the references.

With more than three scenes, submit them together with `submit_batch`; otherwise one `run_template` + `wait_for_job` per scene.

## Step 4: Review and fix drift

Fetch each panel with `get_output`. If a character drifted (face, hair, outfit), re-run only that scene with the sheet attached again and a stronger identity sentence. Do not re-run the whole batch.

## Step 5 (optional): Animate it (漫剧 / motion comic)

Warn first: partner-API video templates use credits for every clip.

- `templates-6-key-frames` (Multi-Keyframe Video Stitching, Wan 2.2): up to 6 panels as keyframes in one video
- `api_kling_v3_flf2v` / `api_seedance2_0_flf2v`: one clip per consecutive panel pair (first frame → last frame)
- `video_ltx2_3_ia2v`: one panel + a dialogue audio file → lip-synced clip
- `template_seedance2_storyboard_to_video`: draws its OWN 8-panel storyboard from a text prompt, then animates it with Seedance 2.0. Use it for a fresh short from the script, with the character sheet as the character image. It does not take the panels from Step 3.

Pass panel images into the video templates with `use_previous_output`, the same way as in Step 3.

## Step 6: Deliver

List every panel (and clip) URL in scene order, each with its scene caption. Do not make a page layout unless asked. If the user wants a page, `utility_image_stitch` (Image Stitch 2x2 Grid) combines four panels into one 2x2 page image, also fed with `use_previous_output`. It does not draw speech balloons or custom panel borders, and longer comics need one page per four panels. Say that plainly; do not promise a layout tool that does not exist.
