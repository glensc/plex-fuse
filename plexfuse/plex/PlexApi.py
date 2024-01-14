from __future__ import annotations

from functools import cache, cached_property
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

    def section_by_title(self, title: str) -> SectionTypes:
        return next(s for s in self.sections if s.title == title)

    @cache
    def library_items(self, library: str):
        return set(self._library_items(library))

    def _library_items(self, library: str):
        section = self.section_by_title(library)
        for m in section.search():
            title = m.title
            if m.year:
                title += f" ({m.year})"
            for guid in m.guids:
                title += f" {{{guid.id.replace('://', '-')}}}"
            yield title
