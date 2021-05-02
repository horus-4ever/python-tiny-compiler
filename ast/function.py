from .ast import AST


class Function(AST):
    def __init__(self, name, parameters, return_type, block):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.block = block


class BuiltinFunction(AST):
    def __init__(self, name, parameters, return_type):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type