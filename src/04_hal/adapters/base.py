"""Base adapter interface for perception backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


class BaseAdapter(ABC):
    """Abstract base class for SNPE, TensorRT, OpenVINO, etc."""

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Backend identifier (e.g. 'snpe', 'tensorrt')."""
        ...

    @abstractmethod
    def load_model(self, model_id: str, model_path: str) -> None:
        """Load model from path. Called lazily on first infer."""
        ...

    @abstractmethod
    def infer(self, image: "np.ndarray", model_id: str) -> dict:
        """Run inference. Returns raw result dict (detections + metadata structure)."""
        ...

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """Return supported model formats (e.g. ['dlc'], ['engine'])."""
        ...

    def is_available(self) -> bool:
        """Check if this backend is available on the current platform."""
        return True
