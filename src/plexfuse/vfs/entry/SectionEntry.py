from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.normalize import normalize
from plexfuse.vfs.entry.EpisodeEntry import EpisodeEntry
from plexfuse.vfs.entry.MovieEntry import MovieEntry
from plexfuse.vfs.entry.SeasonEntry import SeasonEntry

if TYPE_CHECKING:
    from plexfuse.plex.types import SectionTypes


class SectionEntry:
    def __init__(self, section: SectionTypes):
        self.section = section
        self.title: str = normalize(section.title)
        self.type: str = section.type

    @cached_property
    def items(self):
        return [MovieEntry(m) for m in self.section.search()]

    @cached_property
    def items_by_title(self):
        return dict({(m.title, m) for m in self.items})

    @cached_property
    def seasons(self):
        return [SeasonEntry(s) for s in self.section.search(libtype="season")]

    @cached_property
    def episodes(self):
        return [EpisodeEntry(m) for m in self.section.search(libtype="episode")]

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self)
