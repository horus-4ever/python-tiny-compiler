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


class WhileStatement(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class Assignement(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.variable_id = None


class DerefAssignement(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.variable_id = None