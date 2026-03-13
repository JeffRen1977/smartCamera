# 6. PLC Integration Layer

Write AI inference results to factory PLC for closed-loop control. Camera acts as Server/Adapter.

## Modules

| Directory | Protocol | Use |
|-----------|----------|-----|
| `ethernet_ip/` | EtherNet/IP | North American Allen-Bradley primary |
| `modbus_tcp/` | Modbus TCP | Siemens, AutomationDirect |
| `mqtt/` | MQTT | Tier 2 information, HMI, cloud |
| `opc_ua/` | OPC UA | Tier 2 information, analytics |

## Two-Tier Architecture

- **Tier 1 (deterministic)**: EtherNet/IP, Modbus TCP—write to PLC registers
- **Tier 2 (information)**: MQTT, OPC UA—metadata, evidence images, efficiency stats
