from __future__ import annotations

import os
import os.path
import socket
from threading import Thread
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.control.Control import Control


class ControlListener:
    def __init__(self, path: str, control: Control):
        self.path = path
        self.control = control
        self.thread = None
        self.socket = None

    def start(self):
        self.socket = self.listen_socket()
        self.thread = self.create_thread(self.handle)

        return self

    def stop(self):
        self.close_socket()
        self.stop_thread()

    @staticmethod
    def create_thread(handler):
        thread = Thread(target=handler, daemon=True)
        thread.start()
        return thread

    def stop_thread(self):
        if self.thread is None:
            return

        if self.thread.is_alive():
            self.thread.join()

        self.thread = None

    def listen_socket(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.path)
        server.listen()

        return server

    def close_socket(self):
        socket = self.socket
        self.socket = None
        socket.close()
        if os.path.exists(self.path):
            os.unlink(self.path)

    def handle(self):
        while True:
            try:
                conn, addr = self.socket.accept()
            except ConnectionAbortedError as e:
                print(e)
                # Server is shutting down
                if not self.socket:
                    print("No more socket, exiting")
                    return
                continue

            datagram = conn.recv(128)
            if datagram:
                tokens = datagram.decode().strip().split()
                if tokens[0] in self.control.commands:
                    response = self.control.action(tokens[0])
                    conn.send(response)
                else:
                    conn.send(b"Bye\n")
            conn.close()
