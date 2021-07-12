from .ast import AST


class NormalType(AST):
    def __init__(self, name):
        self.type_name = name

    def __eq__(self, other):
        return self.type_name == other.type_name and type(self) is type(other)


class RefType(AST):
    def __init__(self, name):
        self.type_name = name

    def __eq__(self, other):
        return self.type_name == other.type_name and type(self) is type(other)