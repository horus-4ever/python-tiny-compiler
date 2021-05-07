# Generated from language.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .languageParser import languageParser
else:
    from languageParser import languageParser

# This class defines a complete generic visitor for a parse tree produced by languageParser.

class languageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by languageParser#entry_point.
    def visitEntry_point(self, ctx:languageParser.Entry_pointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#structure_declaration.
    def visitStructure_declaration(self, ctx:languageParser.Structure_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#attribute_declaration.
    def visitAttribute_declaration(self, ctx:languageParser.Attribute_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#type_annotation.
    def visitType_annotation(self, ctx:languageParser.Type_annotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#kind.
    def visitKind(self, ctx:languageParser.KindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#ref_type.
    def visitRef_type(self, ctx:languageParser.Ref_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#normal_type.
    def visitNormal_type(self, ctx:languageParser.Normal_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_declaration.
    def visitFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#parameters.
    def visitParameters(self, ctx:languageParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#parameter.
    def visitParameter(self, ctx:languageParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#block.
    def visitBlock(self, ctx:languageParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#statement.
    def visitStatement(self, ctx:languageParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#expression.
    def visitExpression(self, ctx:languageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#make_ref.
    def visitMake_ref(self, ctx:languageParser.Make_refContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#deref.
    def visitDeref(self, ctx:languageParser.DerefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#factor.
    def visitFactor(self, ctx:languageParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#get_attribute.
    def visitGet_attribute(self, ctx:languageParser.Get_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_call.
    def visitFunction_call(self, ctx:languageParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#method_call.
    def visitMethod_call(self, ctx:languageParser.Method_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#classmethod_call.
    def visitClassmethod_call(self, ctx:languageParser.Classmethod_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#arguments.
    def visitArguments(self, ctx:languageParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#field_arguments.
    def visitField_arguments(self, ctx:languageParser.Field_argumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#structure_instantiation.
    def visitStructure_instantiation(self, ctx:languageParser.Structure_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#array.
    def visitArray(self, ctx:languageParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#non_expression.
    def visitNon_expression(self, ctx:languageParser.Non_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#variable_declaration.
    def visitVariable_declaration(self, ctx:languageParser.Variable_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#assignement.
    def visitAssignement(self, ctx:languageParser.AssignementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#condition.
    def visitCondition(self, ctx:languageParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#else_block.
    def visitElse_block(self, ctx:languageParser.Else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#set_attribute.
    def visitSet_attribute(self, ctx:languageParser.Set_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#return_statement.
    def visitReturn_statement(self, ctx:languageParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#true.
    def visitTrue(self, ctx:languageParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#false.
    def visitFalse(self, ctx:languageParser.FalseContext):
        return self.visitChildren(ctx)



del languageParser