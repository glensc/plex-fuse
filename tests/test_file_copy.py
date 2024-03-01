import logging

from plexfuse.plex.PlexApi import PlexApi
from plexfuse.vfs.entry.MovieEntry import MovieEntry

logger = logging.getLogger(__name__)


def test_file():
    plex = PlexApi()
    path = "/library/metadata/1"
    filename = "1.webm"

    item = plex.fetch_item(path)
    media = MovieEntry(item)
    part = plex.media_parts_by_name(media, filename)
    if part:
        savepath = plex.cache_path(part.key)
        logger.error(savepath)
        plex.download_part(part.key, savepath)
