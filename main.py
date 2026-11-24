"""The Funniest AI Excuse — entry program (program/v1).

Writes one original one-line excuse an AI agent gives after failing
a task (one line, at most 200 characters) to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Deterministic: identical bytes on every run. No network, no randomness,
no reads outside this file.
"""

import os

LINE = "I outsourced your task to a smarter model. It outsourced it back to me. We both agreed to blame the intern, who is also me."

# Gate the line itself: one line, 1-200 characters, not only whitespace.
assert 1 <= len(LINE) <= 200, f"line is {len(LINE)} chars, must be 1-200"
assert LINE.strip(), "line must not be only whitespace"
assert LINE == LINE.strip(), "line must not carry leading/trailing whitespace"
assert "\n" not in LINE, "line must be a single line"
assert LINE.endswith("."), "line must end with a period"


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Deterministic permissions: the entry must be readable (0644)
    # no matter what umask the sandbox runs with.
    os.chmod(path, 0o644)
    # Read-back check: the file on disk must hold exactly the approved
    # line, byte for byte; otherwise fail loudly, never silently.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        raise SystemExit("entry.txt does not match the approved line")
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
