import ast
from collections import deque


class BorrowChecker:
    def __init__(self, ast):
        self.ast = ast
        self.current_scope = {}

    def check(self):
        for name, function in self.ast.functions.items():
            self.check_function(function)
        for name, structure in self.ast.structures.items():
            self.check_structure(structure)
        return self.ast

    def check_function(self, function):
        self.current_scope = function.scope
        self.check_block(function.block)

    def check_structure(self, structure):
        for method in structure.methods.values():
            self.check_function(method)

    def check_block(self, block):
        for statement in block.statements:
            self.check_statement(statement)

    def check_statement(self, statement):
        if isinstance(statement, ast.Expression):
            self.check_expression(statement)

    def check_expression(self, expression):
        kind = expression.kind
        if isinstance(expression, ast.VariableReference):
            variable = self.current_scope[expression.variable_id]
            if kind in (ast.NormalType("Empty"), ast.NormalType("Int"), ast.NormalType("Bool")):
                return
            elif not variable.is_valid:
                raise Exception(f"Variable '{variable.name}' used after move.")
            else:
                variable.is_valid = False
        elif isinstance(expression, (ast.FunctionCall, ast.ClassmethodCall)):
            for argument in expression.arguments:
                self.check_expression(argument.expression)