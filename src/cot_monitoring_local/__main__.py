"""Run only the inert constructed-fixture selfcheck."""

import argparse
import json
from pathlib import Path

from .simulator import run_selfcheck


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, choices=(4, 8), default=4)
    parser.add_argument(
        "--output", type=Path,
        help="Optionally create this JSON summary file; existing files are not replaced.",
    )
    args = parser.parse_args(argv)
    summary = run_selfcheck(args.count)
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
