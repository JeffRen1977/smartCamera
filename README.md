# Smart Camera · Configurable Industrial Camera Solution

Software-Defined Camera · Industry 4.0 Adaptive Deployment Platform

## Project Structure

```
smartCamera/
├── docs/                    # Documentation
│   ├── Configurable_Industrial_Camera_Solution.md  # English
│   └── 可配置工业相机解决方案.md                   # Chinese
├── src/
│   ├── 01_business/         # 1. Business & Application Layer
│   │   ├── defect_detection/
│   │   ├── ppe_monitoring/
│   │   ├── predictive_maintenance/
│   │   └── amr_navigation/
│   ├── 02_algorithms/       # 2. Core AI Model Library
│   │   ├── detection/
│   │   ├── tracking/
│   │   ├── ocr/
│   │   ├── segmentation/
│   │   └── audio/
│   ├── 03_orchestration/    # 3. Orchestration & Containerization
│   │   ├── docker/
│   │   ├── k3s/
│   │   └── quantization/
│   ├── 04_hal/              # 4. Perception Adapter Layer
│   │   ├── api/
│   │   ├── adapters/        # SNPE, TensorRT, OpenVINO, VitisAI, RKNN
│   │   └── isp/
│   ├── 05_hardware/         # 5. Heterogeneous Hardware
│   │   └── configs/
│   ├── 06_plc/              # 6. PLC Integration Layer
│   │   ├── ethernet_ip/
│   │   ├── modbus_tcp/
│   │   ├── mqtt/
│   │   └── opc_ua/
│   └── 07_cloud/            # 7. Cloud Platform
│       ├── agent/
│       ├── backend/
│       └── dashboard/
```

## Architecture Layers

| Layer | Directory | Description |
|-------|-----------|-------------|
| 1 | `01_business` | Business scenarios, algorithm mapping |
| 2 | `02_algorithms` | Core algorithm library, framework-agnostic |
| 3 | `03_orchestration` | Docker + K3s + quantization |
| 4 | `04_hal` | Unified API + vendor adapters |
| 5 | `05_hardware` | Hardware configuration |
| 6 | `06_plc` | EtherNet/IP, Modbus TCP, MQTT, OPC UA |
| 7 | `07_cloud` | Device monitoring, model OTA, effect detection |

## Supported Hardware

- Qualcomm: QS610, QS6490, RB5
- NVIDIA: Jetson
- Xilinx: K26 (Kria)
- Rockchip: RV1126
- Cloud: x86/GPU

## Architecture Design Docs

Detailed high-level architecture per layer: [docs/architecture/](docs/architecture/)

- [01 Business Layer](docs/architecture/01_business_layer.md)
- [02 Algorithms](docs/architecture/02_algorithms_layer.md)
- [03 Orchestration](docs/architecture/03_orchestration_layer.md)
- [04 HAL](docs/architecture/04_hal_layer.md)
- [05 Hardware](docs/architecture/05_hardware_layer.md)
- [06 PLC](docs/architecture/06_plc_layer.md)
- [07 Cloud Platform](docs/architecture/07_cloud_platform.md)

See [docs/Configurable_Industrial_Camera_Solution.md](docs/Configurable_Industrial_Camera_Solution.md)
