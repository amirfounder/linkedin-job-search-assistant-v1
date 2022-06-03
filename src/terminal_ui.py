from __future__ import annotations
from typing import Optional
from string import ascii_lowercase


class Terminal:
    def __init__(self):
        self.entrypoint: Optional[Menu] = None
        
        main = Menu('LinkedIn Job Search Assistant')
        outreach = Menu('Recruiter Outreach Menu')
        prospecting = Menu('Recruiter Prospecting Menu')

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have at least 1 menu registered.')
        
        self.entrypoint.show_name()
        self.entrypoint.show_menu()


class Menu:
    def __init__(self, name):
        self.name = name
        self.menu = [{}, {}]

    def register(self, item: Menu | Action):
        key = ascii_lowercase[len(self.menu)]
        idx = 0 if isinstance(item, Menu) else 1
        self.menu[idx][key] = item

    def show_name(self):
        print(f'### {self.name} ###')

    def show_menu(self):
        print('Displaying menu ... (Press a key to select or \'ESC\' to exit to main menu)\n')

        for key, item in self.menu[0].items():
            print(f'{key} ... Navigate to menu: {item.name}')

        for key, item in self.menu[1].items():
            print(f'{key} ... Execute action: {item.name}')


class Action:
    def __init__(self, name, fn, fn_params):
        self.name = name
        self.fn = fn
        self.fn_params = fn_params
        self.results = []

    def execute(self):
        print(f'Preparing to execute action: {self.name}')
        print('Select parameters:')
        self.results.append(self.fn(self.fn_params))
