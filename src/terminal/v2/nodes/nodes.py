from __future__ import annotations
from datetime import timezone, datetime
from typing import TYPE_CHECKING, Optional, TypeVar, Type, Callable

from .base import Node

if TYPE_CHECKING:
    from ..terminal import Terminal


class ExecutionNode(Node):
    def __init__(self, terminal: Terminal, name: str = 'Execution Node', menu: Optional[MenuNode] = None):
        super().__init__(terminal, name)
        self.menu = menu

    def _invoke(self):
        node = self.menu.run()
        node.run()

    def set_menu(self, menu: MenuNode):
        self.menu = menu


class ExecutorNode(Node):
    def __init__(self, terminal: Terminal, name: str, func: Callable, args: tuple = None, kwargs: dict = None):
        super().__init__(terminal, name)
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.executions = []

    def _invoke(self):
        self.print(f'Executing task: {self.name}', nla=True)

        start = datetime.now(timezone.utc)
        result = self.func(*self.args, **self.kwargs)
        end = datetime.now(timezone.utc)

        execution = {
            'name': self.name,
            'result': result,
            'parameters': {
                'args': self.args,
                'kwargs': self.kwargs
            },
            'performance': {
                'start': start.isoformat(),
                'end': end.isoformat(),
                'elapsed': str(end - start)
            }
        }

        self.print('Execution details: ' + self.pprint(execution, dumps=True), nlb=True, nla=True)
        self.executions.append(execution)
        return result

class MenuNode(Node):
    def __init__(self, terminal: Terminal, name: str = 'Menu Node', options: list[Node] = None):
        super().__init__(terminal, name)
        self.menu = self.terminal.menus.create(name, options)

    def show_menu(self):
        self.print('Please select one of the following options from the menu:', nla=True)
        self.menu.print_options()

    def _invoke(self):
        self.show_menu()
        menu_key = self.input()

        while menu_key not in self.menu:
            self.print('Invalid key selected. Please try again:', nla=True)
            self.show_menu()
            menu_key = self.input()

        return self.menu.options[menu_key]

    def add_option(self, option):
        self.menu.add_option(option)


NodeType = TypeVar('NodeType', Node, ExecutionNode, MenuNode, ExecutorNode)

class NodeFactory:
    @property
    def is_empty(self) -> bool:
        return not self._nodes

    @property
    def first(self) -> Optional[None]:
        if self._nodes:
            return self._nodes[0]

    def __init__(self, terminal):
        self.terminal = terminal
        self._nodes = []

    def create(self, cls: Type[NodeType], *args, **kwargs) -> NodeType:
        node = cls(self.terminal, *args, **kwargs)
        self._nodes.append(node)
        return node
