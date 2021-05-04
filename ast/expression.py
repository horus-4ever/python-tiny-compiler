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


class ClassmethodCall(Expression):
    def __init__(self, typename, function_name, arguments):
        super().__init__()
        self.typename = typename
        self.function_name = function_name
        self.arguments = arguments
        self.type_reference = None
        self.func_reference = None


class StructureInstanciation(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.reference = None


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