from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tools" / "_template_tool"
TOOLS_DIR = ROOT / "tools"


@dataclass
class Params:
    tool_slug: str
    package_name: str
    project_name: str
    description: str
    with_cli: bool


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def to_pkg(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if re.match(r"^[0-9]", s):
        s = f"pkg_{s}"
    return s


def scaffold(p: Params) -> Path:
    src_dir = TOOLS_DIR / p.tool_slug
    if src_dir.exists():
        raise SystemExit(f"Destination already exists: {src_dir}")

    # Copy template
    shutil.copytree(TEMPLATE, src_dir)

    # Rename package directory
    (src_dir / "src" / "template_tool").rename(src_dir / "src" / p.package_name)

    # Replace content in files (text files only)
    TEXT_EXT = {
        ".py",
        ".toml",
        ".md",
        ".txt",
        ".ini",
        ".cfg",
        ".yaml",
        ".yml",
        ".json",
    }

    def replace_in_file(fp: Path) -> None:
        if fp.suffix.lower() not in TEXT_EXT:
            return
        try:
            s = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip non-UTF8 or binary-like files
            return
        s = s.replace("template_tool", p.package_name)
        s = s.replace("template-tool", p.project_name)
        s = s.replace("Template Tool", p.project_name)
        s = s.replace("Template for dkdevtools tools. Copy and customize.", p.description)
        fp.write_text(s, encoding="utf-8")

    for fp in src_dir.rglob("*"):
        if fp.is_file():
            # Skip cache/hidden directories just in case
            parts = {part.lower() for part in fp.parts}
            if any(x in parts for x in {".git", "__pycache__", ".pytest_cache"}):
                continue
            replace_in_file(fp)

    # Optionally add CLI skeleton and entry point
    pyproject = src_dir / "pyproject.toml"
    if p.with_cli:
        cli_file = src_dir / "src" / p.package_name / "cli.py"
        cli_file.write_text(
            """
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="{prog}", description="{desc}")
    parser.add_argument("--name", "-n", default="World", help="Name to greet")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(args=argv)
    print(f"Hello, { '{' }args.name{'}' }!")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
""".strip().format(prog=p.project_name, desc=p.description),
            encoding="utf-8",
        )
        # add [project.scripts] entry
        text = pyproject.read_text(encoding="utf-8")
        if "[project.scripts]" not in text:
            text += "\n\n[project.scripts]\n"
        text += f"{p.project_name} = \"{p.package_name}.cli:main\"\n"
        pyproject.write_text(text, encoding="utf-8")

    # Update requirements-all.txt suggestion left to dev
    return src_dir


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Scaffold a new dkdevtools tool from the template")
    ap.add_argument("name", help="Human-friendly tool name, e.g. 'My New Tool'")
    ap.add_argument("--slug", help="Tool folder name, e.g. 'my-new-tool'")
    ap.add_argument("--package", help="Python package name under src/, e.g. 'my_new_tool'")
    ap.add_argument("--desc", default="New dkdevtools tool", help="One-line description")
    ap.add_argument("--cli", action="store_true", help="Add a CLI skeleton and entry point")
    args = ap.parse_args()

    slug = slugify(args.slug or args.name)
    pkg = to_pkg(args.package or args.name)

    p = Params(
        tool_slug=slug,
        package_name=pkg,
        project_name=slug,  # distribution name usually matches slug
        description=args.desc,
        with_cli=bool(args.cli),
    )

    dst = scaffold(p)
    print(f"Scaffolded: {dst}")
    print("Next steps:")
    print(f"  - Add '-e tools/{p.tool_slug}' to requirements-all.txt")
    print(f"  - Run: pip install -e tools/{p.tool_slug}")
    print("  - Write tests in tests/")


if __name__ == "__main__":
    main()
