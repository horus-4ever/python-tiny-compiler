from .statement import Statement
from .variable import VariableState


class Expression(Statement):
    def __init__(self):
        super().__init__()
        self.kind = None
        self.state = VariableState()


class LValueRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class RValueRef(Expression):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        self.variable_id = None


class MakeRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class DeRef(Expression):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class VariableReference(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variable_id = None


class FunctionCall(Expression):
    def __init__(self, name, arguments, generics=[]):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.generics = generics


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


class MethodCall(Expression):
    def __init__(self, expression, func_name, arguments):
        super().__init__()
        self.expression = expression
        self.func_name = func_name
        self.arguments = arguments


class GetAttribute(Expression):
    def __init__(self, expression, name):
        super().__init__()
        self.expression = expression
        self.name = name


class StructureInstanciation(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments


class Litteral(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value


class BinaryExpression(Expression):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class BinaryAdd(BinaryExpression):
    TRAIT = "Add"
    METHOD = "add"
class BinarySub(BinaryExpression):
    TRAIT = "Sub"
    METHOD = "sub"
class BinaryMul(BinaryExpression):
    TRAIT = "Mul"
    METHOD = "mul"
class BinaryEq(BinaryExpression):
    TRAIT = "Eq"
    METHOD = "eq"
class BinaryNeq(BinaryExpression):
    TRAIT = "Eq"
    METHOD = "neq"
class BinaryOr(BinaryExpression):
    pass
class BinaryAnd(BinaryExpression):
    pass


class Number(Litteral):
    pass
class String(Litteral):
    pass
class Bool(Litteral):
    pass