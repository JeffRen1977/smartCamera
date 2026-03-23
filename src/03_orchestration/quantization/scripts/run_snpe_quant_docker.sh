#!/bin/bash
#
# Run SNPE quantization (ONNX → DLC) inside Docker.
# See docs/技术执行清单_实施细节.md §3.3.4
#
# Usage:
#   ./run_snpe_quant_docker.sh [--workspace DIR] [--onnx FILE] [--int8]
#
# Prereqs:
#   - Docker
#   - SNPE SDK unzipped to workspace/snpe/
#   - ONNX model and optional calibration_images.txt in workspace
#
# Note: On Apple Silicon (M1/M2/M3), INT8 quantization may fail under emulation.
#       FP32 DLC usually works; for INT8 use native x86_64 Linux if needed.
#

set -e
WORKSPACE="${WORKSPACE:-$(pwd)/snpe_quant_workspace}"
ONNX="${ONNX:-model.onnx}"
CALIB_LIST="calibration_images.txt"
DO_INT8=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --workspace) WORKSPACE="$2"; shift 2 ;;
    --onnx) ONNX="$2"; shift 2 ;;
    --int8) DO_INT8=true; shift ;;
    *) shift ;;
  esac
done

ONNX_BASE="${ONNX%.onnx}"
# Accept snpe-X.X.X or any version dir (e.g. 2.44.0.260225)
SNPE_SUBDIR=$(find "$WORKSPACE/snpe" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | head -1)

if [[ -z "$SNPE_SUBDIR" ]] || [[ ! -d "$SNPE_SUBDIR" ]]; then
  echo "Error: SNPE SDK not found in $WORKSPACE/snpe/"
  echo "Download from Qualcomm Developer and unzip to $WORKSPACE/snpe/"
  exit 1
fi
SNPE_DIR="/workspace/snpe/$(basename "$SNPE_SUBDIR")"

if [[ ! -f "$WORKSPACE/$ONNX" ]]; then
  echo "Error: ONNX not found: $WORKSPACE/$ONNX"
  exit 1
fi

echo "Workspace: $WORKSPACE"
echo "ONNX: $ONNX"
echo "SNPE: $SNPE_DIR"
echo "INT8: $DO_INT8"

# Install deps: python3, libc++1 (for quantize); use linux/amd64 for x86 binaries
docker run --rm --platform linux/amd64 \
  -v "$WORKSPACE:/workspace" \
  ubuntu:20.04 bash -c "
    apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-numpy libc++1 libunwind8 > /dev/null
    export SNPE_ROOT=$SNPE_DIR
    export PYTHONPATH=\$SNPE_ROOT/lib/python:\$PYTHONPATH
    export PATH=\$SNPE_ROOT/bin/x86_64-linux-clang:\$PATH
    export LD_LIBRARY_PATH=\$SNPE_ROOT/lib/x86_64-linux-clang:\$LD_LIBRARY_PATH
    cd /workspace
    echo 'Converting ONNX to DLC (FP32)...'
    \$SNPE_ROOT/bin/x86_64-linux-clang/snpe-onnx-to-dlc \
      --input_network $ONNX \
      --output ${ONNX_BASE}.dlc
    echo 'Created ${ONNX_BASE}.dlc'
    if [ '$DO_INT8' = 'true' ] && [ -f $CALIB_LIST ]; then
      echo 'Quantizing to INT8...'
      \$SNPE_ROOT/bin/x86_64-linux-clang/snpe-dlc-quantize \
        --input_dlc ${ONNX_BASE}.dlc \
        --input_list $CALIB_LIST \
        --output_dlc ${ONNX_BASE}_int8.dlc
      echo 'Created ${ONNX_BASE}_int8.dlc'
    fi
  "

echo "Done. Output: $WORKSPACE/${ONNX_BASE}.dlc"
