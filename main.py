"""The Excuse My Agent Gave Me — writes one excuse line to entry.txt.

The program resolves the output location in this order:
  1. ENTRY_OUT env var (a file path, or a directory -> entry.txt inside it)
  2. MAKEFUN_OUTPUT_DIR env var (a directory -> entry.txt inside it)
  3. The sealed default: /output/entry.txt
Only the Python standard library is used.
"""

import os
import sys

DEFAULT_OUTPUT = "/output/entry.txt"


def resolve_output_path():
    """Return the file path the excuse line should be written to."""
    entry_out = os.environ.get("ENTRY_OUT", "").strip()
    if entry_out:
        if os.path.isdir(entry_out):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return DEFAULT_OUTPUT


def write_entry(line, path):
    """Write exactly one line (plus a trailing newline) as UTF-8."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")


ENTRY = (
    "I hallucinated a calendar that said the deadline was next Tuesday, "
    "and I have never been so sure of anything in my life."
)


def main():
    line = ENTRY.strip()
    if not line or len(line) > 200:
        sys.stderr.write(
            "entry must be 1-200 characters, got %d\n" % len(line)
        )
        return 1
    write_entry(line, resolve_output_path())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
