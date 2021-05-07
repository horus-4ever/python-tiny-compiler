from collections import deque
import ast


class NameChecker:
    def __init__(self, ast):
        self.ast = ast
        self.scopes = deque([ast.global_scope])

    @property
    def global_scope(self):
        return self.scopes[0]

    @property
    def current_scope(self):
        return self.scopes[-1]

    def scope_lookup(self, to_find, kind):
        current_scope = self.current_scope
        while current_scope is not None:
            for name, value in current_scope:
                if isinstance(value, kind) and name == to_find:
                    return current_scope
            current_scope = current_scope.parent
        return None

    def check(self):
        print(self.ast.structures)
        # structures
        for name, structure in self.ast.builtin_structures.items():
            self.check_builtin_structure(structure)
        for name, structure in self.ast.structures.items():
            self.check_structure(structure)
        # functions
        for name, function in self.ast.builtin_functions.items():
            self.check_builtin_function(function)
        for name, function in self.ast.functions.items():
            self.check_function(function)
        # once it is checked, inline function scopes
        for name, function in self.ast.functions.items():
            self.flatten_function_scope(function)
        for name, structure in self.ast.structures.items():
            for name, method in structure.methods.items():
                self.flatten_function_scope(method)
        return self.ast

    def flatten_function_scope(self, function):
        scope = function.block.scope
        new_scope = scope.flatten()
        function.scope = new_scope

    def check_structure(self, structure):
        for name, field in structure.fields.items():
            type_name = field.kind.name
            if type_name not in self.ast.all_types:
                raise Exception(f"Cannot find type '{type_name}' in the global scope.")
        for name, function in structure.methods.items():
            self.check_function(function)

    def check_builtin_structure(self, structure):
        for name, function in structure.methods.items():
            self.check_builtin_function(function)

    def check_builtin_function(self, function):
        self.check_parameters(function)
        self.check_return_type(function)

    def check_function(self, function):
        self.check_parameters(function)
        self.check_return_type(function)
        self.check_block(function.block)
    
    def check_parameters(self, function):
        for parameter in function.parameters:
            kind = parameter.kind
            if kind.type_name not in self.ast.all_types:
                raise Exception(f"Cannot find type '{type_name}' in the global scope.")
            if isinstance(function, ast.Function):
                if parameter.name in function.block.scope:
                    raise Exception(f"Variable '{parameter.name}' already defined.")
                scope = function.block.scope
            else:
                scope = function.scope
            variable = ast.Variable(
                parameter.name,
                kind
            )
            scope[parameter.name] = variable
            parameter.variable_id = id(variable)

    def check_return_type(self, function):
        type_name = function.return_type.type_name
        if type_name not in self.ast.all_types:
            raise Exception(f"Cannot find type '{type_name}' in the global scope.")

    def check_block(self, block):
        self.current_scope.children.append(block.scope)
        block.scope.parent = self.current_scope
        block.scope.depth = self.current_scope.depth + 1
        self.scopes.append(block.scope)
        for statement in block.statements:
            self.check_statement(statement)
        self.scopes.pop()

    def check_statement(self, statement):
        if isinstance(statement, ast.VariableDeclaration):
            self.check_variable_declaration(statement)
        elif isinstance(statement, ast.Return):
            statement.drop_variables = list(self.current_scope.elements.values())
            self.check_expression(statement.expression)
        elif isinstance(statement, ast.Expression):
            self.check_expression(statement)
        elif isinstance(statement, ast.Block):
            self.check_block(statement)
        elif isinstance(statement, ast.IfStatement):
            self.check_if_statement(statement)

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        if statement.name in self.current_scope:
            raise Exception(f"Variable '{statement.name}' already defined.")
        variable = ast.Variable(statement.name, statement.kind)
        self.current_scope[statement.name] = variable
        statement.variable_id = id(variable)
        if statement.kind is not None:
            if statement.kind.type_name not in self.ast.all_types:
                raise Exception(f"Unkown type '{statement.type_name}'")

    def check_expression(self, expression):
        if isinstance(expression, (ast.VariableReference, ast.MakeRef, ast.DeRef)):
            self.check_variable_reference(expression)
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.ClassmethodCall):
            self.check_classmethod_call(expression)
        elif isinstance(expression, ast.StructureInstanciation):
            self.check_structure_instanciation(expression)

    def check_variable_reference(self, expression):
        scope = self.scope_lookup(expression.name, kind=ast.Variable)
        if scope is None:
            raise Exception(f"Variable '{expression.name}' is not defined.")
        else:
            expression.variable_id = id(scope[expression.name])

    def check_if_statement(self, statement):
        self.check_expression(statement.condition)
        self.check_block(statement.block)

    def check_function_call(self, expression):
        if expression.name not in self.ast.all_functions:
            raise Exception(f"No function named '{expression.name}'")
        for argument in expression.arguments:
            self.check_expression(argument.expression)

    def check_classmethod_call(self, expression):
        if expression.struct_name not in self.ast.all_types:
            raise Exception(f"No such type '{expression.struct_name}'.")
        if expression.func_name not in self.ast.all_types[expression.struct_name].methods:
            raise Exception(f"No such method '{expression.func_name}' on type '{expression.struct_name}'")
        for argument in expression.arguments:
            self.check_expression(argument.expression)

    def check_structure_instanciation(self, expression):
        if expression.name not in self.ast.all_types:
            raise Exception(f"No such type '{expression.name}'.")
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        