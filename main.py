import time
from threading import Thread

from src.terminal.action import Action
from src.terminal.menus.action_menu import ActionMenu
from src.terminal.terminal import Terminal


class MyTerminal(Terminal):
    def __init__(self):

        main = ActionMenu('LinkedIn Job Search Assistant')
        main.register_menu_option(Action('test', lambda: print('testing')))
        main.register_menu_option(Action('another one', lambda: print('another one')))

        super().__init__(main)


if __name__ == '__main__':
    # server_thread = run_server_in_thread()
    terminal = MyTerminal()
    terminal.run()
    # server_thread.join()
    while True:
        pass
