class Root:
    def __init__(self, functions, builtin_functions, types):
        self.functions = functions
        self.builtin_functions = builtin_functions
        self.types = types

    @property
    def all_functions(self):
        return {
            **self.functions,
            **self.builtin_functions
        }