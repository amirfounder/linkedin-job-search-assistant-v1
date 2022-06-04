from threading import Thread

from src.terminal.v2.menus import MenuFactory
from src.terminal.v2.nodes import NodeFactory, EntryPoint


class Terminal:
    def __init__(self):
        self.entrypoint = None
        self.nodes = NodeFactory(self)
        self.menus = MenuFactory(self)
        self.stack = []
        self.keep_running = True

    def create_entrypoint(self):
        """
        Node Factory abstraction method. Builds and returns an entrypoint Node
        :return: Entrypoint
        """
        self.entrypoint = self.nodes.create(EntryPoint)
        return self.entrypoint

    def run(self):
        """
        Runs the terminal. NOTE: To run in non-blocking mode, see Terminal.run_in_thread method
        :return:
        """
        if not self.entrypoint:
            raise Exception('Terminal must have an entrypoint node')

        while self.keep_running:
            self.entrypoint.run()

    def run_in_thread(self, start=True, join=False):
        """
        Runs the terminal in a separate, optionally non-blocking thread.
        :param start: Should start thread on call. Default = True
        :param join: Should join thread on call. Default = False
        :return: Thread
        """
        thread = Thread(target=self.run, daemon=True)
        if start:
            thread.start()
        if join:
            thread.join()
        return thread
