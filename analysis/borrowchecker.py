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
        elif isinstance(statement, (ast.WhileStatement, ast.IfStatement)):
            self.check_expression(statement.condition)
            self.check_block(statement.block)
        elif isinstance(statement, ast.VariableDeclaration):
            self.check_variable_declaration(statement)
        elif isinstance(statement, ast.Assignement):
            self.check_assignement(statement)

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        variable = self.current_scope[statement.variable_id]
        variable.state = statement.expression.state

    def check_assignement(self, statement):
        self.check_expression(statement.expression)
        variable = self.current_scope[statement.variable_id]
        variable.state = statement.expression.state

    def check_expression(self, expression):
        kind = self.ast.all_types[expression.kind.type_name]
        if isinstance(expression, ast.VariableReference):
            self.check_variable_reference(expression)
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.MethodCall):
            self.check_method_call(expression)
        elif isinstance(expression, ast.LValueRef):
            self.check_lvalue_ref(expression)
        elif isinstance(expression, ast.DeRef):
            self.check_expression(expression.expression)
            if not "Copy" in kind.implements:
                raise Exception(f"Cannot dereference '{expression.name}' of type '{kind.name}' which does not implement 'Copy'.")

    def check_function_call(self, expression):
        for argument in expression.arguments:
            self.check_expression(argument.expression)

    def check_method_call(self, expression):
        for argument in expression.arguments:
            self.check_expression(argument.expression)

    def check_variable_reference(self, expression):
        kind = self.ast.all_types[expression.kind.type_name]
        variable = self.current_scope[expression.variable_id]
        if "Copy" in kind.implements:
            return
        elif variable.state.is_moved or variable.state.is_partially_moved :
            raise Exception(f"Variable '{variable.name}' used after move.")
        elif isinstance(expression.kind, ast.NormalType):
            variable.state.is_moved = True

    def check_lvalue_ref(self, expression):
        kind = self.ast.all_types[expression.kind.type_name]
        variable = self.current_scope[expression.variable_id]
        expression.state = variable.state
        if "Copy" in kind.implements:
            return
        elif variable.state.is_moved or variable.state.is_partially_moved :
            raise Exception(f"Variable '{variable.name}' used after move.")