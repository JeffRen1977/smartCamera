"""Unit tests for api/perception_api.py."""

import pytest
from api.perception_api import PerceptionAPI, _image_to_ndarray


def _fake_image(shape=(640, 640, 3)):
    """Array-like with .shape (avoids numpy import on problematic environments)."""
    class FakeArr:
        pass
    arr = FakeArr()
    arr.shape = shape
    return arr


class TestPerceptionAPIInit:
    """Tests for PerceptionAPI initialization."""

    def test_init_with_mock_backend(self) -> None:
        api = PerceptionAPI(backend="mock")
        assert api._backend_name == "mock"

    def test_init_uses_available_backend(self) -> None:
        api = PerceptionAPI(backend=None, fallback_to_mock=True)
        assert api._backend_name in ("mock", "snpe", "tensorrt")


class TestPerceptionAPIInfer:
    """Tests for PerceptionAPI.infer()."""

    def test_infer_with_ndarray(self) -> None:
        api = PerceptionAPI(backend="mock")
        image = _fake_image((640, 640, 3))
        result = api.infer(image, "yolov8n_defect")

        assert "detections" in result
        assert "metadata" in result
        assert result["metadata"]["model_id"] == "yolov8n_defect"
        assert result["metadata"]["backend"] == "mock"
        assert result["metadata"]["image_shape"] == [640, 640, 3]

    def test_infer_invalid_input_returns_error(self) -> None:
        api = PerceptionAPI(backend="mock")
        result = api.infer("not_an_image", "m")  # type: ignore

        assert result["metadata"]["error_code"] == "INVALID_INPUT"
        assert "detections" in result


class TestPerceptionAPIInferAsync:
    """Tests for PerceptionAPI.infer_async()."""

    def test_infer_async_calls_callback(self) -> None:
        import time

        api = PerceptionAPI(backend="mock")
        image = _fake_image((100, 100, 3))
        results: list = []

        def callback(res: dict) -> None:
            results.append(res)

        api.infer_async(image, "m", callback)
        time.sleep(0.5)  # Allow async task to complete

        assert len(results) == 1
        assert results[0]["metadata"]["model_id"] == "m"


class TestPerceptionAPIIO:
    """Tests for set_io and get_image_source."""

    def test_set_io(self) -> None:
        api = PerceptionAPI(backend="mock")
        api.set_io(1, True)
        assert api._io_state[1] is True
        api.set_io(2, 0)
        assert api._io_state[2] is False

    def test_get_image_source(self) -> None:
        api = PerceptionAPI(backend="mock")
        src = api.get_image_source("0")
        assert src is None
        assert "0" in api._image_sources


class TestPerceptionAPIModelResolution:
    """Tests for model path resolution."""

    def test_model_map_override(self) -> None:
        api = PerceptionAPI(backend="mock", model_map={"m1": "/path/to/model.dlc"})
        assert api._resolve_model_path("m1") == "/path/to/model.dlc"

    def test_fallback_to_model_id_when_no_dir(self) -> None:
        api = PerceptionAPI(backend="mock")
        assert api._resolve_model_path("yolov8n") == "yolov8n"


class TestImageToNdarray:
    """Tests for _image_to_ndarray helper."""

    def test_ndarray_like_passthrough(self) -> None:
        """Object with .shape is passed through as-is."""
        arr = _fake_image((10, 20, 3))
        out = _image_to_ndarray(arr)
        assert out is arr
        assert out.shape == (10, 20, 3)

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(ValueError, match="must be np.ndarray or bytes"):
            _image_to_ndarray([1, 2, 3])  # type: ignore
