"""Extract the code blocks from the comfy-sdk skill and check them offline.

Python blocks are parsed with ``ast``; TypeScript blocks are written out as
``.ts`` files for ``tsc --noEmit`` to type-check against the installed
``@comfyorg/sdk``. Placeholders (``<provider>/<model>``, ``{<...>}``) become
dummies first. Nothing here touches the network.

Usage: python sdk_skill_smoke.py <SKILL.md> <ts-out-dir>
"""

import ast
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^```(python|ts)\n(.*?)^```", re.M | re.S)


def fill(code: str) -> str:
    code = code.replace("<provider>/<model>", "dummy/model")
    return re.sub(r"\{<[^>]*>\}", "{}", code)


def main() -> int:
    skill, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    blocks = FENCE.findall(skill.read_text())
    langs = {lang for lang, _ in blocks}
    if langs != {"python", "ts"}:
        print(f"expected python and ts blocks, found {sorted(langs) or 'none'}")
        return 1
    for i, (lang, code) in enumerate(blocks):
        code = fill(code)
        if lang == "python":
            ast.parse(code, filename=f"{skill}#block{i}")
        else:
            (out / f"block{i}.ts").write_text(code)
        print(f"block {i} ({lang}): ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
