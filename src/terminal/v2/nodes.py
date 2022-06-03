from abc import abstractmethod, ABC


class Node(ABC):
    def __init__(self, terminal, name):
        self.terminal = terminal
        self.name = name

    def run(self):
        try:
            self.terminal.stack.append(self)
            result = self._invoke()
            self.terminal.stack.pop()
            return result
        except Exception as e:
            print(f'Exception: {type(e).__name__}: {str(e)}')

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def _invoke(self):
        pass


class NodeFactory:
    @property
    def is_empty(self):
        return not self._nodes

    @property
    def first(self):
        if self._nodes:
            return self._nodes[0]

    def __init__(self, terminal):
        self.terminal = terminal
        self._nodes = []

    def create(self, cls, *args, **kwargs):
        self._nodes.append(cls(self.terminal, *args, **kwargs))
        return self._nodes[-1]


class TaskNode(Node):
    def __init__(self, terminal, name, menu):
        super().__init__(terminal, name)
        self.menu = menu

    def display_info(self):
        print(f'Selected Task: {self.name}')

    def _invoke(self):
        node = self.menu.run()
        node.run()


class TaskExecutorNode(Node):
    def __init__(self, terminal, name, func, args=None, kwargs=None):
        super().__init__(terminal, name)
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

    def display_info(self):
        print(f'Executing task: {self.name}')

    def _invoke(self):
        return self.func(*self.args, **self.kwargs)


class MenuNode(Node):
    def __init__(self, terminal, name, options=None):
        super().__init__(terminal, name)
        self.menu = self.terminal.menus.create(name, options)

    def display_info(self):
        print('Please select one of the following options from the menu:')
        self.menu.show_options()

    def _invoke(self):
        self.display_info()
        menu_key = input('>> ')

        while menu_key not in self.menu.options:
            print('Invalid key selected. Please try again:')
            self.display_info()
            menu_key = input('>> ')

        return self.menu.options[menu_key]


class ExitNode(Node):
    def __init__(self, terminal):
        super().__init__(terminal, 'Exit')
        
    def display_info(self):
        print('Exiting...')

    def _invoke(self):
        pass


class ExitToMainMenuNode(Node):
    def __init__(self, terminal):
        super().__init__(terminal, 'Exit to main menu')

    def display_info(self):
        print('Exiting to main menu...')

    def _invoke(self):
        self.terminal.stack[1:].run()
