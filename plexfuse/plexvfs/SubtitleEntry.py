from __future__ import annotations

from plexfuse.plexvfs.Playable import Playable


class SubtitleEntry:
    def __init__(self, playable: Playable):
        self.playable = playable
