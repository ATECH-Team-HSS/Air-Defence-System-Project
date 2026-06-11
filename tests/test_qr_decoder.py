import numpy as np

from balloon_shooter.auxiliary_vision.qr_decoder import decode_qr


class FakeCode:
    def __init__(self, data: bytes) -> None:
        self.data = data


def test_decode_qr_returns_allowed_value() -> None:
    frame = np.zeros((20, 20, 3), dtype=np.uint8)

    result = decode_qr(frame, decoder=lambda _gray: [FakeCode(b"A")])

    assert result == "A"


def test_decode_qr_ignores_unexpected_value() -> None:
    frame = np.zeros((20, 20, 3), dtype=np.uint8)

    result = decode_qr(frame, decoder=lambda _gray: [FakeCode(b"C")])

    assert result is None
