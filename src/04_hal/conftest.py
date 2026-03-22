"""Pytest fixtures and path setup for HAL tests."""

import sys
from pathlib import Path

# Add 04_hal to path so api, adapters, hal can be imported
_hal_root = Path(__file__).resolve().parent
if str(_hal_root) not in sys.path:
    sys.path.insert(0, str(_hal_root))
