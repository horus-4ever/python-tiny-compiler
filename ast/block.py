from .ast import AST
from .scope import Scope


class Block(AST):
    def __init__(self, statements):
        self.statements = statements
        self.scope = Scope()