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

    def execute(self):
        print(f'Preparing to execute action: {self.name}')
        print('Here are this run\'s current parameters:\n')

        print(self.args)

        print('Would you like to modify them?\n(y)es | (n)o\n')
        response = input()

        if response.lower() == 'y':
            self.args_menu.prompt_menu_option_selection()

        result = self.func(**self.args)

        self.executions.append({
            'timestamp': datetime.now(timezone.utc),
            'result': result,
            'params': self.args
        })

        print(self.executions[-1])
        return result
