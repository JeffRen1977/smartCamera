"""Mock adapter - returns dummy results when SNPE/TensorRT unavailable."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ..base import BaseAdapter

if TYPE_CHECKING:
    import numpy as np


class MockAdapter(BaseAdapter):
    """Development adapter that returns stub results without SDK."""

    def __init__(self) -> None:
        self._models: set[str] = set()

    @property
    def backend_name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return True

    def load_model(self, model_id: str, model_path: str) -> None:
        self._models.add(model_id)

    def infer(self, image: "np.ndarray", model_id: str) -> dict:
        from api.types import InferenceMetadata, InferenceResult

        t0 = time.perf_counter()
        img_shape = tuple(image.shape) if hasattr(image, "shape") else (0, 0, 0)
        t_ms = (time.perf_counter() - t0) * 1000
        return InferenceResult(
            detections=[],
            metadata=InferenceMetadata(
                inference_time_ms=t_ms,
                model_id=model_id,
                backend=self.backend_name,
                image_shape=img_shape,
            ),
        ).to_dict()

    def get_supported_formats(self) -> list[str]:
        return ["mock"]
