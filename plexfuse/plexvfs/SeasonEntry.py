from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.video import Season


class SeasonEntry:
    def __init__(self, item: Season):
        self.title = item.title

    def __str__(self):
        return self.title