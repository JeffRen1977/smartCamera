# 4. Perception Adapter Layer (HAL)

Core of algorithm-hardware decoupling. Unified perception API upward, vendor SDK adapters downward.

## Modules

| Directory | Function |
|-----------|----------|
| `api/` | Unified perception API (Inference / Image / I/O), e.g. `infer(image_raw, model_id)` |
| `adapters/` | Vendor SDK adapters: SNPE, TensorRT, OpenVINO, VitisAI, RKNN |
| `isp/` | ISP tuning drivers for consistent image quality under complex lighting |
