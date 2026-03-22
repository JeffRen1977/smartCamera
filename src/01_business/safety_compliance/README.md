# Safety & Compliance Monitoring (安全與合規性監控)

AI camera as **round-the-clock safety manager**.

## Key Capabilities

### PPE Detection (個人防護裝備檢測)
- Detect if personnel wear hard hat, safety vest, mask before entering
- Real-time alert on violation

### Virtual Fence / Restricted Zone (危險區域入侵警告)
- Define no-go zones (robot range, high-voltage area)
- Trigger alarm or PLC stop when person approaches
- Integrate with EtherNet/IP or Modbus for immediate machine shutdown

### Behavior Risk Analysis (行為風險分析)
- Detect unsafe actions (climbing, fall, prolonged stay in narrow corridor)
- Posture and movement analytics
- Early warning for fatigue or unusual behavior

## Recommended Models
- MoveNet, SSD-MobileNet, YOLO (PPE)
- Pose estimation (behavior, fall detection)
- Person detection + zone logic (virtual fence)

## Recommended Hardware
- QS6490 (multi-station), RB5 (multi-camera)
