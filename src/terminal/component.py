import json
from abc import abstractmethod, ABC


class Component(ABC):
    def __init__(self, component_type, name, terminal=None):
        self.component_type = component_type
        self.name = name
        self.terminal = terminal

    @staticmethod
    def print(*args, newline_before=False, newline_after=False, **kwargs):
        if newline_before:
            print()

        print(*args, **kwargs)

        if newline_after:
            print()

    def pprint(self, obj: dict, indent=4, **kwargs):
        self.print(json.dumps(obj, indent=indent), **kwargs)

    def input(self):
        self.print()
        res = input('>> ')
        self.print()
        return res

    def register_terminal(self, terminal):
        self.terminal = terminal

    def show_name(self):
        title = f'---  {self.component_type}: {self.name}  ---'
        border = '-' * len(title)
        self.print(border, title, border, sep='\n')
        self.print()

    @abstractmethod
    def run(self):
        pass
