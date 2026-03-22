# Detection: YOLO / PaDiM / PatchCore

## YOLOv8 Reference Model (per 技术执行清单_实施细节.md §2.3)

### Export to ONNX

```bash
# 1. Install dependencies first (required before export)
cd src/02_algorithms/detection
pip3 install -r requirements.txt
# Or: pip3 install ultralytics onnx "onnx>=1.12.0,<2.0.0" onnxslim

# 2. Export (yolov8n.pt auto-downloads on first run)
python export_yolov8_onnx.py --model yolov8n.pt --output yolov8n.onnx
# With options: --imgsz 640 --opset 12 --half
```

### Preprocess & Postprocess

```python
from yolov8_utils import preprocess, yolov8_decode, scale_coords

# Preprocess: letterbox + normalize
x, lb = preprocess(img, imgsz=640)  # x: (1,3,640,640) float32

# Run ONNX (or SNPE/TensorRT), get output (1,84,8400)
# output = session.run(None, {"images": x})[0]

# Decode + NMS
detections = yolov8_decode(output, conf_thres=0.25, iou_thres=0.45)
for d in detections:
    d["bbox"] = scale_coords(d["bbox"], lb)  # map to original image
```

### Run inference (ONNX Runtime)

```bash
pip install onnxruntime opencv-python
python run_yolov8_onnx.py --model yolov8n.onnx --image test.jpg
```

### Tests

```bash
cd src/02_algorithms/detection && python -m pytest -v
```

Tests that need numpy/cv2 are skipped on macOS (run on Linux/Ubuntu for full coverage).

### Files

| File | Purpose |
|------|---------|
| `export_yolov8_onnx.py` | Export YOLOv8 to ONNX (CLI) |
| `yolov8_utils.py` | letterbox, preprocess, yolov8_decode, NMS |
| `run_yolov8_onnx.py` | End-to-end inference with ONNX Runtime |
| `test_*.py` | Unit tests (colocated with source) |
