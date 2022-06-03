from __future__ import annotations

from src.terminal.action import Action
from src.terminal.menu import ActionMenu


class Terminal:
    def __init__(self, entrypoint: ActionMenu = None):
        self.entrypoint = entrypoint

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have at least 1 menu registered.')
        self.entrypoint.run()


class MyTerminal(Terminal):
    def __init__(self):

        main = ActionMenu('LinkedIn Job Search Assistant')
        main.register_menu_option(Action('test', lambda: print('testing')))
        main.register_menu_option(Action('another one', lambda: print('another one')))

        super().__init__(main)
