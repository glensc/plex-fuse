from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.media import MediaPart


class PlexVFSFileEntry:
    def __init__(self, part: MediaPart):
        self.size = part.size

    def __len__(self):
        return self.size
