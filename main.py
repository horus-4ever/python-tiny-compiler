import sys
from antlr4 import *
from antlr_output.languageLexer import languageLexer
from antlr_output.languageParser import languageParser
from parser import Parser
from analysis import NameChecker, TypeChecker, BorrowChecker
from codegen import NameConverter, ToIR, ToASM

# alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'
# antlr4 -o antlr_output/ -Dlanguage=Python3 -visitor language.g4
# ('<' normal_type (',' normal_type)* '>')? ;

def main(argv):
    with open("code_examples/test_1") as doc:
        CODE = doc.read()

    input = InputStream(CODE)

    lexer = languageLexer(input)
    tokens = CommonTokenStream(lexer)
    parser = languageParser(tokens)
    tree = parser.entry_point()

    # print(tree.toStringTree(recog=parser))

    ast_parser = Parser()
    ast = ast_parser.visitEntry_point(tree)
    print(ast.functions, "\n", ast.structures)

    name_checker = NameChecker(ast)
    ast = name_checker.check()
    # print(ast.functions, "\n", ast.structures)

    type_checker = TypeChecker(ast)
    ast = type_checker.check()
    # print(ast.functions, "\n", ast.structures)

    borrow_checker = BorrowChecker(ast)
    ast = borrow_checker.check()
    # print(ast.functions, "\n", ast.structures)
    
    name_converter = NameConverter(ast)
    ir = name_converter.convert()
    # print("\n", ir)

    ir_converter = ToIR(ir)
    ir = ir_converter.convert()
    print(ir)
    
    assembly = ToASM(ir)
    assembly = assembly.to_asm()
    with open("out/out.s", "w") as doc:
        doc.write(assembly)


if __name__ == '__main__':
    main(sys.argv)