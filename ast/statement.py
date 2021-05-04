from .ast import AST


class Statement(AST):
    pass


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression
        self.drop_variables = []


class IfStatement(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block