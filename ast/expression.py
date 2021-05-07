from .statement import Statement


class Expression(Statement):
    def __init__(self):
        self.kind = None


class MakeRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class DeRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class VariableReference(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class FunctionCall(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments


class Argument(Expression):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        self.variable_id = 0


class ClassmethodCall(Expression):
    def __init__(self, type_name, func_name, arguments):
        super().__init__()
        self.struct_name = type_name
        self.func_name = func_name
        self.arguments = arguments


class StructureInstanciation(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments


class Litteral(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

class Number(Litteral):
    pass
class String(Litteral):
    pass
class Bool(Litteral):
    pass