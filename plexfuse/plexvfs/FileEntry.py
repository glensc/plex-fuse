from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.media import MediaPart


class FileEntry:
    def __init__(self, part: MediaPart):
        self.size = part.size
        self.key = part.key

    def __len__(self):
        return self.size
