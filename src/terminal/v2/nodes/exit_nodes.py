from src.terminal.v2.nodes.nodes import Node


class ExitNode(Node):
    def __init__(self, terminal):
        super().__init__(terminal, 'Exit menu')

    def _invoke(self):
        self.print('Exiting menu ...')


class ExitToMainMenuNode(Node):
    def __init__(self, terminal):
        super().__init__(terminal, 'Exit to main menu')

    def _invoke(self):
        self.print('Exiting to main menu ...')
        self.terminal.stack = self.terminal.stack[0]
        self.terminal.stack[-1].run()


class ExitProgramNode(Node):
    def __init__(self, terminal):
        super().__init__(terminal, 'Exit program')

    def _invoke(self):
        self.print('Exiting program ...')
        self.terminal.keep_running = False
