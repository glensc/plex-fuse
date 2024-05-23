from time import time


class Timestampable:
    def __init__(self, **kw):
        if self.st_ctime == 0:
            self.st_ctime = int(time())
            self.st_atime = self.st_ctime
            self.st_mtime = self.st_ctime
