from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class PlexVFS(UserDict):
    def __init__(self, plex: PlexApi):
        super().__init__()
        self.plex = plex

    def __missing__(self, path: str):
        if path == "/":
            entry = self.plex.section_types
        else:
            raise ValueError(f"Unsupported path: {path}")

        self[path] = entry

        return entry
