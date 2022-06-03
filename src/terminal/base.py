from abc import abstractmethod, ABC
from string import ascii_lowercase
from typing import Callable, Any

from src.terminal.enums import ComponentType, MenuType


class Component(ABC):
    def __init__(self, component_type: ComponentType, name):
        self.component_type = component_type
        self.name = name

    @staticmethod
    def input():
        res = input('>> ')
        print()
        return res

    def show_name(self):
        title = f'---  {self.component_type}: {self.name}  ---'
        border = '-' * len(title)
        print(border)
        print(title)
        print(border)
        print()

    @abstractmethod
    def run(self):
        pass


class InputConverter:
    @staticmethod
    def try_convert_input(
            value: str,
            to: type,
            validation_fn: Callable[[str], Any],
            conversion_fn: Callable[[str], Any]
    ):
        if not validation_fn(value):
            return value

        if value.endswith(' -y'):
            should_convert = 'y'
        else:
            print(f'Convert value, "", to {to}? y/n')
            should_convert = input()

        if should_convert:
            value = conversion_fn(value)

        return value

    @classmethod
    def try_convert_input_to_bool(cls, value: str) -> bool:
        return cls.try_convert_input(
            value=value,
            to=bool,
            validation_fn=lambda v: v.lower() not in ['true', 'false'],
            conversion_fn=lambda v: True if v.lower() == 'true' else False
        )

    @classmethod
    def try_convert_input_to_decimal(cls, value: str) -> float:
        return cls.try_convert_input(
            value=value,
            to=float,
            validation_fn=lambda v: v.isdecimal(),
            conversion_fn=lambda v: float(v)
        )

    @classmethod
    def try_convert_input_to_int(cls, value) -> int:
        return cls.try_convert_input(
            value=value,
            to=int,
            validation_fn=lambda v: v.isdecimal(),
            conversion_fn=lambda v: int(v)
        )


class Menu(Component, ABC):
    def __init__(self, menu_type: MenuType, name: str):
        super().__init__(ComponentType.Menu, name)
        self.menu_type = menu_type
        self._next_letter_idx = 0

    @property
    def next_letter(self):
        result = ascii_lowercase[self._next_letter_idx]
        self._next_letter_idx += 1
        return result

    @abstractmethod
    def show_menu_options(self):
        pass

    @abstractmethod
    def prompt_menu_option_selection(self):
        pass
