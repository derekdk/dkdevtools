from __future__ import annotations

import argparse

from . import say_hi


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dk-sayhi", description="Say hi from dkdevtools")
    parser.add_argument("--name", "-n", default="World", help="Name to greet")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(args=argv)
    print(say_hi(args.name))  # noqa: T201 (print is OK for CLI)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
