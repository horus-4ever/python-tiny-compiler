class Function:
    def __init__(self, name, statements, return_size, variables):
        self.name = name
        self.statements = statements
        self.return_size = return_size
        self.variables = variables

    @property
    def scope_size(self):
        return sum(map(len, self.variables.values()))


class BuiltinFunction:
    def __init__(self, name, return_size, variables):
        self.name = name
        self.return_size = return_size
        self.variables = variables

    @property
    def scope_size(self):
        return sum(map(len, self.variables.values()))