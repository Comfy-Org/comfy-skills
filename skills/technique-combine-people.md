Combine a user's photo with another person (real or fictional) into a single composite image: $ARGUMENTS

Follow these steps exactly:

## Step 1: Upload the user's photo

If the user provides a photo of themselves, use `upload_file` to upload it. Note the returned filename for use in LoadImage.

## Step 2: Generate a reference image of the other person

Use `KlingOmniProImageNode` (model: `kling-v3-omni`) or `GeminiNanoBanana2V2` to generate a high-quality reference portrait of the target person. Use a detailed prompt describing their iconic appearance. Save and upload the result for use as a second reference.

`GeminiNanoBanana2V2` is the current class name — the older `GeminiNanoBanana2` is marked deprecated in the node catalog and is hidden from `search_nodes`.

Alternatively, if the user provides their own reference image of the second person, upload that instead and skip generation.

## Step 3: Wire both references into the composite node

`GeminiNanoBanana2V2` takes up to 14 reference images directly, as auto-grow slots named `model.images.image_1` through `model.images.image_14`, so no separate batching node is needed — connect the user's photo to `model.images.image_1` and the other person to `model.images.image_2`.

If you do need a standalone image batch elsewhere in the graph, the current class is `BatchImagesNode` (display name "Batch Images"); the older `ImageBatch` is marked deprecated. Its `images` input is an auto-grow list, so call `get_node({ names: ["BatchImagesNode"] })` for the exact slot names before wiring it.

## Step 4: Generate the composite with Nano Banana 2

`GeminiNanoBanana2V2`'s `model` input is a dynamic combo, so the settings it gates are sent under their full dotted names, not flat. Call `get_node({ names: ["GeminiNanoBanana2V2"] })` for the exact input names before you build the graph.

Settings that matter for this recipe:

- **model**: `Nano Banana 2 (Gemini 3.1 Flash Image)`
- **model.thinking_level**: `HIGH` (critical for face accuracy)
- **model.resolution**: `2K`
- **model.aspect_ratio**: `16:9` (or match user preference)
- **model.images.image_1** / **model.images.image_2**: the two references from Step 3
- **response_modalities**: `IMAGE` (top level, not gated by `model`)
- **seed**: top level; vary it for Step 5

### Prompt structure (important):

The prompt should:

1. Explicitly state which reference image is which ("The first image is...", "The second image is...")
2. Emphasize EXACT face reproduction from both references
3. Describe clothing, pose, and setting
4. Specify lighting consistency
5. Call out any artifacts to avoid (e.g., "NO glare on glasses, NO reflections on lenses")

Example prompt:

```
Create a black and white vintage 1970s photograph combining these two people.
The first image is the primary reference - reproduce this man's face EXACTLY as shown:
his specific facial features, smile, dark hair style, and black zip-up jacket. He should
be on the left. The second image shows [PERSON NAME] - reproduce their face exactly as
shown with [iconic features]. They are posing together as close friends in [setting].
[Style instructions]. Important: [any artifact avoidance instructions].
```

## Step 5: Generate multiple variations

Submit 3 workflows with different seeds in parallel. This gives the user options to pick from since face reproduction varies by seed.

## Step 6: Show results and iterate

- Save all outputs locally and open them for the user
- Ask which variation they prefer
- If adjustments are needed (lighting, glare, pose), modify the prompt and regenerate with both the same seed (to stay close) and new seeds

## Model comparison (from testing):

| Model                             | Face accuracy              | Quality   | Speed |
| --------------------------------- | -------------------------- | --------- | ----- |
| **Nano Banana 2 (HIGH thinking)** | Best                       | Excellent | ~45s  |
| Nano Banana Pro                   | Good                       | Excellent | ~40s  |
| Kling O3 (kling-v3-omni)          | Good                       | Good      | ~60s  |
| Flux Kontext Pro                  | Moderate (single ref only) | Good      | ~20s  |
| SDXL img2img                      | Poor                       | Moderate  | ~15s  |

## Key learnings:

- **Two reference images are essential** - without a reference of the second person, models rely on training data and often miss the likeness
- **Nano Banana 2 with HIGH thinking** produces the most accurate face reproduction
- **Explicit prompt instructions** about which image is which person dramatically improves results
- **The SaveImage output directory != LoadImage input directory** on Comfy Cloud - always re-upload generated reference images via `upload_file` before using them in a new workflow
