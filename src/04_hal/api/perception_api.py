"""Unified Perception API - single entry point for AI containers."""

from __future__ import annotations

import concurrent.futures
from pathlib import Path
from typing import Callable

from .types import ErrorCode, InferenceResult

from adapters.router import get_backend
from adapters.base import BaseAdapter
from adapters.snpe import SNPEAdapter
from adapters.tensorrt import TensorRTAdapter
from adapters.mock import MockAdapter

_ADAPTER_REGISTRY: dict[str, type[BaseAdapter]] = {
    "snpe": SNPEAdapter,
    "tensorrt": TensorRTAdapter,
    "mock": MockAdapter,
}


def _create_adapter(backend: str, fallback_to_mock: bool = True) -> BaseAdapter:
    """Create adapter by backend name. Falls back to mock if unavailable and fallback_to_mock."""
    cls = _ADAPTER_REGISTRY.get(backend)
    if cls is None:
        raise ValueError(f"Unknown backend: {backend}. Supported: {list(_ADAPTER_REGISTRY)}")
    adapter = cls()
    if not adapter.is_available():
        if fallback_to_mock and backend != "mock":
            return MockAdapter()
        raise RuntimeError(
            f"Backend '{backend}' is not available. "
            f"Install the required SDK (SNPE/TensorRT) or use backend='mock' for development."
        )
    return adapter


def _image_to_ndarray(image_raw):
    """Convert image_raw (bytes or ndarray) to np.ndarray."""
    if hasattr(image_raw, "shape"):
        return image_raw
    if isinstance(image_raw, (bytes, bytearray)):
        import numpy as np
        try:
            import cv2
            arr = np.frombuffer(image_raw, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Failed to decode image bytes")
            return img
        except ImportError:
            raise ValueError("bytes input requires opencv-python for decoding")
    raise ValueError("image_raw must be np.ndarray or bytes")


class PerceptionAPI:
    """
    Unified Perception API for AI containers.
    Call infer(image_raw, model_id) regardless of SNPE/TensorRT underneath.
    """

    def __init__(
        self,
        backend: str | None = None,
        model_dir: str | Path | None = None,
        model_map: dict[str, str] | None = None,
        fallback_to_mock: bool = True,
    ) -> None:
        """
        Args:
            backend: snpe|tensorrt|openvino. If None, use HAL_BACKEND or auto-detect.
            model_dir: Base directory for model files. model_id maps to {model_dir}/{model_id}.dlc etc.
            model_map: Explicit model_id -> path mapping. Overrides model_dir.
        """
        self._backend_name = backend or get_backend()
        if not self._backend_name:
            # Try first available
            for b in ("tensorrt", "snpe"):
                adapter_cls = _ADAPTER_REGISTRY.get(b)
                if adapter_cls and adapter_cls().is_available():
                    self._backend_name = b
                    break
            if not self._backend_name:
                self._backend_name = "tensorrt"  # Will raise in _create_adapter if unavailable
        self._adapter = _create_adapter(self._backend_name, fallback_to_mock=fallback_to_mock)
        self._model_dir = Path(model_dir) if model_dir else None
        self._model_map = model_map or {}
        self._io_state: dict[int, bool] = {}
        self._image_sources: dict[str, object] = {}
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._loaded_models: set[str] = set()

    def _resolve_model_path(self, model_id: str) -> str:
        """Resolve model_id to filesystem path."""
        if model_id in self._model_map:
            return self._model_map[model_id]
        if self._model_dir:
            for ext in self._adapter.get_supported_formats():
                path = self._model_dir / f"{model_id}.{ext}"
                if path.exists():
                    return str(path)
        # Fallback: model_id as path
        return model_id

    def load_model(self, model_id: str, model_path: str | None = None) -> None:
        """Load model. Lazy-loaded on first infer if not called explicitly."""
        path = model_path or self._resolve_model_path(model_id)
        self._adapter.load_model(model_id, path)

    def infer(self, image_raw, model_id: str) -> dict:
        """
        Synchronous inference. Block until result.

        Args:
            image_raw: np.ndarray (H,W,C) uint8 or bytes (JPEG/RAW)
            model_id: Model identifier, e.g. 'yolov8n_defect'

        Returns:
            dict with keys: detections, metadata (inference_time_ms, backend, etc.)
        """
        from .types import InferenceMetadata, InferenceResult

        try:
            image = _image_to_ndarray(image_raw)
        except Exception as e:
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=0.0,
                    model_id=model_id,
                    backend=self._backend_name,
                    image_shape=(0, 0, 0),
                    error_code=ErrorCode.INVALID_INPUT,
                    error_message=str(e),
                ),
            ).to_dict()

        try:
            if model_id not in self._loaded_models:
                self.load_model(model_id)
                self._loaded_models.add(model_id)
        except Exception as e:
            return InferenceResult(
                detections=[],
                metadata=InferenceMetadata(
                    inference_time_ms=0.0,
                    model_id=model_id,
                    backend=self._backend_name,
                    image_shape=tuple(image.shape),
                    error_code=ErrorCode.MODEL_NOT_LOADED,
                    error_message=str(e),
                ),
            ).to_dict()

        return self._adapter.infer(image, model_id)

    def infer_async(
        self,
        image_raw,
        model_id: str,
        callback: Callable[[dict], None],
    ) -> None:
        """Asynchronous inference. Calls callback with result when done."""
        def _run() -> None:
            result = self.infer(image_raw, model_id)
            callback(result)

        self._executor.submit(_run)

    def set_io(self, pin: int, value: bool | int) -> None:
        """Set GPIO output (e.g. alarm LED, buzzer). Stub for now."""
        self._io_state[pin] = bool(value)
        # TODO: platform-specific GPIO (e.g. gpiod, RPi.GPIO)

    def get_image_source(self, stream_id: str = "0"):
        """Get camera or video stream handle. Stub for now."""
        if stream_id not in self._image_sources:
            # TODO: open camera by stream_id (e.g. /dev/video0, rtsp URL)
            self._image_sources[stream_id] = None
        return self._image_sources[stream_id]
