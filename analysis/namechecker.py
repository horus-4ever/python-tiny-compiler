from collections import deque
import ast


class NameChecker:
    def __init__(self, ast):
        self.ast = ast
        self.scopes = deque([self.ast.global_scope])
        self.current_structure = None

    @property
    def global_scope(self):
        return self.scopes[0]

    @property
    def current_scope(self):
        return self.scopes[-1]

    def scope_lookup(self, to_find, kind):
        current_scope = self.current_scope
        while current_scope is not None:
            for name, value in current_scope.items():
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
        # once it is checked, inline function scopes
        for name, function in self.ast.functions.items():
            self.flatten_function_scope(function)
        for name, structure in self.ast.structures.items():
            for name, method in structure.methods.items():
                self.flatten_function_scope(method)
        return self.ast

    def flatten_function_scope(self, function):
        new_scope = function.scope.flatten()
        print(new_scope)
        function.scope = new_scope

    def check_structure(self, structure):
        self.current_structure = structure
        for name, field in structure.fields.items():
            type_name = field.kind.type_name
            if type_name == "Self":
                type_name = structure.name
                field.kind.name = type_name
            if type_name not in self.ast.all_types:
                raise Exception(f"Cannot find type '{type_name}' in the global scope.")
        for name, function in structure.methods.items():
            self.check_function(function)
        self.current_structure = None

    def check_builtin_structure(self, structure):
        for name, function in structure.methods.items():
            self.check_builtin_function(function)

    def check_builtin_function(self, function):
        self.current_scope.children.append(function.scope)
        function.scope.parent = self.current_scope
        self.scopes.append(function.scope)
        self.check_parameters(function)
        self.check_return_type(function)
        self.scopes.pop()

    def check_function(self, function):
        self.current_scope.children.append(function.scope)
        function.scope.parent = self.current_scope
        self.scopes.append(function.scope)
        if isinstance(function, ast.GenericFunction):
            self.check_generic_function_parameters(function)
        self.check_parameters(function)
        self.check_return_type(function)
        self.check_block(function.block)
        self.scopes.pop()

    def check_generic_function_parameters(self, function):
        for generic_name, generic_type in function.generics.items():
            for trait_name in generic_type.implements:
                if trait_name not in self.ast.traits:
                    raise Exception(f"Trait '{trait_name}' not found in the global scope.")
                trait = self.ast.traits[trait_name]
                for method_name, method in trait.functions.items():
                    parameters = []
                    for parameter in method.parameters:
                        param_kind = type(parameter.kind)
                        if parameter.kind.type_name == "Self":
                            new_parameter = ast.Parameter(parameter.name, param_kind(generic_name))
                        else:
                            new_parameter = ast.Parameter(parameter.name, param_kind(parameter.kind.type_name))
                        parameters.append(new_parameter)
                    if method.return_type.type_name == "Self":
                        return_type = ast.NormalType(generic_name)
                    else:
                        return_type = ast.NormalType(method.return_type.type_name)
                    new_function = ast.FunctionPrototype(method_name, parameters, return_type)
                    generic_type.methods.update({method_name: new_function})
            self.current_scope[generic_name] = generic_type
    
    def check_parameters(self, function):
        for parameter in function.parameters:
            kind = parameter.kind
            if self.current_structure is not None and kind.type_name == "Self":
                kind.type_name = self.current_structure.name
            if self.scope_lookup(kind.type_name, ast.Type) is None:
                raise Exception(f"Cannot find type '{kind.type_name}' in the global scope.")
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
        if self.current_structure is not None and type_name == "Self":
            type_name = self.current_structure.name
            function.return_type.type_name = type_name
        if self.scope_lookup(type_name, ast.Type) is None:
            raise Exception(f"Cannot find type '{type_name}' in the global scope.")

    def check_block(self, block):
        if self.current_scope is not None:
            self.current_scope.children.append(block.scope)
        block.scope.parent = self.current_scope
        self.scopes.append(block.scope)
        for statement in block.statements:
            self.check_statement(statement)
        self.scopes.pop()

    def check_statement(self, statement):
        if isinstance(statement, ast.VariableDeclaration):
            self.check_variable_declaration(statement)
        elif isinstance(statement, (ast.Assignement, ast.DerefAssignement)):
            self.check_assignement(statement)
        elif isinstance(statement, ast.Return):
            # statement.drop_variables = list(self.current_scope.elements.values())
            self.check_expression(statement.expression)
        elif isinstance(statement, ast.Expression):
            self.check_expression(statement)
        elif isinstance(statement, ast.Block):
            self.check_block(statement)
        elif isinstance(statement, ast.IfStatement):
            self.check_if_statement(statement)
        elif isinstance(statement, ast.WhileStatement):
            self.check_while_statement(statement)

    def check_variable_declaration(self, statement):
        self.check_expression(statement.expression)
        if statement.name in self.current_scope:
            raise Exception(f"Variable '{statement.name}' already defined.")
        variable = ast.Variable(statement.name, statement.kind)
        self.current_scope[statement.name] = variable
        statement.variable_id = id(variable)
        if statement.kind is not None:
            if self.scope_lookup(statement.kind.type_name, ast.BuiltinStructure, ast.Structure, ast.Type) is None:
                raise Exception(f"Unkown type '{statement.type_name}'")

    def check_assignement(self, statement):
        self.check_expression(statement.expression)
        scope = self.scope_lookup(statement.name, ast.Variable)
        if scope is None:
            raise Exception(f"Variable '{statement.name}' does not exist.")
        statement.variable_id = id(scope[statement.name])

    def check_expression(self, expression):
        if isinstance(expression, (ast.VariableReference, ast.LValueRef)):
            self.check_variable_reference(expression)
        elif isinstance(expression, ast.RValueRef):
            self.check_rvalue_ref(expression)
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

    def check_get_attribute(self, expression):
        self.check_expression(expression.expression)

    def check_variable_reference(self, expression):
        scope = self.scope_lookup(expression.name, ast.Variable)
        if scope is None:
            raise Exception(f"Variable '{expression.name}' is not defined.")
        else:
            expression.variable_id = id(scope[expression.name])

    def check_rvalue_ref(self, expression):
        self.check_expression(expression.expression)
        new_variable = ast.Variable(None, None)
        self.current_scope[id(new_variable)] = new_variable
        expression.variable_id = id(new_variable)

    def check_deref(self, expression):
        self.check_expression(expression.expression)

    def check_if_statement(self, statement):
        self.check_expression(statement.condition)
        self.check_block(statement.block)

    def check_while_statement(self, statement):
        self.check_expression(statement.condition)
        self.check_block(statement.block)

    def check_function_call(self, expression):
        # print(self.ast.builtin_functions)
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

    def check_method_call(self, expression):
        self.check_expression(expression.expression)
        for argument in expression.arguments:
            self.check_expression(argument.expression)

    def check_structure_instanciation(self, expression):
        if expression.name not in self.ast.all_types:
            raise Exception(f"No such type '{expression.name}'.")
        for name, argument in expression.arguments.items():
            self.check_expression(argument.expression)
        