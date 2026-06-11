import numpy as np

from balloon_shooter.tracker import KalmanBoxTracker, Tracker


def test_tracker_keeps_id_for_overlapping_detection() -> None:
    KalmanBoxTracker.count = 0
    tracker = Tracker(max_age=2, iou_threshold=0.1)

    first_tracks = tracker.update(np.array([[10, 10, 50, 50, 0.9, 1]]))
    second_tracks = tracker.update(np.array([[12, 12, 52, 52, 0.8, 1]]))

    assert first_tracks.shape == (1, 6)
    assert second_tracks.shape == (1, 6)
    assert int(first_tracks[0][4]) == int(second_tracks[0][4])
    assert int(second_tracks[0][5]) == 1


def test_tracker_returns_empty_when_no_detections() -> None:
    tracker = Tracker(max_age=0)

    tracks = tracker.update(np.empty((0, 6)))

    assert tracks.shape == (0, 6)
