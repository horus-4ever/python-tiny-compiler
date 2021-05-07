from .ast import AST


class Statement(AST):
    pass


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression
        self.drop_variables = []


class IfStatement(Statement):
    def __init__(self, condition, block, else_statement=None):
        self.condition = condition
        self.block = block
        self.else_statement = else_statement