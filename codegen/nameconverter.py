import ast
import ir
import hashlib


class NameConverter:
    def __init__(self, ast):
        self.ast = ast

    def convert(self):
        self.convert_structures_to_functions()
        self.types = {}
        for type_name, structure in self.ast.all_types.items():
            new_structure = self.convert_structure(structure)
            self.types[type_name] = new_structure
        for type_name, structure in self.types.items():
            self.convert_structure_fields(structure)
        self.functions = {}
        for func_name, function in self.ast.functions.items():
            new_func = self.convert_function(function)
            self.functions[func_name] = new_func
        self.builtin_functions = {}
        for func_name, function in self.ast.builtin_functions.items():
            new_func = self.convert_builtin_function(function)
            self.builtin_functions[func_name] = new_func
        return ir.Root(self.functions, self.builtin_functions, self.types)

    def convert_structures_to_functions(self):
        for struct_name, structure in self.ast.structures.items():
            for method_name, method in structure.methods.items():
                new_name = f"{struct_name}::{method_name}"
                new_function = ast.Function(new_name, method.parameters, method.return_type, method.block)
                new_function.scope = method.scope
                self.ast.functions[new_name] = new_function
        for struct_name, structure in self.ast.builtin_structures.items():
            for method_name, method in structure.methods.items():
                id_name = f"{struct_name}::{method_name}"
                new_name = f"_{struct_name}__{method_name}"
                new_function = ast.BuiltinFunction(new_name, method.parameters, method.return_type)
                self.ast.builtin_functions[id_name] = new_function

    def convert_structure_fields(self, type):
        structure = self.ast.all_types[type.type_name]
        offset = 0
        for field_name, field in structure.fields.items():
            field_kind = self.types[field.kind.type_name]
            type.fields[field_name] = ir.Field(field_name, field_kind.stack_size, offset)
            offset += field_kind.stack_size
        if not type.is_builtin:
            type.stack_size = offset

    def convert_builtin_function(self, function):
        new_variables = {}
        variable_offset = 0
        for parameter in function.parameters:
            variable = self.convert_variable(parameter, variable_offset)
            new_variables[parameter.variable_id] = variable
            variable_offset += variable.size
        return_size = self.types[function.return_type.type_name].stack_size
        return ir.BuiltinFunction(function.name, return_size, new_variables)
    
    def convert_function(self, function):
        new_func_name = f"func__{hashlib.md5(function.name.encode()).hexdigest()}"
        func_scope = function.scope
        new_variables = {}
        variable_offset = 0
        for variable_id, variable in func_scope.items():
            new_variable = self.convert_variable(variable, variable_offset)
            new_variables[variable_id] = new_variable
            variable_offset += new_variable.size
        statements = self.convert_block(function.block)
        return_size = self.types[function.return_type.type_name].stack_size
        return ir.Function(new_func_name, statements, return_size, new_variables)

    def convert_block(self, block):
        statements = []
        for statement in block.statements:
            if isinstance(statement, ast.Block):
                statements.extend(self.convert_block(statement))
            else:
                statements.append(statement)
        return statements

    def convert_structure(self, structure):
        if isinstance(structure, ast.BuiltinStructure):
            type_name = structure.name
            stack_size = structure.stack_size
            is_builtin = True
            is_copy = "Copy" in structure.implements
            fields = {}
        else:
            type_name = structure.name
            stack_size = 0
            is_builtin = False
            is_copy = False
            fields = {}
        return ir.Type(type_name, fields, stack_size, is_builtin, is_copy)

    def convert_variable(self, variable, offset):
        kind = variable.kind
        if isinstance(kind, ast.RefType):
            size = 4
        else:
            size = self.types[kind.type_name].stack_size
        return ir.Variable(kind, size, offset)