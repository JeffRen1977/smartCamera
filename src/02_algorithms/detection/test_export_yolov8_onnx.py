"""Unit tests for export_yolov8_onnx.py."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.mark.skipif(
    __import__("sys").platform == "darwin",
    reason="ultralytics/cv2/numpy segfault on some macOS; run on Linux",
)
class TestExportMain:
    """Test export script with mocked YOLO."""

    def test_main_calls_export_with_args(self) -> None:
        from export_yolov8_onnx import main

        with patch.object(sys, "argv", [
            "export_yolov8_onnx.py",
            "--model", "yolov8n.pt",
            "--output", "/tmp/out.onnx",
            "--imgsz", "320",
            "--opset", "11",
        ]):
            with patch("ultralytics.YOLO") as mock_yolo:
                mock_model = MagicMock()
                mock_model.export.return_value = "/tmp/yolov8n.onnx"
                mock_yolo.return_value = mock_model
                with patch("export_yolov8_onnx.shutil") as mock_shutil:
                    main()

        mock_model.export.assert_called_once()
        call_kw = mock_model.export.call_args[1]
        assert call_kw["format"] == "onnx"
        assert call_kw["imgsz"] == 320
        assert call_kw["opset"] == 11
        assert call_kw["simplify"] is True
        assert call_kw["dynamic"] is False

    def test_main_no_simplify_flag(self) -> None:
        from export_yolov8_onnx import main

        with patch.object(sys, "argv", [
            "export_yolov8_onnx.py",
            "--model", "m.pt",
            "--no-simplify",
        ]):
            with patch("ultralytics.YOLO") as mock_yolo:
                mock_model = MagicMock()
                mock_model.export.return_value = "/tmp/m.onnx"
                mock_yolo.return_value = mock_model
                main()

        call_kw = mock_model.export.call_args[1]
        assert call_kw["simplify"] is False

