"""
YOLOv8 preprocess & postprocess per 技术执行清单_实施细节.md §2.3.

- Preprocess: letterbox, normalize, channel order (RGB/BGR)
- Postprocess: decode (1,84,8400) -> boxes+classes+scores, NMS
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass

# Numpy imported lazily in functions (avoids macOS segfault on some environments)
_HAS_NUMPY: bool | None = None


def _check_numpy() -> bool:
    global _HAS_NUMPY
    if _HAS_NUMPY is None:
        try:
            import numpy as np  # noqa: F401
            _HAS_NUMPY = True
        except Exception:
            _HAS_NUMPY = False
    return _HAS_NUMPY

# COCO 80 class names (default YOLOv8)
COCO_NAMES = (
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
)


@dataclass
class LetterboxResult:
    """Result of letterbox resize."""

    img: Any  # ndarray (H,W,3)
    scale: float
    pad: tuple[int, int]  # (pad_w, pad_h)
    orig_shape: tuple[int, int]
    new_shape: tuple[int, int]


def letterbox(
    img: Any,
    new_shape: tuple[int, int] = (640, 640),
    color: int = 114,
) -> LetterboxResult:
    """
    Resize image with aspect ratio, pad to new_shape.
    Returns resized image and scale/pad for coordinate mapping.
    """
    if not _check_numpy():
        raise RuntimeError("numpy required for letterbox")
    import numpy as np
    h, w = img.shape[:2]
    h_new, w_new = new_shape
    r = min(h_new / h, w_new / w)
    h_res, w_res = int(h * r), int(w * r)
    img_res = np.array(img)
    try:
        import cv2
        img_res = cv2.resize(img_res, (w_res, h_res), interpolation=cv2.INTER_LINEAR)
    except ImportError:
        from PIL import Image
        pil = Image.fromarray(img_res)
        pil = pil.resize((w_res, h_res), getattr(Image, "LANCZOS", Image.BILINEAR))
        img_res = np.array(pil)
    dh, dw = h_new - h_res, w_new - w_res
    pad_w, pad_h = dw // 2, dh // 2
    canvas = np.full((h_new, w_new, img.shape[2]), color, dtype=img.dtype)
    canvas[pad_h : pad_h + h_res, pad_w : pad_w + w_res] = img_res
    return LetterboxResult(
        img=canvas,
        scale=r,
        pad=(pad_w, pad_h),
        orig_shape=(h, w),
        new_shape=new_shape,
    )


def preprocess(
    img: Any,
    imgsz: int = 640,
    normalize: bool = True,
    channel_first: bool = True,
    bgr: bool = True,
) -> tuple[Any, LetterboxResult | None]:
    """
    Preprocess image for YOLOv8 inference.

    Args:
        img: (H,W,3) uint8
        imgsz: target size
        normalize: divide by 255
        channel_first: return (1,3,H,W) for model input
        bgr: input is BGR (OpenCV default)

    Returns:
        (tensor, letterbox_result) - tensor for model, letterbox for coordinate mapping
    """
    if not _check_numpy():
        raise RuntimeError("numpy required for preprocess")
    import numpy as np
    lb = letterbox(img, (imgsz, imgsz))
    x = lb.img.astype(np.float32)
    if normalize:
        x = x / 255.0
    if channel_first:
        x = x.transpose(2, 0, 1)  # HWC -> CHW
        x = np.expand_dims(x, axis=0)  # CHW -> NCHW
    return x, lb


def yolov8_decode(
    output: Any,
    conf_thres: float = 0.25,
    iou_thres: float = 0.45,
    nc: int = 80,
    class_names: tuple[str, ...] = COCO_NAMES,
) -> list[dict[str, Any]]:
    """
    Decode YOLOv8 ONNX output (1,84,8400) and apply NMS.

    Output format: list of {class_id, class_name, confidence, bbox: [x1,y1,x2,y2]}
    """
    if not _check_numpy():
        raise RuntimeError("numpy required for decode")
    import numpy as np
    # output: (1, 84, 8400) - 4 xywh + 80 class scores
    if output.ndim == 3:
        output = output[0]  # (84, 8400)
    # Transpose to (8400, 84)
    pred = output.T
    boxes = pred[:, :4]   # x_center, y_center, w, h
    scores = pred[:, 4:]  # (8400, 80)
    class_ids = np.argmax(scores, axis=1)
    confs = np.max(scores, axis=1)
    mask = confs >= conf_thres
    boxes = boxes[mask]
    class_ids = class_ids[mask]
    confs = confs[mask]
    # xywh -> xyxy
    x1 = boxes[:, 0] - boxes[:, 2] / 2
    y1 = boxes[:, 1] - boxes[:, 3] / 2
    x2 = boxes[:, 0] + boxes[:, 2] / 2
    y2 = boxes[:, 1] + boxes[:, 3] / 2
    boxes_xyxy = np.stack([x1, y1, x2, y2], axis=1)
    # NMS
    keep = _nms(boxes_xyxy, confs, iou_thres)
    result = []
    for i in keep:
        cid = int(class_ids[i])
        result.append({
            "class_id": cid,
            "class_name": class_names[cid] if cid < len(class_names) else str(cid),
            "confidence": float(confs[i]),
            "bbox": boxes_xyxy[i].tolist(),
        })
    return result


def _nms(boxes: Any, scores: Any, iou_threshold: float) -> list[int]:
    """Non-maximum suppression (numpy-only)."""
    if not _check_numpy():
        raise RuntimeError("numpy required for NMS")
    import numpy as np
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = np.argsort(-scores)
    keep = []
    while len(order) > 0:
        i = order[0]
        keep.append(int(i))
        if len(order) == 1:
            break
        order = order[1:]
        xx1 = np.maximum(x1[i], x1[order])
        yy1 = np.maximum(y1[i], y1[order])
        xx2 = np.minimum(x2[i], x2[order])
        yy2 = np.minimum(y2[i], y2[order])
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        iou = inter / (areas[i] + areas[order] - inter)
        order = order[iou <= iou_threshold]
    return keep


def scale_coords(
    coords: list[float],
    lb: LetterboxResult,
) -> list[float]:
    """Map coordinates from model space back to original image."""
    if not _check_numpy():
        return coords
    import numpy as np
    x1, y1, x2, y2 = coords
    pad_w, pad_h = lb.pad
    s = lb.scale
    h_orig, w_orig = lb.orig_shape
    x1 = (x1 - pad_w) / s
    y1 = (y1 - pad_h) / s
    x2 = (x2 - pad_w) / s
    y2 = (y2 - pad_h) / s
    x1 = max(0, min(x1, w_orig))
    y1 = max(0, min(y1, h_orig))
    x2 = max(0, min(x2, w_orig))
    y2 = max(0, min(y2, h_orig))
    return [x1, y1, x2, y2]
