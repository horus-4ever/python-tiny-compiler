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
        result.set_builtins(**builtin_functions, **builtin_structs)
        return result

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
            type = TypeReference(kind.normal_type().IDENTIFIER().getText())
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

    def visitReturn_statement(self, ctx):
        return Return(self.visitExpression(ctx.expression()))

    def visitVariable_declaration(self, ctx):
        variable_name = ctx.IDENTIFIER().getText()
        expression = self.visitExpression(ctx.expression())
        type = ctx.type_annotation()
        if type:
            type = self.visitType_annotation(ctx.type_annotation())
        return VariableDeclaration(variable_name, expression, type=type)

    def visitExpression(self, ctx):
        if ctx.factor():
            return self.visitFactor(ctx.factor())
        if ctx.function_call():
            return self.visitFunction_call(ctx.function_call())

    def visitFactor(self, ctx):
        if ctx.NUMBER():
            return Number(ctx.NUMBER().getText())
        if ctx.string():
            return String(ctx.string().getText())
        elif ctx.IDENTIFIER():
            return VariableReference(ctx.IDENTIFIER().getText())
    
    def visitFunction_call(self, ctx):
        name = ctx.IDENTIFIER().getText()
        arguments = self.visitArguments(ctx.arguments())
        return FunctionCall(name, arguments, None)
    
    def visitArguments(self, ctx):
        if ctx is None:
            return []
        return [self.visitExpression(expression) for expression in ctx.expression()]