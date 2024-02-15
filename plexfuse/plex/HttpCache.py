from __future__ import annotations

import logging
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

        # Set log levels
        loggers = [
            "requests_cache.session",
            "requests_cache.policy.actions",
            "requests_cache.policy.expiration",
            "requests_cache.backends",
            "requests_cache.backends.base",
            "requests_cache.backends.sqlite",
        ]
        stderr_handler = logging.StreamHandler()

        for name in loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(stderr_handler)

        return CachedSession(
            cache_name=str(self.cache_path),
            # Plex sends "Cache-Control: no-cache" headers
            cache_control=False,
            urls_expire_after=self.urls_expire_after,
            # Plex doesn't Send Vary: X-Plex-Container-Start
            match_headers=['X-Plex-Container-Start'],
        )
