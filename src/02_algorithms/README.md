# 2. Core AI Model Library

Algorithm arsenal, framework-agnostic. Models in ONNX etc., no hardware binding.

## Modules

| Directory | Algorithm Type | Typical Models |
|-----------|----------------|----------------|
| `detection/` | Object / anomaly detection | YOLO, PaDiM, PatchCore |
| `tracking/` | Tracking / pose | ByteTrack, MoveNet |
| `ocr/` | Text recognition | PaddleOCR |
| `segmentation/` | Semantic segmentation / depth | BiSeNetV2, MiDaS |
| `audio/` | Audio prediction | 1D-CNN, CRNN |

## Adaptive Logic

Models are pure math, quickly retrainable for new scenarios (e.g., hard hat → carton defect).
