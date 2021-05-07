from antlr_output.languageVisitor import languageVisitor
from ast import *
from mybuiltins import builtin_functions, builtin_structs


class Parser(languageVisitor):
    def visitEntry_point(self, ctx):
        functions = []
        structures = []
        for function in ctx.function_declaration():
            functions.append(self.visitFunction_declaration(function))
        for structure in ctx.structure_declaration():
            structures.append(self.visitStructure_declaration(structure))
        result = Root(structures, functions)
        result.set_builtins(builtin_functions, builtin_structs)
        return result

    def visitStructure_declaration(self, ctx):
        name = ctx.IDENTIFIER().getText()
        methods = {}
        attributes = {}
        for function in ctx.function_declaration():
            function = self.visitFunction_declaration(function)
            methods[function.name] = function
        for attribute in ctx.attribute_declaration():
            attribute = self.visitAttribute_declaration(attribute)
            attributes[attribute.name] = attribute
        return Structure(name, attributes, methods)

    def visitAttribute_declaration(self, ctx):
        attribute_name = ctx.IDENTIFIER().getText()
        kind = self.visitType_annotation(ctx.type_annotation())
        return Field(attribute_name, kind)

    def visitFunction_declaration(self, ctx):
        function_name = ctx.IDENTIFIER().getText()
        if ctx.parameters():
            parameters = self.visitParameters_list(ctx.parameters())
        else:
            parameters = []
        return_type = self.visitType_annotation(ctx.type_annotation())
        block = self.visitBlock(ctx.block())
        return Function(function_name, parameters, return_type, block)

    def visitParameters_list(self, ctx):
        parameters = []
        for parameter in ctx.parameter():
            name = parameter.IDENTIFIER().getText()
            param_type = self.visitType_annotation(parameter.type_annotation())
            parameters.append(Parameter(name, param_type))
        return parameters

    def visitType_annotation(self, ctx):
        kind = ctx.kind()
        if kind.ref_type():
            type = RefType(kind.ref_type().normal_type().IDENTIFIER().getText())
        elif kind.normal_type():
            type = NormalType(kind.normal_type().IDENTIFIER().getText())
        return type

    def visitBlock(self, ctx):
        statements = []
        for statement in ctx.statement():
            statements.append(self.visitStatement(statement))
        return Block(statements)

    def visitStatement(self, ctx):
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        else:
            return self.visitNon_expression(ctx.non_expression())

    def visitNon_expression(self, ctx):
        if ctx.variable_declaration():
            return self.visitVariable_declaration(ctx.variable_declaration())
        elif ctx.return_statement():
            return self.visitReturn_statement(ctx.return_statement())
        elif ctx.block():
            return self.visitBlock(ctx.block())
        elif ctx.condition():
            return self.visitCondition(ctx.condition())

    def visitReturn_statement(self, ctx):
        return Return(self.visitExpression(ctx.expression()))

    def visitCondition(self, ctx):
        condition = self.visitExpression(ctx.expression())
        block = self.visitBlock(ctx.block())
        else_block = self.visitElse_block(ctx.else_block())
        return IfStatement(condition, block, else_block)

    def visitElse_block(self, ctx):
        if ctx is None:
            return None
        if ctx.condition():
            return self.visitCondition(ctx.condition())
        else:
            return self.visitBlock(ctx.block())

    def visitVariable_declaration(self, ctx):
        variable_name = ctx.IDENTIFIER().getText()
        expression = self.visitExpression(ctx.expression())
        type_name = ctx.type_annotation()
        if type_name:
            type_name = self.visitType_annotation(ctx.type_annotation())
        return VariableDeclaration(variable_name, expression, type_name)

    def visitExpression(self, ctx):
        if ctx.factor():
            return self.visitFactor(ctx.factor())
        if ctx.function_call():
            return self.visitFunction_call(ctx.function_call())
        elif ctx.classmethod_call():
            return self.visitClassmethod_call(ctx.classmethod_call())
        elif ctx.structure_instantiation():
            return self.visitStructure_instantiation(ctx.structure_instantiation())
        elif ctx.make_ref():
            return self.visitMake_ref(ctx.make_ref())
        elif ctx.deref():
            return self.visitDeref(ctx.deref())

    def visitStructure_instantiation(self, ctx):
        structure_name = ctx.IDENTIFIER().getText()
        fields_arguments = self.visitField_arguments(ctx.field_arguments())
        return StructureInstanciation(structure_name, fields_arguments)

    def visitField_arguments(self, ctx):
        if ctx is None:
            return {}
        result = {}
        for name, expression in zip(ctx.IDENTIFIER(), ctx.expression()):
            result[name.getText()] = FieldArgument(name.getText(), self.visitExpression(expression))
        return result

    def visitMake_ref(self, ctx):
        return MakeRef(ctx.IDENTIFIER().getText())

    def visitDeref(self, ctx):
        return DeRef(ctx.IDENTIFIER().getText())

    def visitFactor(self, ctx):
        if ctx.NUMBER():
            return Number(ctx.NUMBER().getText())
        if ctx.STRING():
            return String(ctx.STRING().getText()[1:-1])
        elif ctx.IDENTIFIER():
            return VariableReference(ctx.IDENTIFIER().getText())
        elif ctx.true():
            return Bool(1)
        elif ctx.false():
            return Bool(0)
    
    def visitFunction_call(self, ctx):
        name = ctx.IDENTIFIER().getText()
        arguments = self.visitArguments(ctx.arguments())
        return FunctionCall(name, arguments)
    
    def visitArguments(self, ctx):
        if ctx is None:
            return []
        return [Argument(self.visitExpression(expression)) for expression in ctx.expression()]

    def visitClassmethod_call(self, ctx):
        typename = ctx.normal_type().getText()
        methodname = ctx.IDENTIFIER().getText()
        arguments = self.visitArguments(ctx.arguments())
        return ClassmethodCall(
            typename,
            methodname,
            arguments
        )