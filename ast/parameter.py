from .ast import AST


class Parameter(AST):
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind