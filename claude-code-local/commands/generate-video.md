---
description: Generate, edit, or extend a video with your local ComfyUI
---

Generate, edit, or extend a video on the user's own ComfyUI based on their description: $ARGUMENTS

Follow these steps:

0. Call `server_info` first to confirm a local ComfyUI is reachable, and check `hardware` — video is far more VRAM/time sensitive than images, so read GPU/VRAM before promising a timeline.

**Step 1 — Route the named model family.** If the user named a provider, model, or capability (e.g. "Kling", "Veo", "Sora", "Runway", "MiniMax"), check both routes before doing anything else: one `search_templates` lookup with the family name (pass `exclude_api=True` to isolate a local OSS template) and one `nodes(action="search", query=<name>)` lookup (for the partner/API node). Some families — MiniMax H3 is a current example — ship as BOTH free OSS weights and a paid partner node under the same display title; others exist only as a partner node. Tell them apart by internal/node name (an OSS template/node uses a plain prefix like `video_*`; a partner/API node uses `api_*` and lives in a `partner/`-prefixed category) and, where the search results expose it, row tags.

- **Family exists only as partner/API** (no matching OSS template): route directly. Confirm the alias with `list_partner_models` / `partner_model_schema`, then run it with `partner_generate` (executes on the partner's infrastructure, no local ComfyUI in the path) or `emit_partner_workflow` + `run_workflow` if the family is one of the five aliases that map to a local node (flux-2, flux-pro, kling-i2v, nano-banana, seedance — video-relevant: kling-i2v, seedance). Either way this ALWAYS spends credits — proceed only with the user's consent (see the spend-consent step below).
- **Family exists as both OSS and partner/API**: do NOT auto-route to the paid path. Tell the user both options exist — free OSS (runs on their own GPU, slower, no per-run charge) vs. paid partner/API (fast, no local hardware concern, costs per run) — and ask which they want, unless they already said which one (e.g. "the free version", "local", "OSS", or named a paid partner product explicitly) or one route is genuinely infeasible right now. Once the route is chosen: partner/API continues as in the bullet above; OSS continues to Step 2 using the matching template.

Never tell a user a free/OSS route doesn't exist for a family that has one — that's a wrong answer, not a cautious one.

2. Use `search_templates` with relevant queries like "text to video", "image to video", or "video generation" (filter by `tag="video"` if the text search returns too many image results) to find a matching template. Inspect with `get_template` — its `local_check` matters more here than for images, since a video model can need real extra VRAM or a missing model file — then `fetch_template` to write the runnable JSON.

3. If the user provides an input image (for image-to-video), stage it with `upload_file` first, then reference the returned path in the workflow's image slot.

4. Before running, make sure the workflow's been checked against the LIVE install — trust `get_template`/`fetch_template`'s own `local_check`, or call `validate_workflow` directly on a hand-edited workflow. Known validator blind spot: a huge allocation can validate clean and still OOM-kill ComfyUI at execution time — for a large resolution/duration request, say so before running rather than after a crash, and check `get_logs` if the process dies mid-run.

5. Spend consent: an OSS video template is free. A partner/API route (`partner_generate`, or `run_workflow`/`run_template` on a workflow carrying a partner-API node) spends credits. Only pass `confirm_spend=True` after the user has actually agreed — never set it just to clear a `spend_consent_required` error.

6. Submit with `run_workflow` / `run_template`, preferring `wait=False` for video (these run long) and polling with `job(action="wait", prompt_id=...)` (up to a 3600s ceiling) or streaming progress with `job(action="watch", prompt_id=...)`. Use `job(action="status")` / `job(action="error")` to inspect afterward, `job(action="cancel")` if the user asks to stop.

7. Report the result — the saved output path(s), or `fetch_outputs` if submitted async. Video files are saved to disk, not previewed inline — tell the user where.

If a step fails, show the actual error. Common local video issues: a missing model file (`search_models` -> `download_model`), a missing custom node pack (`workflow_deps` -> `install_node` -> `restart_comfyui`), or insufficient VRAM for the requested length/resolution — in the last case, suggest a shorter or lower-resolution run rather than declaring it impossible.

## Model notes: MiniMax H3 (as of 2026-08)

Model facts change over time. The following was accurate as of 2026-08 — confirm current details with `search_templates`, `nodes(action="search", ...)`, and `nodes(action="get", ...)` rather than assuming they still hold.

- H3 is the current best open-source video model (tier 0), on par with closed-source SOTA models like Seedance 2.x. If a user wants the best open-source video model and doesn't name one, recommend H3.
- H3 always has two routes: OSS weights (free, executes on the user's own GPU) and a paid partner/API node. Both exist at the same time. Never tell a user only the paid route exists.
- Both routes share the same display title, "MiniMax H3: Text to Video" (and the image-to-video variant). Tell them apart by internal name: `video_minimax_h3_*` is OSS, `api_minimax_h3_*` is the paid API node. A `search_templates` call with `exclude_api=True` also isolates the OSS template.
- Before building the OSS workflow, check `server_info`'s `hardware` field and set expectations from it:
  - Dynamic VRAM means H3 runs on any VRAM size — the constraint is speed, not whether it runs at all.
  - Comfortable range: a 30-series-or-newer GPU with 16+ GB VRAM.
  - Reference benchmarks on the basic workflow: 5 seconds at 480p takes about 9 minutes on a 3060; about 15 minutes for 5 seconds on a 16 GB card.
  - Generation time scales exponentially with pixel count, not linearly. Re-estimate for the resolution the user actually wants — don't scale the numbers above linearly.
  - Quote the estimate before running so a user on a weak GPU can decide with full information. Slow is not the same as impossible — never present a long local run as infeasible.
- Model files: use the int8 base model on all GPUs, including 50-series cards, and the NVFP4 text encoder on all GPUs. The official template's default file choices are correct for nearly every GPU — don't second-guess them without a specific reason. Use `search_models` / `download_model` if a file is missing.
- The partner/API node's resolution and duration options are that node's dropdown, not the model's real limits:
  - OSS accepts any resolution in multiples of 32, up to about 2K.
  - OSS duration follows a 17k+5-frame grid at 24fps (k = 0, 1, 2, ...), up to about 15 seconds max.
  - OSS has native stereo audio.
  - If the user asks for something outside the API node's presets (e.g. exactly 1000x1000), don't call it impossible — offer the OSS route, which can do it.
  - For production-quality output, suggest generating at the native ~768p canvas and upscaling afterward, rather than requesting a large canvas directly.
- Trust evidence over assumption: a successful local H3 run earlier this session, or H3 model files already present on disk (check with `search_models`), proves the free route is available here — never claim afterward that it isn't.
- `hailuo` (the alias `partner_generate` / `list_partner_models` uses) is the older MiniMax Hailuo family, not H3. Don't mix Hailuo's parameters into an H3 request. That said, a user who says "Hailuo 03" most likely means H3 — confirm rather than assuming they want the old Hailuo family.
- The OSS image-to-video template ships with one helper node left disconnected on purpose, and `validate_workflow` will flag it. That's expected: after `fetch_template`, validate, then either prune the disconnected helper pair or wire an IMAGE link into it, then call `validate_workflow` again on the edited graph and proceed only when it passes — the first result described the pre-edit workflow. Validate twice, run once. Don't treat that first validation failure as a dead end.
