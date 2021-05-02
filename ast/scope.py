from .ast import AST


class Scope(AST):
    def __init__(self):
        self.depth = 0
        self.parent = None
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