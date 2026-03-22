# 4. Perception Adapter Layer (HAL)

Core of algorithm-hardware decoupling. Unified perception API upward, vendor SDK adapters downward.

## Quick Start

```python
# Add src/04_hal to PYTHONPATH
import sys
sys.path.insert(0, "/path/to/smartCamera/src/04_hal")

from hal import PerceptionAPI

api = PerceptionAPI(backend="snpe")  # or None for auto-detect, "mock" for dev
result = api.infer(image, model_id="yolov8n_defect")
# result: {"detections": [...], "metadata": {"inference_time_ms": 12, "backend": "snpe", ...}}
```

## Modules

| Directory | Function |
|-----------|----------|
| `api/` | Unified perception API (Inference / Image / I/O), e.g. `infer(image_raw, model_id)` |
| `adapters/` | Vendor SDK adapters: SNPE, TensorRT, OpenVINO, VitisAI, RKNN, mock |
| `isp/` | ISP tuning drivers for consistent image quality under complex lighting |

## Adapters

| Backend | Target | Model Format | Status |
|---------|--------|--------------|--------|
| snpe | Qualcomm RB5, QS610 | DLC | Prototype (SDK required) |
| tensorrt | NVIDIA Jetson | Engine | Prototype (SDK required) |
| mock | Any (dev) | - | Stub for testing without hardware |

## Tests

Tests are colocated with source files (`api/test_*.py`, `adapters/test_*.py`):

```bash
cd src/04_hal && python -m pytest -v
```
