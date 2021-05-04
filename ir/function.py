class Function:
    def __init__(self, name, return_value, variables, instructions):
        self.name = name
        self.return_value = return_value
        self.variables = variables
        self.instructions = instructions

    @property
    def return_size(self):
        return len(self.return_value)

    @property
    def scope_size(self):
        return sum(map(len, self.variables))

    def __repr__(self):
        result = f"{self.name}:\n"
        for instruction in self.instructions:
            result += repr(instruction) + "\n"
        return result


class BuiltinFunction:
    def __init__(self, name, return_value, variables):
        self.name = name
        self.return_value = return_value
        self.variables = variables

    @property
    def return_size(self):
        return len(self.return_value)

    @property
    def scope_size(self):
        return sum(map(len, self.variables))

    def __repr__(self):
        result = f"{self.name}: (builtin)\n"
        return result
