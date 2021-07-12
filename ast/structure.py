from .ast import AST


class Type(AST):
    pass


class GenericType(Type):
    def __init__(self, name, implements):
        self.name = name
        self.implements = implements
        self.methods = {}


class Structure(Type):
    def __init__(self, name, fields, methods, implements=()):
        self.name = name
        self.fields = fields
        self.methods = methods
        self.implements = implements

    def __len__(self):
        return 0


class BuiltinStructure(Type):
    def __init__(self, name, stack_size, fields, builtin_methods, implements=()):
        self.name = name
        self.stack_size = stack_size
        self.fields = fields
        self.methods = builtin_methods
        self.implements = implements

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