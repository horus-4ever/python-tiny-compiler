from .ast import AST
from .scope import Scope


class Root(AST):
    def __init__(self, structures, functions):
        self.global_scope = Scope()
        for function in functions:
            self.global_scope[function.name] = function
        for structure in structures:
            self.global_scope[structure.name] = structure

        self.functions = {}
        for function in functions:
            self.functions[function.name] = function
        self.structures = {}
        for structure in structures:
            self.structures[structure.name] = structure
        self.builtin_functions = {}
        self.builtin_structures = {}

    def set_builtins(self, builtin_functions, builtin_structures):
        self.builtin_functions = builtin_functions
        self.builtin_structures = builtin_structures
        self.global_scope.extend({**builtin_functions, **builtin_structures})

    @property
    def all_types(self):
        return {
            **self.structures,
            **self.builtin_structures
        }