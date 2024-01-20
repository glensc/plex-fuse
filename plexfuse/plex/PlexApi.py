from __future__ import annotations

from functools import cache, cached_property
from os import makedirs
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING

from plexapi.server import PlexServer

from plexfuse.plex.PlexVFSMovie import PlexVFSMovie
from plexfuse.plex.PlexVFSSection import PlexVFSSection

if TYPE_CHECKING:
    from plexapi.media import MediaPart
    from plexapi.video import Movie

    from plexfuse.plex.types import SectionTypes


class PlexApi:
    CACHE_PATH = Path("cache")
    CACHE_VERSION = str(2)

    @cached_property
    def server(self):
        return PlexServer()

    @property
    def session(self):
        return self.server._session

    @property
    def token(self):
        return self.server._token

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
        return {PlexVFSSection(s) for s in self.sections if s.type == type}

    def section_by_title(self, title: str) -> SectionTypes | None:
        it = (s for s in self.sections if s.title == title)

        try:
            return next(it)
        except StopIteration:
            return None

    @cache
    def library_items(self, library: str):
        return set(self._library_items(library))

    def library_items_titles(self, library: str):
        for title, m in self.library_items(library):
            yield PlexVFSMovie(m, title)

    def _library_items(self, library: str):
        section = self.section_by_title(library)
        if section is None:
            return None
        for m in section.search():
            # Handle directory separator in filename
            title = m.title.replace("/", "∕")
            year = m.__dict__.get("year", None)
            if m.TYPE != "artist" and year:
                title += f" ({year})"

            guids = m.guids if m.guid.startswith("plex://") else []
            for guid in guids:
                title += f" {{{guid.id.replace('://', '-')}}}"
            yield title, m

    def library_item(self, library: str, title: str):
        it = (m for m_title, m in self.library_items(library) if m_title == title)

        try:
            return next(it)
        except StopIteration:
            return None

    def media_part_names(self, item: Movie):
        if item is None:
            return None
        yield from (fn for fn, part in self.media_parts(item))

    def media_parts_by_name(self, item: Movie, filename: str) -> MediaPart | None:
        it = (part for fn, part in self.media_parts(item)
              if PureWindowsPath(part.file).name == filename)

        try:
            return next(it)
        except StopIteration:
            return None

    @staticmethod
    def media_parts(item: Movie):
        for media in item.media:
            for part in media.parts:
                # Remove directory part (Windows server on Unix)
                # We need to handle Windows and Unix differences,
                # hence the PureWindowsPath class
                yield PureWindowsPath(part.file).name, part

    def url(self, key: str, include_token=False):
        return self.server.url(key, includeToken=include_token)

    def fetch_item(self, key: str):
        return self.library.fetchItem(key)

    def cache_path(self, item):
        """Return cache path of item consisting machine uuid and item key"""
        return \
            self.CACHE_PATH \
            / self.server.machineIdentifier \
            / self.CACHE_VERSION \
            / item.key.lstrip("/")

    def download_part(self, part, overwrite=False):
        url = self.url(part.key)
        headers = {"X-Plex-Token": self.token}
        response = self.session.get(url, headers=headers, stream=True)
        if response.status_code not in (200, 201, 204):
            errtext = response.text.replace("\n", " ")
            message = f"({response.status_code}): {response.url} {errtext}"
            raise RuntimeError(message)

        savepath = self.cache_path(part)
        if overwrite is False and savepath.exists():
            return savepath

        makedirs(Path(savepath).parent, exist_ok=True)

        with open(savepath, "wb") as handle:
            for chunk in response.iter_content(chunk_size=None):
                handle.write(chunk)
