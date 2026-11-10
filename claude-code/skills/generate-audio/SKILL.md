---
name: generate-audio
description: Generate speech, music, or sound effects on Comfy Cloud. Use when the user asks for audio, music, a soundtrack, sound effects, ambience, or text-to-speech that is not a clone of a specific recording.
---

# Generate audio

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`). The user signs in with that connector's OAuth flow. Use the signed-in account. There is no API key to collect in chat, and there is no local ComfyUI install to start.

Voice cloning from a reference recording is a different skill. Use this one for new audio from a description.

The server's tool descriptions and the built-in `generate-audio` prompt own parameter names. Discover templates and nodes live. Audio node names change, including which save node is current, so take the save node from `search_nodes` rather than from an older note.

## What to do

1. If the user named a provider or model and wants finished audio, look it up with `search_nodes`. When the match is a partner model, call `partner_generate` for audio. Its description names providers, not model ids, so pass your best-guess model slug. A wrong slug is rejected before the job is queued, and the error names the closest real slugs (`Did you mean`). Re-call once, and only when a suggestion keeps the provider prefix of the slug you guessed. If the bounce names a `params.model` tier, send that tier with the slug. A tier-shaped guess belongs in `params.model`; re-calling the bare slug runs that entry's default tier at a different price. Say which slug you switched to. If that re-call bounces too, stop. Suggestions are ranked across the whole registry, so one may name a provider the user never asked for. If none keeps your guess's provider prefix, do not re-call — that call queues and charges — and ask which model to use. Inside `submit_batch`, resend only the bounced item. If the tool says "unknown model" with no close match, or "not yet implemented", or the node is not a partner node, continue below. If they asked to build a workflow, skip `partner_generate` and wire that node into the graph.
2. Prefer a template. `search_templates` for speech, music, or sound effects, and set the tool's audio media-type filter when it has one. Run a fit with `get_template_schema` and `run_template`.
3. If no template fits, `search_nodes` and `search_models` for the task, then submit a graph. Give every node a `_meta.title`. Include a prompt or source input and a current audio save node wired to the result. Partner nodes often omit the save node.
4. Wait with `wait_for_job`, then `get_output`, with a short description so the file has a useful name. In chat, hand back the link the tool returns. When a download command is present and this session has a shell, run it unchanged.
5. When they asked for a workflow they can reopen, `save_workflow` and return `get_workflow_canvas_url`. Say the layout is auto-generated.
6. When they ask to adjust this result (seed, prompt wording, duration, or a different reference) rather than a new sound, do not rebuild the graph and do not re-send the JSON. Call `submit_workflow` with `from_prompt_id` set to the run being adjusted and `input_overrides` holding only the changed inputs (`{nodeId: {inputName: value}}`). If you do not know the node id, call `get_job_status` with `include_workflow: true` on that prompt id first. A new reference still goes through `upload_file`; override the loader input with the returned name. If that result came from `partner_generate`, there is no workflow to rerun: call `partner_generate` again with the changed fields. If they want this exact audio edited rather than the workflow's inputs changed, use `use_previous_output` or `partner_generate` media inputs.

Fewer audio templates may exist than image templates. Say what the search returned. Discovery does not spend generation credits. A generation needs an active Comfy Cloud subscription. If a run is refused, check `get_billing_status` and report what it says.
