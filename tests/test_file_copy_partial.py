import logging

from plexfuse.plex.PlexApi import PlexApi

logger = logging.getLogger(__name__)


def test_file():
    plex = PlexApi()
    path = "/library/metadata/1"
    filename = "1.webm"

    item = plex.fetch_item(path)
    part = plex.media_parts_by_name(item, filename)
    plex.download_part(part)

    def sizes(gen):
        return list(map(lambda x: len(x), gen))

    assert [1024] == sizes(plex.request_file(part.key, offset=0, size=1024))
    assert [1024] == sizes(plex.request_file(part.key, offset=1024, size=1024))
    assert [512] == sizes(plex.request_file(part.key, offset=1024, size=512))
