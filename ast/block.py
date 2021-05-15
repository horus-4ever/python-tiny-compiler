from .ast import AST
from .scope import Scope


class Block(AST):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements
        self.scope = Scope()