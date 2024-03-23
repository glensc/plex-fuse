from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FsOptions:
    cache_path: str | None = None
    http_cache: bool | None = None
    control_path: str | None = None
    listen_events: bool | None = None
