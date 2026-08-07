---
description: Search models on your local ComfyUI install
---

Search for models available to the user's own ComfyUI: $ARGUMENTS

Use `search_models` — it has three modes depending on what's given: a text `query` searches filenames across folders; a `folder` (e.g. "checkpoints", "loras", "vae") lists that folder's files; neither lists the folder names themselves. This reads the LOCAL disk live on every call — filenames only, no registry metadata (base model, hash, source) attached. Note the response shape differs by mode: `query` returns `rows`, `folder` returns `files`.

An absent name is not proof the model doesn't exist: it may be present under a folder or mode you haven't checked yet, so re-check a narrower folder before concluding it's genuinely missing (getting this wrong triggers a redundant multi-GB download). Only suggest `download_model` once you're confident it's actually absent.

Present results in a table: filename, folder (if known). If there are many, show a reasonable page and mention the total, offering to narrow by folder or query.
