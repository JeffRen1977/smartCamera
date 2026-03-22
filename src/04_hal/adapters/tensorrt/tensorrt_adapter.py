"""NVIDIA TensorRT adapter for Jetson Orin / Xavier."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ..base import BaseAdapter

if TYPE_CHECKING:
    import numpy as np

# Lazy import; TensorRT may not be installed on dev machines
_TRT_AVAILABLE = False
try:
    import tensorrt as trt
    _TRT_AVAILABLE = True
except ImportError:
    pass


class TensorRTAdapter(BaseAdapter):
    """TensorRT backend adapter. Uses Engine files."""

    def __init__(self) -> None:
        self._engines: dict[str, object] = {}
        self._contexts: dict[str, object] = {}
        self._model_paths: dict[str, str] = {}

    @property
    def backend_name(self) -> str:
        return "tensorrt"

    def is_available(self) -> bool:
        return _TRT_AVAILABLE

    def load_model(self, model_id: str, model_path: str) -> None:
        if not _TRT_AVAILABLE:
            raise RuntimeError(
                "TensorRT not installed. Install TensorRT for Engine support."
            )
        logger = trt.Logger(trt.Logger.WARNING)
        with open(model_path, "rb") as f:
            engine = trt.Runtime(logger).deserialize_cuda_engine(f.read())
        ctx = engine.create_execution_context()
        self._engines[model_id] = engine
        self._contexts[model_id] = ctx
        self._model_paths[model_id] = model_path

    def infer(self, image: "np.ndarray", model_id: str) -> dict:
        from api.types import ErrorCode, InferenceMetadata, InferenceResult

        img_shape = tuple(image.shape) if hasattr(image, "shape") else (0, 0, 0)

        if not _TRT_AVAILABLE:
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=0.0,
                    model_id=model_id,
                    backend=self.backend_name,
                    image_shape=img_shape,
                    error_code=ErrorCode.BACKEND_UNAVAILABLE,
                    error_message="TensorRT not installed",
                ),
            ).to_dict()

        if model_id not in self._engines:
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
            # Placeholder: real impl would copy input to GPU, execute_v2, copy output
            detections = []  # TODO: run TensorRT, decode YOLO output
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
        return ["engine", "onnx"]
