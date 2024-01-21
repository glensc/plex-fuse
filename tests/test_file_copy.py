import logging

from plexfuse.plex.PlexApi import PlexApi

logger = logging.getLogger(__name__)


def test_file():
    plex = PlexApi()
    path = "/library/metadata/1"
    filename = "1.webm"

    item = plex.fetch_item(path)
    part = plex.media_parts_by_name(item, filename)
    if part:
        savepath = plex.cache_path(part.key)
        logger.error(savepath)
        plex.download_part(part.key, savepath)
