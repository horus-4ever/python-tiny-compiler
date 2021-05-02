from .ast import AST


class Type(AST):
    def __init__(self, name):
        self.name = name


class TypeReference(AST):
    def __init__(self, name, reference=None):
        self.name = name
        self.reference = reference


class RefType(Type):
    pass