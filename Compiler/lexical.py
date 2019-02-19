from token import Token

breakChars = [' ', '\n','','\t']
symbolChars = ['+', '-', '*', '/', '%', '<', "<=", '>', ">=", '=', "==","!=","&&","||","!",";",",",'.',"(",")","{","}"]

def writeTokens(fileName,tokenList):
    outFile = open(fileName,"w")
    for token in tokenList:
        outTokenString = token.name
        outTokenString += "         "
        outTokenString += " line " + str(token.line)
        outTokenString += " cols " + str(token.colStart) + "-" +str(token.colEnd)
        outTokenString += " is"
        outTokenString += " " + token.flavor
        if "Constant" in token.flavor:
            outTokenString += " (value = " + token.name + ")"
        outTokenString += "\n"
        outFile.write(outTokenString)

def buildToken(tokenString, line, colStart, colEnd):
    print("BUILDING TOKEN " + tokenString)
    newToken = Token()
    newToken.name = tokenString
    newToken.line = line
    newToken.colEnd = colEnd
    newToken.colStart = colStart
    if tokenString[0] in symbolChars:
        newToken.flavor = "\'" + tokenString + "\'"
    elif tokenString[0].isdigit():
        if "." in tokenString:
            newToken.flavor = "T_DoubleConstant"
        else:
            newToken.flavor = "T_IntConstant"
    else:
        newToken.flavor = "T_Identifier"
    return newToken

def buildTokenList(fileContents):
    tokenList = []
    #iterate over file contents
    goingMerry = ""
    line = 1
    colStart = -1
    colEnd = -1
    col = 0
    for c in fileContents:
        col += 1
        print("CHAR: " + c + " COL: " + str(col))
        if c in breakChars:
            #print("BREAKING, PACK IT UP")

            #package up what we have
            if len(goingMerry) > 0:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""

            if c == '\n':
                print("RESETTING COL")
                line += 1
                col = 0
                colStart = -1
                colEnd = -1
        elif c in symbolChars:
            if len(goingMerry) == 0:
                colStart=col
                colEnd=col
                goingMerry += str(c)
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry=""
            elif goingMerry[0].isdigit() and "." not in goingMerry:
                goingMerry += str(c)
            else:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""

                colStart = col
                goingMerry += str(c)
        elif c.isdigit():
            #print(str(col) + " " + "1")

            if len(goingMerry) == 0:
                goingMerry += str(c)
                colStart = col
                print("ASSIGNED COL START: " + str(colStart))
            elif goingMerry[0] not in symbolChars:
                goingMerry += str(c)
            elif goingMerry[0] in symbolChars:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""

                colStart=col
                goingMerry += str(c)            
        else:
            if len(goingMerry) == 0:
                colStart = col
                goingMerry += str(c)
            elif goingMerry[0].isdigit():
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                
                colStart = col
                goingMerry = ""
                goingMerry += str(c)        
        #increment values

    if len(goingMerry) > 0:
        colEnd = col
        tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
    return tokenList

    #print("building token list")
