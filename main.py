import time
from threading import Thread

from src.terminal.terminal import MyTerminal


if __name__ == '__main__':
    # server_thread = run_server_in_thread()
    terminal = MyTerminal()
    terminal.run()
    # server_thread.join()
    while True:
        pass
