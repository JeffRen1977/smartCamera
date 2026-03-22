# Logistics & Throughput (生態位優化與物流自動化)

Improve material flow and throughput efficiency.

## Key Capabilities

### Bottleneck Analysis (產線瓶頸分析)
- Heatmap and cycle time analysis
- Identify workstations where line dwells too long
- Support shift and layout optimization

### Auto Sorting & Warehousing (自動分揀與入庫)
- Identify material type and barcode on conveyor
- Send signals to sorting robot for auto stacking or boxing
- Integration with PLC for diverter/actuator control

### Embodied Robot Navigation (具身機器人導航)
- Provide obstacle avoidance and environment perception for AGV/AMR
- Navigate in complex human-machine mixed environments
- Semantic segmentation for ground, obstacles, people

## Recommended Models
- BiSeNetV2, MiDaS (segmentation, depth)
- YOLO, ByteTrack (object detection, tracking)
- Cycle time / heatmap analytics

## Recommended Hardware
- RB5 (ISP/HDR), Jetson, Xilinx K26
