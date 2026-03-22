"""Detection algorithms: YOLOv8, etc."""

from .yolov8_utils import (
    preprocess,
    yolov8_decode,
    letterbox,
    LetterboxResult,
    scale_coords,
    COCO_NAMES,
)

__all__ = [
    "preprocess",
    "yolov8_decode",
    "letterbox",
    "LetterboxResult",
    "scale_coords",
    "COCO_NAMES",
]
