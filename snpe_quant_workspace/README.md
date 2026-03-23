# SNPE 量化工作目录

用于 §3.3 SNPE 量化流程。详见 `docs/技术执行清单_实施细节.md`。

## 目录结构

```
snpe_quant_workspace/
├── README.md                 # 本文件
├── model.onnx                # 待转换 ONNX（你放入，如 yolov8n.onnx）
├── calibration_images.txt    # 校准图像路径列表（每行一个路径）
├── calib/                    # 原始校准图像（任意尺寸）
│   └── .gitkeep
├── calib_640/                # 640×640 校准图像（resize_calib_images.py 生成）
├── snpe/                     # SNPE SDK（你下载并解压到此）
│   └── snpe-2.x.x/           # 如 snpe-2.15.0
└── *.dlc                     # 输出（FP32 / INT8 DLC）
```

## 使用步骤

1. **放入 ONNX**：将 `yolov8n.onnx` 等拷贝到本目录，或改名为 `model.onnx`。
2. **下载 SNPE**：从 [Qualcomm Neural Processing SDK](https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk) 下载 Linux x86_64 版，解压到 `snpe/`。
3. **准备校准图像**：放入 `calib/`。若图像不是 640×640，先运行：
   ```bash
   python src/03_orchestration/quantization/scripts/resize_calib_images.py
   ```
   会生成 `calib_640/`（letterbox 至 640×640）和 `calibration_images.txt`。若已是 640×640，则运行 `ls calib/*.jpg | head -200 > calibration_images.txt`。
4. **运行 Docker 量化**：
   ```bash
   cd /path/to/smartCamera
   ./src/03_orchestration/quantization/scripts/run_snpe_quant_docker.sh \
     --workspace ./snpe_quant_workspace \
     --onnx yolov8n.onnx \
     --int8
   ```
