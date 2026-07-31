Composite a semi-transparent subject into a scene so the background shows through, by generating subject and background together, segmenting the subject out, inpainting the hole it leaves, and recompositing at a controllable opacity.

Use this when the user wants a ghostly, holographic, or partially see-through character in a scene — typically as the reference or first frame for a video model such as Seedance. Prompting alone will not get you there; the transparency has to be a compositing step you control, not a phrase in the prompt.

Before building this by hand, run `search_templates` — a ready-made template you can clone beats hand-wiring, and the catalog moves.

Check first that you need this recipe rather than a simpler one, because "transparent" covers two different asks:

- **A subject on a transparent background** (an alpha cutout, no scene) — that is native RGBA generation, not compositing. Use the Layer Diffuse family (`LayeredDiffusionApply` into `LayeredDiffusionDecodeRGBA`), or segment an existing image and keep the alpha. Do not use this recipe.
- **A subject that is itself see-through, with a scene visible through it** — that is this recipe. The scene behind the subject has to be reconstructed before anything can show through, which is what Steps 2-4 do.

Follow these steps exactly.

## Step 1: Generate the subject and the background together in one image

Generate the character **in** the scene, in a single image, from a single prompt. Do not generate the character and the background separately — that is the failure mode this recipe exists to avoid (see Key learnings).

Use whichever image node the user's request points at, e.g. `GeminiNanoBanana2V2` or `KlingOmniProImageNode`. Node availability moves, so confirm the current class with `search_nodes` (`category: "partner/image"`) rather than assuming, and call `get_node` for the exact input slot names — several of these nodes gate their settings behind a dynamic `model` combo and take dotted input names like `model.resolution`.

Prompt for a fully opaque, normally-lit character. Transparency is applied in Step 4; asking for it here just makes the model guess.

Keep this image. It is used three more times: as the segmentation input, as the IPAdapter reference, and as the composite source. Steps 1-4 can be one workflow; if you split them across submissions, re-upload the generated image with `upload_file` first — on Comfy Cloud the `SaveImage` output directory is not the `LoadImage` input directory.

## Step 2: Segment the subject out of that image

Produce a `MASK` covering the character. Pick the node that fits how the character has to be identified:

| Node | What it needs | Good for |
| --- | --- | --- |
| `SAM3Segment` | a text `prompt` (e.g. "the woman in the red coat") | Naming one subject in a scene that contains several |
| `BiRefNetRMBG` | just `image` plus a `model` choice | Clean single-subject cutouts; `BiRefNet-matting` for hair and soft edges |
| `LayerMask: BiRefNetUltraV2` (+ `LayerMask: LoadBiRefNetModelV2`) | a loaded `BIREFNET_MODEL` | The same family with explicit `detail_erode` / `detail_dilate` / black-and-white-point controls |
| `SAM3Segmentation` (+ `LoadSAM3Model`) | point or box prompts | Precise manual control when a text prompt picks the wrong thing |
| `RemoveBackground` (+ `LoadBackgroundRemovalModel`) | a loaded `BACKGROUND_REMOVAL` model | Core-node path, mask output only |

`SAM3Segment` and `BiRefNetRMBG` are single self-contained nodes (no separate loader), so they are the cheapest place to start.

Keep **two** versions of this mask:

- the **tight** mask, for compositing the character back in Step 4;
- a **grown** mask, for the inpaint in Step 3, so no rim of character pixels survives to be reconstructed into the background:

```json
{
  "class_type": "GrowMask",
  "inputs": { "mask": ["segmentation_node", 0], "expand": 12, "tapered_corners": true }
}
```

## Step 3: Inpaint the hole with IPAdapter

The grown mask leaves a character-shaped hole in the scene. Fill it by inpainting, with IPAdapter conditioning the fill on the original image so the reconstructed patch matches the scene's lighting, palette, and texture instead of inventing new content.

Wire it as: checkpoint → IPAdapter → inpaint conditioning → sampler → decode.

```json
{
  "ipadapter_loader": {
    "class_type": "IPAdapterUnifiedLoader",
    "inputs": { "model": ["checkpoint", 0], "preset": "PLUS (high strength)" }
  },
  "ipadapter": {
    "class_type": "IPAdapterAdvanced",
    "inputs": {
      "model": ["ipadapter_loader", 0],
      "ipadapter": ["ipadapter_loader", 1],
      "image": ["original_image", 0],
      "weight": 0.8,
      "weight_type": "linear",
      "combine_embeds": "concat",
      "start_at": 0.0,
      "end_at": 1.0,
      "embeds_scaling": "V only",
      "attn_mask": ["grow_mask", 0]
    }
  },
  "inpaint_cond": {
    "class_type": "InpaintModelConditioning",
    "inputs": {
      "positive": ["positive_prompt", 0],
      "negative": ["negative_prompt", 0],
      "vae": ["checkpoint", 2],
      "pixels": ["original_image", 0],
      "mask": ["grow_mask", 0],
      "noise_mask": true
    }
  }
}
```

Then run `KSampler` with `model` from the `IPAdapterAdvanced` output (not the raw checkpoint — that is what applies the IPAdapter conditioning) and `positive` / `negative` / `latent_image` from `inpaint_cond`'s three outputs, and decode with `VAEDecode`. `VAEEncodeForInpaint` is the alternative latent path if the checkpoint is not an inpainting model; it takes its own `grow_mask_by`, so you can skip the separate `GrowMask` on that branch.

Two things to resolve at run time rather than assume: `IPAdapterUnifiedLoader` needs IPAdapter and CLIP-vision weights compatible with the checkpoint (use `search_models`, or wire `IPAdapterModelLoader` + `CLIPVisionLoader` explicitly via `IPAdapterAdvanced`'s `clip_vision` input), and the enum values above (`preset`, `weight_type`, `embeds_scaling`) should be confirmed with `get_node` before submitting.

Prompt the inpaint for the background only — describe what should be behind the character, never the character.

The output of this step is the reconstructed **background plate**: the same scene, no character, lighting and perspective intact.

## Step 4: Recomposite the subject at a controllable opacity

You now hold two aligned layers at the same resolution: the original image (character in place) and the background plate. Because the character was never moved, compositing needs no alignment work — the tight mask from Step 2 puts it back exactly where it was.

Scale the mask to set opacity, then composite:

```json
{
  "opacity": {
    "class_type": "SolidMask",
    "inputs": { "value": 0.45, "width": 1280, "height": 720 }
  },
  "faded_mask": {
    "class_type": "MaskComposite",
    "inputs": {
      "destination": ["tight_mask", 0],
      "source": ["opacity", 0],
      "x": 0,
      "y": 0,
      "operation": "multiply"
    }
  },
  "composite": {
    "class_type": "ImageCompositeMasked",
    "inputs": {
      "destination": ["background_plate", 0],
      "source": ["original_image", 0],
      "x": 0,
      "y": 0,
      "resize_source": false,
      "mask": ["faded_mask", 0]
    }
  }
}
```

`ImageCompositeMasked` blends per pixel by mask value, so a mask multiplied down to `0.45` gives a 45% character over a 100% background — the background genuinely shows through, and `value` is a dial the user can move without regenerating anything. Size `SolidMask` to the image: `MaskComposite` multiplies only where the two masks overlap and does not resize, so a short `SolidMask` silently leaves the rest of the character at full opacity. Run `FeatherMask` on the tight mask first if the edge reads as cut out.

If a downstream step needs the character as a standalone RGBA layer instead of a flattened frame, use `JoinImageWithAlpha` (`image` = original image, `alpha` = faded mask).

## Step 5: Hand the composite to the video model

The composited frame is a normal image, so it feeds any image-conditioned video node — for the Seedance case, `ByteDance2ReferenceNode` (reference-to-video) or `ByteDance2FirstLastFrameNode` (first-frame). These gate their inputs behind a dynamic `model` combo, so call `get_node` for the exact slot names before wiring, and confirm the current class with `search_nodes` (`category: "partner/video"`).

Save the background plate and the tight mask alongside the composite. Regenerating a different opacity, or re-cutting the composite for another shot, is then a Step 4 re-run rather than a full rebuild.

## Key learnings:

- **Prompting alone cannot control transparency** — models treat "semi-transparent" as a style hint, so opacity comes out inconsistent across seeds and unmovable after the fact. Hold the character and the background as separate layers and the opacity becomes a number you set.
- **Generating the character separately from the background looks disconnected** — a character generated on its own and pasted over a separately generated scene reads as a sticker: the lighting direction, perspective, colour temperature, and grain never agree. Generate both together in one image first, then take them apart. That is the whole reason for Steps 1–3.
- **Inpaint the hole, do not skip it** — the character is occluding scene content that has to exist before anything can show through it. Without the reconstruction pass there is nothing behind the character to reveal.
- **Grow the mask for the inpaint, keep it tight for the composite** — one mask cannot do both jobs. A tight inpaint mask leaves a halo of character-coloured pixels that the fill then propagates outward; a grown composite mask eats the character's edges.
- **The character never moves**, so the composite needs no alignment step — this is the practical payoff of generating together, on top of the visual coherence.
