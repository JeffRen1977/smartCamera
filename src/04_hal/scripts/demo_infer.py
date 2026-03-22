#!/usr/bin/env python3
"""Demo: Unified Perception API usage."""

import sys
from pathlib import Path

# Add 04_hal to path so "from hal import ..." works
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import numpy as np
from hal import PerceptionAPI


def main() -> None:
    # Auto-detect backend, or use mock when SNPE/TensorRT unavailable
    api = PerceptionAPI(backend=None)

    # Create dummy image (640x640 RGB)
    image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)

    result = api.infer(image, model_id="yolov8n_defect")
    print("Result keys:", result.keys())
    print("Detections:", result.get("detections", []))
    print("Metadata:", result.get("metadata", {}))
    print("Backend used:", result.get("metadata", {}).get("backend", "?"))


if __name__ == "__main__":
    main()
