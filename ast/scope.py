import ast


class Scope(dict):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.parent = None
        self.children = []

    def flatten(self):
        result = Scope()
        for name, element in self.items():
            if isinstance(element, ast.Variable):
                result[id(element)] = element
            else:
                result[name] = element
        result.parent = self.parent
        for child in self.children:
            result.update(child.flatten())
        return result

    @property
    def generics(self):
        return {name: value for name, value in self.items() if isinstance(value, ast.GenericType)}

    @property
    def variables(self):
        return {name: value for name, value in self.items() if isinstance(value, ast.Variable)}

    def lookup(self, name, kind="type"):
        if kind == "type":
            kind = ast.Type
        elif kind == "function":
            kind = ast.Function
        else:
            raise NotImplementedError()
        current_scope = self
        while current_scope is not None:
            for element_name, value in current_scope.items():
                if element_name == name and isinstance(value, kind):
                    return value
            current_scope = current_scope.parent
        raise Exception("Not found.", name)

    """
    def __len__(self):
        return sum(map(len, self.flatten()))
    """