from src.terminal.component import Component
from src.terminal.enums import MenuType, ComponentType
from src.terminal.menus.base import Menu


class ActionMenu(Menu):
    def __init__(self, name):
        super().__init__(MenuType.ActionMenu, name)
        self.options: dict[str, Component] = {}

    def run(self):
        self.terminal.stack.append(self)
        self.show_name()
        self._prompt_menu_option_selection()

    def register_menu_option(self, item):
        self.options[self.next_letter] = item

    def _prompt_menu_option_selection(self):
        self._show_menu_options()
        selected_option_key = self.input()

        while selected_option_key not in self.options:
            if selected_option_key == 'X':
                self.print('Exiting menu ...')
                return

            self.print('You have pressed an invalid key. Please try again.')
            self._show_menu_options()

            selected_option_key = self.input()

        selected_option = self.options[selected_option_key]
        selected_option.run()

    def _show_menu_options(self):
        self.print('Displaying menu ... (Select a key or "X" to exit to main menu)\n')

        statements = []
        for k, v in self.options.items():
            if v.component_type == ComponentType.Menu:
                statements.insert(0, f'{k}) Navigate to menu: {v.name}')
            if v.component_type == ComponentType.Action:
                statements.append(f'{k}) Execute action: {v.name}')

        for statement in statements:
            print(statement)
