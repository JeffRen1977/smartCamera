# 6. PLC 工业控制层 (PLC Integration Layer)

将 AI 推理结果写入工厂 PLC，实现闭环控制。相机作为 Server/Adapter。

## 模块

| 目录 | 协议 | 用途 |
|------|------|------|
| `ethernet_ip/` | EtherNet/IP | 北美 Allen-Bradley 主攻 |
| `modbus_tcp/` | Modbus TCP | Siemens、AutomationDirect |
| `mqtt/` | MQTT | Tier 2 信息层、HMI、云端 |
| `opc_ua/` | OPC UA | Tier 2 信息层、数据分析 |

## 双层架构

- **Tier 1（确定性控制）**: EtherNet/IP、Modbus TCP，写入 PLC 寄存器
- **Tier 2（信息层）**: MQTT、OPC UA，元数据、证据图像、效率统计
