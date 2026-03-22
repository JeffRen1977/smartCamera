"""Unit tests for adapters (base, mock, snpe, tensorrt)."""

import pytest
from adapters.base import BaseAdapter
from adapters.mock import MockAdapter
from adapters.snpe import SNPEAdapter
from adapters.tensorrt import TensorRTAdapter


def _fake_image(shape=(64, 64, 3)):
    """Create array-like with .shape (avoids numpy import which can segfault on some macOS)."""
    class FakeArr:
        pass
    arr = FakeArr()
    arr.shape = shape
    return arr


class TestMockAdapter:
    """Tests for MockAdapter."""

    def test_is_available(self) -> None:
        adapter = MockAdapter()
        assert adapter.is_available() is True

    def test_backend_name(self) -> None:
        adapter = MockAdapter()
        assert adapter.backend_name == "mock"

    def test_load_model(self) -> None:
        adapter = MockAdapter()
        adapter.load_model("yolov8n", "/fake/path")
        assert "yolov8n" in adapter._models

    def test_infer_returns_valid_structure(self) -> None:
        adapter = MockAdapter()
        adapter.load_model("m", "/p")
        image = _fake_image((640, 640, 3))
        result = adapter.infer(image, "m")

        assert "detections" in result
        assert "metadata" in result
        assert isinstance(result["detections"], list)
        assert result["metadata"]["model_id"] == "m"
        assert result["metadata"]["backend"] == "mock"
        assert result["metadata"]["image_shape"] == [640, 640, 3]
        assert "inference_time_ms" in result["metadata"]

    def test_get_supported_formats(self) -> None:
        adapter = MockAdapter()
        assert adapter.get_supported_formats() == ["mock"]


class TestSNPEAdapter:
    """Tests for SNPEAdapter (SDK usually not installed)."""

    def test_backend_name(self) -> None:
        adapter = SNPEAdapter()
        assert adapter.backend_name == "snpe"

    def test_is_available_or_not(self) -> None:
        adapter = SNPEAdapter()
        # May be True if SNPE installed, False otherwise
        assert isinstance(adapter.is_available(), bool)

    def test_infer_without_sdk_returns_error_structure(self) -> None:
        adapter = SNPEAdapter()
        image = _fake_image()
        result = adapter.infer(image, "test")

        assert "detections" in result
        assert "metadata" in result
        assert result["metadata"]["backend"] == "snpe"
        # When SDK not available, should have error_code
        if not adapter.is_available():
            assert result["metadata"].get("error_code") == "BACKEND_UNAVAILABLE"

    def test_get_supported_formats(self) -> None:
        adapter = SNPEAdapter()
        assert "dlc" in adapter.get_supported_formats()


class TestTensorRTAdapter:
    """Tests for TensorRTAdapter (SDK usually not installed)."""

    def test_backend_name(self) -> None:
        adapter = TensorRTAdapter()
        assert adapter.backend_name == "tensorrt"

    def test_is_available_or_not(self) -> None:
        adapter = TensorRTAdapter()
        assert isinstance(adapter.is_available(), bool)

    def test_infer_without_sdk_returns_error_structure(self) -> None:
        adapter = TensorRTAdapter()
        image = _fake_image()
        result = adapter.infer(image, "test")

        assert "detections" in result
        assert "metadata" in result
        assert result["metadata"]["backend"] == "tensorrt"
        if not adapter.is_available():
            assert result["metadata"].get("error_code") == "BACKEND_UNAVAILABLE"

    def test_get_supported_formats(self) -> None:
        adapter = TensorRTAdapter()
        formats = adapter.get_supported_formats()
        assert "engine" in formats or "onnx" in formats
