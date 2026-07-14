---
name: comfy
description: Generate images, video, audio, and 3D with Comfy Cloud — search hundreds of models and workflow templates, run custom ComfyUI workflows, and manage generation jobs through the hosted Comfy Cloud MCP server. Cloud-only — connects to the hosted service, not a local ComfyUI install. Use for any "generate/edit an image", "make a video", "text to 3D", or ComfyUI workflow task.
---

# Comfy Cloud

Comfy Cloud runs [ComfyUI](https://www.comfy.org) in the cloud and exposes it to
agents as an MCP server: image/video/audio/3D generation via partner models
(Ideogram, Flux, Kling, Veo, Seedance, and more) and open-source pipelines,
plus full ComfyUI workflow authoring — search templates, override inputs,
submit custom graphs, and fetch outputs as signed URLs.

> **Scope**: this skill connects to the hosted **Comfy Cloud** MCP server and
> requires a Comfy account — it does not drive a local ComfyUI install. A
> local-ComfyUI MCP is on the roadmap and will ship as a separate skill; until
> then, for local instances see
> [comfy-cli](https://docs.comfy.org/comfy-cli/getting-started).

## Connect

The server supports two auth methods: **OAuth** (browser sign-in, nothing to
manage — recommended) and **API keys** (for headless or CI setups).

### Option A — OAuth (recommended)

```bash
openclaw mcp set comfy '{"url":"https://cloud.comfy.org/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login comfy
openclaw gateway restart
```

`openclaw mcp login` prints an authorization URL — open it, sign in to your
Comfy account, and finish the flow as the CLI directs (it may ask you to rerun
with `--code <code>`). Verify with `openclaw mcp status --verbose`. Note that
OpenClaw ignores static `headers` on a server entry once `auth: "oauth"` is
set, so don't combine the two.

### Option B — API key (headless / CI)

1. **Get an API key** — sign in at [cloud.comfy.org](https://cloud.comfy.org),
   then create a key under **Settings → API Keys**. Keys start with `comfyui-`.

2. **Export it** (put this in your shell profile or OpenClaw's env):

   ```bash
   export COMFY_API_KEY="comfyui-..."
   ```

3. **Register the MCP server with OpenClaw:**

   ```bash
   openclaw mcp set comfy '{"url":"https://cloud.comfy.org/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${COMFY_API_KEY}"}}'
   openclaw gateway restart
   ```

   The server also accepts the key as an `X-API-Key: ${COMFY_API_KEY}` header,
   but prefer the `Authorization: Bearer` form above — standard headers survive
   every client's proxy layer, and some OpenClaw builds have dropped custom
   headers on streamable-http transports (see openclaw#65590). If you get a
   `401` with a key you know is valid, you are probably hitting that: switch to
   the Bearer form, route through mcporter, or just use OAuth (Option A).

Either way: browsing/search tools work with any account; generation consumes
Comfy Cloud credits and needs a subscription or credit balance.

## Which tools to use

**Images and video from a named model** (Ideogram, Flux, Gemini, Kling, Veo,
Seedance, …): call `partner_generate` — it runs the provider through Comfy
Cloud and saves the result to your asset library. Do not hand-build a workflow
for plain text-to-image/video when a partner model is named.

**Anything workflow-shaped** (open-source models, LoRA/ControlNet, multi-step
pipelines): start from a template — `search_templates` → `get_template_schema`
→ `run_template` with `input_overrides`. For fully custom graphs use
`submit_workflow` (the graph must end in an output node like SaveImage, or
validation rejects it). Save and reuse with `save_workflow` /
`run_saved_workflow`.

**Editing an existing image**: `upload_file` first, then reference the
uploaded file from a LoadImage node (or pass it to `partner_generate` for
image-to-image partners). Never inline base64 image data into a workflow.

**Getting results**: `wait_for_job` → `get_output`. Outputs come back as
time-limited signed URLs — download them exactly as returned (don't edit query
params, they're part of the signature). `get_queue` and `cancel_job` manage
in-flight jobs; `submit_batch` / `wait_for_batch` fan out variations.

**Discovery**: `search_models` (checkpoints/LoRAs on the platform),
`search_nodes` (available ComfyUI nodes with wiring hints),
`get_prompting_guide` (model-specific prompting advice).

## Example prompts

- "Generate an image of a cozy bookstore café on a rainy afternoon with
  Ideogram and download it to ./bookstore.png"
- "Take ./product.jpg, remove the background, and upscale the result 2×"
- "Find a text-to-video template for Kling, run it with the prompt 'a paper
  boat drifting down a rain gutter, cinematic', and give me the output URL"

## Notes

- Generation spends Comfy Cloud credits; search/discovery tools are free.
- Full MCP docs and per-client setup: [docs.comfy.org/cloud/mcp](https://docs.comfy.org/cloud/mcp)
