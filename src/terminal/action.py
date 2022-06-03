import json
from datetime import datetime, timezone

from src.terminal.component import Component
from src.terminal.enums import ComponentType
from src.terminal.menus.action_args_menu import ActionArgsMenu
from src.terminal.utils import pprint


class Action(Component):
    def __init__(self, name, func):
        super().__init__(ComponentType.Action, name)
        self.func = func
        self.args = {}
        self.args_menu = ActionArgsMenu(f'{name} : Args Menu', self.args)
        self.executions = []

    def run(self):
        keep_running, results = True, []

        while keep_running:
            self.execute()
            self.print('Would you like to rerun this function? y/n')
            keep_running = self.input() == 'y'

        return self.executions

    def prompt_args_modifications(self):
        self._show_current_args()
        print('Would you like to modify them? y/n')
        response = self.input()

        while response == 'y':
            self.args_menu._prompt_menu_option_selection()
            self._show_current_args()
            self.print('Would you like to modify them? y/n')
            response = self.input()

    def _show_current_args(self):
        self.print('Here are this run\'s current parameters:')
        self.pprint(self.args, newline_before=True, newline_after=True)

    def _execute(self):
        start = datetime.now(timezone.utc)
        result = self.func(**self.args)
        end = datetime.now(timezone.utc)

        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'result': result,
            'params': self.args,
            'performance': {
                'start': start.isoformat(),
                'end': end.isoformat(),
                'elapsed': str(end - start)
            }
        }

    def execute(self):
        self.show_name()
        self.print(f'Preparing to execute function: "{self.name}()"')
        self.prompt_args_modifications()

        self.print(f'Running function: "{self.name}"')
        self.print()
        execution = self._execute()
        self.print()

        self.print(f'Execution details: {self.pprint(execution)}')
        self.print()
        self.executions.append(execution)
