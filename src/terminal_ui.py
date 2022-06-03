from __future__ import annotations

from datetime import timezone, datetime
from typing import Optional
from string import ascii_lowercase


class Terminal:
    def __init__(self):
        self.entrypoint: Optional[Menu] = None
        
        main = Menu('LinkedIn Job Search Assistant')
        main.register(Action('test', lambda x: f'testing: {x}'))

        self.entrypoint = main

    def run(self):
        if not self.entrypoint:
            raise Exception('Terminal must have at least 1 menu registered.')
        
        self.entrypoint.show_menu()


class Menu:
    def __init__(self, name):
        self.name = name
        self.menu = [{}, {}]

    def register(self, item: Menu | Action):
        key = ascii_lowercase[len(self.menu)]
        idx = 0 if isinstance(item, Menu) else 1
        self.menu[idx][key] = item

    def show_menu(self):
        print(f'### {self.name} ###')
        print('Displaying menu ... (Select a key or \'ESC\' to exit to main menu)\n')

        for key, item in self.menu[0].items():
            print(f'{key} ... Navigate to menu: {item.name}')

        for key, item in self.menu[1].items():
            print(f'{key} ... Execute action: {item.name}')


class Action:
    def __init__(self, name, func, params = None):
        self.name = name
        self.func = func
        self.params = {}
        self.executions = []

        if params:
            for k, v in params.items():
                self.params[ascii_lowercase[len(self.params)]] = [k, v]

    def execute(self):
        print(f'Preparing to execute action: {self.name}')
        print('Here are this run\'s current parameters:\n')
        
        self.prompt_instance_parameters()
        
        print('Would you like to modify them?\n(y)es | (n)o\n')
        response = input()
        
        if response.lower() == 'y':
            self.prompt_instance_parameters()
            
        result = self.func(self.params)

        self.executions.append({
            'timestamp': datetime.now(timezone.utc),
            'result': result,
            'params': self.params
        })

        return result

    def display_params_menu(self):
        for k, v in self.params.items():
            print(f'{k} ... Set value for {v[0]}. Current value is "{v[1]}"')
        print('\n')

    def prompt_instance_parameters(self):
        print('Setting parameter for this run...')

        self.display_params_menu()
        key = input()

        while key not in self.params:
            if key == 'esc':
                return

            print('Invalid key entered. Please try again ...')
            self.display_params_menu()
            key = input()

        name, value = self.params[key]

        print(f'Valid key entered! Setting parameter "{name}". Enter a value to overwrite existing: {value} ...')

        new_value = input()
        new_value = self.try_convert_to_bool(new_value)

        self.params[key][2] = new_value

    @staticmethod
    def try_convert_to_bool(value):
        if value.lower() not in ['true', 'false']:
            return value

        if value.endswith('-y'):
            response = 'y'
        else:
            print(f'Would you like us to convert your response, "{value}", to bool type?\n(y)es OR (n)o')
            response = input()

        if response == 'y':
            value = True if value.lower() == 'true' else False

        return value

