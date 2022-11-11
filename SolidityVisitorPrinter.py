from sol_dystoneVisitor import sol_dystoneVisitor
from gen.SolidityLexer import SolidityLexer
from gen.SolidityParser import SolidityParser

from antlr4 import *
import os.path

def main():
    lexer = SolidityLexer(FileStream("input/solidity_input.sol", encoding="utf-8"))
    #입력, 출력 파일 이름 print
    targetdir = r"input"
    tdir = r"output"
    files = os.listdir(targetdir)
    print("start Dystonizer solidity file")
    print("")

    print("input files...")
    for i in files:
        print(i)
    files2 = os.listdir(tdir)

    print("output file...")
    for i in files2:
        print(i)
    print("")

    token_stream = CommonTokenStream(lexer)

    parser = SolidityParser(token_stream)
    tree = parser.sourceUnit()

    visitor = sol_dystoneVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    main()