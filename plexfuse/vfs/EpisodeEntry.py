from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.vfs.Playable import Playable

if TYPE_CHECKING:
    from plexapi.video import Episode


class EpisodeEntry(Playable):
    def __init__(self, item: Episode):
        super().__init__(item)
