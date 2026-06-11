import cv2
import numpy as np

from balloon_shooter.auxiliary_vision.shape_detector import detect_shapes


def test_detect_shapes_finds_red_square() -> None:
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    cv2.rectangle(frame, (30, 30), (80, 80), (0, 0, 255), -1)

    shapes = detect_shapes(frame)

    assert "Red Square" in shapes
