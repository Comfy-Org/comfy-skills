---
description: Find pre-built workflow templates for your local ComfyUI
---

Search for ComfyUI workflow templates for the user's own install: $ARGUMENTS

Use `search_templates` to find pre-built templates matching the query — this searches the built-in gallery, not the live install. Filter by `tag`/`type` (exact match) or `model`/`provider` (substring); pass `exclude_api=True` to show only templates that run without a partner API. Results are cached with a 24h TTL and are NOT read from the local install, so a match here doesn't yet mean it runs here.

For a promising match, follow up with `get_template(name)` — its `local_check` block reports whether the CURRENT install can actually run it (missing nodes or models show up there). Only call `fetch_template` once the user wants to proceed with a specific template.

Present results in a clean format:
- Template title
- Description (first sentence)
- Tags
- Models used
- Whether `local_check` reported it runnable here, if you already looked it up

If there are many results, show the top 10, mention the total count, and offer to page further with `offset`.
