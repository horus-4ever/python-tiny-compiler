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
        # builtin functions
        for name, function in filter(
            lambda element: isinstance(element[1], ast.BuiltinFunction),
            self.global_scope
        ):
            self.check_builtin_function(function)
        # functions
        for name, function in filter(
            lambda element: isinstance(element[1], ast.Function),
            self.global_scope
        ):
            self.check_function(function)
        return self.ast

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
            if kind.reference is None and kind.name in self.global_scope:
                kind.reference = self.global_scope[kind.name]
            elif kind.reference is None:
                raise Exception(f"Cannot find type '{kind.name}' in the global scope.")
            if isinstance(function, ast.Function):
                if parameter.name in function.block.scope:
                    raise Exception(f"Variable '{parameter.name}' already defined.")
                function.block.scope[parameter.name] = ast.Variable(
                    function.block.scope,
                    parameter.name,
                    kind.reference
                )

    def check_return_type(self, function):
        kind = function.return_type
        if kind.reference is None and kind.name in self.global_scope:
            kind.reference = self.global_scope[kind.name]
        elif kind.reference is None:
            raise Exception(f"Cannot find type '{kind.name}' in the global scope.")

    def check_block(self, block):
        block.scope.parent = self.current_scope
        block.scope.depth = self.current_scope.depth + 1
        self.scopes.append(block.scope)
        for statement in block.statements:
            self.check_statement(statement)
        self.scopes.pop()

    def check_statement(self, statement):
        if isinstance(statement, ast.VariableDeclaration):
            if statement.name in self.current_scope:
                raise Exception(f"Variable '{statement.name}' already defined.")
            self.current_scope[statement.name] = ast.Variable(
                self.current_scope,
                statement.name,
                statement.type
            )
            statement.reference = self.current_scope[statement.name]
            if statement.type is not None:
                type = statement.type
                if type.name not in self.global_scope:
                    raise Exception(f"Unkown type '{type.name}'")
                type.reference = self.global_scope[type.name]
        if isinstance(statement, ast.Return):
            self.check_expression(statement.expression)
        elif isinstance(statement, ast.Expression):
            self.check_expression(statement)

    def check_expression(self, expression):
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
