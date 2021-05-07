class Segment:
    pass


class RODATA(Segment):
    def __init__(self):
        self.id = 0
        self.string_litterals = {}

    def add_string_litteral(self, string):
        if string in self.string_litterals.values():
            return self.id
        else:
            self.string_litterals[self.id] = string
            self.id += 1
            return self.id - 1

    def __repr__(self):
        result = ".rodata\n"
        for id, string in self.string_litterals.items():
            result += f"{id}: {string}"
        return result


class TEXT(Segment):
    def __init__(self):
        self.extern_functions = set()
        self.instructions = []

    def add(self, *instructions):
        self.instructions.extend(instructions)

    def __repr__(self):
        result = ""
        for instruction in self.instructions:
            result += f"{instruction}\n"
        return result


class Program:
    def __init__(self):
        self.rodata = RODATA()
        self.text = TEXT()

    def __repr__(self):
        return f"PROGRAM\n{repr(self.rodata)}\n\n{repr(self.text)}"