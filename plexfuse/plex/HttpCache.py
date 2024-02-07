from __future__ import annotations

from datetime import timedelta
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class HttpCache:
    def __init__(self, cache_path: Path):
        self.cache_path = cache_path

    @property
    def urls_expire_after(self):
        from requests_cache import DO_NOT_CACHE

        CACHE_1h = 60 * 60
        CACHE_1d = timedelta(days=1)

        return {
            "*/library/sections/*/all?includeGuids=1": CACHE_1d,
            "*/library/sections/*/all?includeGuids=1&type=3": CACHE_1h,
            "*/library/sections/*/all?includeGuids=1&type=4": CACHE_1h,

            # Some reload
            "*/library/metadata/*": CACHE_1d,

            # default policy is not to cache
            "*": DO_NOT_CACHE,
        }

    @cached_property
    def session(self):
        from requests_cache import CachedSession

        return CachedSession(
            cache_name=str(self.cache_path),
            cache_control=True,
            urls_expire_after=self.urls_expire_after,
        )
