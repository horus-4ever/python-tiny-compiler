from .ast import AST
from .scope import Scope


class Root(AST):
    def __init__(self, structures, functions):
        self.global_scope = Scope()
        for function in functions:
            self.global_scope[function.name] = function
        for structure in structures:
            self.global_scope[structure.name] = structure

    def set_builtins(self, **builtins):
        self.global_scope.extend(builtins)