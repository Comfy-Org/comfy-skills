---
name: clone-voice
description: Clone a voice from a reference recording and speak new lines with it on Comfy Cloud. Use when the user wants to copy a voice, match a recording they supply, or perform text-to-speech in that voice, including a multi-speaker script read in cloned voices.
---

# Clone a voice

Run this on the hosted Comfy Cloud connector (`https://cloud.comfy.org/mcp`). The user signs in with that connector's OAuth flow. There is no API key to collect, and the clone runs in the cloud, not on a local ComfyUI install.

This workflow is not one of the server's built-in product prompts. The tool descriptions still own parameter names. Template ids and node ids in older notes go stale. Resolve them with `search_templates` and `get_template_schema` on this run.

## Consent, before any generation

Voice cloning reproduces a real person's voice. Proceed only when the clip is the user's own voice, a voice they have explicit permission to clone, or a fictional or synthetic voice with no real person behind it. If the request would impersonate someone to a third party, put words in a real person's mouth that they did not say, or pass as a genuine recording of something they never said, stop and say why. If it is ambiguous, ask who the voice belongs to and what the audio is for before spending credits.

## Reference clip

Ask for a clip when they have not given one. One speaker, no music bed, natural pace, roughly 10–90 seconds. A noisy clip produces a noisy clone. If the clip has music or a second speaker, ask for a cleaner one. In chat, ask them to attach the clean clip. Trim with a local tool only when this session has a shell and they want a shorter window.

## What to do

1. `upload_file` the clip and keep the returned name. Keep the upload and the generation in the same signed-in session.
2. `search_templates` for voice cloning or reference text-to-speech in the language and speaker count they asked for. Read `get_template_schema` and override the audio input and the text (or dialogue) input it lists. Do not reuse node ids from a previous template.
3. For several lines, prefer one batch submit if the server exposes it, with a different seed per line, then wait until the batch is finished before collecting outputs.
4. Wait with `wait_for_job` (or the batch wait tool), then `get_output`. In chat, share the returned links. When a download command exists and this session has a shell, run it unchanged.
5. Change one setting at a time, and try a new seed before retuning. Say which control you changed.

A non-fatal widget warning on a load-audio node is not a failed job. Read the tool result before resubmitting. Discovery does not spend generation credits. This generation needs an active Comfy Cloud subscription. If a run is refused, check `get_billing_status` and report what it says.
