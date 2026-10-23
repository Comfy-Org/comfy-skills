---
description: Search nodes on your local ComfyUI install
---

Search for ComfyUI node classes available on the user's own install: $ARGUMENTS

Use the grouped `nodes` tool — it reads the LIVE local catalog (`object_info`, including custom nodes) on every call, so an outdated install shows outdated nodes:

- `nodes(action="search", query=...)` — find a class name by keyword.
- `nodes(action="get", name=...)` — one class's full input/output schema.
- `nodes(action="list", produces=..., accepts=..., category=..., pack=..., label=...)` — filtered browse; a bare call lists everything.
- `nodes(action="upstream"|"downstream", name=..., limit=...)` — what feeds into / is fed from a class.
- `nodes(action="path", from_type=..., to_type=...)` — chains between two connection types.
- `nodes(action="types"|"categories")` — the connection-type / category taxonomy.

Pick the action that matches what the user actually asked: a keyword ("what nodes handle upscaling") -> `search`; a specific class's details -> `get`; "what nodes take an IMAGE" -> `list` with `accepts`; "how do I get from a LATENT to an IMAGE" -> `path`.

If a node the user expects is missing, or a returned node isn't from the pack they expect, mention `node_dependencies` / `workflow_deps` as the follow-up rather than guessing why.

Present results clearly: node name and display name, category, pack (or "core" for built-in), inputs and outputs. If the user is assembling a pipeline, suggest which nodes to wire together.
