from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.vfs.entry.AttrEntry import AttrEntry

if TYPE_CHECKING:
    from plexapi.media import MediaPart

    from plexfuse.vfs.ChunkedFile import ChunkedFile
    from plexfuse.vfs.Playable import Playable


class FileEntry(AttrEntry):
    def __init__(self, part: MediaPart, playable: Playable, reader: ChunkedFile):
        self.size = part.size
        self.key = part.key
        self.playable = playable
        self.reader = reader

    @property
    def attr(self):
        try:
            return self.playable.timestamps
        except AttributeError:
            return {}

    def read(self, offset: int, size: int):
        return self.reader.read(self.key, size=size, offset=offset, max_size=self.size)

    def __len__(self):
        return self.size
