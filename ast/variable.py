from .ast import AST


class VariableDeclaration(AST):
    def __init__(self, name, expression, kind=None):
        self.name = name
        self.expression = expression
        self.kind = kind
        self.variable_id = None


class Variable(AST):
    def __init__(self, name, kind=None):
        self.name = name
        self.kind = kind
        self.is_moved = False
        self.is_partially_moved = False