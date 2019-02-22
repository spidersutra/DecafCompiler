import sys
import lexical
import lex

def compile(fname):
    inputFile = open(fname, "r")
    outFileName = fname.split(".")[0] + ".out"

    fileContents = inputFile.read()
    tokenList = lex.buildTokenList(fileContents)
    lex.printTokens(tokenList)
    # for t in tokenList:
    #     print(t.name,t.line,t.colStart,t.colEnd)
    # lex.writeTokens(outFileName,tokenList)
    


filename = sys.argv[1]
compile(filename)    