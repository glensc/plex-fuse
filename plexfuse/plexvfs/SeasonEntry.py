from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.normalize import normalize

if TYPE_CHECKING:
    from plexapi.video import Season


class SeasonEntry:
    def __init__(self, item: Season):
        self.item = item
        self.title = normalize(item.title)

    def __str__(self):
        return self.title
