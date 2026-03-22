# Technical Execution Implementation Details

> Implementation guide for Section 7 (P0/P1 tasks) of the Configurable Industrial Camera Solution.

---

## 1. P0: Unified Perception API Specification

### 1.1 Objective

Define a **standard interface** between AI containers and the underlying inference runtime. Upper algorithm containers call this interface only; they do not care whether the backend is SNPE or TensorRT. Coverage: image input, inference trigger, result format, I/O control.

### 1.2 API Definition

#### 1.2.1 Initialization

| Interface | Signature | Description |
|-----------|-----------|-------------|
| `init()` | `PerceptionAPI(backend=None)` | Optional `backend`; auto-detect if not specified |
| Auto-detect | Read `/proc/device-tree`, CPU info | Identify Qualcomm / NVIDIA / other platforms |
| Env override | `HAL_BACKEND=snpe|tensorrt|openvino` | Force a backend |

#### 1.2.2 Inference

| Interface | Signature | Description |
|-----------|-----------|-------------|
| Sync | `infer(image_raw, model_id) -> result` | Block until result |
| Async | `infer_async(image_raw, model_id, callback)` | High throughput, callback-based |
| Load model | `load_model(model_id, model_path)` | Lazy load on first `infer` |

**Arguments**:

- `image_raw`: `numpy.ndarray` (H, W, C) or `bytes`; RGB/BGR; H/W per model
- `model_id`: string, e.g. `yolov8n_defect`, mapped to actual model path internally

#### 1.2.3 I/O Control (Optional)

| Interface | Signature | Description |
|-----------|-----------|-------------|
| Set output | `set_io(pin, value)` | Simple GPIO trigger (alarm, buzzer) |
| Image source | `get_image_source(stream_id)` | Camera/video stream handle |

### 1.3 Data Format

#### Input

| Format | Type | Description |
|--------|------|-------------|
| Image | `np.ndarray` (H,W,C) uint8 | C=3 RGB or BGR per model |
| Alternative | `bytes` (JPEG/RAW) | Decoded to ndarray in API layer |

#### Output (unified structure)

```json
{
  "detections": [
    {
      "class_id": 0,
      "class_name": "hard_hat",
      "confidence": 0.92,
      "bbox": [x1, y1, x2, y2],
      "extra": {}
    }
  ],
  "metadata": {
    "inference_time_ms": 12.5,
    "model_id": "yolov8n_defect",
    "backend": "snpe",
    "image_shape": [640, 640, 3]
  }
}
```

- `detections`: list of detections; empty array if none
- `metadata`: inference time, model_id, backend, image shape

### 1.4 Pre/Post Processing Responsibilities

| Stage | Layer | Description |
|-------|-------|-------------|
| Normalize / Resize | API layer | Unified per-model requirements |
| Inference | Adapter | Runs inference only, outputs raw tensor |
| NMS / Decode | API layer | Unified postprocessing; adapter not involved |
| Error codes | Adapter | Clear codes for debugging |

### 1.5 Error Codes

| Code | Meaning |
|------|---------|
| `OK` | Success |
| `MODEL_NOT_LOADED` | Model not loaded or path invalid |
| `INVALID_INPUT` | Bad image format/size |
| `INFERENCE_FAILED` | Inference failed |
| `BACKEND_UNAVAILABLE` | Specified backend unavailable |

### 1.6 Python Example

```python
from hal import PerceptionAPI

api = PerceptionAPI(backend="snpe")  # or None for auto-detect
result = api.infer(image, model_id="yolov8n_defect")
# result: {"detections": [...], "metadata": {"inference_time_ms": 12, ...}}
```

### 1.7 C++ Example

```cpp
#include "hal/perception_api.h"

auto api = PerceptionAPI::Create(/* backend */);
auto result = api->Infer(image, "yolov8n_defect");
```

---

## 2. P0: SNPE and TensorRT Adapter Prototypes

### 2.1 Hardware

| Platform | Model | Purpose | Notes |
|----------|-------|--------|-------|
| Qualcomm | RB5 (QRB5165) | SNPE validation | QS610/QS6490 for production |
| NVIDIA | Jetson Orin Nano or Xavier NX | TensorRT validation | Or Orin NX for more throughput |

### 2.2 Software Environment

#### 2.2.1 Qualcomm RB5 (SNPE)

| Item | Version / Requirement |
|------|----------------------|
| OS | Ubuntu 20.04 / Yocto |
| SNPE SDK | 2.x (Qualcomm Developer) |
| Python | 3.8+ |
| Model format | DLC (convert via snpe-onnx-to-dlc) |

**Steps**:

1. Install SNPE runtime: `libSnpeDspRuntime.so`, `libSNPE.so`, etc.
2. Install SNPE Python: `snpe-sdk/python`
3. ONNX → DLC: `snpe-onnx-to-dlc` or `snpe-dlc-converter`

#### 2.2.2 NVIDIA Jetson (TensorRT)

| Item | Version / Requirement |
|------|----------------------|
| OS | JetPack 5.x / 6.x |
| TensorRT | Preinstalled with JetPack |
| Python | 3.8+ |
| Model format | Engine (built by TensorRT Builder) |

**Steps**:

1. Use `trtexec` or Python API to convert ONNX → Engine
2. Support FP16/INT8
3. First run builds Engine; cache to disk for faster startup

### 2.3 Reference Model: YOLOv8n

| Attribute | Value |
|-----------|-------|
| Model | YOLOv8n (ultralytics) |
| Input | 640×640×3, FP32 or INT8 |
| Output | Bounding boxes + class + confidence |
| Export | `model.export(format="onnx")` |

**Export ONNX**:

```bash
yolo export model=yolov8n.pt format=onnx imgsz=640
```

### 2.4 Adapter Implementation

#### 2.4.1 Base Interface

```python
class BaseAdapter(ABC):
    @abstractmethod
    def load_model(self, model_id: str, model_path: str) -> None: ...

    @abstractmethod
    def infer(self, image: np.ndarray) -> dict: ...

    @abstractmethod
    def get_supported_formats(self) -> list[str]: ...
```

#### 2.4.2 SNPE Adapter Flow

1. Load DLC: `snpe.load_from_dlc(path)`
2. Set input: `set_input_tensor(name, data)`
3. Execute: `execute()`
4. Get output: `get_output_tensor(name)`
5. Convert to unified output format

#### 2.4.3 TensorRT Adapter Flow

1. Deserialize Engine or build from ONNX
2. Create execution context
3. Copy input to GPU
4. `execute_v2()`
5. Copy output, convert to unified format

### 2.5 Acceptance Criteria

| Item | Criterion |
|------|-----------|
| Dual board | Same YOLOv8n runs on both RB5 and Jetson via `infer(img, "yolov8n")` |
| Consistent output | Same input → unified output format (detections + metadata) |
| Performance | Record latency as baseline |
| Switch | Use `HAL_BACKEND=snpe` or `tensorrt` without changing app code |

### 2.6 Directory and Deliverables

```
src/04_hal/
├── api/
│   ├── perception_api.py
│   └── types.py
├── adapters/
│   ├── base.py
│   ├── router.py
│   ├── snpe/
│   │   └── snpe_adapter.py
│   └── tensorrt/
│       └── tensorrt_adapter.py
```

**Deliverable**: Run same demo on RB5 and Jetson; provide log and detection screenshots.

---

## 3. P1: Model Optimization Automation (Quantization Pipeline)

### 3.1 Objective

- **Input**: ONNX model
- **Output**: SNPE INT8 DLC, TensorRT Engine
- **Form**: PC-side CLI or scripts
- **Next**: Package outputs into Docker images for edge pull

### 3.2 Toolchain

| Target | Tool | Input | Output |
|--------|------|-------|--------|
| Qualcomm | SNPE DLC Converter | ONNX | DLC (FP32/INT8) |
| NVIDIA | TensorRT (trtexec / Python) | ONNX | Engine (FP16/INT8) |
| Xilinx K26 | Vitis AI (P2) | ONNX | Xmodel |
| Rockchip | RKNN-Toolkit2 (P2) | ONNX | RKNN |

### 3.3 SNPE Quantization

#### Environment

- PC: x86_64 Linux / Windows with SNPE SDK
- Python scripts call `snpe-dlc-converter` or `snpe-onnx-to-dlc`

#### Steps

1. **ONNX → DLC (FP32)**
   ```bash
   snpe-onnx-to-dlc --input_model model.onnx --output_model model.dlc
   ```

2. **INT8 quantization** (needs calibration data)
   - 100–500 representative images
   - Use `snpe-dlc-quantize` or Python
   ```bash
   snpe-dlc-quantize --input_dlc model.dlc --input_list calibration_images.txt --output_dlc model_int8.dlc
   ```

3. **Validation**: Compare FP32 vs INT8 accuracy (mAP, recall) on device

#### Calibration Data

- `calibration_images.txt`: one path per line
- Image size must match inference (e.g. 640×640)

### 3.4 TensorRT Quantization

#### Environment

- PC: CUDA + TensorRT (or Docker `nvcr.io/nvidia/tensorrt`)
- Or build Engine on Jetson directly

#### Steps

1. **FP16** (quick validation)
   ```bash
   trtexec --onnx=model.onnx --saveEngine=model_fp16.engine --fp16
   ```

2. **INT8** (needs calibrator)
   - Implement `IInt8EntropyCalibrator2` or use Python `trt.Builder`
   ```bash
   trtexec --onnx=model.onnx --saveEngine=model_int8.engine --int8 --calib=calibration.cache
   ```

3. **Validation**: Compare FP32/FP16/INT8 accuracy and latency

### 3.5 CLI Design

```bash
quantize --model model.onnx --target snpe --output model.dlc [--int8] [--calib-dir ./calib]
quantize --model model.onnx --target tensorrt --output model.engine [--fp16|--int8] [--calib-dir ./calib]

# Examples
quantize --model yolov8n.onnx --target snpe --output yolov8n.dlc --int8 --calib-dir ./calib_images
quantize --model yolov8n.onnx --target tensorrt --output yolov8n.engine --fp16
```

### 3.6 Pipeline Steps (Automation)

1. **Validate ONNX**: opset, inputs/outputs, dynamic shape
2. **Select tool** by target: snpe / tensorrt
3. **Quantize**: FP32→DLC/Engine, optional INT8
4. **Accuracy check** (optional): run on validation set, report mAP
5. **Package**: DLC/Engine + runtime into Docker image

### 3.7 Docker Packaging

```
FROM hal-runtime:latest
COPY yolov8n.dlc /models/yolov8n_defect.dlc
# or
COPY yolov8n.engine /models/yolov8n_defect.engine
```

- Different targets → different images: `scene-defect:snpe-rb5`, `scene-defect:tensorrt-jetson`
- Edge pulls image per `HAL_BACKEND`

### 3.8 Directory Structure

```
src/03_orchestration/
└── quantization/
    ├── quantize.py
    ├── snpe/
    │   ├── onnx_to_dlc.py
    │   └── quantize_int8.py
    ├── tensorrt/
    │   ├── onnx_to_engine.py
    │   └── calibrate.py
    ├── common/
    │   ├── validate_onnx.py
    │   └── accuracy_check.py
    └── calib/          # .gitignore
```

### 3.9 Acceptance Criteria

| Item | Criterion |
|------|-----------|
| ONNX input | Accept standard YOLOv8n ONNX |
| SNPE output | DLC runs on RB5 (FP32 or INT8) |
| TensorRT output | Engine runs on Jetson (FP16 or INT8) |
| CLI | Single command with `--int8` and `--calib-dir` support |
| Packaging | Quantized artifacts copy into Docker and run successfully |

---

## 4. Appendix: Mapping to Master Document

| Master doc section | This document |
|--------------------|---------------|
| 7.1 P0 Unified API | Section 1 |
| 7.2 P0 SNPE/TensorRT adapters | Section 2 |
| 7.3 P1 Quantization pipeline | Section 3 |

---

*Document v1.0 · Companion to Configurable Industrial Camera Solution Technical Execution Checklist · For engineering leads and dev teams*
