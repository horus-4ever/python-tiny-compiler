import ast


class TypeChecker:
    def __init__(self, ast):
        self.ast = ast
        self.current_scope = {}

    @property
    def global_scope(self):
        return self.ast.global_scope

    def check(self):
        for name, structure in self.ast.structures.items():
            self.check_structure(structure)
        for name, function in self.ast.functions.items():
            self.check_function(function)
        return self.ast

    def check_structure(self, structure):
        for name, method in structure.methods.items():
            self.check_function(method)

    def check_function(self, function):
        self.current_scope = function.scope
        # check statements
        self.check_block(function.block)
        # check return type
        expected_return_type = function.return_type
        has_return_statements = self.recursive_check_return_type(expected_return_type, function.block)
        if not has_return_statements:
            if expected_return_type != ast.NormalType("Empty"):
                raise Exception(f"The return type must be '{expected_return_type}', but nothing is returned.")

    def recursive_check_return_type(self, expected_return_type, block):
        has_return_statements = False
        for statement in block.statements:
            if isinstance(statement, ast.Return):
                has_return_statements = True
                if statement.expression.kind != expected_return_type:
                    raise Exception(f"Wrong return type. Expected '{expected_return_type}', got '{statement.expression.kind}'.")
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
            # print("aqh", statement.expression.type_name)
        elif isinstance(statement, ast.Block):
            self.check_block(statement)
        elif isinstance(statement, ast.IfStatement):
            self.check_if_statement(statement)

    def check_expression(self, expression):
        if isinstance(expression, ast.Number):
            expression.kind = ast.NormalType("Int")
        elif isinstance(expression, ast.String):
            expression.kind = ast.NormalType("Str")
        elif isinstance(expression, ast.Bool):
            expression.kind = ast.NormalType("Bool")
        elif isinstance(expression, ast.VariableReference):
            variable = self.current_scope[expression.variable_id]
            expression.kind = variable.kind
        elif isinstance(expression, ast.MakeRef):
            variable = self.current_scope[expression.variable_id]
            expression.kind = ast.RefType(variable.kind.type_name)
        elif isinstance(expression, ast.DeRef):
            variable = self.current_scope[expression.variable_id]
            expression.kind = ast.NormalType(variable.kind.type_name)
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.ClassmethodCall):
            self.check_classmethod_call(expression)
        elif isinstance(expression, ast.StructureInstanciation):
            self.check_structure_instanciation(expression)

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        if statement.kind is not None:
            if statement.kind != statement.expression.kind:
                raise Exception(f"Wrong type in variable declaration. Left: '{statement.kind}' and Right: '{statement.expression.kind}'")
        else:
            variable = self.current_scope[statement.variable_id]
            statement.kind = statement.expression.kind
            variable.kind = statement.kind

    def check_function_call(self, expression):
        function = self.ast.all_functions[expression.name]
        if len(expression.arguments) != len(function.parameters):
            raise Exception(f"Expected '{len(function.parameters)}' argument, but '{len(expression.arguments)}' were provided.")
        # typecheck arguments
        for argument in expression.arguments:
            self.check_expression(argument.expression)
            argument.kind = argument.expression.kind
        for argument, parameter in zip(expression.arguments, function.parameters):
            argument.variable_id = parameter.variable_id
            if argument.kind != parameter.kind:
                raise Exception(f"Wrong type. Expected '{parameter.kind}', got '{argument.kind}'.")
        expression.kind = function.return_type

    def check_classmethod_call(self, expression):
        method = self.ast.all_types[expression.struct_name].methods[expression.func_name]
        if len(expression.arguments) != len(method.parameters):
            raise Exception(f"Expected '{len(method.parameters)}' argument, but '{len(expression.arguments)}' were provided.")
        for argument in expression.arguments:
            self.check_expression(argument.expression)
            argument.kind = argument.expression.kind
        for argument, parameter in zip(expression.arguments, method.parameters):
            argument.variable_id = parameter.variable_id
            if argument.kind != parameter.kind:
                raise Exception(f"Wrong type. Expected '{parameter.kind}', got '{argument.kind}'.")
        expression.kind = method.return_type

    def check_if_statement(self, statement):
        self.check_expression(statement.condition)
        if statement.condition.type_name != "Bool":
            raise Exception(f"Expected 'Bool', but found '{statement.condition.type_name}'")
        self.check_block(statement.block)

    def check_structure_instanciation(self, expression):
        expression.type_name = expression.name
        structure = self.ast.all_types[expression.name]
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        if len(expression.arguments) != len(structure.fields):
            raise Exception(f"Structure '{expression.name}' has got '{len(structure.fields)}' fields.")
        for name, kind in structure.fields.items():
            if expression.arguments[name].expression.type_name != kind.type_name:
                raise Exception(f"Expected '{kind.type_name}', but got '{expression.arguments[name].expression.type_name}'")