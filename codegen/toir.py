import ir
import ast
import hashlib


class ToIR:
    def __init__(self, code):
        self.ir = code
        self.result = ir.Program()
        self.current_scope = None
        self.condition_number = 0

    @staticmethod
    def convert_function_name(name):
        return f"func__{hashlib.md5(name.encode()).hexdigest()}"

    def convert(self):
        self.create_main()
        # print(self.ir.functions)
        for func_name, function in self.ir.functions.items():
            self.convert_function(function)
        return self.result

    def create_main(self):
        function = self.ir.functions["main"]
        self.result.text.add(ir.LABEL("main"))
        self.result.text.add(ir.FUNCTION_PRELUDE())
        self.result.text.add(ir.PREPARE_RETURN(function.return_size))
        self.result.text.add(ir.PREPARE_SCOPE(function.scope_size))
        self.result.text.add(ir.CALL_FUNCTION(function.name))
        self.result.text.add(ir.POP_SCOPE(function.scope_size))
        self.result.text.add(ir.FUNCTION_END())

    def convert_function(self, function):
        self.current_scope = function.variables
        # print(function.name, function.variables)
        self.result.text.add(ir.LABEL(function.name))
        self.result.text.add(ir.FUNCTION_PRELUDE())
        self.convert_statements(function.statements)
        self.result.text.add(ir.FUNCTION_END())
    
    def convert_statements(self, statements):
        for statement in statements:
            self.convert_statement(statement)

    def convert_statement(self, statement):
        if isinstance(statement, ast.Expression):
            self.convert_expression(statement)
        elif isinstance(statement, ast.VariableDeclaration):
            self.convert_variable_declaration(statement)
        elif isinstance(statement, ast.Return):
            self.convert_return(statement)
        elif isinstance(statement, ast.IfStatement):
            self.convert_if_statement(statement)
    
    def convert_expression(self, expression):
        if isinstance(expression, ast.FunctionCall):
            self.convert_function_call(expression)
        elif isinstance(expression, ast.ClassmethodCall):
            self.convert_classmethod_call(expression)
        elif isinstance(expression, ast.String):
            string_id = self.result.rodata.add_string_litteral(expression.value)
            string_label = f"string_{string_id}"
            self.result.text.add(ir.LOAD_STRING_LITTERAL(string_label, len(expression.value)))
        elif isinstance(expression, ast.Number):
            self.result.text.add(ir.LOAD_VALUE(int(expression.value)))
        elif isinstance(expression, ast.Bool):
            self.result.text.add(ir.LOAD_VALUE(expression.value))
        elif isinstance(expression, ast.VariableReference):
            self.convert_variable_reference(expression)
        elif isinstance(expression, ast.MakeRef):
            self.convert_make_ref(expression)
        elif isinstance(expression, ast.DeRef):
            self.convert_deref(expression)

    def convert_function_call(self, expression):
        func_name = expression.name
        function = self.ir.all_functions[func_name]
        self._convert_function_call(expression, function)

    def convert_classmethod_call(self, expression):
        func_name = f"{expression.struct_name}::{expression.func_name}"
        function = self.ir.all_functions[func_name]
        self._convert_function_call(expression, function)

    def _convert_function_call(self, expression, function):
        new_func_name = function.name
        self.result.text.add(ir.PREPARE_RETURN(function.return_size))
        self.result.text.add(ir.PREPARE_SCOPE(function.scope_size))
        for argument in expression.arguments:
            self.convert_argument(argument, function)
        self.result.text.add(ir.CALL_FUNCTION(new_func_name))
        self.result.text.add(ir.POP_SCOPE(function.scope_size))

    def convert_argument(self, argument, function):
        variable = function.variables[argument.variable_id]
        self.convert_expression(argument.expression)
        self.result.text.add(ir.STORE_ARGUMENT(variable.offset, variable.size))

    def convert_variable_declaration(self, statement):
        self.convert_expression(statement.expression)
        variable = self.current_scope[statement.variable_id]
        self.result.text.add(ir.STORE_VARIABLE(variable.offset, variable.size))

    def convert_return(self, statement):
        self.convert_expression(statement.expression)
        expr_len = self.ir.types[statement.expression.kind.type_name].stack_size
        self.result.text.add(ir.RETURN(expr_len))

    def convert_variable_reference(self, expression):
        variable = self.current_scope[expression.variable_id]
        self.result.text.add(ir.LOAD_VARIABLE(variable.offset, variable.size))

    def convert_make_ref(self, expression):
        variable = self.current_scope[expression.variable_id]
        self.result.text.add(ir.LOAD_REF(variable.offset))

    def convert_deref(self, expression):
        variable = self.current_scope[expression.variable_id]
        self.result.text.add(ir.LOAD_DEREF(variable.offset, 8))

    def convert_if_statement(self, statement):
        if_label_name = f".if__{self.condition_number}"
        else_label_name = f".else__{self.condition_number}"
        self.condition_number += 1
        self.result.text.add(ir.LABEL(if_label_name))
        self.convert_expression(statement.condition)
        size = self.ir.types["Bool"].stack_size
        self.result.text.add(ir.POP_JMP_IF_FALSE(size, else_label_name))
        self.convert_statements(statement.block.statements)
        self.result.text.add(ir.LABEL(else_label_name))