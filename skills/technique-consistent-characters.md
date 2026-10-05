Keep one or more specific characters visually consistent across multiple shots or scenes (images or video) using reference images: $ARGUMENTS

Follow these steps exactly:

## Step 1: Lock one reference set per character

If the user supplied a photo or drawing, `upload_file` it and note the returned filename. Otherwise generate a clean, neutral-pose, plain-background portrait per character with `GeminiNanoBanana2V2` (model `Nano Banana 2 (Gemini 3.1 Flash Image)`, `model.thinking_level` `HIGH`) or `KlingOmniProImageNode`. Optionally expand each into a turnaround sheet with a template from `search_templates({ query: "character turnaround sheet" })`.

Generate each character in a SEPARATE run, one character per generation. This split is what prevents traits bleeding between characters. Save every output and re-upload it with `upload_file` before using it in another workflow.

## Step 2: Wire references one per slot, never as an array

Call `get_node({ names: [...] })` first and copy the exact slot names it returns. Multi-reference inputs are auto-grow lists (`COMFY_AUTOGROW_V3`), often nested under the selected `model` option: `GeminiNanoBanana2V2` exposes `model.images.image_1` … `image_14`; `MiniMaxH3ReferenceToVideo` exposes `ref_images.*`. Put exactly one reference image per slot. A flat `images: [...]` array or a top-level `image_1` is silently ignored.

`KlingOmniProImageNode` and `KlingOmniProImageToVideoNode` (up to 7) take `reference_images` as a single IMAGE batch instead: build it with `BatchImagesNode`, one reference per its auto-grow slot.

```json
"1": { "class_type": "LoadImage", "inputs": { "image": "mira_ref.png" } },
"2": { "class_type": "LoadImage", "inputs": { "image": "bram_ref.png" } },
"3": { "class_type": "GeminiNanoBanana2V2", "inputs": {
  "model": "Nano Banana 2 (Gemini 3.1 Flash Image)",
  "model.images.image_1": ["1", 0],
  "model.images.image_2": ["2", 0],
  "prompt": "Image 1 is MIRA ... Image 2 is BRAM ..." } }
```

With `run_template`, address the slot by the same dotted path in `input_overrides`. With `partner_generate`, each reference is its own `medias[]` item with its role (see the partner playbook).

## Step 3: Name every slot and state the exact count

Every shot's prompt must:

1. Say which slot is which character, by name, with 2-3 distinguishing traits: "Image 1 is MIRA: silver hair, burn scar on right cheek. Image 2 is BRAM: shaved head, chipped front tooth."
2. State the exact number of people: "Exactly two people, Mira and Bram; no other people."
3. Describe each character's action and position (left/right), plus the shared setting and lighting.
4. Say what must not change: "Keep Mira's face, hair and outfit exactly as in Image 1."

The explicit count plus per-slot naming is what stops the model rendering one character twice.

## Step 4: Multi-character scenes

Feed ALL characters' references into one node, one slot each, with the Step 3 prompt. If a character still duplicates or traits bleed, split: generate the scene with one character, re-upload it, then run an image-edit pass that adds the second character from its reference (Flux Kontext, Qwen Image Edit or Nano Banana 2 edit, via `search_templates({ query: "image edit reference" })`).

## Step 5: Shot-to-shot consistency

Reuse the SAME reference files for every shot. Never use the previous shot's output as the character reference (drift compounds); use it only as a scene/lighting reference in an extra slot if the node allows. Keep `seed` fixed per character across shots where the node exposes one, and vary only the shot description. Chain with `use_previous_output` or re-upload.

## Step 6: Video shots

For motion, use a template from `search_templates({ query: "reference to video" })` (at time of writing: Seedance 2.5 up to 20 images, MiniMax H3 up to 9, HappyHorse up to 9, Wan3.0 two images, Gemini Omni 1.1 Flash). Wire references per Step 2 and prompt per Step 3. For a locked character performing a given motion, use a character-replacement / motion-control template (SCAIL-2, Kling Motion Control, Wan Animate 2) with one character per run.

## Step 7: Variations and iteration

Submit 2-3 seeds per shot in parallel, show the results, and ask which to keep. Regenerate only the shots that drifted, with the same references and a tightened Step 3 prompt.

## Key learnings:

- **One reference set per character**, each generated in its own run
- **One reference per auto-grow slot** - slot names come from `get_node`, never an array
- **Name every slot and state the exact person count** in the prompt
- **Same references for every shot** - never the previous shot's output
- **The SaveImage output directory != LoadImage input directory** on Comfy Cloud - re-upload with `upload_file` between workflows
