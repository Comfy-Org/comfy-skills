---
description: Clone a voice from a reference recording and speak text with it using Comfy Cloud
---

Clone a voice from a reference recording and generate speech with it: $ARGUMENTS

## Step 0 — Consent check (do this first, every time)

Voice cloning reproduces a real person's voice. Before generating anything, confirm the
request is one of:

- The user cloning **their own** voice.
- A voice the user has **explicit permission** to clone (a colleague who asked for it, a
  voice actor under contract, a synthetic or licensed voice).
- A clearly **fictional or synthetic** voice with no real person behind it.

Do **not** proceed if the request is to impersonate someone to a third party, put words in a
real person's mouth they would object to, or produce audio that could pass as a genuine
recording of something they never said. If the ask is ambiguous, ask the user who the voice
belongs to and what the audio is for before spending credits. If it drifts toward deception,
stop and say why.

## Step 1 — Get a reference recording

Ask the user for a reference clip if they have not supplied one. What makes a good reference:

- **One speaker only.** No cross-talk, no music bed, no laughter over the top.
- **10–90 seconds.** Longer does not improve the clone; 30s of clean speech beats 90s of noisy.
- **Natural speech** at a normal pace — not shouting, not whispering, not reading robotically.
- Accepted formats: `.mp3`, `.wav`, `.flac`, `.ogg`.

Reference quality dominates output quality. A noisy clip produces a noisy clone no amount of
parameter tuning will fix. If the clip has music or a second speaker, say so and ask for a
cleaner one rather than generating from it.

If the clip needs trimming to a clean window, do it locally with ffmpeg before uploading:

```bash
ffmpeg -y -i <source> -ss <START> -t <SECONDS> -ar 44100 -ac 1 ref.wav
```

## Step 2 — Upload the reference

```
upload_file(file_path: "<absolute path to the clip>", client_os: "<darwin|linux|windows>")
```

Note the returned `name` — that is what the `LoadAudio` node references. On a hosted/remote
session this returns a `PUT` command for the user's own shell; run it exactly as emitted and
read `name` out of the JSON it prints.

## Step 3 — Generate speech

Run the Chatterbox zero-shot voice-cloning template, pointing `LoadAudio` at the uploaded
reference and `FL_ChatterboxTTS` at the line to speak:

```
run_template(
  name: "audio-chatterbox_tts",
  input_overrides: {
    "6": { "audio": "<name from upload_file>" },
    "4": { "text": "<the line to speak>", "seed": <vary per line>, "exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.8 }
  }
)
```

Then poll `get_job_status` until completed and call `get_output` with a short `description`
so the saved file gets a useful name.

`run_template` returns `conversion_warning: Node 6 (LoadAudio): 1 extra widget values not
mapped` on this template. That is the node's `audioUI` preview widget and is **non-fatal** —
the job runs as submitted. Do not cancel or resubmit over it.

**For more than one line, call `submit_batch` once** with a `run_template` item per line
rather than running this template N times — one spend confirmation, one round of polling,
and `get_batch_output` collects them all. Vary `seed` per line so repeated phrases do not
come out identically stamped.

For a non-English target language, use `audio-chatterbox_tts_multilingual` instead and set
its language input. For multi-speaker dialogue from a single script, use
`audio-chatterbox_tts_dialog`.

## Step 4 — Tuning

Change one knob at a time, and re-roll `seed` before reaching for the others — an odd read is
more often an unlucky sample than a wrong parameter.

| Knob | Raise it | Lower it |
|---|---|---|
| `exaggeration` (0–1) | more animated, more expressive | flatter, calmer, more deadpan |
| `cfg_weight` (0–1) | tighter adherence to the reference | ~0.3 slows pacing; often clearer for fast talkers |
| `temperature` (0–1) | more variation between runs | ~0.4 when a line keeps coming out erratic |

## Notes

- Generation consumes Comfy Cloud credits and needs a workspace with credits on it. The
  discovery tools (`search_templates`, `search_models`) work without a subscription; this
  command does not.
- `upload_file` accepts audio as well as images — the reference does **not** need to be
  hosted anywhere public first, and it does not need a separate API key. Keep the upload and
  the generation in this one MCP session.
- If `run_template` reports an unknown template name, run
  `search_templates(q: "chatterbox")` and use the exact `name` it returns.
