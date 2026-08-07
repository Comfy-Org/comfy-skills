Generate, edit, or extend a video using Comfy Cloud based on the user's description: $ARGUMENTS

Follow these steps exactly:

**Step 0 — Route the named model family.** If the user named a provider, model, or capability (e.g. "Kling", "Veo", "Sora", "Runway", "MiniMax"), check both routes before doing anything else: one `search_nodes` lookup with the named term (for the partner/API node), and one `search_templates` lookup with the family name (for an OSS template). Some families — MiniMax H3 is a current example — ship as BOTH OSS weights and a paid partner node under the same display title; others exist only as a partner node. Tell them apart by internal name (an OSS template/node uses a plain prefix like `video_*`; a partner/API node uses `api_*` and lives under a `partner/` category) and, where the search results expose it, row tags.

- **Family exists only as partner/API** (no matching OSS template, node category starts with `partner/`): route directly. Try `partner_generate` first — see its tool description for the currently-wired model ids. Pass `type: "video"` plus the partner's model slug, `prompt`, and any optional fields (`aspect_ratio`/`seed`/`duration`/`medias[]`). On success, return the artifact URL(s) and **stop** — do NOT continue with the workflow steps below. If `partner_generate` returns "unknown model" or "not yet implemented", continue to Step 1.
- **Family exists as both OSS and partner/API**: do NOT auto-route to the paid path. Tell the user both options exist — OSS (no partner/API fee, but running it still spends ordinary Comfy Cloud compute credits, and it's typically slower; it's only actually free of charge when the user runs it themselves on their own local ComfyUI install) vs. paid partner/API (fast, no local hardware concern, costs the partner's per-run price on top of compute) — and ask which they want, unless they already said which one (e.g. "the free version", "local", "OSS", or named a paid partner product explicitly) or one route is genuinely infeasible right now. Once the route is chosen: partner/API continues as in the bullet above; OSS continues to Step 1 using the matching template.

Never tell a user the OSS route doesn't exist for a family that has one — that's a wrong answer, not a cautious one.

1. Use `search_templates` with relevant queries like "text to video", "image to video", or "video generation" to find a pre-built video workflow template. Filter by tag "video" if the text search returns too many image results. If a good template exists, use it as the base workflow instead of building from scratch.

2. If no suitable template was found, use `search_models` to find an appropriate video model. Common video models include: LTX-Video, Wan Video, HunyuanVideo, AnimateDiff, CogVideoX. Pick the best match based on the user's description.

3. If the user provides an input image (for image-to-video), use `upload_file` to upload it first. Use the returned filename in a LoadImage node.

4. Build a ComfyUI API-format workflow JSON with the appropriate video nodes. Video workflows typically use specialized loader nodes (e.g. LTXVLoader, WanVideoModelLoader), video-specific samplers, and video output nodes (e.g. VHS_VideoCombine). If using a template, modify the prompt and settings as needed.

5. **Validate the workflow has inputs and outputs before submitting.** Confirm the JSON contains:
   - At least one **input node** the user's intent flows through (CLIPTextEncode for the prompt, LoadImage for image-to-video, etc.).
   - At least one **output/save node** wired to the final video tensor (e.g. `VHS_VideoCombine`, `SaveAnimatedWEBP`, `SaveVideo`, or the partner node's own save output).

   API-backed partner nodes (Kling, Nano Banana, Gemini, Veo, etc.) often produce a video tensor but **do not include a save node by default** — you must add one and wire it to their output. Without it the job runs successfully but produces nothing retrievable, wasting compute. Do not skip this check.

6. Call `submit_workflow` with the workflow JSON. Note: video generation typically takes longer than image generation (30s-2min+).

7. Poll `get_job_status` every 5 seconds until the job is completed. Show the user a brief status update while waiting. Mention that video generation takes longer than images. If the user asks to cancel, use `cancel_job` with the prompt_id.

8. Call `get_output` to retrieve the generated video. Pass a short `description` parameter (e.g. "cat running through field") so the saved file gets a descriptive name.

9. Tell the user where the video file was saved and how to view it. Video outputs are saved to disk but not previewed inline.

If any step fails, show the error clearly. Common video generation issues: model not available on cloud, insufficient GPU memory for long videos, unsupported video length.

## Model notes: MiniMax H3 (as of 2026-08)

Model facts change over time. The following was accurate as of 2026-08 — confirm current details with `search_templates`, `search_nodes`, and `get_node` rather than assuming they still hold.

- H3 is the current best open-source video model (tier 0), on par with closed-source SOTA models like Seedance 2.x. If a user wants the best open-source video model and doesn't name one, recommend H3.
- As of 2026-08, H3 ships with two routes: OSS weights and a paid partner/API node — confirm both are currently live with `search_templates`/`search_nodes` rather than assuming this holds forever. OSS carries no partner/API fee, but running it on Comfy Cloud still spends ordinary Comfy Cloud compute credits — it's only free of charge outright when the user runs it locally on their own ComfyUI install. Don't conclude the OSS route is gone from one empty or ambiguous lookup; broaden the search before telling a user there's no OSS option, and don't let that session-local evidence override what a fresh, authoritative lookup says either.
- As of 2026-08, both routes share the same display title, "MiniMax H3: Text to Video" (and the image-to-video variant), told apart by internal name: `video_minimax_h3_*` is OSS, `api_minimax_h3_*` is the paid API node. Confirm the current prefix with `search_nodes`/`get_node` before relying on it — naming can change. A `search_nodes` call with `exclude_api=True` also isolates the OSS node in the current catalog.
- Before building the OSS workflow, ask about the user's hardware and set expectations from it. Dynamic VRAM offloading widens what a GPU can attempt, but it is not a guarantee — out-of-memory is still possible, and actual headroom depends on resolution, duration, VRAM, and system RAM together, not VRAM alone:
  - Tested comfortable range (as of 2026-08): a 30-series-or-newer GPU with 16+ GB VRAM and enough system RAM that offloaded weights don't starve the host.
  - Reference benchmarks on the basic workflow, same date: 5 seconds at 480p takes about 9 minutes on a 3060; about 15 minutes for 5 seconds on a 16 GB card. Below the tested range, OOM becomes more likely — if it happens, suggest a lower resolution or shorter duration rather than assuming the run will simply succeed slower.
  - Generation time scales exponentially with pixel count, not linearly. Re-estimate for the resolution the user actually wants — don't scale the numbers above linearly.
  - Quote the estimate before running so a user on a weak GPU can decide with full information. Slow is not the same as impossible, but OOM is a real outcome on undersized hardware — don't promise success on every GPU.
- Model files: use the int8 base model on all GPUs, including 50-series cards, and the NVFP4 text encoder on all GPUs. The official template's default file choices are correct for nearly every GPU — don't second-guess them without a specific reason.
- The partner/API node's resolution and duration options are that node's dropdown, not necessarily the model's full real limits. Treat the numbers below as the 2026-08 reference point and confirm current ones with `get_node` on the OSS node before enforcing a hard cutoff:
  - As of 2026-08: OSS accepts any resolution in multiples of 32, up to about 2K.
  - As of 2026-08: OSS duration follows a 17k+5-frame grid at 24fps (k = 0, 1, 2, ...), up to about 15 seconds max.
  - As of 2026-08: OSS has native stereo audio.
  - If the user asks for something outside the API node's presets (e.g. exactly 1000x1000), don't call it impossible before checking — the OSS node's actual schema (via `get_node`) may still support it.
  - For production-quality output, suggest generating at the native ~768p canvas and upscaling afterward, rather than requesting a large canvas directly.
- Evidence beats assumption, but keep it scoped: if you already ran OSS H3 successfully, or a tool call already showed the model files present, treat that as proof the OSS route exists for this request — don't contradict it later in the same turn because of an unrelated error. That said, this doesn't override a fresh, authoritative `search_templates`/`search_nodes` result — if a live lookup says the OSS route isn't currently available, trust the live result over older evidence.
- `hailuo` (the alias `partner_generate` uses) is the older MiniMax Hailuo family, not H3. Don't mix Hailuo's parameters into an H3 request. That said, a user who says "Hailuo 03" most likely means H3 — confirm rather than assuming they want the old Hailuo family.
- The OSS image-to-video template ships with one helper node left disconnected on purpose, and validation will flag it. That's expected: after fetching the template, validate, then either prune the disconnected helper pair or wire an IMAGE link into it, and proceed. Don't treat that validation failure as a dead end.
