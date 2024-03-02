from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class Monitor:
    def __init__(self, plex: PlexApi):
        self.plex = plex
        self.notifier = None

    def start(self):
        self.notifier = self.plex.server.startAlertListener(
            callback=self.event_handler,
            callbackError=self.event_handler,
        )
        self.notifier.start()
        print("Started notifier:", self.notifier)

    def stop(self):
        if not self.notifier:
            return
        print("Stopping notifier:", self.notifier)
        if self.notifier.is_alive():
            self.notifier.join()
        self.notifier = None

    @property
    def is_alive(self):
        return self.notifier and self.notifier.is_alive()

    @staticmethod
    def event_handler(data):
        print("plex event: ", data)
