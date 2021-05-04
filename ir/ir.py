class Instruction:
    def __repr__(self):
        return f"{self.__class__.__name__}\t{vars(self)}"


class DROP_VARIABLES(Instruction):
    def __init__(self, variables):
        self.variables = variables


class DROP_EXPRESSION(Instruction):
    def __init__(self, expr_kind):
        self.expr_kind = expr_kind


class LOAD_STRING_LITTERAL(Instruction):
    def __init__(self, id):
        self.id = id


class PREPARE_RETURN(Instruction):
    def __init__(self, size):
        self.size = size


class PREPARE_SCOPE(Instruction):
    def __init__(self, scope_size):
        self.scope_size = scope_size


class POP_SCOPE(Instruction):
    def __init__(self, scope_size):
        self.scope_size = scope_size


class LOAD_VALUE(Instruction):
    def __init__(self, value):
        self.value = value


class LOAD_VARIABLE(Instruction):
    def __init__(self, variable):
        self.variable = variable


class CALL_FUNCTION(Instruction):
    def __init__(self, function):
        self.function = function


class STORE_VARIABLE(Instruction):
    def __init__(self, variable):
        self.variable = variable


class RETURN(Instruction):
    def __init__(self, expr_kind):
        self.expr_kind = expr_kind


class POP_JMP_IF_FALSE(Instruction):
    def __init__(self, expr_kind, label):
        self.expr_kind = expr_kind
        self.label = label


class LABEL(Instruction):
    def __init__(self, label):
        self.label = label


class SAVE(Instruction):
    pass
class RESTORE(Instruction):
    pass
"""
LOAD_FUNCTION "func_name"
LOAD_VALUE value
LOAD_VARIABLE variable
CALL_FUNCTION "func_name"
SAVE
RESTORE
STORE_VARIABLE variable
"""