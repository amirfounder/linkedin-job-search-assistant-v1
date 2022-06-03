from datetime import datetime, timezone
from src.terminal.base import Component
from src.terminal.enums import ComponentType
from src.terminal.menu import ActionArgsMenu


class Action(Component):
    def __init__(self, name, func):
        super().__init__(ComponentType.Action, name)
        self.func = func
        self.args = {}
        self.args_menu = ActionArgsMenu(f'{name} : Args Menu', self.args)
        self.executions = []

    def run(self):
        self.execute()

    def show_current_args(self):
        print('Here are this run\'s current parameters:')
        print('')
        print(self.args)
        print('')

    def prompt_args_modifications(self):
        self.show_current_args()
        print('Would you like to modify them? y/n')
        response = input()

        while response == 'y':
            self.args_menu.prompt_menu_option_selection()
            self.show_current_args()
            print('Would you like to modify them? y/n')
            response = input()

    def execute(self):
        self.show_name()
        print(f'Preparing to execute function: "{self.name}()"')
        self.prompt_args_modifications()

        print(f'Running function: "{self.name}()"')

        print()
        result = self.func(**self.args)
        print()

        self.executions.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'result': result,
            'params': self.args
        })
        print(self.executions[-1])
        return result
