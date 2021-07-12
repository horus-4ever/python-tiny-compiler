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


    # Enter a parse tree produced by languageParser#trait_declaration.
    def enterTrait_declaration(self, ctx:languageParser.Trait_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#trait_declaration.
    def exitTrait_declaration(self, ctx:languageParser.Trait_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#function_prototype.
    def enterFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        pass

    # Exit a parse tree produced by languageParser#function_prototype.
    def exitFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        pass


    # Enter a parse tree produced by languageParser#builtin_function.
    def enterBuiltin_function(self, ctx:languageParser.Builtin_functionContext):
        pass

    # Exit a parse tree produced by languageParser#builtin_function.
    def exitBuiltin_function(self, ctx:languageParser.Builtin_functionContext):
        pass


    # Enter a parse tree produced by languageParser#builtin_structure.
    def enterBuiltin_structure(self, ctx:languageParser.Builtin_structureContext):
        pass

    # Exit a parse tree produced by languageParser#builtin_structure.
    def exitBuiltin_structure(self, ctx:languageParser.Builtin_structureContext):
        pass


    # Enter a parse tree produced by languageParser#implements.
    def enterImplements(self, ctx:languageParser.ImplementsContext):
        pass

    # Exit a parse tree produced by languageParser#implements.
    def exitImplements(self, ctx:languageParser.ImplementsContext):
        pass


    # Enter a parse tree produced by languageParser#generics.
    def enterGenerics(self, ctx:languageParser.GenericsContext):
        pass

    # Exit a parse tree produced by languageParser#generics.
    def exitGenerics(self, ctx:languageParser.GenericsContext):
        pass


    # Enter a parse tree produced by languageParser#generic.
    def enterGeneric(self, ctx:languageParser.GenericContext):
        pass

    # Exit a parse tree produced by languageParser#generic.
    def exitGeneric(self, ctx:languageParser.GenericContext):
        pass


    # Enter a parse tree produced by languageParser#generics_ref.
    def enterGenerics_ref(self, ctx:languageParser.Generics_refContext):
        pass

    # Exit a parse tree produced by languageParser#generics_ref.
    def exitGenerics_ref(self, ctx:languageParser.Generics_refContext):
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


    # Enter a parse tree produced by languageParser#reference.
    def enterReference(self, ctx:languageParser.ReferenceContext):
        pass

    # Exit a parse tree produced by languageParser#reference.
    def exitReference(self, ctx:languageParser.ReferenceContext):
        pass


    # Enter a parse tree produced by languageParser#rvalue_ref.
    def enterRvalue_ref(self, ctx:languageParser.Rvalue_refContext):
        pass

    # Exit a parse tree produced by languageParser#rvalue_ref.
    def exitRvalue_ref(self, ctx:languageParser.Rvalue_refContext):
        pass


    # Enter a parse tree produced by languageParser#lvalue_ref.
    def enterLvalue_ref(self, ctx:languageParser.Lvalue_refContext):
        pass

    # Exit a parse tree produced by languageParser#lvalue_ref.
    def exitLvalue_ref(self, ctx:languageParser.Lvalue_refContext):
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


    # Enter a parse tree produced by languageParser#binary_expression.
    def enterBinary_expression(self, ctx:languageParser.Binary_expressionContext):
        pass

    # Exit a parse tree produced by languageParser#binary_expression.
    def exitBinary_expression(self, ctx:languageParser.Binary_expressionContext):
        pass


    # Enter a parse tree produced by languageParser#binary_and.
    def enterBinary_and(self, ctx:languageParser.Binary_andContext):
        pass

    # Exit a parse tree produced by languageParser#binary_and.
    def exitBinary_and(self, ctx:languageParser.Binary_andContext):
        pass


    # Enter a parse tree produced by languageParser#binary_or.
    def enterBinary_or(self, ctx:languageParser.Binary_orContext):
        pass

    # Exit a parse tree produced by languageParser#binary_or.
    def exitBinary_or(self, ctx:languageParser.Binary_orContext):
        pass


    # Enter a parse tree produced by languageParser#binary_eq.
    def enterBinary_eq(self, ctx:languageParser.Binary_eqContext):
        pass

    # Exit a parse tree produced by languageParser#binary_eq.
    def exitBinary_eq(self, ctx:languageParser.Binary_eqContext):
        pass


    # Enter a parse tree produced by languageParser#binary_neq.
    def enterBinary_neq(self, ctx:languageParser.Binary_neqContext):
        pass

    # Exit a parse tree produced by languageParser#binary_neq.
    def exitBinary_neq(self, ctx:languageParser.Binary_neqContext):
        pass


    # Enter a parse tree produced by languageParser#binary_mul.
    def enterBinary_mul(self, ctx:languageParser.Binary_mulContext):
        pass

    # Exit a parse tree produced by languageParser#binary_mul.
    def exitBinary_mul(self, ctx:languageParser.Binary_mulContext):
        pass


    # Enter a parse tree produced by languageParser#binary_add.
    def enterBinary_add(self, ctx:languageParser.Binary_addContext):
        pass

    # Exit a parse tree produced by languageParser#binary_add.
    def exitBinary_add(self, ctx:languageParser.Binary_addContext):
        pass


    # Enter a parse tree produced by languageParser#binary_sub.
    def enterBinary_sub(self, ctx:languageParser.Binary_subContext):
        pass

    # Exit a parse tree produced by languageParser#binary_sub.
    def exitBinary_sub(self, ctx:languageParser.Binary_subContext):
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


    # Enter a parse tree produced by languageParser#deref_assignement.
    def enterDeref_assignement(self, ctx:languageParser.Deref_assignementContext):
        pass

    # Exit a parse tree produced by languageParser#deref_assignement.
    def exitDeref_assignement(self, ctx:languageParser.Deref_assignementContext):
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


    # Enter a parse tree produced by languageParser#while_statement.
    def enterWhile_statement(self, ctx:languageParser.While_statementContext):
        pass

    # Exit a parse tree produced by languageParser#while_statement.
    def exitWhile_statement(self, ctx:languageParser.While_statementContext):
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