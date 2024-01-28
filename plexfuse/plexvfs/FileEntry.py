from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.media import MediaPart

    from plexfuse.plexvfs.Playable import Playable


class FileEntry:
    def __init__(self, part: MediaPart, playable: Playable = None):
        self.size = part.size
        self.key = part.key
        self.playable = playable

    def timestamps(self):
        try:
            return self.playable.timestamps
        except AttributeError:
            return {}

    def __len__(self):
        return self.size
