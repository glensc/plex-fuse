from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.vfs.Playable import Playable

if TYPE_CHECKING:
    from plexapi.video import Movie


class MovieEntry(Playable):
    def __init__(self, item: Movie):
        super().__init__(item)
