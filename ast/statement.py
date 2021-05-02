from .ast import AST


class Statement(AST):
    pass


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression