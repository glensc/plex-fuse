from plexfuse.plexvfs.ControlEntry import ControlEntry
from plexfuse.plexvfs.DirEntry import DirEntry


class Control:
    @property
    def root(self):
        return ["control"]

    @property
    def commands(self):
        return ["reload", "status"]

    def reload(self):
        return ""

    def status(self):
        return ""

    def handle(self, pc: int, pe: list[str]):
        if pc == 1 and pe[0] in self.root:
            return DirEntry(self.commands)

        if pc != 2 or pe[0] != self.root[0]:
            return

        if pe[1] in self.commands:
            return ControlEntry(pe[1], getattr(self, pe[1]))
