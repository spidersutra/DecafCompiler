import sys
import lexical

def compile(fname):
    inputFile = open(fname, "r")
    fileContents = inputFile.read()
    #print(fileContents)
    tokenList = lexical.buildTokenList(fileContents)
    for t in tokenList:
        print(t.name)
    


filename = sys.argv[1]
compile(filename)    