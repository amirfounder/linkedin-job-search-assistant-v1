from threading import Thread

from src.terminal.v2.menus import MenuFactory
from src.terminal.v2.nodes import NodeFactory


class Terminal:
    def __init__(self):
        self.entrypoint = None
        self.nodes = NodeFactory(self)
        self.menus = MenuFactory(self)
        self.stack = []
        self.keep_running = True

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have an entrypoint node')

        while self.keep_running:
            self.entrypoint.run()

    def run_in_thread(self, start=True, join=False):
        thread = Thread(target=self.run)
        if start:
            thread.start()
        if join:
            thread.join()
        return thread
