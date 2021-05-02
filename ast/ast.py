class AST:
    def __repr__(self):
        string = "{}({})".format(type(self).__name__, vars(self))
        return string