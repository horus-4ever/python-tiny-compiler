import ast
import ir
import hashlib


class ToIR:
    def __init__(self, ast):
        self.ast = ast
        self.condition_label_number = 0
        self.result = ir.Program()

    def convert(self):
        self.convert_methods_to_functions()
        for name, structure in filter(
            lambda element: isinstance(element[1], ast.BuiltinStructure),
            self.ast.global_scope
        ):
            for name, function in structure.methods.items():
                new_function = self.convert_builtin_function(function)
                function.ir_reference = new_function
        for name, function in filter(
            lambda element: isinstance(element[1], ast.BuiltinFunction),
            self.ast.global_scope
        ):
            new_function = self.convert_builtin_function(function)
            function.ir_reference = new_function

        for name, function in filter(
            lambda element: isinstance(element[1], ast.Function),
            self.ast.global_scope
        ):
            func_name = f"function_{hashlib.md5(function.name.encode()).hexdigest()}"
            new_function = ir.Function(func_name, None, None, None)
            function.ir_reference = new_function
            self.result.text.functions[new_function.name] = new_function
        for name, function in filter(
            lambda element: isinstance(element[1], ast.Function),
            self.ast.global_scope
        ): 
            self.convert_function(function)
        return self.result

    def convert_methods_to_functions(self):
        for struct_name, structure in filter(
            lambda element: isinstance(element[1], ast.Structure),
            self.ast.global_scope.elements.copy().items()
        ):
            for func_name, function in structure.methods.items():
                function.name = f"{struct_name}::{func_name}"
                self.ast.global_scope[function.name] = function

    def convert_function(self, function):
        # scope variables
        function_scope = function.block.scope.flatten()
        variables = []
        offset = 0
        for variable in function_scope:
            new_variable = ir.Variable(variable.kind.name, len(variable), offset)
            variable.ir_reference = new_variable
            variables.append(new_variable)
            offset += len(variable)
        function.ir_reference.variables = variables
        # return value
        return_type = function.return_type
        return_value = ir.Variable(return_type.reference.name, len(return_type.reference), 0)
        function.ir_reference.return_value = return_value
        # instructions
        self.condition_label_number = 0
        instructions = self.convert_block(function.block)
        instructions.append(ir.RETURN(function.return_type.reference))
        # function
        function.ir_reference.instructions = instructions

    def convert_builtin_function(self, function):
        # scope variables
        function_scope = function.parameters
        variables = []
        offset = 0
        for parameter in function_scope:
            new_variable = ir.Variable(parameter.kind.name, len(parameter.kind.reference), offset)
            parameter.ir_reference = new_variable
            variables.append(new_variable)
            offset += len(parameter.kind.reference)
        # return value
        return_type = function.return_type
        return_value = ir.Variable(return_type.reference.name, len(return_type.reference), 0)
        # function
        return ir.BuiltinFunction(function.name, return_value, variables)

    def convert_block(self, block):
        result = []
        this_scope_variables = [variable.ir_reference for variable in block.scope.elements.values()]
        print(this_scope_variables)
        for statement in block.statements:
            result.extend(self.convert_statement(statement))
        result.append(ir.DROP_VARIABLES(this_scope_variables))
        return result

    def convert_statement(self, statement):
        result = []
        if isinstance(statement, ast.VariableDeclaration):
            result.extend(self.convert_expression(statement.expression))
            result.append(ir.STORE_VARIABLE(statement.reference.ir_reference))
        elif isinstance(statement, ast.Return):
            result.extend(self.convert_expression(statement.expression))
            result.append(ir.DROP_VARIABLES([variable.ir_reference for variable in statement.drop_variables]))
            result.append(ir.RETURN(statement.expression.kind))
        elif isinstance(statement, ast.Expression):
            result.extend(self.convert_expression(statement))
            result.append(ir.DROP_EXPRESSION(statement.kind))
        elif isinstance(statement, ast.IfStatement):
            result.extend(self.convert_if_statement(statement))
        return result

    def convert_expression(self, expression):
        result = []
        if isinstance(expression, ast.Number):
            result.append(ir.LOAD_VALUE(expression))
        elif isinstance(expression, ast.Bool):
            result.append(ir.LOAD_VALUE(expression))
        elif isinstance(expression, ast.String):
            id = self.result.rodata.add_string_litteral(expression.value)
            result.append(ir.LOAD_STRING_LITTERAL(id))
        elif isinstance(expression, ast.FunctionCall):
            result.append(ir.PREPARE_RETURN(expression.reference.ir_reference.return_size))
            for argument in expression.arguments:
                result.extend(self.convert_expression(argument))
            if isinstance(expression.reference, ast.BuiltinFunction):
                func_name = expression.name
            else:
                func_name = f"function_{hashlib.md5(expression.name.encode()).hexdigest()}"
            result.append(ir.PREPARE_SCOPE(expression.reference.ir_reference.scope_size))
            result.append(ir.CALL_FUNCTION(func_name))
            result.append(ir.POP_SCOPE(expression.reference.ir_reference.scope_size))
        elif isinstance(expression, ast.VariableReference):
            result.append(ir.LOAD_VARIABLE(expression.reference.ir_reference))
        elif isinstance(expression, ast.ClassmethodCall):
            func_name = f"_{expression.typename}__{expression.function_name}"
            result.append(ir.PREPARE_RETURN(expression.func_reference.ir_reference.return_size))
            for argument in expression.arguments:
                result.extend(self.convert_expression(argument))
            result.append(ir.PREPARE_SCOPE(expression.func_reference.ir_reference.scope_size))
            result.append(ir.CALL_FUNCTION(func_name))
            result.append(ir.POP_SCOPE(expression.func_reference.ir_reference.scope_size))
        return result

    def convert_if_statement(self, statement):
        result = []
        result.extend(self.convert_expression(statement.condition))
        result.append(ir.POP_JMP_IF_FALSE(statement.condition.kind, self.condition_label_number))
        result.extend(self.convert_block(statement.block))
        result.append(ir.LABEL(self.condition_label_number))
        self.condition_label_number += 1
        return result