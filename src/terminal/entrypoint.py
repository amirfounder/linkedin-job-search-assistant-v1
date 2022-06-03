from __future__ import annotations

from src.terminal.v2.nodes import MenuNode, ExecutorNode, ExecutionNode
from src.terminal.v2.terminal import Terminal
from src.services.terminal import open_linkedin


def run_terminal_in_thread():
    terminal = Terminal()

    entrypoint = terminal.nodes.create(ExecutionNode, name='LinkedIn Job Search Assistant')
    menu = terminal.nodes.create(MenuNode, name='Main Menu')
    menu.add_option(terminal.nodes.create(ExecutorNode, name='Open LinkedIn', func=open_linkedin))
    menu.add_option(terminal.nodes.create(ExecutorNode, name='Print "Hello World"', func=lambda: print('Hello World')))
    entrypoint.set_menu(menu)

    terminal.entrypoint = entrypoint
    return terminal.run_in_thread()
