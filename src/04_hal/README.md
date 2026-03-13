# 4. 感知适配层 (Perception Adapter Layer / HAL)

整个系统实现「解耦」的核心。统一感知 API 对上提供标准接口，厂商 SDK 适配器对下映射到具体硬件。

## 模块

| 目录 | 功能 |
|------|------|
| `api/` | 统一感知 API (Inference / Image / I/O)，标准接口如 `infer(image_raw, model_id)` |
| `adapters/` | 厂商 SDK 适配器：SNPE、TensorRT、OpenVINO、VitisAI、RKNN |
| `isp/` | ISP 调优驱动，确保不同厂商相机在复杂光影下成像一致 |
