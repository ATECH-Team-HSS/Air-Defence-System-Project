from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from balloon_shooter.auxiliary_vision import decode_qr, detect_shapes  # noqa: E402
from balloon_shooter.config import AppConfig, Roi, load_config  # noqa: E402


def main() -> int:
    args = _parse_args()
    config = load_config(args.config)
    source = args.source if args.source is not None else config.video.source
    qr_roi = args.qr_roi or config.auxiliary_vision.qr_roi
    shape_roi = args.shape_roi or config.auxiliary_vision.shape_roi

    if _is_image_file(source):
        frame = cv2.imread(str(source))
        if frame is None:
            print(f"ERROR: cannot read image {source!r}")
            return 1
        _process_frame(frame, qr_roi, shape_roi)
        _write_or_show(frame, args.output, config, args.no_display)
        return 0

    capture = cv2.VideoCapture(_coerce_source(source))
    if not capture.isOpened():
        print(f"ERROR: cannot open source {source!r}")
        return 1

    last_frame = None
    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                print("WARNING: failed to read frame.")
                return 1
            last_frame = frame
            _process_frame(frame, qr_roi, shape_roi)
            if not args.no_display:
                cv2.imshow(config.auxiliary_vision.window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            elif args.output:
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

    if args.output and last_frame is not None:
        cv2.imwrite(str(args.output), last_frame)
    return 0


def _process_frame(frame, qr_roi: Roi, shape_roi: Roi) -> tuple[str | None, list[str]]:
    qr_frame = _crop(frame, qr_roi)
    shape_frame = _crop(frame, shape_roi)
    qr_value = decode_qr(qr_frame)
    shapes = detect_shapes(shape_frame)

    _draw_roi(frame, qr_roi, (0, 255, 0), f"QR: {qr_value or 'None'}")
    shape_text = ", ".join(shapes) if shapes else "None"
    _draw_roi(frame, shape_roi, (255, 0, 0), f"Shapes: {shape_text}")
    print(f"QR: {qr_value or 'None'}, Shapes: {shape_text}")
    return qr_value, shapes


def _crop(frame, roi: Roi):
    return frame[roi.y : roi.y + roi.height, roi.x : roi.x + roi.width]


def _draw_roi(frame, roi: Roi, color: tuple[int, int, int], label: str) -> None:
    left, top, right, bottom = roi.as_xyxy()
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    cv2.putText(
        frame,
        label,
        (left, max(20, top - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
    )


def _write_or_show(
    frame,
    output: Path | None,
    config: AppConfig,
    no_display: bool,
) -> None:
    if output:
        cv2.imwrite(str(output), frame)
    if not no_display:
        cv2.imshow(config.auxiliary_vision.window_name, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the auxiliary QR/shape demo.")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    parser.add_argument("--source", type=str)
    parser.add_argument("--qr-roi", type=_parse_roi)
    parser.add_argument("--shape-roi", type=_parse_roi)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-display", action="store_true")
    return parser.parse_args()


def _parse_roi(value: str) -> Roi:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("ROI must be x,y,width,height")
    try:
        return Roi(*(int(part) for part in parts))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ROI values must be integers") from exc


def _is_image_file(source: int | str) -> bool:
    if isinstance(source, int):
        return False
    suffix = Path(source).suffix.lower()
    return suffix in {".bmp", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def _coerce_source(source: int | str) -> int | str:
    if isinstance(source, str) and source.isdigit():
        return int(source)
    return source


if __name__ == "__main__":
    raise SystemExit(main())
