from plexfuse.plex.ChunkedFile import ChunkedFile
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.PlexVFS import PlexVFS


def test_file():
    plex = PlexApi()
    plexvfs = PlexVFS(plex)
    cf = ChunkedFile(plex, plexvfs)
    cf.chunk_size = 16

    key = "/library/parts/38908/1705801932/file.avi"
    # A test reading first chunk
    assert len(cf.read(key, 0, cf.chunk_size)) == cf.chunk_size
    # A test reading chunk that spans two chunk
    assert len(cf.read(key, int(cf.chunk_size / 2), cf.chunk_size)) == cf.chunk_size
