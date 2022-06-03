from __future__ import annotations

from datetime import timezone, datetime
from typing import Optional
from string import ascii_lowercase

from src.terminal.action import Action
from src.terminal.menu import ActionMenu


class Terminal:
    def __init__(self):
        self.entrypoint: Optional[ActionMenu] = None
        
        main = ActionMenu('LinkedIn Job Search Assistant')
        main.register_menu_option(Action('test', lambda x: f'testing: {x}'))

        self.entrypoint = main

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have at least 1 menu registered.')
        
        self.entrypoint.run()

