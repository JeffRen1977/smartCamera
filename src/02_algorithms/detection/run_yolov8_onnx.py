#!/usr/bin/env python3
"""
Run YOLOv8 ONNX inference (preprocess + ORT + postprocess).

Usage:
  python run_yolov8_onnx.py --model yolov8n.onnx --image test.jpg
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Add parent for imports when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from yolov8_utils import preprocess, yolov8_decode, scale_coords


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="ONNX model path")
    parser.add_argument("--image", required=True, help="Input image path")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--iou", type=float, default=0.45, help="NMS IoU threshold")
    args = parser.parse_args()

    import numpy as np
    try:
        import cv2
        img = cv2.imread(args.image)
    except ImportError:
        from PIL import Image
        img = np.array(Image.open(args.image).convert("RGB"))
        img = img[:, :, ::-1]  # RGB -> BGR for consistency
    if img is None:
        raise SystemExit(f"Failed to load image: {args.image}")

    x, lb = preprocess(img, imgsz=args.imgsz)
    try:
        import onnxruntime as ort
    except ImportError:
        raise SystemExit("Install onnxruntime: pip install onnxruntime")

    sess = ort.InferenceSession(
        args.model,
        providers=["CPUExecutionProvider"],
    )
    in_name = sess.get_inputs()[0].name
    output = sess.run(None, {in_name: x.astype(np.float32)})[0]

    detections = yolov8_decode(output, conf_thres=args.conf, iou_thres=args.iou)
    for d in detections:
        d["bbox"] = scale_coords(d["bbox"], lb)

    print(f"Detections: {len(detections)}")
    for i, d in enumerate(detections[:10]):
        print(f"  {i+1}. {d['class_name']} {d['confidence']:.2f} bbox={d['bbox']}")
    if len(detections) > 10:
        print(f"  ... and {len(detections)-10} more")


if __name__ == "__main__":
    main()
