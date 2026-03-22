"""Unified data types and error codes for the Perception API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Standard error codes for adapter responses."""

    OK = "OK"
    MODEL_NOT_LOADED = "MODEL_NOT_LOADED"
    INVALID_INPUT = "INVALID_INPUT"
    INFERENCE_FAILED = "INFERENCE_FAILED"
    BACKEND_UNAVAILABLE = "BACKEND_UNAVAILABLE"


@dataclass
class Detection:
    """Single detection result."""

    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]  # (x1, y1, x2, y2)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceMetadata:
    """Metadata accompanying inference results."""

    inference_time_ms: float
    model_id: str
    backend: str
    image_shape: tuple[int, ...]
    error_code: ErrorCode = ErrorCode.OK
    error_message: str | None = None


@dataclass
class InferenceResult:
    """Unified inference result structure."""

    detections: list[Detection]
    metadata: InferenceMetadata

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "detections": [
                {
                    "class_id": d.class_id,
                    "class_name": d.class_name,
                    "confidence": d.confidence,
                    "bbox": list(d.bbox),
                    "extra": d.extra,
                }
                for d in self.detections
            ],
            "metadata": {
                "inference_time_ms": self.metadata.inference_time_ms,
                "model_id": self.metadata.model_id,
                "backend": self.metadata.backend,
                "image_shape": list(self.metadata.image_shape),
                "error_code": self.metadata.error_code.value,
                "error_message": self.metadata.error_message,
            },
        }
