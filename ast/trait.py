from .ast import AST


class Trait(AST):
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions
