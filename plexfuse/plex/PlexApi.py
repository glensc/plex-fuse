from __future__ import annotations

from functools import cache, cached_property
from os import makedirs
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING

from plexapi.server import PlexServer

from plexfuse.plexvfs.LibraryEntry import LibraryEntry
from plexfuse.plexvfs.PlexMatch import PlexMatch
from plexfuse.plexvfs.SectionEntry import SectionEntry

if TYPE_CHECKING:
    from plexapi.media import MediaPart
    from plexapi.video import Episode, Movie, Show


class PlexApi:
    CACHE_PATH = Path("cache")
    CACHE_VERSION = str(2)
    CHUNK_SIZE = 1024 * 1024 * 16

    @cached_property
    def server(self):
        return PlexServer()

    @property
    def session(self):
        return self.server._session

    @property
    def token(self):
        return self.server._token

    @cached_property
    def library(self):
        return LibraryEntry(self.server.library)

    @cached_property
    def sections(self) -> list[SectionEntry]:
        return self.library.sections

    @property
    def section_types(self) -> set[str]:
        return self.library.section_types

    def sections_by_type(self, type: str) -> list[SectionEntry] | None:
        try:
            return self.library.sections_by_type[type]
        except KeyError:
            return None

    def section_by_title(self, title: str) -> SectionEntry | None:
        try:
            return self.library.section_by_title[title]
        except KeyError:
            return None

    def library_items(self, library: str):
        try:
            return self.library.section_by_title[library].items
        except KeyError:
            return None

    def library_item(self, library: str, title: str):
        try:
            return self.library.section_by_title[library].items_by_title[title]
        except KeyError:
            return None

    @cache
    def all_seasons(self, library):
        try:
            return self.library.section_by_title[library].seasons
        except KeyError:
            return None

    @cache
    def all_episodes(self, library):
        try:
            return self.library.section_by_title[library].episodes
        except KeyError:
            return None

    def show_seasons(self, library: str, title: str):
        show: Show = self.library_item(library, title)
        if not show:
            return None
        return [season for season in self.all_seasons(library)
                if season.item.parentRatingKey == show.item.ratingKey]

    def season_episodes(self, library: str, show_title: str, season_name: str):
        try:
            rating_key = [m.item.ratingKey
                          for m in self.show_seasons(library, show_title)
                          if m.title == season_name][0]
        except IndexError:
            return None

        return [m for m in self.all_episodes(library) if m.item.parentRatingKey == rating_key]

    def episode_files(self, library: str, show_title: str, season_name: str, episode_title: str):
        episode = self.show_episode(library, show_title, season_name, episode_title)
        if not episode:
            return None
        parts = self.media_part_names(episode.item)
        if parts is None:
            return None
        return list(parts)

    def episode_part(self, library: str, show_title: str, season_name: str, episode_title: str, part_name: str):
        episode = self.show_episode(library, show_title, season_name, episode_title)
        if not episode:
            return None
        part = self.media_parts_by_name(episode.item, part_name)
        return part

    def show_episode(self, library: str, show_title: str, season_name: str, episode_title: str):
        show: Show = self.library_item(library, show_title)
        if not show:
            return None

        episodes = self.season_episodes(library, show_title, season_name)
        try:
            return [episode for episode in episodes if episode.title == episode_title][0]
        except IndexError:
            return None

    @cached_property
    def plexmatch(self):
        return PlexMatch()

    def plexmatch_content(self, library: str, title: str):
        playable = self.library_item(library, title)
        if not playable:
            return None

        return self.plexmatch.content(playable)

    def media_part_names(self, item: Movie | Episode):
        if item is None:
            return None
        yield from (fn for fn, part in self.media_parts(item))
        if item.type == "movie":
            yield ".plexmatch"

    def media_parts_by_name(self, item: Movie | Episode, filename: str) -> MediaPart | None:
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
        return self.library.library.fetchItem(key)

    def cache_path(self, path: str):
        """Return cache path of item consisting machine uuid and a path"""
        return \
            self.CACHE_PATH \
            / self.server.machineIdentifier \
            / self.CACHE_VERSION \
            / path.lstrip("/")

    def request_file(self, key: str, size=None, offset=None):
        url = self.url(key)
        headers = {"X-Plex-Token": self.token}
        accepted_status = (200, 201, 204)
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
        if offset is not None:
            if size is not None:
                headers["Range"] = f"bytes={offset}-{offset + size - 1}"
            else:
                headers["Range"] = f"bytes={offset}-"
            accepted_status = (206,)
        elif size is not None:
            raise ValueError("size not supported without offset")

        response = self.session.get(url, headers=headers, stream=True)
        if response.status_code not in accepted_status:
            message = f"({response.status_code}): {response.url}"
            raise RuntimeError(message)

        yield from response.iter_content(chunk_size=self.CHUNK_SIZE)

    def download_part(self, key: str, savepath: Path,
                      size=None, offset=None, overwrite=False):
        if overwrite is False and savepath.exists():
            return savepath

        content = self.request_file(key, size, offset)
        makedirs(savepath.parent, exist_ok=True)
        with open(savepath, "wb") as handle:
            for chunk in content:
                handle.write(chunk)

        return savepath
