import errno
from time import time

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory


class PlexFS(fuse.Fuse):
    def getattr(self, path: str):
        st = PlexDirectory()

        st.st_atime = int(time())
        st.st_mtime = st.st_atime
        st.st_ctime = st.st_atime
        if path == "/":
            pass
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path: str, offset: int):
        dirents = [".", ".."]
        for r in dirents:
            yield fuse.Direntry(r)
