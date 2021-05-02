from .ast import AST


class Structure(AST):
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods


class BuiltinStructure(AST):
    def __init__(self, name, stack_size, fields, builtin_methods):
        self.name = name
        self.stack_size = stack_size
        self.fields = fields
        self.builtin_methods = builtin_methods