"""Unit tests for adapters/router.py."""

import os
import pytest
from adapters.router import get_backend, detect_platform


class TestGetBackend:
    """Tests for get_backend()."""

    def test_env_var_overrides(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HAL_BACKEND", "snpe")
        assert get_backend() == "snpe"

        monkeypatch.setenv("HAL_BACKEND", "tensorrt")
        assert get_backend() == "tensorrt"

        monkeypatch.setenv("HAL_BACKEND", "openvino")
        assert get_backend() == "openvino"

    def test_env_var_case_insensitive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HAL_BACKEND", "SNPE")
        assert get_backend() == "snpe"

        monkeypatch.setenv("HAL_BACKEND", "  TensorRT  ")
        assert get_backend() == "tensorrt"

    def test_invalid_env_falls_back_to_detect(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HAL_BACKEND", "unknown_backend")
        # detect_platform may return None on non-embedded systems
        result = get_backend()
        assert result is None or result in ("snpe", "tensorrt", "openvino")


class TestDetectPlatform:
    """Tests for detect_platform()."""

    def test_returns_none_or_valid_backend(self) -> None:
        result = detect_platform()
        assert result is None or result in ("snpe", "tensorrt", "openvino")
