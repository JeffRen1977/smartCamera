# Human-Augmented Assembly (手動組裝指引與錯誤預防)

Core scenario for reducing quality issues caused by **human error**. Real-time step verification and visual SOP guidance.

## Key Capabilities

### In-Process Verification (即時步驟驗證)
- Camera monitors assembly actions in real time
- Examples: Was the washer missed? Is the torque sequence correct?
- Immediate feedback before defect propagates

### Visual SOP (視覺化標準作業程序)
- When operator error is detected, system shows on-screen prompts or voice alerts
- Closed-loop error correction reduces rework
- Step-by-step guidance overlaid on work area

### Digital Traveler (自動化數位日誌)
- Auto-capture assembly process photos linked to product serial number
- 100% image traceability for aerospace, medical, and high-compliance industries
- Supports audit and quality recall

## Recommended Models
- Pose/keypoint estimation (assembly action verification)
- Object detection (missing parts, wrong sequence)
- Sequence/state recognition

## Recommended Hardware
- QS6490 (multi-station), RB5, Jetson, Xilinx K26
