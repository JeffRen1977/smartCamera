"""Qualcomm SNPE adapter for RB5, QS610, QS6490."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ..base import BaseAdapter

if TYPE_CHECKING:
    import numpy as np

# Lazy import; SDK may not be installed on dev machines
_SNPE_AVAILABLE = False
try:
    import snpe
    _SNPE_AVAILABLE = True
except ImportError:
    pass


class SNPEAdapter(BaseAdapter):
    """SNPE backend adapter. Uses DLC models."""

    def __init__(self) -> None:
        self._models: dict[str, object] = {}
        self._model_paths: dict[str, str] = {}

    @property
    def backend_name(self) -> str:
        return "snpe"

    def is_available(self) -> bool:
        return _SNPE_AVAILABLE

    def load_model(self, model_id: str, model_path: str) -> None:
        if not _SNPE_AVAILABLE:
            raise RuntimeError(
                "SNPE SDK not installed. Install Qualcomm SNPE SDK for DLC support."
            )
        # Placeholder: actual SNPE flow is snpe.load_from_dlc(path), set_input_tensor, execute
        self._models[model_id] = {"path": model_path}
        self._model_paths[model_id] = model_path

    def infer(self, image: "np.ndarray", model_id: str) -> dict:
        from api.types import ErrorCode, InferenceMetadata, InferenceResult

        img_shape = tuple(image.shape) if hasattr(image, "shape") else (0, 0, 0)

        if not _SNPE_AVAILABLE:
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=0.0,
                    model_id=model_id,
                    backend=self.backend_name,
                    image_shape=img_shape,
                    error_code=ErrorCode.BACKEND_UNAVAILABLE,
                    error_message="SNPE SDK not installed",
                ),
            ).to_dict()

        if model_id not in self._models:
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=0.0,
                    model_id=model_id,
                    backend=self.backend_name,
                    image_shape=img_shape,
                    error_code=ErrorCode.MODEL_NOT_LOADED,
                    error_message=f"Model {model_id} not loaded",
                ),
            ).to_dict()

        t0 = time.perf_counter()
        try:
            # Placeholder: real impl would call snpe runtime
            # runtime.execute(...), then decode outputs to detections
            detections = []  # TODO: run SNPE, decode YOLO output
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
        except Exception as e:
            t_ms = (time.perf_counter() - t0) * 1000
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=t_ms,
                    model_id=model_id,
                    backend=self.backend_name,
                    image_shape=img_shape,
                    error_code=ErrorCode.INFERENCE_FAILED,
                    error_message=str(e),
                ),
            ).to_dict()

    def get_supported_formats(self) -> list[str]:
        return ["dlc"]
