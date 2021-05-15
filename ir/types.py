class Type:
    def __init__(self, type_name, fields, stack_size, is_builtin, is_copy):
        self.type_name = type_name
        self.fields = fields
        self.stack_size = stack_size
        self.is_builtin = is_builtin
        self.is_copy = is_copy

    def __len__(self):
        return self.stack_size


class Field:
    def __init__(self, name, size, offset):
        self.name = name
        self.size = size
        self.offset = offset