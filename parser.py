from antlr_output.languageVisitor import languageVisitor
from ast import *
# from mybuiltins import builtin_functions, builtin_structs, builtin_traits


class Parser(languageVisitor):
    def position(self, ctx):
        start = ctx.start
        stop = ctx.stop
        return (start.start, stop.stop, start.line, start.column)

    def visitEntry_point(self, ctx):
        builtin_functions = {}
        builtin_structures = {}
        for function in ctx.builtin_function():
            new_function = self.visitBuiltin_function(function)
            builtin_functions[new_function.name] = new_function
        for structure in ctx.builtin_structure():
            new_structure = self.visitBuiltin_structure(structure)
            builtin_structures[new_structure.name] = new_structure
        functions = {}
        structures = {}
        traits = {}
        for function in ctx.function_declaration():
            new_function = self.visitFunction_declaration(function)
            functions[new_function.name] = new_function
        for structure in ctx.structure_declaration():
            new_structure = self.visitStructure_declaration(structure)
            structures[new_structure.name] = new_structure
        for trait in ctx.trait_declaration():
            new_trait = self.visitTrait_declaration(trait)
            traits[new_trait.name] = new_trait
        result = Root(structures, functions, traits, builtin_functions, builtin_structures)
        return result

    def visitBuiltin_function(self, ctx):
        function_prototype = self.visitFunction_prototype(ctx.function_prototype())
        return BuiltinFunction(
            function_prototype.name,
            function_prototype.parameters,
            function_prototype.return_type
        )

    def visitBuiltin_structure(self, ctx):
        name = ctx.IDENTIFIER().getText()
        stack_size = int(ctx.NUMBER().getText())
        methods = {}
        for method in ctx.builtin_function():
            new_method = self.visitBuiltin_function(method)
            methods[new_method.name] = new_method
        if ctx.implements():
            implements = self.visitImplements(ctx.implements())
        else:
            implements = []
        return BuiltinStructure(
            name,
            stack_size,
            {},
            methods,
            implements
        )

    def visitGenerics(self, ctx):
        result = {}
        for generic in ctx.generic():
            new_generic = self.visitGeneric(generic)
            result[new_generic.name] = new_generic
        return result

    def visitGeneric(self, ctx):
        name = ctx.IDENTIFIER().getText()
        if ctx.implements() is not None:
            implements = self.visitImplements(ctx.implements())
        else:
            implements = None
        return GenericType(name, implements)

    def visitImplements(self, ctx):
        result = []
        for normal_type in ctx.normal_type():
            result.append(normal_type.IDENTIFIER().getText())
        return result

    def visitTrait_declaration(self, ctx):
        name = ctx.IDENTIFIER().getText()
        functions = {}
        for function in ctx.function_prototype():
            new_function = self.visitFunction_prototype(function)
            functions[new_function.name] = new_function
        return Trait(name, functions)

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
        if ctx.implements():
            implements = self.visitImplements(ctx.implements())
        else:
            implements = ()
        return Structure(name, attributes, methods, implements)

    def visitAttribute_declaration(self, ctx):
        attribute_name = ctx.IDENTIFIER().getText()
        kind = self.visitType_annotation(ctx.type_annotation())
        return Field(attribute_name, kind)

    def visitFunction_prototype(self, ctx):
        function_name = ctx.IDENTIFIER().getText()
        if ctx.parameters():
            parameters = self.visitParameters_list(ctx.parameters())
        else:
            parameters = []
        return_type = self.visitType_annotation(ctx.type_annotation())
        return FunctionPrototype(function_name, parameters, return_type)

    def visitFunction_declaration(self, ctx):
        function_name = ctx.IDENTIFIER().getText()
        if ctx.parameters():
            parameters = self.visitParameters_list(ctx.parameters())
        else:
            parameters = []
        return_type = self.visitType_annotation(ctx.type_annotation())
        block = self.visitBlock(ctx.block())
        if ctx.generics():
            generics = self.visitGenerics(ctx.generics())
            return GenericFunction(function_name, parameters, return_type, block, generics)
        else:
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
        elif ctx.while_statement():
            return self.visitWhile_statement(ctx.while_statement())
        elif ctx.assignement():
            return self.visitAssignement(ctx.assignement())
        elif ctx.deref_assignement():
            return self.visitDeref_assignement(ctx.deref_assignement())

    def visitReturn_statement(self, ctx):
        return Return(self.visitExpression(ctx.expression()))

    def visitCondition(self, ctx):
        condition = self.visitExpression(ctx.expression())
        block = self.visitBlock(ctx.block())
        else_block = self.visitElse_block(ctx.else_block())
        return IfStatement(condition, block, else_block)

    def visitWhile_statement(self, ctx):
        condition = self.visitExpression(ctx.expression())
        block = self.visitBlock(ctx.block())
        return WhileStatement(condition, block)

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

    def visitAssignement(self, ctx):
        variable_name = ctx.IDENTIFIER().getText()
        expression = self.visitExpression(ctx.expression())
        return Assignement(variable_name, expression)

    def visitDeref_assignement(self, ctx):
        variable_name = ctx.IDENTIFIER().getText()
        expression = self.visitExpression(ctx.expression())
        return DerefAssignement(variable_name, expression)

    def visitExpression(self, ctx):
        if ctx.factor():
            return self.visitFactor(ctx.factor())
        if ctx.function_call():
            return self.visitFunction_call(ctx.function_call())
        elif ctx.classmethod_call():
            return self.visitClassmethod_call(ctx.classmethod_call())
        elif ctx.structure_instantiation():
            return self.visitStructure_instantiation(ctx.structure_instantiation())
        elif ctx.lvalue_ref():
            return self.visitLvalue_ref(ctx.lvalue_ref())
        elif ctx.rvalue_ref():
            return self.visitRvalue_ref(ctx.rvalue_ref())
        elif ctx.deref():
            return self.visitDeref(ctx.deref())
        elif ctx.LPAREN():
            return self.visitMethod_call(ctx)
        elif ctx.IDENTIFIER():
            return self.visitGet_attribute(ctx)
        else:
            return self.visitBinary_expression(ctx)
    
    def visitBinary_expression(self, ctx):
        if ctx.EQ(): kind = BinaryEq
        elif ctx.NEQ(): kind = BinaryNeq
        elif ctx.ADD(): kind = BinaryAdd
        elif ctx.SUB(): kind = BinarySub
        elif ctx.MUL(): kind = BinaryMul
        left, right = map(self.visitExpression, ctx.expression())
        return kind(left, right)

    def visitGet_attribute(self, ctx):
        expression = self.visitExpression(ctx.expression()[0])
        name = ctx.IDENTIFIER().getText()
        return GetAttribute(expression, name)

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

    def visitReference(self, ctx):
        if ctx.rvalue_ref():
            return self.visitRvalue_ref(ctx.rvalue_ref())
        else:
            return self.visitLvalue_ref(ctx.lvalue_ref())
    
    def visitRvalue_ref(self, ctx):
        expression = self.visitExpression(ctx.expression())
        return RValueRef(expression)

    def visitLvalue_ref(self, ctx):
        name = ctx.IDENTIFIER().getText()
        return LValueRef(name)

    def visitDeref(self, ctx):
        return DeRef(self.visitExpression(ctx.expression()))

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
        elif ctx.expression():
            return self.visitExpression(ctx.expression())

    def visitMethod_call(self, ctx):
        expression = self.visitExpression(ctx.expression()[0])
        name = ctx.IDENTIFIER().getText()
        arguments = [Argument(expression)] + self.visitArguments(ctx.arguments())
        return MethodCall(expression, name, arguments)
    
    def visitFunction_call(self, ctx):
        name = ctx.IDENTIFIER().getText()
        arguments = self.visitArguments(ctx.arguments())
        if ctx.generics_ref():
            generics = self.visitGenerics_ref(ctx.generics_ref())
        else:
            generics = []
        return FunctionCall(name, arguments, generics)

    def visitGenerics_ref(self, ctx):
        generic_types = []
        for normal_type in ctx.normal_type():
            name = normal_type.IDENTIFIER().getText()
            generic_types.append(NormalType(name))
        return generic_types
    
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