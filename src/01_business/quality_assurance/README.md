# Quality Assurance & Zero-Defect (高精度質量保證)

Use AI to replace human inspection for finer, faster quality checks.

## Key Capabilities

### Micro-Defect Detection (微小缺陷檢測)
- PCB solder defects
- Micro-cracks on metal surfaces
- Part orientation (correct side) or wrong-part assembly

### Label & Character Recognition (OCR/OCV)
- Auto-read product labels, wire encoding, batch numbers
- Verify label placement and content vs. system records
- OCV (Optical Character Verification) for print quality

### 3D Dimension Measurement (三維尺寸測量)
- With depth sensing (3D ToF)
- Detect shape deviation or stack height
- Ensure assembly precision

## Recommended Models
- YOLOv8-Nano, PaDiM, PatchCore (defect detection)
- PaddleOCR (label/code reading)
- 3D/Depth models (dimension measurement)

## Recommended Hardware
- QS610, QS6490, RB5, Xilinx K26 (defect)
- RB5, Jetson (OCR, 3D)
