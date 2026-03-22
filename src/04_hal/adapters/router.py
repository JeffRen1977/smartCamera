"""Adapter router: select backend by env var or platform auto-detect."""

from __future__ import annotations

import os
from pathlib import Path


def detect_platform() -> str | None:
    """Detect hardware platform from /proc/device-tree or CPU info."""
    # Qualcomm RB5 / QCS: device-tree often has qualcomm in compatible
    dt_compatible = Path("/proc/device-tree/compatible")
    if dt_compatible.exists():
        try:
            compat = dt_compatible.read_bytes().decode("ascii", errors="ignore")
            if "qualcomm" in compat.lower():
                return "snpe"
            if "nvidia" in compat.lower() or "tegra" in compat.lower():
                return "tensorrt"
        except OSError:
            pass

    # Fallback: check for Jetson (nvidia jetson)
    nv_path = Path("/etc/nv_tegra_release")
    if nv_path.exists():
        return "tensorrt"

    # CPU info for x86 (OpenVINO)
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        try:
            text = cpuinfo.read_text()
            if "Intel" in text or "AMD" in text:
                return "openvino"
        except OSError:
            pass

    return None


def get_backend() -> str | None:
    """
    Get backend name: HAL_BACKEND env var, or platform auto-detect.
    Returns snpe|tensorrt|openvino|vitis_ai|rknn or None.
    """
    env = os.environ.get("HAL_BACKEND", "").lower().strip()
    if env in ("snpe", "tensorrt", "openvino", "vitis_ai", "rknn"):
        return env
    return detect_platform()
