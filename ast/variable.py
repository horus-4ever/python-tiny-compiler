from .ast import AST


class VariableDeclaration(AST):
    def __init__(self, name, expression, type=None):
        self.name = name
        self.expression = expression
        self.type = type
        self.reference = None


class Variable(AST):
    def __init__(self, scope, name, kind=None):
        self.scope = scope
        self.name = name
        self.kind = kind