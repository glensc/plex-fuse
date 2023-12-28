import logging

from plexapi.media import MediaPart

from plexfuse.plex.PlexApi import PlexApi

logger = logging.getLogger(__name__)


def test_file():
    plex = PlexApi()
    path = "/library/metadata/1"
    filename = "1.webm"

    item = plex.fetch_item(path)
    part: MediaPart = plex.part_by_filename(item, filename)
    if part:
        savepath = plex.cache_path(part)
        logger.error(savepath)
        plex.download_part(part)
