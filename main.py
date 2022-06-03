import time
from threading import Thread

from src.terminal.terminal import Terminal


if __name__ == '__main__':
    # server_thread = run_server_in_thread()
    terminal = Terminal()
    terminal.run()
    # server_thread.join()
    while True:
        pass
