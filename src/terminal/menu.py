from __future__ import annotations

from typing import Any

from src.terminal.base import Menu, Component, InputConverter
from src.terminal.enums import MenuType, ComponentType


class ActionMenu(Menu):
    def __init__(self, name):
        super().__init__(MenuType.ActionMenu, name)
        self.options: dict[str, Component] = {}

    def run(self):
        self.prompt_menu_option_selection()

    def register_menu_option(self, item):
        self.options[self.next_letter] = item

    def prompt_menu_option_selection(self):
        self.show_menu_options()
        selected_option_key = input()

        while selected_option_key not in self.options:
            self.show_menu_options()
            selected_option_key = input()

        selected_option = self.options[selected_option_key]
        selected_option.run()

    def show_menu_options(self):
        print(f'### {self.name} ###')
        print('Displaying menu ... (Select a key or \'ESC\' to exit to main menu)\n')

        statements = []
        for k, v in self.options.items():
            if v.component_type == ComponentType.Menu:
                statements.insert(0, f'{k} ... Navigate to menu: {v.name}')
            if v.component_type == ComponentType.Action:
                statements.append(f'{k} ... Execute action: {v.name}')

        for statement in statements:
            print(statement)
        print('\n')


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
        selected_option_key = input()

        while selected_option_key not in self.options:
            self.show_menu_options()
            selected_option_key = input()

        name = self.options[selected_option_key]
        value = self.args[name]

        print(f'Enter new value for parameter: {name}')
        new_value = input()

        converters = [
            InputConverter.try_convert_input_to_bool,
            InputConverter.try_convert_input_to_int,
            InputConverter.try_convert_input_to_decimal
        ]

        for converter in converters:
            if isinstance(new_value, str):
                new_value = converter(new_value)

        print(f'Overwriting parameter: {name}: {value} with {new_value}')

    def show_menu_options(self):
        print(f'### {self.name} ###')
        print('Displaying menu ... (Select a key or \'ESC\' to exit to main menu)\n')

        for key, name in self.options.items():
            value = self.args[name]
            print(f'{key} ... Parameter: {name}. Current value: {value}')
        print('\n')
