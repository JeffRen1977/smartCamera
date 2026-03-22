"""Unit tests for yolov8_utils.py."""

import pytest
from unittest.mock import patch


def _fake_img(shape=(100, 80, 3)):
    """Minimal array-like for tests (avoids numpy import issues)."""
    class Fake:
        pass
    f = Fake()
    f.shape = shape
    f.dtype = "uint8"
    return f


@pytest.mark.skip(reason="numpy segfault on some macOS; run on Linux/Ubuntu")
class TestYolov8Decode:
    """Tests for yolov8_decode (numpy required)."""

    def test_decode_empty_when_all_low_conf(self) -> None:
        try:
            import numpy as np
            from yolov8_utils import yolov8_decode
        except ImportError:
            pytest.skip("numpy required")
        # Output with all zeros -> no detections above conf_thres
        out = np.zeros((1, 84, 8400), dtype=np.float32)
        result = yolov8_decode(out, conf_thres=0.25)
        assert result == []

    def test_decode_returns_list_of_dicts(self) -> None:
        try:
            import numpy as np
            from yolov8_utils import yolov8_decode
        except ImportError:
            pytest.skip("numpy required")
        out = np.zeros((1, 84, 8400), dtype=np.float32)
        out[0, 4, 0] = 0.9  # class 0, anchor 0, high conf
        out[0, 0:4, 0] = [320, 320, 50, 50]  # box
        result = yolov8_decode(out, conf_thres=0.5)
        assert isinstance(result, list)
        if result:
            d = result[0]
            assert "class_id" in d and "class_name" in d and "confidence" in d and "bbox" in d
            assert len(d["bbox"]) == 4


class TestLetterboxResult:
    """Tests for LetterboxResult (dataclass)."""

    def test_letterbox_result_attrs(self) -> None:
        from yolov8_utils import LetterboxResult
        lb = LetterboxResult(img=None, scale=1.0, pad=(0, 0), orig_shape=(100, 80), new_shape=(640, 640))
        assert lb.scale == 1.0
        assert lb.pad == (0, 0)
        assert lb.orig_shape == (100, 80)


class TestCocoNames:
    """Tests for COCO_NAMES constant."""

    def test_coco_has_80_classes(self) -> None:
        from yolov8_utils import COCO_NAMES
        assert len(COCO_NAMES) == 80

    def test_coco_first_is_person(self) -> None:
        from yolov8_utils import COCO_NAMES
        assert COCO_NAMES[0] == "person"


class TestScaleCoords:
    """Tests for scale_coords."""

    def test_scale_coords_returns_unchanged_when_no_numpy(self) -> None:
        from yolov8_utils import scale_coords, LetterboxResult
        with patch("yolov8_utils._check_numpy", return_value=False):
            lb = LetterboxResult(img=None, scale=1.0, pad=(0, 0), orig_shape=(100, 100), new_shape=(640, 640))
            result = scale_coords([10.0, 20.0, 50.0, 80.0], lb)
        assert result == [10.0, 20.0, 50.0, 80.0]
