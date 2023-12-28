from functools import cached_property
from os import makedirs
from pathlib import Path, PureWindowsPath

from plexapi.server import PlexServer


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
    def sections(self):
        return self.library.sections()

    @cached_property
    def section_types(self):
        return {s.type for s in self.sections}

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

    def download_part(self, part):
        url = self.url(part.key)
        headers = {"X-Plex-Token": self.token}
        response = self.session.get(url, headers=headers, stream=True)
        if response.status_code not in (200, 201, 204):
            errtext = response.text.replace("\n", " ")
            message = f"({response.status_code}): {response.url} {errtext}"
            raise RuntimeError(message)

        savepath = self.cache_path(part)
        makedirs(Path(savepath).parent, exist_ok=True)

        with open(savepath, "wb") as handle:
            for chunk in response.iter_content(chunk_size=None):
                handle.write(chunk)

    def part_by_filename(self, item, filename):
        for media in item.media:
            for part in media.parts:
                # Remove directory part (Windows server on Unix)
                # We need to handle Windows and Unix differences,
                # hence the PureWindowsPath class
                basename = PureWindowsPath(part.file).name
                if basename == filename:
                    return part
