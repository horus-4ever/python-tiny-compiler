from .statement import Statement


class Expression(Statement):
    def __init__(self):
        self.kind = None


class VariableReference(Expression):
    def __init__(self, name, reference=None):
        super().__init__()
        self.name = name
        self.reference = reference


class FunctionCall(Expression):
    def __init__(self, name, arguments, reference=None):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.reference = reference


class Litteral(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

class Number(Litteral):
    pass
class String(Litteral):
    pass