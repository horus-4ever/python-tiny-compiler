from .ast import AST


class Parameter(AST):
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        self.variable_id = 0

    def __eq__(self, other):
        return self.kind == other.kind