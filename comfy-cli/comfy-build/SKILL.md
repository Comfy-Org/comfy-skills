---
name: comfy-build
description: Build a ComfyUI distribution on the Comfy developer platform with comfy-cli — turn a local ComfyUI install, a workflow file, or a described intent into a distribution that builds, pin its dependencies before the first paid build, and read a failed build's log. Scaffold only; the guidance is not written yet.
---

# comfy-build

Turning a starting point into a ComfyUI distribution that builds, driven entirely
through `comfy distribution` in [comfy-cli](https://github.com/Comfy-Org/comfy-cli).

## This skill is a scaffold

**It carries no guidance yet.** The file exists so the installer has something to
deliver and so a later revision reaches users without a CLI release. Everything
below is what will fill it, not what it says today.

**Until it is filled, do not improvise a build.** Read `comfy distribution --help`
and the per-command `--help` for the real command surface, tell the user this
skill is still a stub, and do not guess at a definition — cutting a version
starts a build that costs the user money.

## What will fill it

- **The path**: the command sequence from each of the three starting points — a
  local install, a workflow file, a described intent — and when to leave it.
- **Platform facts an agent cannot infer**: what a distribution is, that a
  version is immutable so a fix is always a new cut, and what a build costs in
  time so the user hears expectations before paying.
- **The pinning method**: how to anticipate a dependency conflict across
  ComfyUI, every custom node and torch, before the first paid build.
- **The limits of the free checks**: `validate` proves existence, not
  resolution, so a passing validate is not a safe build.
- **Failure reading**: how to map a failed target's build log to one definition
  edit, one revision per failed cut.
- **The restated guardrails**: what the platform website enforces at creation
  time, restated so the CLI path refuses what the website would refuse.

## For maintainers

The design and the features that fill this file are in
[Local agent access to the builder via comfy-cli skills](https://app.notion.com/p/3c26d73d365081ef9322ca2978e49d3d).

`comfy skills install` fetches this file from `main` and writes it beside the
skills comfy-cli bundles, so a merge here reaches users on their next install
without waiting on a CLI release.
The directory name and the `name:` above must stay identical — comfy-cli's
installer rejects a mismatch, and it rejects it on the user's machine, not here.
