from .ast import AST


class Function(AST):
    def __init__(self, name, parameters, return_type, block):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.block = block
        self.scope = {}


class GenericFunction(AST):
    def __init__(self, name, parameters, return_type, block, generics):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.block = block
        self.generics = generics
        self.scope = {}


class BuiltinFunction(AST):
    def __init__(self, name, parameters, return_type):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.scope = {}


class FunctionPrototype(AST):
    def __init__(self, name, parameters, return_type):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type