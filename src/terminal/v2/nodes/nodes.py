from __future__ import annotations
from datetime import timezone, datetime
from typing import TYPE_CHECKING, Optional, Callable

from .base import Node
from ..menu import MenuModel

if TYPE_CHECKING:
    from ..terminal import Terminal


def now():
    return datetime.now(timezone.utc)


class EntryPoint(Node):
    def __init__(self, terminal: Terminal, name: str, menu: Menu):
        super().__init__(terminal, name)
        self.menu = menu
        self.pools = []

    def _invoke(self):
        selected_option = self.menu.run()
        selected_option.run()

    def create_task_pool(self, name):
        pool = self.terminal.nodes.create(TaskPool, name=name)
        self.pools.append(pool)
        return pool


class TaskPool(Node):
    def __init__(self, terminal: Terminal, name: str, menu: Menu):
        super().__init__(terminal, name)
        self.menu = menu
        self.pools = []
        self.tasks = []

    def _invoke(self):
        option = self.menu.run()
        option.run()

    def create_task_pool(self, name):
        pool = self.terminal.nodes.create(TaskPool, name=name)
        self.pools.append(pool)
        return pool

    def create_task(self):
        pass


class Task(Node):
    def __init__(self, terminal: Terminal, name: str, menu: Menu):
        super().__init__(terminal, name)
        self.menu = menu

    def _invoke(self):
        option = self.menu.run()
        option.run()


class Executor(Node):
    def __init__(
            self,
            terminal: Terminal,
            name: str,
            service: Callable,
            args: tuple = None,
            kwargs: dict = None,
            safe_invoke: bool = True,
            print_execution: bool = False,
    ):
        super().__init__(terminal, name)
        self.service = service
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.safe_invoke = safe_invoke,
        self.print_execution = print_execution
        self.executions = []

    def _run_service(self):
        start = now()
        result = self.service(*self.args, **self.kwargs)
        end = now()

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

        self.executions.append(execution)
        return execution

    def _invoke(self):
        try:
            execution = self._run_service()
            if self.print_execution:
                self.pprint(execution)
        except Exception as e:
            print(f'Exception caught: {type(e).__name__} - {str(e)}')
            if not self.safe_invoke:
                raise e


class Menu(Node):
    def __init__(self, terminal: Terminal, name: str, menu: MenuModel):
        super().__init__(terminal, name)
        self.menu = menu

    def _print_options(self):
        for option, node in self.menu.options.items():
            print(f'{option}) {node.name}')

    def _prompt_selection(self):
        self.print('Please select one of the following options')
        self._print_options()
        return self.input()

    def _invoke(self):
        selection = self._prompt_selection()
        while selection not in self.menu.options:
            self.print('Invalid key. Please try again')
            selection = self._prompt_selection()
        return self.menu.options[selection]
