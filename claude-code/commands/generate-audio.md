---
description: Generate audio (speech or sound effects) with Comfy Cloud
---

Generate audio using Comfy Cloud based on the user's description: $ARGUMENTS

Follow these steps exactly:

**Step 0 — Route partner-API requests directly.** If the user named a provider, model, or capability (e.g. "ElevenLabs", "Stability Audio", "Sonilo"), do one `search_nodes` lookup with the named term. If the matching node's category starts with `api node/`, try `partner_generate` first — see its tool description for the currently-wired model ids. Pass `type: "audio"` plus the partner's model slug, `prompt`, and any optional fields (`seed`/`duration`/`medias[]`). On success, return the artifact URL(s) and **stop** — do NOT continue with the workflow steps below. If `partner_generate` returns "unknown model" or "not yet implemented", or the matching node has no `api node/` prefix (OSS model), continue to Step 1.

1. Use `search_templates` with queries like "audio generation", "text to audio", "music generation", or "sound effects" and set `media_type` to "audio" to find a pre-built audio workflow template. If a good template exists, use it as the base workflow instead of building from scratch.

2. If no suitable template was found, use `search_nodes` to find audio-related nodes. Search for "audio" to discover available audio generation and processing nodes. Use `search_models` to find audio models if needed.

3. Build a ComfyUI API-format workflow JSON with the appropriate audio nodes. Audio workflows vary depending on the task (music generation, sound effects, text-to-speech, etc.) and available nodes.

4. **Validate the workflow has inputs and outputs before submitting.** Confirm the JSON contains:
   - At least one **input node** carrying the user's intent (text prompt node, LoadAudio for audio-to-audio, etc.).
   - At least one **output/save node** wired to the final audio tensor (`SaveAudio` or the partner node's own save output).

   API-backed partner nodes often produce an audio tensor but **do not include a save node by default** — you must add one and wire it to their output. Without it the job runs successfully but produces nothing retrievable, wasting compute. Do not skip this check.

5. Call `submit_workflow` with the workflow JSON.

6. Poll `get_job_status` every 5 seconds until the job is completed. Show the user a brief status update while waiting. If the user asks to cancel, use `cancel_job` with the prompt_id.

7. Call `get_output` to retrieve the generated audio. Pass a short `description` parameter (e.g. "ambient forest sounds") so the saved file gets a descriptive name.

8. Tell the user where the audio file was saved and how to play it. Audio outputs are saved to disk but not previewed inline.

If any step fails, show the error clearly. Audio generation support in ComfyUI is newer than image generation, so fewer templates and models may be available.
