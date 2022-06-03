from src.terminal.v2.menus import MenuFactory
from src.terminal.v2.nodes import NodeFactory


class Terminal:
    def __init__(self):
        self.entrypoint = None
        self.nodes = NodeFactory(self)
        self.menus = MenuFactory(self)
        self.stack = []

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have an entrypoint node')

        self.entrypoint.run()
