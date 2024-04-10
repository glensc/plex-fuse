from plexfuse.vfs.entry.ControlSockEntry import ControlSockEntry


class ControlVFS:
    CONTROL_SOCK = "control.sock"

    def __init__(self, control_path: str = None):
        self.control_path = control_path

    @property
    def root(self):
        if self.control_path is None:
            return []

        return [
            self.CONTROL_SOCK,
        ]

    def handle(self, pc: int, pe: list[str]):
        if self.control_path is None:
            return
        if pc == 1 and pe[0] == self.CONTROL_SOCK:
            return ControlSockEntry(pe[0], self.control_path)
