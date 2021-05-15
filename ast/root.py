from .ast import AST
from .scope import Scope


class Root(AST):
    def __init__(self, structures, functions, traits, builtin_functions, builtin_structures):
        self.functions = functions
        self.structures = structures
        self.traits = traits
        self.builtin_functions = builtin_functions
        self.builtin_structures = builtin_structures

    def set_builtins(self, builtin_ast):
        self.builtin_functions.update(builtin_ast.builtin_functions)
        self.builtin_structures.update(builtin_ast.builtin_structures)
        self.traits.update(builtin_ast.traits)

    @property
    def all_types(self):
        return {
            **self.structures,
            **self.builtin_structures
        }

    @property
    def all_functions(self):
        return {
            **self.functions,
            **self.builtin_functions
        }