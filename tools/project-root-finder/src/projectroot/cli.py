from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


DEFAULT_MARKERS = [".git", "pyproject.toml", "package.json", ".hg", ".svn"]


def find_project_root(start: Path, markers: Iterable[str] = DEFAULT_MARKERS) -> Path | None:
    start = start.resolve()
    markers_set = set(markers)
    for current in [start, *start.parents]:
        for m in markers_set:
            if (current / m).exists():
                return current
    return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="project-root-finder",
        description="Find the root directory of a project by looking for marker files/directories.",
    )
    p.add_argument(
        "--start",
        "-s",
        type=Path,
        default=Path.cwd(),
        help="Starting directory (default: current working directory)",
    )
    p.add_argument(
        "--markers",
        "-m",
        nargs="*",
        default=DEFAULT_MARKERS,
        help=f"Marker names to look for (default: {', '.join(DEFAULT_MARKERS)})",
    )
    p.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output, exit code indicates success (0) or not found (1)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(args=argv)

    root = find_project_root(args.start, args.markers)
    if root is None:
        return 1
    if not args.quiet:
        print(str(root))  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
