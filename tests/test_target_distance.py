from balloon_shooter.target_distance import (
    bbox_center,
    is_within_threshold,
    pixel_offset,
)


def test_bbox_center_and_offset() -> None:
    bbox = (10, 20, 30, 60)

    assert bbox_center(bbox) == (20, 40)
    assert pixel_offset(bbox, (25, 35)) == (5, -5)


def test_is_within_threshold() -> None:
    bbox = (10, 10, 30, 30)

    assert is_within_threshold(bbox, (22, 18), 5, 5)
    assert not is_within_threshold(bbox, (40, 20), 5, 5)
