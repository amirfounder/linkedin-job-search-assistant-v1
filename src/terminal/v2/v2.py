from __future__ import annotations

from src.terminal.v2.nodes import MenuNode, TaskExecutorNode, TaskNode
from src.terminal.v2.terminal import Terminal


def main():
    terminal = Terminal()

    def func():
        print('this is a test')

    executor = terminal.nodes.create(TaskExecutorNode, name='Executor', func=func)
    menu = terminal.nodes.create(MenuNode, name='Menu', options=[executor])
    test = terminal.nodes.create(TaskNode, name='Test', menu=menu)
    
    terminal.entrypoint = test
    terminal.run()


if __name__ == '__main__':
    main()
