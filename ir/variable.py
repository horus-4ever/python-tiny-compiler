class Variable:
    def __init__(self, typename, size, offset):
        self.typename = typename
        self.size = size
        self.offset = offset

    def __len__(self):
        return self.size