from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.plexvfs.MovieEntry import MovieEntry

if TYPE_CHECKING:
    from plexfuse.plex.types import SectionTypes


class SectionEntry:
    def __init__(self, section: SectionTypes):
        self.section = section
        self.title: str = section.title
        self.type: str = section.type

    @property
    def name(self):
        return self.title

    @cached_property
    def items(self):
        return [MovieEntry(m) for m in self.section.search()]

    def __str__(self):
        return self.name
