---
name: help
description: Explain what Comfy Cloud can create and how to start. Use when the user asks what this plugin can do, how to sign in, whether they need a local install or an API key, or for examples of images, video, audio, or 3D they can request.
---

# What Comfy Cloud can do

Comfy Cloud is the hosted connector at `https://cloud.comfy.org/mcp`. The user signs in with OAuth on the plugin's Connectors tab, or with `/mcp` in Claude Code. Chat does not use an API key. Nothing here starts a local ComfyUI install. Workflows run on Comfy Cloud GPUs.

Say this briefly, in their words:

- Generate or edit a still image from a description or a source picture.
- Generate, edit, or extend video, including image-to-video.
- Generate music, sound effects, or speech. Cloning a voice from a recording is a separate step and needs permission to use that voice.
- Generate a 3D model from text or from an image.
- Remove a background, or upscale an image they attach.
- Search models, nodes, and workflow templates, then run a template or build a graph.
- Keep a character consistent across shots by loading the live technique from the server.
- Refine a previous result without rebuilding it: rerun that job with only the inputs that changed.
- Cancel a job or check the queue when they change their mind.

Catalog search does not spend generation credits. Running a generation needs an active Comfy Cloud subscription. Offer `get_billing_status` when they ask what a run will cost or why a run was refused.

Examples they can try: a mountain lake at golden hour; a short clip of a paper boat in a gutter; an upscale of a photo they attach; a template search for image-to-video.

Point them at <https://docs.comfy.org/cloud/mcp> for the tool list. Do not invent tools, models, or templates that search did not return.
