from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.media import MediaPart

    from plexfuse.plexvfs.Playable import Playable


class FileEntry:
    def __init__(self, part: MediaPart, playable: Playable = None, reader=None):
        self.size = part.size
        self.key = part.key
        self.playable = playable
        self.reader = reader

    def timestamps(self):
        try:
            return self.playable.timestamps
        except AttributeError:
            return {}

    def read(self, offset: int, size: int):
        return self.reader.read(self.key, size=size, offset=offset, max_size=self.size)

    def __len__(self):
        return self.size
