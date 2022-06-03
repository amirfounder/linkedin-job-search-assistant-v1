from __future__ import annotations


class Terminal:
    def __init__(self, entrypoint=None):
        self.entrypoint = entrypoint
        self.stack = []

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have an entrypoint.')

        self.entrypoint.register_terminal(self)
        self.entrypoint.run()
