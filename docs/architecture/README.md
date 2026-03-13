# Configurable Industrial Camera Solution — Layered Architecture Design

This directory contains **detailed high-level architecture** for each layer, for engineering implementation reference.

## Document Index

| Layer | Document | Core Responsibility |
|-------|----------|---------------------|
| 1 | [01_business_layer.md](01_business_layer.md) | Scene config, scene routing, algorithm selection |
| 2 | [02_algorithms_layer.md](02_algorithms_layer.md) | Model repository, algorithm modules, ONNX management |
| 3 | [03_orchestration_layer.md](03_orchestration_layer.md) | Docker, K3s, quantization pipeline |
| 4 | [04_hal_layer.md](04_hal_layer.md) | Unified perception API, vendor adapters, ISP |
| 5 | [05_hardware_layer.md](05_hardware_layer.md) | Platform capability, BSP config |
| 6 | [06_plc_layer.md](06_plc_layer.md) | EtherNet/IP, Modbus TCP, MQTT, OPC UA |
| 7 | [07_cloud_platform.md](07_cloud_platform.md) | Device monitoring, model OTA, effect detection |

## Layer Relationships

```mermaid
flowchart TD
    L1[1. Business]
    L2[2. Algorithms]
    L3[3. Orchestration]
    L4[4. HAL]
    L5[5. Hardware]
    L6[6. PLC]
    L7[7. Cloud]

    L1 -->|scenario->model| L2
    L2 -->|ONNX| L3
    L3 -->|container+quant| L4
    L4 -->|inference| L5
    L1 -->|AI result| L6
    L4 -->|AI result| L6
    L7 -->|OTA/deploy| L3
    L4 -->|metrics/samples| L7
    L3 -->|heartbeat| L7
```

## Design Highlights by Layer

| Layer | Design Highlights |
|-------|-------------------|
| Business | Declarative config, scenario-algorithm decoupling, PLC mapping configurable |
| Algorithms | Framework-agnostic, ONNX primary, metadata traceable |
| Orchestration | Build once deploy everywhere, K3s lightweight, quantization automated |
| HAL | Unified API, runtime selection, adapter extensible |
| Hardware | Capability declaration, config-driven |
| PLC | Two-tier architecture, Memory Map, EDS support |
| Cloud | Device monitoring, model OTA, effect loop |
