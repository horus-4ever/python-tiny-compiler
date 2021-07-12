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
        self.check_implements(structure)

    def check_implements(self, structure):
        for implement in structure.implements:
            trait = self.ast.traits[implement]
            for func_name, trait_func in trait.functions.items():
                if func_name not in structure.methods:
                    raise Exception(f"Structure '{structure.name}' implements the '{trait.name}' trait but does not define the '{func_name}' function.")
                method = structure.methods[func_name]
                if len(method.parameters) != len(trait_func.parameters):
                    raise Exception("Why ?")
                for param2 in trait_func.parameters:
                    for param1 in method.parameters:
                        if type(param2.kind) is not type(param1.kind):
                            raise Exception("Wrong types!")
                        param2_type_name = param2.kind.type_name if param2.kind.type_name != "Self" else structure.name
                        param1_type_name = param1.kind.type_name
                        if param1_type_name != param2_type_name:
                            raise Exception("Wrong types!")

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
        elif isinstance(statement, ast.Assignement):
            self.check_assignement(statement)
        elif isinstance(statement, ast.DerefAssignement):
            self.check_deref_assignement(statement)
        elif isinstance(statement, ast.Return):
            self.check_expression(statement.expression)
            # print("aqh", statement.expression.type_name)
        elif isinstance(statement, ast.Block):
            self.check_block(statement)
        elif isinstance(statement, ast.IfStatement):
            self.check_if_statement(statement)
        elif isinstance(statement, ast.WhileStatement):
            self.check_while_statement(statement)

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
        elif isinstance(expression, ast.LValueRef):
            variable = self.current_scope[expression.variable_id]
            expression.kind = ast.RefType(variable.kind.type_name)
        elif isinstance(expression, ast.RValueRef):
            self.check_expression(expression.expression)
            variable = self.current_scope[expression.variable_id]
            variable.kind = expression.expression.kind
            expression.kind = ast.RefType(variable.kind.type_name)
        elif isinstance(expression, ast.DeRef):
            self.check_deref(expression)
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.ClassmethodCall):
            self.check_classmethod_call(expression)
        elif isinstance(expression, ast.MethodCall):
            self.check_method_call(expression)
        elif isinstance(expression, ast.StructureInstanciation):
            self.check_structure_instanciation(expression)
        elif isinstance(expression, ast.BinaryExpression):
            self.check_binary_expression(expression)
        elif isinstance(expression, ast.GetAttribute):
            self.check_get_attribute(expression)

    def check_binary_expression(self, expression):
        self.check_expression(expression.left)
        self.check_expression(expression.right)
        trait_name, function_name = expression.TRAIT, expression.METHOD
        left_type_name = expression.left.kind.type_name
        # check if the type implements the trait
        kind = self.current_scope.lookup(left_type_name)
        trait = self.ast.traits[trait_name]
        method = trait.functions[function_name]
        if trait_name not in kind.implements:
            raise Exception(f"Type '{kind.name}' must implement the trait '{trait}' to use the corresponding operator.")
        # left and right expected types
        left_parameter, right_parameter = method.parameters
        if left_parameter.kind.type_name == "Self":
            left_expected = type(left_parameter.kind)(left_type_name)
        else:
            left_expected = left_parameter.kind
        if right_parameter.kind.type_name == "Self":
            right_expected = type(right_parameter.kind)(left_type_name)
        else:
            right_expected = right_parameter.kind
        left_kind, right_kind = expression.left.kind, expression.right.kind
        if left_expected != left_kind or right_expected != right_kind:
            raise Exception(f"Wrong types. ('{left_expected}', '{right_expected}') but got ('{left_kind}', '{right_kind}')")
        # return type
        return_type = method.return_type
        if return_type.type_name == "Self":
            new_return_type = type(return_type)(left_type_name)
        else:
            new_return_type = type(return_type)(return_type.type_name)
        expression.kind = new_return_type
        method_call = ast.ClassmethodCall(left_type_name, function_name, [ast.Argument(expression.left), ast.Argument(expression.right)])
        self.check_classmethod_call(method_call)
        expression.classmethod_call = method_call

    def check_get_attribute(self, expression):
        self.check_expression(expression.expression)
        kind = self.ast.all_types[expression.expression.kind.type_name]
        attr_name = expression.name
        if attr_name not in kind.fields:
            raise Exception(f"Field '{attr_name}' not found on type '{kind}'.")
        field = kind.fields[attr_name]
        expression.kind = field.kind

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        if statement.kind is not None:
            if statement.kind != statement.expression.kind:
                raise Exception(f"Wrong type in variable declaration. Left: '{statement.kind}' and Right: '{statement.expression.kind}'")
        else:
            variable = self.current_scope[statement.variable_id]
            statement.kind = statement.expression.kind
            variable.kind = statement.kind

    def check_assignement(self, statement):
        self.check_expression(statement.expression)
        variable = self.current_scope[statement.variable_id]
        if variable.kind != statement.expression.kind:
            raise Exception(f"Wrong type in assignement. Left: '{variable.kind}', and Right: '{statement.expression.kind}'")

    def check_deref_assignement(self, statement):
        self.check_expression(statement.expression)
        variable = self.current_scope[statement.variable_id]
        if ast.NormalType(variable.kind.type_name) != statement.expression.kind:
            raise Exception(f"Wrong type in assignement. Left: '{ast.NormalType(variable.kind.type_name)}', and Right: '{statement.expression.kind}'")

    def check_deref(self, expression):
        self.check_expression(expression.expression)
        expr_kind = expression.expression.kind
        if not isinstance(expr_kind, ast.RefType):
            raise Exception(f"Cannot dereference non-ref expression.")
        kind = self.ast.all_types[expr_kind.type_name]
        if not "Copy" in kind.implements:
            raise Exception(f"Cannot dereference expression of type '{kind.name}', which does not implement 'Copy'.")
        expression.kind = ast.NormalType(kind.name)


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
        kind = self.current_scope.lookup(expression.struct_name)
        method = kind.methods[expression.func_name]
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

    def check_method_call(self, expression):
        self.check_expression(expression.expression)
        kind = self.ast.all_types[expression.expression.kind.type_name]
        if expression.func_name not in kind.methods:
            raise Exception(f"No such method '{expression.func_name}' on struct '{kind.name}'.")
        method = kind.methods[expression.func_name]
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
        if statement.condition.kind != ast.NormalType("Bool"):
            raise Exception(f"Expected 'Bool', but found '{statement.condition.kind}'")
        self.check_block(statement.block)

    def check_while_statement(self, statement):
        self.check_expression(statement.condition)
        if statement.condition.kind != ast.NormalType("Bool"):
            raise Exception(f"Expected 'Bool' but found '{statement.condition.kind}'")
        self.check_block(statement.block)

    def check_structure_instanciation(self, expression):
        expression.kind = ast.NormalType(expression.name)
        structure = self.ast.all_types[expression.name]
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        if len(expression.arguments) != len(structure.fields):
            raise Exception(f"Structure '{expression.name}' has got '{len(structure.fields)}' fields.")
        for name, field in structure.fields.items():
            if expression.arguments[name].expression.kind.type_name != field.kind.type_name:
                raise Exception(f"Expected '{kind.type_name}', but got '{expression.arguments[name].expression.type_name}'")