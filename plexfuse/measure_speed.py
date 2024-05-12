from __future__ import annotations

from contextlib import contextmanager
from time import monotonic
from typing import TYPE_CHECKING

from humanize import naturalsize

if TYPE_CHECKING:
    from pathlib import Path


@contextmanager
def measure_speed(part: Path):
    start = monotonic()
    print(f"Downloading: {part}")
    yield
    now = monotonic()
    file_size = part.stat().st_size
    rate = file_size / (now - start)
    speed = naturalsize(rate, binary=True)

    print(f"Downloaded in {speed}/s: {part}")
