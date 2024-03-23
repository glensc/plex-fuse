from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class Monitor:
    def __init__(self, plex: PlexApi):
        self.plex = plex
        self.notifier = None

    def start(self):
        # Perform self-test, like PlexAPI
        try:
            import websocket
        except ImportError:
            print("Can't use Monitor without websocket")
            return None

        del websocket

        self.notifier = self.plex.server.startAlertListener(
            callback=self.event_handler,
            callbackError=self.event_handler,
        )
        print("Started notifier:", self.notifier)
        self.event_handler("test")

        return self

    def stop(self):
        if not self.notifier:
            return

        print("Stopping notifier:", self.notifier)
        self.notifier.stop()

        if self.notifier.is_alive():
            self.notifier.join(timeout=10)
            if self.notifier.is_alive():
                print("Thread for notifier is still alive:", self.notifier)

        self.notifier = None

    @property
    def is_alive(self):
        return self.notifier and self.notifier.is_alive()

    @staticmethod
    def event_handler(data):
        print("plex event: ", data)
