import sys
import lexical

def compile(fname):
    inputFile = open(fname, "r")
    outFileName = fname.split(".")[0] + ".out"
    fileContents = inputFile.read()
    #print(fileContents)
    tokenList = lexical.buildTokenList(fileContents)
    for t in tokenList:
        print(t.name,t.line,t.colStart,t.colEnd)
    lexical.writeTokens(outFileName,tokenList)
    


filename = sys.argv[1]
compile(filename)    