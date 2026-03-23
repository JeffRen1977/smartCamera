#!/usr/bin/env python3
"""
Resize calibration images to 640×640 (letterbox) for SNPE quantization.
Uses same logic as inference preprocessing; preserves aspect ratio.

Usage:
  python resize_calib_images.py [--input DIR] [--output DIR] [--size 640] [--dry-run]
  # Default: input=snpe_quant_workspace/calib, output=snpe_quant_workspace/calib_640
"""

import argparse
import sys
from pathlib import Path

# Add detection module for yolov8_utils
_DETECTION_DIR = Path(__file__).resolve().parents[3] / "02_algorithms" / "detection"
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(_DETECTION_DIR) not in sys.path:
    sys.path.insert(0, str(_DETECTION_DIR))

from yolov8_utils import letterbox


def main():
    ap = argparse.ArgumentParser(description="Resize calib images to 640×640 (letterbox)")
    ap.add_argument("--input", "-i", type=Path, default=_PROJECT_ROOT / "snpe_quant_workspace/calib",
                    help="Input directory with source images")
    ap.add_argument("--output", "-o", type=Path, default=_PROJECT_ROOT / "snpe_quant_workspace/calib_640",
                    help="Output directory for 640×640 images")
    ap.add_argument("--size", "-s", type=int, default=640, help="Target size (default 640)")
    ap.add_argument("--dry-run", action="store_true", help="Only list files, do not resize")
    args = ap.parse_args()

    try:
        import numpy as np
        import cv2
    except ImportError as e:
        print("Error: need opencv-python and numpy. pip install opencv-python numpy", file=sys.stderr)
        sys.exit(1)

    exts = {".jpg", ".jpeg", ".png", ".bmp"}
    files = sorted([f for f in args.input.iterdir() if f.suffix.lower() in exts])
    if not files:
        print(f"No images found in {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"Would resize {len(files)} images: {args.input} -> {args.output}")
        for f in files[:5]:
            print(f"  {f.name}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
        return

    args.output.mkdir(parents=True, exist_ok=True)
    for i, fp in enumerate(files):
        img = cv2.imread(str(fp))
        if img is None:
            print(f"Skip (unreadable): {fp.name}", file=sys.stderr)
            continue
        lb = letterbox(img, (args.size, args.size))
        out_path = args.output / fp.name
        cv2.imwrite(str(out_path), lb.img)
        if (i + 1) % 50 == 0 or i == 0:
            print(f"Resized {i + 1}/{len(files)}: {fp.name} -> {out_path}")

    # Write calibration_images.txt
    out_list = args.output.parent / "calibration_images.txt"
    rel = args.output.parent
    with open(out_list, "w") as f:
        for fp in args.output.iterdir():
            if fp.suffix.lower() in exts:
                # Use path relative to workspace (for Docker: /workspace/calib_640/img001.jpg)
                p = fp.relative_to(rel)
                f.write(f"{p}\n")
    print(f"Wrote {out_list} ({len(list(args.output.iterdir()))} entries)")


if __name__ == "__main__":
    main()
