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


    # Visit a parse tree produced by languageParser#trait_declaration.
    def visitTrait_declaration(self, ctx:languageParser.Trait_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_prototype.
    def visitFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#builtin_function.
    def visitBuiltin_function(self, ctx:languageParser.Builtin_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#builtin_structure.
    def visitBuiltin_structure(self, ctx:languageParser.Builtin_structureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#implements.
    def visitImplements(self, ctx:languageParser.ImplementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#generics.
    def visitGenerics(self, ctx:languageParser.GenericsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#generic.
    def visitGeneric(self, ctx:languageParser.GenericContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#generics_ref.
    def visitGenerics_ref(self, ctx:languageParser.Generics_refContext):
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


    # Visit a parse tree produced by languageParser#reference.
    def visitReference(self, ctx:languageParser.ReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#rvalue_ref.
    def visitRvalue_ref(self, ctx:languageParser.Rvalue_refContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#lvalue_ref.
    def visitLvalue_ref(self, ctx:languageParser.Lvalue_refContext):
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


    # Visit a parse tree produced by languageParser#binary_expression.
    def visitBinary_expression(self, ctx:languageParser.Binary_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_and.
    def visitBinary_and(self, ctx:languageParser.Binary_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_or.
    def visitBinary_or(self, ctx:languageParser.Binary_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_eq.
    def visitBinary_eq(self, ctx:languageParser.Binary_eqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_neq.
    def visitBinary_neq(self, ctx:languageParser.Binary_neqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_mul.
    def visitBinary_mul(self, ctx:languageParser.Binary_mulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_add.
    def visitBinary_add(self, ctx:languageParser.Binary_addContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#binary_sub.
    def visitBinary_sub(self, ctx:languageParser.Binary_subContext):
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


    # Visit a parse tree produced by languageParser#deref_assignement.
    def visitDeref_assignement(self, ctx:languageParser.Deref_assignementContext):
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


    # Visit a parse tree produced by languageParser#while_statement.
    def visitWhile_statement(self, ctx:languageParser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#true.
    def visitTrue(self, ctx:languageParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#false.
    def visitFalse(self, ctx:languageParser.FalseContext):
        return self.visitChildren(ctx)



del languageParser