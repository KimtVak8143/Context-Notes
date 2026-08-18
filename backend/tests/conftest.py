from __future__ import annotations

import importlib
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def _is_outside_backend(module_name: str) -> bool:
    module = sys.modules.get(module_name)
    module_file = getattr(module, "__file__", None)
    if not module_file:
        return False
    try:
        return not Path(module_file).resolve().is_relative_to(BACKEND_ROOT)
    except Exception:
        return False


# Ensure local backend package resolution wins in CI and avoids collisions
# with any third-party "app" modules available in the runner environment.
sys.path.insert(0, str(BACKEND_ROOT))

if _is_outside_backend("app"):
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name, None)

importlib.invalidate_caches()
