from __future__ import annotations

from src.terminal.v2.nodes import MenuNode, TaskExecutorNode, TaskNode
from src.terminal.v2.terminal import Terminal


def main():
    terminal = Terminal()

    def func():
        print('Hello World!')

    def func2():
        print('Howdy')

    executor2 = terminal.nodes.create(TaskExecutorNode, name='Print "Howdy"', func=func2)
    executor = terminal.nodes.create(TaskExecutorNode, name='Print "Hello World"', func=func)
    menu = terminal.nodes.create(MenuNode, name='Menu', options=[executor, executor2])
    test = terminal.nodes.create(TaskNode, name='Test', menu=menu)
    
    terminal.entrypoint = test
    terminal.run()


if __name__ == '__main__':
    main()
