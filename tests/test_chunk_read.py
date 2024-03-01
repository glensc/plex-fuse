from plexfuse.plex.PlexApi import PlexApi
from plexfuse.vfs.ChunkedFile import ChunkedFile


def test_file():
    plex = PlexApi()
    cf = ChunkedFile(plex)
    cf.chunk_size = 16

    key = "/library/parts/38908/1705801932/file.avi"
    # A test reading first chunk
    assert len(cf.read(key, 0, cf.chunk_size)) == cf.chunk_size
    # A test reading chunk that spans two chunk
    assert len(cf.read(key, int(cf.chunk_size / 2), cf.chunk_size)) == cf.chunk_size

    # A test that chunked content is full content
    cf.chunk_size = 6
    offset = 8
    size = 8
    chunked = cf.read(key, offset, size)
    cf.chunk_size = 1024
    unchunked = cf.read(key, offset, size)
    assert chunked == unchunked
