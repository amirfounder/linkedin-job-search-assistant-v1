from string import ascii_lowercase

from src.terminal.v2.nodes import ExitNode, ExitProgramNode, ExitToMainMenuNode, Node


class MenuModel:
    def __init__(self, name: str, default_options: list[Node] = None, options: list[Node] = None):
        self.name = name
        self._options = options or [] + default_options or []
        self.options = {}

        self._default_options_len = len(default_options)
        self._next_key_idx = 0
        self._build_options_map()

    @property
    def next_key_idx(self) -> int:
        res = self._next_key_idx
        self._next_key_idx += 1
        return res

    @property
    def next_key(self) -> str:
        return ascii_lowercase[self.next_key_idx]

    def _build_options_map(self):
        self._next_key_idx = 0
        self.options.clear()
        for option in self._options:
            key = self.next_key
            while key in self.options:
                key = self.next_key
            self.options[key] = option

    def add_option(self, option: Node):
        self._options.insert(len(self.options) - self._default_options_len, option)
        self._build_options_map()


class MenuFactory:
    def __init__(self, terminal):
        self.terminal = terminal
        self._menus = []

    def create(self, name: str, options: list = None) -> MenuModel:
        if options is None:
            options = []

        default_options = [
            ExitNode(self.terminal),
            ExitToMainMenuNode(self.terminal),
            ExitProgramNode(self.terminal),
        ]

        menu = MenuModel(name, default_options, options)

        self._menus.append(menu)
        return menu
