from plexfuse.plex.ChunkedFile import ChunkedFile
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.PlexVFS import PlexVFS


def test_file():
    plex = PlexApi()
    plexvfs = PlexVFS(plex)
    cf = ChunkedFile(plex, plexvfs)
    cf.chunk_size = 16

    assert cf.chunk_number(0) == 0
    assert cf.chunk_number(1) == 0
    assert cf.chunk_number(16) == 1
    assert cf.chunk_number(17) == 1
    assert cf.chunk_number(31) == 1

    assert cf.base_offset(0) == 0
    assert cf.base_offset(1) == 16
    assert cf.base_offset(2) == 32

    assert cf.chunk_offset(15) == 15
    assert cf.chunk_offset(16) == 0
    assert cf.chunk_offset(17) == 1
    assert cf.chunk_offset(31) == 15
    assert cf.chunk_offset(32) == 0
