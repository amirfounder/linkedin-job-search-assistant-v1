from typing import Any

from src.terminal.menus.base import Menu
from src.terminal.enums import MenuType
from src.terminal.utils import try_convert_input


class ActionArgsMenu(Menu):
    def __init__(self, name, args: dict[str, Any]):
        super().__init__(MenuType.ParameterMenu, name)
        self.args = args
        self.options = {}

        for k, v in args.items():
            self.options[self.next_letter] = k

    def run(self):
        self.prompt_menu_option_selection()

    def prompt_menu_option_selection(self):
        self.show_menu_options()
        selected_option_key = self.input()

        while selected_option_key not in self.options:
            if selected_option_key == 'N':
                self.prompt_menu_option_registration()

            self.show_menu_options()
            selected_option_key = self.input()

        name = self.options[selected_option_key]
        value = self.args[name]

        print(f'Enter new value for parameter: {name}')
        
        new_value = self.input()
        new_value = try_convert_input(new_value)

        print(f'Overwriting parameter: {name}: {value} with {new_value}')
        self.args[name] = new_value

    def prompt_menu_option_registration(self):
        key = self.next_letter

        self.print('Registering a new arg...')
        self.print('Please enter the name of the function arg:')
        name = self.input()
        self.print('Please enter the value of the function arg:')
        value = self.input()

        self.options[key] = name
        self.args[name] = value

        print(f'Successfully registered a new function argument: ({key}) {name}: {value}')

    def show_menu_options(self):
        self.show_name()
        print('Displaying menu ... (Select a key or \'X\' to exit to main menu)\n')

        for key, name in self.options.items():
            value = self.args[name]
            print(f'{key}) Overwrite parameter: {name}: {value}')

        print('N) Register new parameter ...')
