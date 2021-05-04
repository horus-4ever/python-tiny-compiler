from .ast import AST


class Structure(AST):
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods

    def __len__(self):
        return 0


class BuiltinStructure(AST):
    def __init__(self, name, stack_size, fields, builtin_methods):
        self.name = name
        self.stack_size = stack_size
        self.fields = fields
        self.methods = builtin_methods

    def __len__(self):
        return self.stack_size


class Field(AST):
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


class FieldArgument(AST):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.reference = None