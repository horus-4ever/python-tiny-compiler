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
    def __init__(self, string_label, size):
        self.string_label = string_label
        self.size = size


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
    def __init__(self, variable_offset, size):
        self.variable_offset = variable_offset
        self.size = size


class LOAD_DEREF(Instruction):
    def __init__(self, size):
        self.size = size


class LOAD_REF(Instruction):
    def __init__(self, variable_offset):
        self.variable_offset = variable_offset


class CALL_FUNCTION(Instruction):
    def __init__(self, func_name):
        self.func_name = func_name


class STORE_VARIABLE(Instruction):
    def __init__(self, variable_offset, size):
        self.variable_offset = variable_offset
        self.size = size
        

class STORE_VARIABLE_DEREF(Instruction):
    def __init__(self, variable_offset, size):
        self.variable_offset = variable_offset
        self.size = size


class STORE_ARGUMENT(Instruction):
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size


class GET_ATTR(Instruction):
    def __init__(self, offset, size, expr_size):
        self.offset = offset
        self.size = size
        self.expr_size = expr_size


class GET_ATTR_DEREF(Instruction):
    def __init__(self, offset, size, expr_size):
        self.offset = offset
        self.size = size
        self.expr_size = expr_size


class RETURN(Instruction):
    def __init__(self, size):
        self.size = size


class POP_JMP_IF_FALSE(Instruction):
    def __init__(self, size, label_name):
        self.size = size
        self.label_name = label_name


class JMP(Instruction):
    def __init__(self, label_name):
        self.label_name = label_name


class LABEL(Instruction):
    def __init__(self, name):
        self.name = name


class FUNCTION_PRELUDE(Instruction):
    pass
class FUNCTION_END(Instruction):
    pass
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