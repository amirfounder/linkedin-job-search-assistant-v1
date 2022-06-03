from __future__ import annotations

from typing import Optional

from src.terminal.action import Action
from src.terminal.menu import ActionMenu


class Terminal:
    def __init__(self):
        self.entrypoint: Optional[ActionMenu] = None
        
        main = ActionMenu('LinkedIn Job Search Assistant')
        main.register_menu_option(Action('test', lambda: print('testing')))
        main.register_menu_option(Action('another one', lambda : print('another one')))

        self.entrypoint = main

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have at least 1 menu registered.')
        
        self.entrypoint.run()

