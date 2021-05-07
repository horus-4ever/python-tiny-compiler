class Variable:
    def __init__(self, type_name, size, offset):
        self.type_name = type_name
        self.size = size
        self.offset = offset

    def __len__(self):
        return self.size