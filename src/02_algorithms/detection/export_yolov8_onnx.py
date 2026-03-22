#!/usr/bin/env python3
"""
Export YOLOv8 to ONNX per 技术执行清单_实施细节.md §2.3.

Usage:
  python export_yolov8_onnx.py [--model yolov8n.pt] [--output model.onnx] [--imgsz 640]
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export YOLOv8 to ONNX (edge-optimized)")
    parser.add_argument(
        "--model",
        default="yolov8n.pt",
        help="Model path (yolov8n.pt, yolov8s.pt, or runs/detect/train/weights/best.pt)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output ONNX path (default: {model stem}.onnx)",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Input size (default: 640)")
    parser.add_argument("--opset", type=int, default=12, help="ONNX opset (default: 12)")
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic axes")
    parser.add_argument("--no-simplify", action="store_true", help="Disable ONNX simplify")
    parser.add_argument("--half", action="store_true", help="FP16 export")
    args = parser.parse_args()

    try:
        from ultralytics import YOLO
    except ImportError:
        raise SystemExit(
            "Install dependencies: pip install ultralytics onnx onnxslim\n"
            "Or: pip install -r src/02_algorithms/detection/requirements.txt"
        )
    try:
        import onnx  # required by Ultralytics for export
    except ImportError:
        raise SystemExit(
            "Install onnx: pip install onnx \"onnx>=1.12.0,<2.0.0\" onnxslim"
        )

    model_path = Path(args.model)
    if not model_path.exists() and "/" not in args.model and "\\" not in args.model:
        # Allow Ultralytics auto-download (yolov8n.pt, yolov8s.pt, etc.)
        pass

    print(f"Exporting {args.model} (imgsz={args.imgsz}, opset={args.opset})")
    model = YOLO(args.model)
    out_path = model.export(
        format="onnx",
        imgsz=args.imgsz,
        opset=args.opset,
        simplify=not args.no_simplify,
        dynamic=args.dynamic,
        half=args.half,
    )
    out_path = Path(out_path)
    if args.output:
        dest = Path(args.output)
        if dest != out_path:
            import shutil
            shutil.copy(out_path, dest)
            out_path = dest
    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
