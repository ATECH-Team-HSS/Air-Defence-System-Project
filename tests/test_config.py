from pathlib import Path

from balloon_shooter.config import Roi, load_config


def test_load_config_resolves_model_path(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
video:
  source: "0"
  model_path: "weights/best.pt"
  class_names: ["Blue", "Red"]
  device: "cpu"
targeting:
  x_changer: 12
safety:
  forbidden_fire_zone:
    enabled: true
    rect: [10, 20, 30, 40]
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.video.source == 0
    assert config.video.model_path == tmp_path / "weights" / "best.pt"
    assert config.video.class_names == ("Blue", "Red")
    assert config.video.device == "cpu"
    assert config.targeting.x_tolerance == 12
    assert config.safety.forbidden_fire_zone == Roi(10, 20, 30, 40)
