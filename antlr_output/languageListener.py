# Generated from language.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .languageParser import languageParser
else:
    from languageParser import languageParser

# This class defines a complete listener for a parse tree produced by languageParser.
class languageListener(ParseTreeListener):

    # Enter a parse tree produced by languageParser#entry_point.
    def enterEntry_point(self, ctx:languageParser.Entry_pointContext):
        pass

    # Exit a parse tree produced by languageParser#entry_point.
    def exitEntry_point(self, ctx:languageParser.Entry_pointContext):
        pass


    # Enter a parse tree produced by languageParser#structure_declaration.
    def enterStructure_declaration(self, ctx:languageParser.Structure_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#structure_declaration.
    def exitStructure_declaration(self, ctx:languageParser.Structure_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#attribute_declaration.
    def enterAttribute_declaration(self, ctx:languageParser.Attribute_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#attribute_declaration.
    def exitAttribute_declaration(self, ctx:languageParser.Attribute_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#type_annotation.
    def enterType_annotation(self, ctx:languageParser.Type_annotationContext):
        pass

    # Exit a parse tree produced by languageParser#type_annotation.
    def exitType_annotation(self, ctx:languageParser.Type_annotationContext):
        pass


    # Enter a parse tree produced by languageParser#kind.
    def enterKind(self, ctx:languageParser.KindContext):
        pass

    # Exit a parse tree produced by languageParser#kind.
    def exitKind(self, ctx:languageParser.KindContext):
        pass


    # Enter a parse tree produced by languageParser#ref_type.
    def enterRef_type(self, ctx:languageParser.Ref_typeContext):
        pass

    # Exit a parse tree produced by languageParser#ref_type.
    def exitRef_type(self, ctx:languageParser.Ref_typeContext):
        pass


    # Enter a parse tree produced by languageParser#normal_type.
    def enterNormal_type(self, ctx:languageParser.Normal_typeContext):
        pass

    # Exit a parse tree produced by languageParser#normal_type.
    def exitNormal_type(self, ctx:languageParser.Normal_typeContext):
        pass


    # Enter a parse tree produced by languageParser#function_declaration.
    def enterFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#function_declaration.
    def exitFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#parameters.
    def enterParameters(self, ctx:languageParser.ParametersContext):
        pass

    # Exit a parse tree produced by languageParser#parameters.
    def exitParameters(self, ctx:languageParser.ParametersContext):
        pass


    # Enter a parse tree produced by languageParser#parameter.
    def enterParameter(self, ctx:languageParser.ParameterContext):
        pass

    # Exit a parse tree produced by languageParser#parameter.
    def exitParameter(self, ctx:languageParser.ParameterContext):
        pass


    # Enter a parse tree produced by languageParser#block.
    def enterBlock(self, ctx:languageParser.BlockContext):
        pass

    # Exit a parse tree produced by languageParser#block.
    def exitBlock(self, ctx:languageParser.BlockContext):
        pass


    # Enter a parse tree produced by languageParser#statement.
    def enterStatement(self, ctx:languageParser.StatementContext):
        pass

    # Exit a parse tree produced by languageParser#statement.
    def exitStatement(self, ctx:languageParser.StatementContext):
        pass


    # Enter a parse tree produced by languageParser#expression.
    def enterExpression(self, ctx:languageParser.ExpressionContext):
        pass

    # Exit a parse tree produced by languageParser#expression.
    def exitExpression(self, ctx:languageParser.ExpressionContext):
        pass


    # Enter a parse tree produced by languageParser#make_ref.
    def enterMake_ref(self, ctx:languageParser.Make_refContext):
        pass

    # Exit a parse tree produced by languageParser#make_ref.
    def exitMake_ref(self, ctx:languageParser.Make_refContext):
        pass


    # Enter a parse tree produced by languageParser#deref.
    def enterDeref(self, ctx:languageParser.DerefContext):
        pass

    # Exit a parse tree produced by languageParser#deref.
    def exitDeref(self, ctx:languageParser.DerefContext):
        pass


    # Enter a parse tree produced by languageParser#factor.
    def enterFactor(self, ctx:languageParser.FactorContext):
        pass

    # Exit a parse tree produced by languageParser#factor.
    def exitFactor(self, ctx:languageParser.FactorContext):
        pass


    # Enter a parse tree produced by languageParser#get_attribute.
    def enterGet_attribute(self, ctx:languageParser.Get_attributeContext):
        pass

    # Exit a parse tree produced by languageParser#get_attribute.
    def exitGet_attribute(self, ctx:languageParser.Get_attributeContext):
        pass


    # Enter a parse tree produced by languageParser#function_call.
    def enterFunction_call(self, ctx:languageParser.Function_callContext):
        pass

    # Exit a parse tree produced by languageParser#function_call.
    def exitFunction_call(self, ctx:languageParser.Function_callContext):
        pass


    # Enter a parse tree produced by languageParser#method_call.
    def enterMethod_call(self, ctx:languageParser.Method_callContext):
        pass

    # Exit a parse tree produced by languageParser#method_call.
    def exitMethod_call(self, ctx:languageParser.Method_callContext):
        pass


    # Enter a parse tree produced by languageParser#classmethod_call.
    def enterClassmethod_call(self, ctx:languageParser.Classmethod_callContext):
        pass

    # Exit a parse tree produced by languageParser#classmethod_call.
    def exitClassmethod_call(self, ctx:languageParser.Classmethod_callContext):
        pass


    # Enter a parse tree produced by languageParser#arguments.
    def enterArguments(self, ctx:languageParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by languageParser#arguments.
    def exitArguments(self, ctx:languageParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by languageParser#field_arguments.
    def enterField_arguments(self, ctx:languageParser.Field_argumentsContext):
        pass

    # Exit a parse tree produced by languageParser#field_arguments.
    def exitField_arguments(self, ctx:languageParser.Field_argumentsContext):
        pass


    # Enter a parse tree produced by languageParser#structure_instantiation.
    def enterStructure_instantiation(self, ctx:languageParser.Structure_instantiationContext):
        pass

    # Exit a parse tree produced by languageParser#structure_instantiation.
    def exitStructure_instantiation(self, ctx:languageParser.Structure_instantiationContext):
        pass


    # Enter a parse tree produced by languageParser#array.
    def enterArray(self, ctx:languageParser.ArrayContext):
        pass

    # Exit a parse tree produced by languageParser#array.
    def exitArray(self, ctx:languageParser.ArrayContext):
        pass


    # Enter a parse tree produced by languageParser#non_expression.
    def enterNon_expression(self, ctx:languageParser.Non_expressionContext):
        pass

    # Exit a parse tree produced by languageParser#non_expression.
    def exitNon_expression(self, ctx:languageParser.Non_expressionContext):
        pass


    # Enter a parse tree produced by languageParser#variable_declaration.
    def enterVariable_declaration(self, ctx:languageParser.Variable_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#variable_declaration.
    def exitVariable_declaration(self, ctx:languageParser.Variable_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#assignement.
    def enterAssignement(self, ctx:languageParser.AssignementContext):
        pass

    # Exit a parse tree produced by languageParser#assignement.
    def exitAssignement(self, ctx:languageParser.AssignementContext):
        pass


    # Enter a parse tree produced by languageParser#condition.
    def enterCondition(self, ctx:languageParser.ConditionContext):
        pass

    # Exit a parse tree produced by languageParser#condition.
    def exitCondition(self, ctx:languageParser.ConditionContext):
        pass


    # Enter a parse tree produced by languageParser#else_block.
    def enterElse_block(self, ctx:languageParser.Else_blockContext):
        pass

    # Exit a parse tree produced by languageParser#else_block.
    def exitElse_block(self, ctx:languageParser.Else_blockContext):
        pass


    # Enter a parse tree produced by languageParser#set_attribute.
    def enterSet_attribute(self, ctx:languageParser.Set_attributeContext):
        pass

    # Exit a parse tree produced by languageParser#set_attribute.
    def exitSet_attribute(self, ctx:languageParser.Set_attributeContext):
        pass


    # Enter a parse tree produced by languageParser#return_statement.
    def enterReturn_statement(self, ctx:languageParser.Return_statementContext):
        pass

    # Exit a parse tree produced by languageParser#return_statement.
    def exitReturn_statement(self, ctx:languageParser.Return_statementContext):
        pass


    # Enter a parse tree produced by languageParser#true.
    def enterTrue(self, ctx:languageParser.TrueContext):
        pass

    # Exit a parse tree produced by languageParser#true.
    def exitTrue(self, ctx:languageParser.TrueContext):
        pass


    # Enter a parse tree produced by languageParser#false.
    def enterFalse(self, ctx:languageParser.FalseContext):
        pass

    # Exit a parse tree produced by languageParser#false.
    def exitFalse(self, ctx:languageParser.FalseContext):
        pass



del languageParser