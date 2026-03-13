# 2. 核心算法库 (Core AI Model Library)

算法武器库，保持框架中立 (Framework Agnostic)。模型为 ONNX 等通用格式，不含硬件绑定代码。

## 模块

| 目录 | 算法类型 | 典型模型 |
|------|----------|----------|
| `detection/` | 目标检测 / 异常检测 | YOLO、PaDiM、PatchCore |
| `tracking/` | 追踪 / 姿态估计 | ByteTrack、MoveNet |
| `ocr/` | 文字识别 | PaddleOCR |
| `segmentation/` | 语义分割 / 深度估计 | BiSeNetV2、MiDaS |
| `audio/` | 音频预测 | 1D-CNN、CRNN |

## 自适应逻辑

模型为纯数学逻辑，可快速重训以适应新场景（如从安全帽检测改为纸箱缺陷检测）。
