import ast


class TypeChecker:
    def __init__(self, ast):
        self.ast = ast

    @property
    def global_scope(self):
        return self.ast.global_scope

    def check(self):
        for name, structure in filter(
            lambda element: isinstance(element[1], ast.Structure),
            self.ast.global_scope
        ):
            self.check_structure(structure)
        for name, function in filter(
            lambda element: isinstance(element[1], ast.Function),
            self.ast.global_scope
        ):
            self.check_function(function)
        return self.ast

    def check_structure(self, structure):
        for name, method in structure.methods.items():
            self.check_function(method)

    def check_function(self, function):
        # check statements
        self.check_block(function.block)
        # check return type
        expected_return_type = function.return_type.reference
        has_return_statements = self.recursive_check_return_type(expected_return_type, function.block)
        if not has_return_statements:
            if expected_return_type is not self.global_scope["Empty"]:
                raise Exception(f"The return type must be '{expected_return_type.name}', but nothing is returned.")

    def recursive_check_return_type(self, expected_return_type, block):
        has_return_statements = False
        for statement in block.statements:
            if isinstance(statement, ast.Return):
                has_return_statements = True
                if statement.expression.kind is not expected_return_type:
                    raise Exception(f"Wrong return type. Expected '{expected_return_type.name}', got '{statement.expression.kind.name}'.")
        return has_return_statements

    def check_block(self, block):
        for statement in block.statements:
            self.check_statement(statement)

    def check_statement(self, statement):
        if isinstance(statement, ast.Expression):
            self.check_expression(statement)
        elif isinstance(statement, ast.VariableDeclaration):
            self.check_variable_declaration(statement)
        elif isinstance(statement, ast.Return):
            self.check_expression(statement.expression)
        elif isinstance(statement, ast.Block):
            self.check_block(statement)
        elif isinstance(statement, ast.IfStatement):
            self.check_if_statement(statement)

    def check_expression(self, expression):
        if isinstance(expression, ast.Number):
            expression.kind = self.global_scope["Int"]
        elif isinstance(expression, ast.String):
            expression.kind = self.global_scope["Str"]
        elif isinstance(expression, ast.Bool):
            expression.kind = self.global_scope["Bool"]
        elif isinstance(expression, ast.VariableReference):
            expression.kind = expression.reference.kind
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.ClassmethodCall):
            self.check_classmethod_call(expression)
        elif isinstance(expression, ast.StructureInstanciation):
            self.check_structure_instanciation(expression)

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        if statement.type is not None:
            if statement.type.reference is not statement.expression.kind:
                raise Exception(f"Wrong type in variable declaration. Left: '{statement.type.name}' and Right: '{statement.expression.kind.name}'")
        else:
            statement.reference.kind = statement.expression.kind

    def check_function_call(self, expression):
        if len(expression.arguments) != len(expression.reference.parameters):
            raise Exception(f"Expected '{len(expression.reference.parameters)}' argument, but '{len(expression.arguments)}' were provided.")
        # typecheck arguments
        for argument in expression.arguments:
            self.check_expression(argument)
        for argument, parameter in zip(expression.arguments, expression.reference.parameters):
            if argument.kind is not parameter.kind.reference:
                raise Exception(f"Wrong type. Expected '{parameter.kind.reference.name}', got '{argument.kind.name}'.")
        expression.kind = expression.reference.return_type.reference

    def check_classmethod_call(self, expression):
        if len(expression.arguments) != len(expression.func_reference.parameters):
            raise Exception(f"Expected '{len(expression.func_reference.parameters)}' argument, but '{len(expression.arguments)}' were provided.")
        for argument in expression.arguments:
            self.check_expression(argument)
        for argument, parameter in zip(expression.arguments, expression.func_reference.parameters):
            if argument.kind is not parameter.kind.reference:
                raise Exception(f"Wrong type. Expected '{parameter.kind.reference.name}', got '{argument.kind.name}'.")
        expression.kind = expression.func_reference.return_type.reference

    def check_if_statement(self, statement):
        self.check_expression(statement.condition)
        if statement.condition.kind is not self.global_scope["Bool"]:
            raise Exception(f"Expected 'Bool', but found '{statement.condition.kind.name}'")
        self.check_block(statement.block)

    def check_structure_instanciation(self, expression):
        expression.kind = expression.reference
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        if len(expression.arguments) != len(expression.reference.fields):
            raise Exception(f"Structure '{expression.name}' has got '{len(expression.reference.fields)}' fields.")
        for name, kind in expression.reference.fields.items():
            print(expression.arguments[name].expression.kind, "\n", kind)
            if expression.arguments[name].expression.kind is not kind.kind.reference:
                raise Exception(f"Expected '{kind.kind.reference.name}', but got '{expression.arguments[name].expression.kind.name}'")