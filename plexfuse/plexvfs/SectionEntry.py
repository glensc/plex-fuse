from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.types import SectionTypes


class SectionEntry:
    def __init__(self, section: SectionTypes):
        self.title: str = section.title
        self.type: str = section.type

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.name
