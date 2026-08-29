---
description: Check the comfy-cli project anchoring your local ComfyUI
---

Report the operator-anchored comfy-cli project state.

Call `project(action="status")`. comfy-cli resolves the project by walking up from ITS OWN working directory, not this chat's — so with `COMFY_PROJECT` unset, the answer describes wherever this MCP server's process happens to be running, and relative `workflow_path` / `out_path` / `out_dir` arguments passed to other tools land there too. If that's a surprise to the user, mention `COMFY_PROJECT` (an absolute path, read once per process) as the fix.

If no project is governed yet and the user wants one, use `project(action="init")` to create `comfy.yaml` plus the project directories — check status first, since re-running init on an already-governed directory raises `project_already_exists`.
