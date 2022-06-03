from time import sleep

from src.services.server import run_server_in_thread
from src.terminal.entrypoint import run_terminal_in_thread


if __name__ == '__main__':
    server_thread = run_server_in_thread()
    sleep(.5)
    terminal_thread = run_terminal_in_thread()
    server_thread.join()
    terminal_thread.join()
