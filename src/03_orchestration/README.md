# 3. 算法编排与容器化层 (Orchestration Layer)

实现快速布置的关键。Docker 容器打包算法与依赖，K3s 负责编排，量化工具针对目标硬件生成优化模型。

## 模块

| 目录 | 功能 |
|------|------|
| `docker/` | Dockerfile、镜像构建脚本 |
| `k3s/` | K3s 编排配置、部署清单 |
| `quantization/` | ONNX → SNPE DLC / TensorRT Engine / Vitis AI / RKNN 的量化流水线 |
