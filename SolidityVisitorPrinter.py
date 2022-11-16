from sol2DIR.Dystonizer import *

from antlr4 import *
import os


def convert(inputfile: FileStream):
    lexer = SolidityLexer(inputfile)
    token_stream = CommonTokenStream(lexer)
    parser = SolidityParser(token_stream)
    tree = parser.sourceUnit()
    DystonizerStep3().visit(tree)


def main():
    # 입력, 출력 파일 이름 print
    srcDir = r"input"
    dstDir = r"output"
    print("start Dystonizer solidity file")

    for file in os.listdir(srcDir):
        print("input files...\n")
        convert(FileStream(f"input/{file}", encoding="utf-8"))

    for file in os.listdir(dstDir):
        print("output files...")
        print(file)


if __name__ == '__main__':
    main()
