from balloon_shooter.config import Roi
from balloon_shooter.safety import evaluate_target_safety, point_in_roi


def test_point_in_roi() -> None:
    roi = Roi(10, 10, 20, 20)

    assert point_in_roi((15, 15), roi)
    assert not point_in_roi((35, 15), roi)


def test_target_in_forbidden_zone_is_not_safe() -> None:
    bbox = (10, 10, 30, 30)
    forbidden_zone = Roi(0, 0, 40, 40)

    decision = evaluate_target_safety(bbox, forbidden_zone)

    assert not decision.safe
    assert decision.reason == "target in forbidden zone"


def test_no_target_is_not_safe() -> None:
    decision = evaluate_target_safety(None, Roi())

    assert not decision.safe
    assert decision.reason == "no target"
