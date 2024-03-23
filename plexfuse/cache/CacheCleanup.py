import time
from datetime import timedelta
from functools import cached_property

from timeloop import Timeloop

tl = Timeloop()


class CacheCleanup:
    def __init__(self):
        ...

    def start(self):
        return tl.start()

    def stop(self):
        return tl.stop()

    @cached_property
    def loop(self):
        return Timeloop()

    @tl.job(interval=timedelta(seconds=5))
    def cleanup(self):
        print("run cleanup:", time.ctime())
