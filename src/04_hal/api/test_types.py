"""Unit tests for api/types.py."""

import pytest
from api.types import (
    ErrorCode,
    Detection,
    InferenceMetadata,
    InferenceResult,
)


class TestErrorCode:
    """Tests for ErrorCode enum."""

    def test_error_codes_defined(self) -> None:
        assert ErrorCode.OK == "OK"
        assert ErrorCode.MODEL_NOT_LOADED == "MODEL_NOT_LOADED"
        assert ErrorCode.INVALID_INPUT == "INVALID_INPUT"
        assert ErrorCode.INFERENCE_FAILED == "INFERENCE_FAILED"
        assert ErrorCode.BACKEND_UNAVAILABLE == "BACKEND_UNAVAILABLE"

    def test_error_code_value(self) -> None:
        assert ErrorCode.OK.value == "OK"
        assert ErrorCode.MODEL_NOT_LOADED.value == "MODEL_NOT_LOADED"


class TestDetection:
    """Tests for Detection dataclass."""

    def test_detection_creation(self) -> None:
        d = Detection(
            class_id=0,
            class_name="hard_hat",
            confidence=0.92,
            bbox=(10.0, 20.0, 100.0, 150.0),
        )
        assert d.class_id == 0
        assert d.class_name == "hard_hat"
        assert d.confidence == 0.92
        assert d.bbox == (10.0, 20.0, 100.0, 150.0)
        assert d.extra == {}

    def test_detection_with_extra(self) -> None:
        d = Detection(
            class_id=1,
            class_name="person",
            confidence=0.85,
            bbox=(0, 0, 50, 80),
            extra={"track_id": 42},
        )
        assert d.extra["track_id"] == 42


class TestInferenceMetadata:
    """Tests for InferenceMetadata dataclass."""

    def test_metadata_creation(self) -> None:
        m = InferenceMetadata(
            inference_time_ms=12.5,
            model_id="yolov8n_defect",
            backend="snpe",
            image_shape=(640, 640, 3),
        )
        assert m.inference_time_ms == 12.5
        assert m.model_id == "yolov8n_defect"
        assert m.backend == "snpe"
        assert m.image_shape == (640, 640, 3)
        assert m.error_code == ErrorCode.OK
        assert m.error_message is None

    def test_metadata_with_error(self) -> None:
        m = InferenceMetadata(
            inference_time_ms=0.0,
            model_id="x",
            backend="snpe",
            image_shape=(0, 0, 0),
            error_code=ErrorCode.MODEL_NOT_LOADED,
            error_message="File not found",
        )
        assert m.error_code == ErrorCode.MODEL_NOT_LOADED
        assert m.error_message == "File not found"


class TestInferenceResult:
    """Tests for InferenceResult dataclass."""

    def test_to_dict_empty_detections(self) -> None:
        result = InferenceResult(
            detections=[],
            metadata=InferenceMetadata(
                inference_time_ms=10.0,
                model_id="yolov8n",
                backend="mock",
                image_shape=(640, 640, 3),
            ),
        )
        d = result.to_dict()
        assert d["detections"] == []
        assert d["metadata"]["inference_time_ms"] == 10.0
        assert d["metadata"]["model_id"] == "yolov8n"
        assert d["metadata"]["backend"] == "mock"
        assert d["metadata"]["image_shape"] == [640, 640, 3]
        assert d["metadata"]["error_code"] == "OK"

    def test_to_dict_with_detections(self) -> None:
        result = InferenceResult(
            detections=[
                Detection(
                    class_id=0,
                    class_name="hard_hat",
                    confidence=0.92,
                    bbox=(1, 2, 3, 4),
                    extra={"key": "value"},
                ),
            ],
            metadata=InferenceMetadata(
                inference_time_ms=5.0,
                model_id="m",
                backend="snpe",
                image_shape=(320, 320, 3),
            ),
        )
        d = result.to_dict()
        assert len(d["detections"]) == 1
        det = d["detections"][0]
        assert det["class_id"] == 0
        assert det["class_name"] == "hard_hat"
        assert det["confidence"] == 0.92
        assert det["bbox"] == [1, 2, 3, 4]
        assert det["extra"] == {"key": "value"}
