from .ast import AST


class Scope(AST):
    def __init__(self):
        self.depth = 0
        self.parent = None
        self.children = []
        self.elements = {}

    def extend(self, dct):
        self.elements.update(dct)

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __iter__(self):
        return iter(self.elements.items())

    def __contains__(self, key):
        return key in self.elements

    def flatten(self):
        result = []
        for element in self.elements.values():
            result.append(element)
        for child in self.children:
            result.extend(child.flatten())
        return result

    def __len__(self):
        return sum(map(len, self.flatten()))