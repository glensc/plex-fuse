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
        pe = path.split("/")[1:]
        pc = len(pe)
        st = PlexDirectory()

        if path == "/":
            pass
        elif pc == 1 and pe[0] in self.plex.section_types:
            pass
        elif pc == 2 and pe[1] in self.plex.sections_by_type(pe[0]):
            pass
        elif pc == 3 and pe[2] in self.plex.library_items_titles(pe[1]):
            pass
        elif pc == 4 and pe[0] == "movie" \
                and (m := self.plex.library_item(pe[1], pe[2])) \
                and pe[3] in self.plex.media_part_names(m) \
                and (part := self.plex.media_parts_by_name(m, pe[3])):

            return PlexFile(st_size=part.size)
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path: str, offset: int):
        pe = path.split("/")[1:]
        pc = len(pe)

        dirents = [".", ".."]
        if path == "/":
            dirents.extend(self.vfs["/"])
        elif pc == 1 and pe[0] in self.plex.section_types:
            dirents.extend(self.vfs[path])
        elif pc == 2:
            dirents.extend(self.vfs[path])
        elif pc == 3 and pe[0] == "movie":
            dirents.extend(self.vfs[path])

        for r in dirents:
            yield fuse.Direntry(r)
