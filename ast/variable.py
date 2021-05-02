from .ast import AST


class VariableDeclaration(AST):
    def __init__(self, name, expression, type=None):
        self.name = name
        self.expression = expression
        self.type = type


class Variable(AST):
    def __init__(self, scope, name, type=None):
        self.scope = scope
        self.name = name
        self.type = type