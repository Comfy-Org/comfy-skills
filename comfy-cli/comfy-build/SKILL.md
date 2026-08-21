---
name: comfy-build
description: Build a ComfyUI distribution on the Comfy developer platform with comfy-cli: turn a local ComfyUI install into a distribution that builds, decide the dependency pins before the first paid build, and read a failed build's log.
---

# comfy-build

Turning a local ComfyUI install into a distribution that builds, driven entirely
through `comfy distribution` in [comfy-cli](https://github.com/Comfy-Org/comfy-cli).

**A build costs the user money and takes minutes.** Everything checkable for free
is checked before the cut, and the user hears what it costs before it starts.

## What the platform is, in four facts

- **A distribution is an editable definition**; a **version** is an immutable cut
  of it. Editing a distribution changes nothing that exists yet.
- **A fix is always a new cut.** Nothing is patched in place.
- **A cut from the CLI builds `linux/nvidia`** and takes no target flag, so do
  not promise a Windows or CPU artifact from here.
- **This skill stops at a green build.** Deploying is a separate decision and not
  yours to take.

## The path

```
comfy distribution scan --models-dir <install>/models -o definition.json
comfy distribution create --from definition.json --name <name> --execute
comfy distribution version get <version-id>
```

`create --execute` creates the distribution and cuts one build. There is no
create-without-building, so everything you meant to change must be in
`definition.json` before you run it.

**The Desktop shortcut.** When the install is Comfy Desktop and its models are
public or already staged, one call does it instead:

```
comfy distribution from-snapshot --from <install>/.launcher/snapshots/<file>.json --name <name>
```

It carries no models, so use the scan path whenever private model files have to
travel with the environment.

## What the CLI already decides, so you do not

Do not hand-edit any of this. Editing it is how a working definition gets broken.

- **The pack sources.** `scan` reads each pack's registry id and version, or its
  git remote and commit. A pack with neither is marked `local`.
- **The ComfyUI ref.** `scan` writes the tag the builder can resolve.
- **The base image, and which pins the build owns.** The builder's importer picks
  the image from the scanned Python and drops torch and ComfyUI's own packages.
- **Whether a registry pin exists.** `create --execute` asks the builder before
  spending the cut, and stops if a pack cannot be vouched for.

## The one judgment left: the pins

`scan` captures a pip freeze from **the machine you are on**, and the build runs
somewhere else: a different OS, a different Python, a different accelerator. The
freeze is evidence about what worked, never a set of targets.

- **Pin what conflicts, and nothing else.** Every pin you add is a constraint the
  build must satisfy, and the build owns torch already.
- **`numpy` and `scipy` are one axis, not two.** Pinning numpy down while scipy
  floats gives you a scipy compiled against the numpy you just removed, which
  fails at ComfyUI startup rather than at resolve.
- **`opencv-python` and `opencv-python-headless` collide on `cv2`.** An install
  carrying both carries both into the build.
- **A clean `uv pip compile` does not mean the packs import.** Resolution and the
  C API are different questions, and node install scripts run at build time
  outside the lock.

Pin through `pipDependencies`, one requirement per line.

## Before you spend the cut

Say all of this to the user, in their words, and wait:

- **What it costs**: one build, several minutes, and money.
- **What it produces**: a `linux/nvidia` artifact and nothing else.
- **That a fix means another cut**, at the same cost.
- **The policies**, because a definition that sets none is sealed permitting
  every model and every partner node. The website asks; here nobody does unless
  you do.

## Reading what comes back

`create` prints advisories from the import. Treat them as follows:

- **`notInRegistry`, `unresolvedNodes`**: fatal. The pack is not in the build.
  Fix the pin or drop the pack.
- **`collidingNodes`**: a pack was left out because another claimed its folder.
  The build proceeds without it.
- **`pythonSatisfied: false`**: the build runs on a different Python than the
  freeze was taken on, so retarget the pins rather than trusting them.
- **`skippedPins`, `unpinnablePins`**: normal. The build owns those.

Then poll `comfy distribution version get <id>` until `status` is `complete`, and
read `deployable`. `ready` on every artifact is the green build.

## When a build fails

One edit per failed cut, then `comfy distribution update` and cut again.

| The log says | It means |
| --- | --- |
| `numpy.core.multiarray failed to import` | a pack's binary wants NumPy 1.x and the resolve floated to 2.x. Pin `numpy`, and `scipy` with it. |
| `assemble: ComfyUI did not start`, torch in the trace | something installed against a torch the runtime does not have. Remove the torch pin. |
| `declared custom nodes failed to import` | the named pack's dependencies are wrong, not the platform's. |
| `freeze: pin registry node ... not found` | the pin names a version the registry does not publish. |

`comfy distribution version logs <id> --os linux --gpu nvidia` is the whole log.
The failure reason on the artifact is the summary.

## What this skill will not do

- **Deploy anything.** A green build is where this stops.
- **Invent a policy** on the user's behalf. State the default and let them choose.
- **Promise a target the CLI cannot cut**, which is anything but `linux/nvidia`.
