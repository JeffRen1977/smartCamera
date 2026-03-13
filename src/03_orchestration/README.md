# 3. Orchestration & Containerization Layer

Key to fast deployment. Docker packages algorithms and dependencies, K3s orchestrates, quantization produces hardware-optimized models.

## Modules

| Directory | Function |
|-----------|----------|
| `docker/` | Dockerfile, image build scripts |
| `k3s/` | K3s config, deployment manifests |
| `quantization/` | ONNX → SNPE DLC / TensorRT Engine / Vitis AI / RKNN pipeline |
