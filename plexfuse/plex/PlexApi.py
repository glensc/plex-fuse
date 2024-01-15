from __future__ import annotations

from functools import cache, cached_property
from pathlib import PureWindowsPath
from typing import TYPE_CHECKING

from plexapi.server import PlexServer

if TYPE_CHECKING:
    from plexapi.library import (MovieSection, MusicSection, PhotoSection,
                                 ShowSection)
    from plexapi.media import MediaPart
    from plexapi.video import Movie
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

    def library_items_titles(self, library: str):
        for title, m in self.library_items(library):
            yield title

    def _library_items(self, library: str):
        section = self.section_by_title(library)
        for m in section.search():
            title = m.title
            year = m.__dict__.get("year", None)
            if m.TYPE != "artist" and year:
                title += f" ({year})"

            guids = m.guids if m.guid.startswith("plex://") else []
            for guid in guids:
                title += f" {{{guid.id.replace('://', '-')}}}"
            yield title, m

    def library_item(self, library: str, title: str):
        it = (m for m_title, m in self.library_items(library) if m_title == title)
        return next(it)

    def media_part_names(self, item: Movie):
        yield from (fn for fn, part in self.media_parts(item))

    def media_parts_by_name(self, item: Movie, filename: str) -> MediaPart:
        return next(part for fn, part in self.media_parts(item)
                    if PureWindowsPath(part.file).name == filename)

    @staticmethod
    def media_parts(item: Movie):
        for media in item.media:
            for part in media.parts:
                # Remove directory part (Windows server on Unix)
                # We need to handle Windows and Unix differences,
                # hence the PureWindowsPath class
                yield PureWindowsPath(part.file).name, part
