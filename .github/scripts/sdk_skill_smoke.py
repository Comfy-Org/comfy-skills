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

# CommonMark fenced blocks: an opener of 3+ backticks or tildes (up to three
# spaces in), closed only by the same character at least as long, with nothing
# but whitespace after it.
OPEN = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")


def fences(text: str) -> list[tuple[str, str]]:
    blocks, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = OPEN.match(lines[i])
        # A backtick fence's info string may not itself contain a backtick.
        if m is None or (m[2][0] == "`" and "`" in m[3]):
            i += 1
            continue
        indent, fence, lang = len(m[1]), m[2], (m[3].split() or [""])[0]
        close = re.compile(rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        body, i = [], i + 1
        while i < len(lines) and not close.match(lines[i]):
            line = lines[i]
            body.append(line[min(indent, len(line) - len(line.lstrip(" "))) :])
            i += 1
        if i == len(lines):
            raise SystemExit(f"unclosed {fence} fence ({lang or 'no info string'})")
        i += 1
        if lang in ("python", "ts"):
            blocks.append((lang, "\n".join(body) + "\n"))
    return blocks


def fill(code: str) -> str:
    code = code.replace("<provider>/<model>", "dummy/model")
    return re.sub(r"\{<[^>]*>\}", "{}", code)


def main() -> int:
    skill, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    blocks = fences(skill.read_text())
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
