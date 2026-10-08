---
name: comfy-sdk
description: Build an app that generates images, video or audio through Comfy Router using the Comfy SDK (Python `comfy-sdk` or TypeScript `@comfyorg/sdk`). Use when a task mentions the Comfy SDK, Comfy Router, `models.run`, or adding generation to an app via api.comfy.org. Not for driving the `comfy` CLI, ComfyUI workflows or custom nodes (see the `comfy` skill).
---

# comfy-sdk — build with Comfy Router

Steering only. Model names, schemas, prices and default timeouts change:
discover them at run time (section 3) or read them off the installed SDK, and
never paste one from memory.

## 1. Pick the right client

- **Router** (partner models, `https://api.comfy.org`) is reached through the
  `models` namespace:
  - Python: `Comfy().models` (`AsyncComfy().models` for asyncio).
  - TypeScript: the **module-level** `comfy.models`, after `comfy.config({ credentials })`
    or with `COMFY_API_KEY` set. `new Comfy({ apiKey })` is the Comfy Cloud
    *workflow* client and has **no** `.models`.
- **Cloud** (`/api/v2/jobs`, run a ComfyUI workflow) is the class client in both SDKs.
- Both use the same `COMFY_API_KEY`. Hosts are separate: `COMFY_ROUTER_BASE_URL`
  redirects Router, `COMFY_BASE_URL` redirects Cloud. Leave both unset in production.

```python
from comfy_sdk import Comfy

client = Comfy()  # reads COMFY_API_KEY
result = client.models.run("<provider>/<model>", {<provider's native body>})
```

```ts
import { comfy } from "@comfyorg/sdk";

comfy.config({ credentials: process.env.COMFY_API_KEY });
const { kind, data, requestId } = await comfy.models.run("<provider>/<model>", {<native body>});
```

## 2. Credentials stay on the server

- The SDKs read `COMFY_API_KEY` from the **process environment**; neither loads a
  `.env` file. Your framework does that (`python-dotenv`, Next.js `.env.local`,
  etc.). An explicit `api_key=` / `credentials` argument always wins over the variable.
- Never expose the key to a browser bundle (no `NEXT_PUBLIC_` / `VITE_` prefix). Call
  Router from a server route and return the result to the page.
- Preflight before any paid call: list models (section 3). A `401` there means the
  key, not the model, is wrong.

## 3. Discover, then call

- `GET /v2/models` lists what the credential can run, with billing facts. Paginate
  with `next_cursor` while `has_more` is true; treat cursors as opaque.
- `GET /v2/models/{provider}/{model}/openapi.json` is that model's input/output schema.
  The second argument to `run` / `submit` is the provider's **native body**, forwarded
  unchanged, so build it from this schema, not from another provider's shape.
- TypeScript wraps both: `comfy.models.list()` walks the catalog and
  `comfy.models.schema(model)` fetches the document. In Python, if the installed
  `client.models` has no such helper, call the two routes on the Router host
  yourself with `Authorization: Bearer <COMFY_API_KEY>`.
- A model id is exactly two segments, `provider/model`.

## 4. `run`, `submit` or `subscribe`

- `run` blocks until the generation is finished. The wait is **server side**:
  Router holds the connection up to its own deadline, then answers
  `504 deadline_exceeded`. The SDK retries that with the same `Idempotency-Key`
  and `Retry-After`, collecting the running generation rather than starting a
  second one.
- `submit` returns a handle with a `request_id` at once. Use it in any web request
  handler, serverless function or job queue that cannot hold a connection for
  minutes. Collect later, even from another process, with
  `models.handle(model, request_id)` then `get()` / `status()` / `cancel()`.
- `subscribe` is submit + poll + collect with a progress callback. Its timeout is
  **client side only**; when it expires it makes one best-effort cancel. A
  generation already running at the partner completes and is billed regardless.
- There are no webhooks or push events: the status route is how you follow a
  request. `submit` / `handle` / `subscribe` need `comfy-sdk` / `@comfyorg/sdk`
  0.3.0 or newer.

## 5. Timeouts: units and what they bound

- Python `models.run(..., timeout=)` is **seconds** and defaults to the SDK's own
  run timeout, sized to Router's deadline. `Comfy(timeout=...)` sizes ordinary API
  calls and does **not** change the run default.
- TypeScript `{ timeoutMs }` is **milliseconds**; its default is longer than
  Router's deadline so a same-key collect still fits. Prefer an `AbortSignal` to
  `timeoutMs: null`.
- The exact defaults move between releases. Read them from the installed SDK
  (the `run` signature, `DEFAULT_RUN_TIMEOUT_MS`) instead of hard-coding a number.
- Do not set a run timeout below a realistic generation (tens of seconds to
  minutes). If your platform caps request duration (serverless, proxies), switch
  to `submit` instead of lowering the timeout.

## 6. Retries and idempotency are already handled

- Every `run` / `submit` mints an `Idempotency-Key` and reuses it for its own
  retries, so a retried attempt is charged at most once. Calling `run` again is a
  **new key and a new charge**: do not wrap it in your own retry loop.
- To retry one logical call across processes or restarts, pass
  `idempotency_key=` / `{ idempotencyKey }` yourself and keep the body identical;
  the same key with a different body is refused `409 invalid_input` (use a new key).

## 7. Errors: branch on `error_type`

Python raises classes from `comfy_sdk.router_exceptions`; TypeScript throws
`routerErrors.*`, all descending from `RouterError`. Both carry the wire
`error_type` (`exc.error_type` in Python, `err.errorType` in TypeScript; also the
`X-Comfy-Error-Type` header).

- `insufficient_credits` (`402`): stop and tell the user to add credits. Never retry.
- `content_policy_violation`: do not resend the same prompt.
- `rate_limited` / `concurrency_limit_exceeded`: honour `Retry-After` (the SDK does).
- `not_enabled` (`403`): the workspace is not on this model or route yet; terminal.
- `provider_timeout` vs `deadline_exceeded`: both `504`; the first is the partner,
  the second is Comfy's bound. The SDK retries the second with the same key.
- An unrecognised `error_type` surfaces as the base `RouterError`, so keep a
  catch-all branch.
- A queued request can finish as `COMPLETED` **with** an `error_type`; `get()` raises
  the typed error, and the event iterator yields it as the last observation.

## 8. Results

- Python `run` returns the provider's payload as-is. TypeScript returns
  `{ kind, data, requestId }` (`kind` is `"json"` or `"binary"`; branch on it) and
  caps the buffered body (`maxBytes`).
- Asset URLs in a result are time-limited. Download or re-host what you want to
  keep before responding to the user; do not store a partner URL as a permanent link.

## 9. Before the first generation

1. Key read server side; `GET /v2/models` succeeds.
2. Model chosen from that list; body built from its `openapi.json`.
3. `run` only where the process can wait minutes; otherwise `submit`.
4. Timeout in the right unit, or left at the default.
5. `insufficient_credits` surfaced to the user, not retried.

## Read next

- Quickstart: https://docs.comfy.org/development/comfy-router/quickstart
- Queued delivery: https://docs.comfy.org/development/comfy-router/queue
- Error buckets: https://docs.comfy.org/development/comfy-router/reference#error-buckets
- SDK READMEs: https://github.com/Comfy-Org/comfy-python-sdk and
  https://github.com/Comfy-Org/comfy-typescript-sdk
