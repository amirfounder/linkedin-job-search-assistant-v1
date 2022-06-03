from datetime import datetime, timezone
from src.terminal.base import Component
from src.terminal.enums import ComponentType
from src.terminal.menu import ActionArgsMenu


class Action(Component):
    def __init__(self, name, func, params=None):
        super().__init__(ComponentType.Action, name)
        self.func = func
        self.args_menu = ActionArgsMenu(f'{name} : Args Menu')
        self.executions = []

    def run(self):
        self.execute()

    def execute(self):
        print(f'Preparing to execute action: {self.name}')
        print('Here are this run\'s current parameters:\n')

        print(self.args_menu)

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