from __future__ import annotations

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

        return {
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
