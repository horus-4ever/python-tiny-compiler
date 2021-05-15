from .ast import AST


class Type(AST):
    pass


class GenericType(Type):
    def __init__(self, name, implements):
        self.name = name
        self.implements = implements


class NormalType(Type):
    def __init__(self, name):
        self.type_name = name

    def __eq__(self, other):
        return self.type_name == other.type_name and type(self) is type(other)


class RefType(Type):
    def __init__(self, name):
        self.type_name = name

    def __eq__(self, other):
        return self.type_name == other.type_name and type(self) is type(other)