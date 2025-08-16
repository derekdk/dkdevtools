from __future__ import annotations

import sys
from pathlib import Path

# Add the src/ directory for this tool to the Python path so tests work without installation
_THIS_DIR = Path(__file__).resolve().parent
_SRC = (_THIS_DIR.parent / "src").resolve()
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
