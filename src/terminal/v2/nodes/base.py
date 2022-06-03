import json
from abc import ABC, abstractmethod

from src.terminal.v2.terminal import Terminal


class Node(ABC):
    def __init__(self, terminal: Terminal, name: str):
        self.terminal = terminal
        self.name = name

    def run(self):
        self.terminal.stack.append(self)
        try:
            res = self._invoke()
            return res
        except Exception as e:
            print(f'Exception: {type(e).__name__}: {str(e)}')
        finally:
            self.terminal.stack.pop()

    def pprint(self, obj, *args, dumps=True, **kwargs):
        if 'nla' not in kwargs:
            kwargs['nla'] = True
        if 'nlb' not in kwargs:
            kwargs['nlb'] = True

        res = json.dumps(obj, indent=4)

        if dumps:
            return res
        self.print(res, *args, **kwargs)

    @staticmethod
    def print(*args, nlb=False, nla=False, **kwargs):
        if nlb:
            print()

        print(*args, **kwargs)

        if nla:
            print()

    def input(self):
        self.print()
        res = input('>> ')
        self.print()
        return res

    @abstractmethod
    def _invoke(self):
        pass
