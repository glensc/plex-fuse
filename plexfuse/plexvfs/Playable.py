from __future__ import annotations

from functools import cached_property
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING

from plexfuse.normalize import normalize

if TYPE_CHECKING:
    from plexapi.media import Guid, MediaPart, SubtitleStream
    from plexapi.video import Episode, Movie


class Playable:
    def __init__(self, item: Episode | Movie):
        self.item = item

    def __str__(self):
        return self.title

    @property
    def timestamps(self):
        return {
            "st_ctime": self.ctime,
            "st_atime": self.atime,
            "st_mtime": self.mtime,
        }

    @property
    def ctime(self):
        return self.item.addedAt.timestamp()

    @property
    def atime(self):
        try:
            return self.item.lastViewedAt.timestamp()
        except AttributeError:
            return self.mtime

    @property
    def mtime(self):
        return self.item.updatedAt.timestamp()

    @property
    def guids(self) -> list[Guid]:
        return self.item.guids if self.item.guid.startswith("plex://") else []

    @cached_property
    def title(self):
        title = f"{self.item.seasonEpisode} " if self.item.TYPE == "episode" else ""
        title += self.item.title
        year = self.item.__dict__.get("year", None)
        if year:
            title += f" ({year})"

        for guid in self.guids:
            title += f" {{{guid.id.replace('://', '-')}}}"

        return normalize(title)

    @cached_property
    def subtitles(self):
        # Use basename of movie file if there's only one part
        basename = Path(next(iter(self.media_parts))).stem if len(self.media_parts) == 1 else None

        def inner():
            s: SubtitleStream
            for s in self.item.subtitleStreams():
                if s.key is None:
                    # Not downloadable. Embedded in video
                    continue
                if basename:
                    title = f"{basename}.{s.languageCode}.{s.codec}"
                else:
                    title = f"{s.language} ({s.languageCode}).{s.codec}"
                yield title, s

        return dict(inner())

    @cached_property
    def media_parts(self):
        def inner():
            part: MediaPart
            for part in self.item.iterParts():
                # Remove directory part (Windows server on Unix)
                # We need to handle Windows and Unix differences,
                # hence the PureWindowsPath class
                yield PureWindowsPath(part.file).name, part

        return dict(inner())
