import time
from datetime import timedelta

from timeloop import Timeloop

tl = Timeloop()


class CacheCleanup:
    def __init__(self):
        ...

    @tl.job(interval=timedelta(seconds=5))
    def cleanup(self):
        print("run cleanup:", time.ctime())
