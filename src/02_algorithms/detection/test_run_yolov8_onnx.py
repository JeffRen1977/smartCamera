"""Unit tests for run_yolov8_onnx.py."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent))


class TestRunArgParse:
    """Test argument parsing."""

    def test_requires_model_and_image(self) -> None:
        from run_yolov8_onnx import main

        with patch.object(sys, "argv", ["run_yolov8_onnx.py"]):
            with pytest.raises(SystemExit):
                main()

    @pytest.mark.skipif(
        __import__("sys").platform == "darwin",
        reason="cv2/numpy segfault on some macOS; run on Linux",
    )
    def test_main_with_mocked_pipeline(self) -> None:
        """Test main flow with mocked cv2, onnxruntime, preprocess, decode."""
        pytest.importorskip("onnxruntime", reason="onnxruntime required")
        from run_yolov8_onnx import main
        from yolov8_utils import LetterboxResult

        fake_img = object()  # Any object for preprocess return
        lb = LetterboxResult(img=None, scale=1.0, pad=(0, 0), orig_shape=(100, 100), new_shape=(640, 640))

        with patch.object(sys, "argv", [
            "run_yolov8_onnx.py", "--model", "m.onnx", "--image", "x.jpg",
        ]):
            with patch("run_yolov8_onnx.cv2") as mock_cv2:
                mock_cv2.imread.return_value = MagicMock()
                with patch("run_yolov8_onnx.preprocess", return_value=(MagicMock(), lb)):
                    with patch("run_yolov8_onnx.yolov8_decode", return_value=[
                        {"class_id": 0, "class_name": "person", "confidence": 0.9, "bbox": [10, 10, 50, 80]},
                    ]) as mock_decode:
                        with patch("run_yolov8_onnx.scale_coords", side_effect=lambda b, _: b):
                            with patch("onnxruntime.InferenceSession") as mock_ort_sess:
                                sess = MagicMock()
                                sess.get_inputs.return_value = [MagicMock(name="images")]
                                sess.run.return_value = [MagicMock()]
                                mock_ort_sess.return_value = sess
                                main()

        mock_decode.assert_called_once()
        assert mock_decode.return_value[0]["class_name"] == "person"
