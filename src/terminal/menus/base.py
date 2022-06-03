from __future__ import annotations

from abc import ABC, abstractmethod
from string import ascii_lowercase

from src.terminal.component import Component
from src.terminal.enums import MenuType, ComponentType


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
