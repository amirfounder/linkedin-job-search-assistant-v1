from typing import TypeVar, Optional, Type

from src.terminal.v2.nodes.base import Node
from src.terminal.v2.nodes.exit_nodes import ExitNode, ExitProgramNode, ExitToMainMenuNode
from src.terminal.v2.nodes.nodes import ExecutionNode, ExecutorNode, MenuNode

NodeType = TypeVar(
    'NodeType',
    Node,
    ExecutionNode,
    MenuNode,
    ExecutorNode,
    ExitNode,
    ExitProgramNode,
    ExitToMainMenuNode,
)

class NodeFactory:
    @property
    def is_empty(self) -> bool:
        return not self._nodes

    @property
    def first(self) -> Optional[None]:
        if self._nodes:
            return self._nodes[0]

    def __init__(self, terminal):
        self.terminal = terminal
        self._nodes = []

    def create(self, cls: Type[NodeType], *args, **kwargs) -> NodeType:
        node = cls(self.terminal, *args, **kwargs)
        self._nodes.append(node)
        return node
