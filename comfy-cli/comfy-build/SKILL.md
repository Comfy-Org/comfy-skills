---
name: comfy-build
description: Build a ComfyUI distribution on the Comfy developer platform with comfy-cli — turn a working local ComfyUI install into a distribution that builds in the cloud, pin its dependencies before the first paid build, and read the build's verdict. Use when someone asks to deploy, package, or cloud-run their install.
---

# comfy-build

There is a platform. A user asking to run their ComfyUI "in the cloud" is asking for a **distribution**, which the Comfy platform builds for them — not for a Dockerfile you write yourself. Nothing inside a ComfyUI install points at the platform, so this is the one thing you cannot discover from the working directory.

The whole surface is `comfy distribution` in [comfy-cli](https://github.com/Comfy-Org/comfy-cli). Start with `comfy distribution --help`; every step below names the command that does it.

**Covered here: a working local install.** A user holding only a workflow file, or only a description of what they want, is not covered yet — say so rather than improvising one.

## The path

**Define, check locally, create, read.** In that order, and the third step is the one that costs something.

| Step | Command | What it is for |
| --- | --- | --- |
| Define | `comfy distribution scan --python <comfyui-python> -o definition.json` | Evidence about the install. Not a buildable definition — see below. |
| Define | `comfy distribution resolve <filename> …` | Which local models have a hash-matched public download, so they need no upload. `--execute` runs this itself; use it early to know what the upload will weigh. |
| Check | `comfy distribution create --from definition.json --name <name>` (no `--execute`) | Offline preview of exactly what would be sent. Makes no network call. |
| Create | `comfy distribution create --from definition.json --name <name> --execute` | **Creates the distribution and immediately cuts build 1.** |
| Read | `comfy distribution version get <version-id>` | `status`, `artifactCounts`, and a `failureReason` per target. |
| Read | `comfy distribution version logs <version-id>` | The build log for one target. |
| Revise | `comfy distribution update <id> --from definition.json`, then `comfy distribution validate <id>`, then `comfy distribution version create <id>` | The only way to change anything. Every cut is a new version. |

**There is no create-without-building.** `--execute` creates *and* cuts, so the free server-side `validate` cannot run before the first build. Everything checkable for free, check before `--execute`; `validate` is the gate on every cut after that.

## Ask the platform, never remember

Versions move. Read them at run time, and never carry one in from memory.

| Question | Command |
| --- | --- |
| What Python, CUDA and torch will the build run? | `comfy distribution base-images` |
| Which os/gpu targets can be cut? | `comfy distribution build-targets` |
| Which folders may a model go in? | `comfy distribution model-dirs` |
| What did this version actually seal? | `comfy distribution version manifest <version-id>` |
| Can I reach the builder? | `comfy distribution list` |

`comfy cloud whoami` reports only the OAuth session and names a production URL. It says `signed_in: false` while a `COMFY_BUILDER_TOKEN` in the environment is working perfectly. **It is not the answer to "can I build".** `comfy distribution list` returning a list is.

## Authoring the definition

`scan` writes evidence, not something you can build. Three of its fields need judgment before anything is sent.

### Custom nodes: prefer the registry pin

`scan` reports each pack as `source: git` (a checkout with an origin and a HEAD) or `source: local`. **`--execute` refuses to upload a local node**, and `comfy node install` writes archives rather than clones, so on an install built with the comfy CLI every pack scans as local and the default path dead-ends.

Do not go hunting for a git tag — a registry version is a package semver and often has no tag at all. Each installed pack's `pyproject.toml` carries the two fields the builder wants:

```toml
name = "comfyui-kjnodes"     # the registry node id
version = "1.4.9"            # the registry version
```

which becomes:

```json
{ "id": "comfyui-kjnodes", "name": "comfyui-kjnodes", "registryVersion": "1.4.9" }
```

The builder resolves that pair against the registry and installs the published artifact. A node sets **exactly one** source:

- `repository` (an `https://github.com/{org}/{repo}` URL), optionally with a `gitRef`,
- `registryVersion` plus `id`, or
- `blobId`, for something genuinely private.

Two nodes resolving to the same `custom_nodes/` directory are rejected at the boundary, case-insensitively.

### The ComfyUI pin: prefix it and prove it

`scan` writes `baseComfyVersion` from the install's version marker, which is bare (`0.30.2`). The builder resolves that field as a **git ref**, and ComfyUI tags releases with a `v`. **An unedited scan definition fails its first build for this reason alone.** Set the tag, and confirm it exists before spending a build:

```
git ls-remote --tags https://github.com/comfyanonymous/ComfyUI.git v0.30.2
```

### Pins: the freeze is evidence, and the target is not this machine

`scan`'s `pipDependencies` is a `pip freeze` of the install, tagged in its header with the platform it came from. It describes the machine the workflow ran on. The build runs somewhere else — `comfy distribution base-images` says where.

- **Torch, torchvision and torchaudio: pin all three or none.** The builder installs that stack itself, freezes it, and holds every other install to those exact versions. Pinning any one of the three **replaces** the builder's line and **releases the other two**, so a lone `torch==` pin is how a mismatched torchvision arrives transitively and the build dies with `torchvision::nms does not exist`. Dropping all three is the safe default; keeping all three means matching what `comfy distribution base-images` reports.
- **Never use a local version tag** (`+cu130`, `+cpu`). The linux/nvidia resolve runs against PyPI alone, where such a version does not exist, so the pin that looks most correct is the one that fails.
- **Pin what actually conflicts, and nothing else.** `pipDependencies` is applied as an override, which forces a version rather than adding a package: pinning something nothing else requires installs nothing.
- **A bare name is not a pin.** `torch` without a version, or a pin carrying an environment marker, is ignored rather than honoured — write an exact `==` or leave it out.
- **Option lines are dropped** from `pipDependencies`, so `--index-url` and friends cannot redirect the resolve. Do not try.

Prove the set resolves before spending a build — against PyPI alone and the base image's Python, which is what the builder does:

```
uv pip compile pins.txt --python-version <base image python> --python-platform x86_64-unknown-linux-gnu
```

A freeze can be unbuildable because the install itself is inconsistent: `comfy node install` can leave an environment that already fails `pip check`. Run it. A conflict there is a conflict about to be shipped.

## What `validate` proves, and what it does not

`comfy distribution validate <id>` is free, and worth running before every cut after the first. It checks the definition's **shape**, that a ComfyUI version is pinned, and that each pinned pip package and version **exists**. It does not resolve the set together, so it returns `ok: true` on definitions that die at assemble.

Two ways to read it wrong:

- **`ok: true` is not "it will build".** The local resolve above is the primary check; `validate` is a second net.
- **The CLI prints "Definition resolves." and then the JSON.** Read the JSON. `warnings[]` carries definite ref misses — an unresolvable `baseComfyVersion` or node ref appears there while `ok` stays `true`.

## What the website sets that this path does not

A distribution created through the website's wizard always carries the fields below. A definition authored here carries only what is put in it, and **nothing errors when a policy is missing — the version simply seals as allow-all.** Set each one, or say its default out loud before creating.

| Field | The wizard's rule | Here |
| --- | --- | --- |
| `baseComfyVersion` | Refuses to create without one; never defaults to a branch. | Required for a cut too. Set the `v`-prefixed tag. |
| `baseImage` | Always written; the catalog's default when unpicked. | Omitted means whatever the catalog defaults to at cut time, which moves. Set it from `comfy distribution base-images`. |
| `modelPolicy` | Always written. Allow-all is a blocklist naming nothing. | Absent means allow-all, sealed into the version's manifest. |
| `partnerNodePolicy` | Always written, same encoding. | Absent means every partner node is permitted. |
| `customNodePolicy` | Always written. | The website records it; no service reads it today. Do not describe it to the user as an enforced restriction. |
| name | Defaults to "New Build". | `--name` defaults to `untitled-distribution`. Ask. |

Both real policies share one shape: `{"mode": "blocklist", "list": []}` permits everything, and `{"mode": "allowlist", "list": [...]}` permits only what it names.

## Before creating, say this

The cut happens inside `--execute` and is not revisable — a fix is always a new version. So state it in one short block, then create:

- **What is going in:** the ComfyUI pin, the base image with the Python and CUDA it brings, how many packs and how each is sourced, how many models and whether they upload or download.
- **What is permitted:** the model, partner-node and custom-node postures in plain words, including the ones defaulting to allow-all.
- **What it costs:** the default cut builds `linux/nvidia` only. A green build takes roughly ten minutes, a dependency failure usually surfaces in one or two, and the build sandbox is cut off after two hours.
- **That it is one-way:** every correction is a new cut.

## Reading the verdict

`comfy distribution version get` reports `artifactCounts` and, on a failed artifact, a `failureReason`; `comfy distribution version logs` gives that target's log. Three failures only a build surfaces, each pointing back at a rule above:

| What the failure says | What it means |
| --- | --- |
| `freeze: pin ComfyUI "...": ref not found in remote advertisement` | The ComfyUI pin is not a real git ref. Prefix the tag. |
| `assemble: ComfyUI did not start` | Something was installed against a torch the runtime does not have — usually one torch-stack member pinned while the other two were released. |
| `no version of ... your requirements are unsatisfiable` | A pin PyPI cannot serve, usually a local version tag. |

## For maintainers

The design and the features that fill this file are in
[Local agent access to the builder via comfy-cli skills](https://app.notion.com/p/3c26d73d365081ef9322ca2978e49d3d).

`comfy skills install` fetches this file from `main` and writes it beside the
skills comfy-cli bundles, so a merge here reaches users on their next install
without waiting on a CLI release.
The directory name and the `name:` above must stay identical — comfy-cli's
installer rejects a mismatch, and it rejects it on the user's machine, not here.
