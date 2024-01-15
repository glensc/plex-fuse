import errno

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.fs.PlexVFS import PlexVFS
from plexfuse.plex.PlexApi import PlexApi


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.plex = PlexApi()
        self.vfs = PlexVFS(self.plex)

    def getattr(self, path: str):
        st = PlexDirectory()

        if path == "/":
            st.st_nlink = 2 + len(self.vfs[path])
            return st

        pe = path.split("/")[1:]
        pc = len(pe)

        if pc == 1 and pe[0] in self.plex.section_types:
            st.st_nlink = 2 + len(self.vfs[path])
        elif pc == 2 and pe[1] in self.plex.sections_by_type(pe[0]):
            st.st_nlink = 2 + len(self.vfs[path])
        elif pc == 3 and pe[2] in self.plex.library_items_titles(pe[1]):
            st.st_nlink = 2 + len(self.vfs[path])
        elif pc == 4 and pe[0] == "movie":
            part = self.vfs[path][0]

            return PlexFile(st_size=part.size)
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path: str, offset: int):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            for r in self.vfs[path]:
                yield fuse.Direntry(r)
        except ValueError as e:
            print(e)
