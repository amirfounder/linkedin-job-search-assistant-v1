from string import ascii_lowercase
from typing import Optional

from src.terminal.v2.nodes import ExitNode, Node


class Menu:
    def __init__(self, name: str, options: list[Node]):
        self.name = name
        self.options = {}
        self._next_key_idx = 0
        self._next_key = None

        for option in options:
            key = self.next_key
            while key in self.options:
                key = self.next_key

            self.options[key] = option

    @property
    def next_key_idx(self):
        res = self._next_key_idx
        self._next_key_idx += 1
        return res

    @property
    def next_key(self):
        return ascii_lowercase[self.next_key_idx]

    def show_options(self):
        for option, node in self.options.items():
            print(f'{option}) {node.name}')
        print()

    def add_option(self, option: Node):
        self.options[self.next_key] = option


class MenuFactory:
    def __init__(self, terminal):
        self.terminal = terminal
        self._menus = []

    def create(self, name: str, options: Optional[list[Node]] = None):
        options.append(ExitNode(self.terminal))
        self._menus.append(Menu(name, options or []))
        return self._menus[-1]