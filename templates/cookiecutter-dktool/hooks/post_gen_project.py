from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# After generation, suggest adding the tool to requirements-all.txt
print("\nNext steps:")
print("  - Add '-e tools/{{cookiecutter.tool_slug}}' to requirements-all.txt")
print("  - pip install -e tools/{{cookiecutter.tool_slug}}")
