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
        return self.ast

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
            type_name = parameter.kind.name
            if type_name not in self.ast.all_types:
                raise Exception(f"Cannot find type '{type_name}' in the global scope.")
            if isinstance(function, ast.Function):
                if parameter.name in function.block.scope:
                    raise Exception(f"Variable '{parameter.name}' already defined.")
                function.block.scope[parameter.name] = ast.Variable(
                    function.block.scope,
                    parameter.name,
                    None
                )

    def check_return_type(self, function):
        type_name = function.return_type.name
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
        self.current_scope[statement.name] = ast.Variable(
            None,
            statement.name,
            statement.type
        )
        statement.reference = self.current_scope[statement.name]
        if statement.type is not None:
            type = statement.type
            if type.name not in self.global_scope:
                raise Exception(f"Unkown type '{type.name}'")
            type.reference = self.global_scope[type.name]

    def check_expression(self, expression):
        # print("\n===================\nGOT IT\n====================")
        if isinstance(expression, ast.VariableReference):
            scope = self.scope_lookup(expression.name, kind=ast.Variable)
            if scope is None:
                raise Exception(f"Variable '{expression.name}' is not defined.")
            else:
                print(expression.name)
                expression.reference = scope[expression.name]
        elif isinstance(expression, ast.FunctionCall):
            if expression.name in self.global_scope:
                expression.reference = self.global_scope[expression.name]
            else:
                raise Exception(f"No function named '{expression.name}'")
            for argument in expression.arguments:
                self.check_expression(argument)
        elif isinstance(expression, ast.ClassmethodCall):
            self.check_classmethod_call(expression)
        elif isinstance(expression, ast.StructureInstanciation):
            self.check_structure_instanciation(expression)

    def check_if_statement(self, statement):
        self.check_expression(statement.condition)
        self.check_block(statement.block)

    def check_classmethod_call(self, expression):
        if expression.typename in self.global_scope:
            expression.type_reference = self.global_scope[expression.typename]
        if expression.function_name in expression.type_reference.methods:
            expression.func_reference = expression.type_reference.methods[expression.function_name]
        else:
            raise Exception(f"Not such method '{expression.function_name}' on type '{expression.typename}'")
        for argument in expression.arguments:
            self.check_expression(argument)

    def check_structure_instanciation(self, expression):
        if expression.name in self.global_scope:
            expression.reference = self.global_scope[expression.name]
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        