from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexapi.server import PlexServer

if TYPE_CHECKING:
    from plexapi.library import (MovieSection, MusicSection, PhotoSection,
                                 ShowSection)

    SectionTypes = MovieSection | ShowSection | MusicSection | PhotoSection


class PlexApi:
    @cached_property
    def server(self):
        return PlexServer()

    @property
    def library(self):
        return self.server.library

    @cached_property
    def sections(self) -> list[SectionTypes]:
        return self.library.sections()

    @property
    def section_types(self) -> set[str]:
        return {s.type for s in self.sections}

    def sections_by_type(self, type: str) -> set[str]:
        return {s.title for s in self.sections if s.type == type}
