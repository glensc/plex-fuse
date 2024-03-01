from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.cache.FileCache import FileCache

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class ChunkedFile:
    def __init__(self, plex: PlexApi):
        super().__init__()
        self.plex = plex
        self.chunk_size = plex.CHUNK_SIZE
        self.files = FileCache()

    def read(self, path: str, offset: int, size: int, max_size: int):
        # To avoid reading beyond end of file, adjusting size
        if offset + size > max_size:
            size = max_size - offset
        chunk_number = self.chunk_number(offset)
        chunk_offset = self.chunk_offset(offset)

        reads = []
        while size > 0:
            cache_path = self.cache_path(path, chunk_number)

            with self.files.cached_fh(cache_path) as fp:
                fp.seek(chunk_offset)
                buffer = fp.read(size)
                read_bytes = len(buffer)
                size -= read_bytes
                reads.append(buffer)

            chunk_offset = 0
            chunk_number += 1

        return b"".join(reads)

    def cache_path(self, path: str, chunk_number: int):
        file = self.plex.cache_path(path)
        filename = f"{file.stem}-{self.chunk_size}-{chunk_number}{file.suffix}"
        cache_path = file.parent / filename

        if not cache_path.exists():
            print(f"Downloading: {cache_path}")
            base_offset = self.base_offset(chunk_number)
            self.plex.download_part(path, cache_path,
                                    offset=base_offset, size=self.chunk_size)

        return cache_path

    def base_offset(self, chunk_number: int):
        """ return absolute offset where chunk numner starts """
        return self.chunk_size * chunk_number

    def chunk_number(self, offset: int):
        """ return chunk number where the absolute offset would be """
        return offset // self.chunk_size

    def chunk_offset(self, offset: int):
        """ return relative offset in chunk for absolute offset """
        chunk_number = self.chunk_number(offset)
        base_offset = self.base_offset(chunk_number)
        return offset - base_offset
