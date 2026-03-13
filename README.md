# Smart Camera · 可配置工业相机解决方案

软件定义相机 (Software-Defined Camera) · 工业 4.0 自适应部署平台

## 项目结构

```
smartCamera/
├── docs/                    # 方案文档
│   └── 可配置工业相机解决方案.md
├── src/
│   ├── 01_business/         # 1. 用户业务与应用场景层
│   │   ├── defect_detection/
│   │   ├── ppe_monitoring/
│   │   ├── predictive_maintenance/
│   │   └── amr_navigation/
│   ├── 02_algorithms/       # 2. 核心算法库
│   │   ├── detection/
│   │   ├── tracking/
│   │   ├── ocr/
│   │   ├── segmentation/
│   │   └── audio/
│   ├── 03_orchestration/     # 3. 算法编排与容器化层
│   │   ├── docker/
│   │   ├── k3s/
│   │   └── quantization/
│   ├── 04_hal/              # 4. 感知适配层
│   │   ├── api/
│   │   ├── adapters/        # SNPE, TensorRT, OpenVINO, VitisAI, RKNN
│   │   └── isp/
│   ├── 05_hardware/         # 5. 异构硬件算力层
│   │   └── configs/
│   ├── 06_plc/              # 6. PLC 工业控制层
│   │   ├── ethernet_ip/
│   │   ├── modbus_tcp/
│   │   ├── mqtt/
│   │   └── opc_ua/
│   └── 07_cloud/            # 7. 云平台监控与管理
│       ├── agent/
│       ├── backend/
│       └── dashboard/
```

## 架构层级

| 层级 | 目录 | 说明 |
|------|------|------|
| 1 | `01_business` | 业务场景定义，映射到算法 |
| 2 | `02_algorithms` | 核心算法库，框架中立 |
| 3 | `03_orchestration` | Docker + K3s + 量化 |
| 4 | `04_hal` | 统一 API + 厂商适配器 |
| 5 | `05_hardware` | 硬件配置 |
| 6 | `06_plc` | EtherNet/IP、Modbus TCP、MQTT、OPC UA |
| 7 | `07_cloud` | 设备监控、模型 OTA、效果检测 |

## 支持硬件

- Qualcomm: QS610、QS6490、RB5
- NVIDIA: Jetson
- Xilinx: K26 (Kria)
- Rockchip: RV1126
- Cloud: x86/GPU

## 架构设计文档

各层详细高层架构设计见 [docs/architecture/](docs/architecture/)：

- [01 业务层](docs/architecture/01_business_layer.md)
- [02 算法库](docs/architecture/02_algorithms_layer.md)
- [03 编排层](docs/architecture/03_orchestration_layer.md)
- [04 感知适配层 (HAL)](docs/architecture/04_hal_layer.md)
- [05 硬件层](docs/architecture/05_hardware_layer.md)
- [06 PLC 层](docs/architecture/06_plc_layer.md)
- [07 云平台](docs/architecture/07_cloud_platform.md)

详见 [docs/可配置工业相机解决方案.md](docs/可配置工业相机解决方案.md)
