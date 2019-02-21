from token import Token

breakChars = [' ', '\n','','\t']
symbolChars = ['+', '-', '*', '/', '%', '<', "<=", '>', ">=", '=', "==","!=","&&","||","!",";",",",'.',"(",")","{","}"]


def writeTokens(fileName,tokenList):
    outFile = open(fileName,"w")
    for token in tokenList:
        outTokenString = ""
        if token.hasError:
            outTokenString += "\n*** Error line " + str(token.line) + "." + "\n"
            if token.errorType == "too long":
                outTokenString += "*** Identifier too long: " + "\"" + token.name + "\"" + "\n\n"
            elif token.errorType == "unrecognized char":
                outTokenString += "*** Unrecognized char: \'" + token.name + "\'\n\n"
            elif token.errorType == "unterminated string":
                outTokenString += "*** Unterminated string constant: " + token.name + "\n"

        if token.errorType != "unrecognized char" and token.errorType != "unterminated string":
            outTokenString += token.name
            outTokenString += "         "
            outTokenString += " line " + str(token.line)
            outTokenString += " cols " + str(token.colStart) + "-" +str(token.colEnd)
            outTokenString += " is"
            outTokenString += " " + token.flavor

        if token.errorType == "too long":
            outTokenString += " (truncated to " + token.name[0:31] + ")"

        if "Constant" in token.flavor:
            outTokenString += " (value = " + token.name + ")"
        
        outTokenString += "\n"
        outFile.write(outTokenString)

def checkForStringEnd(c):
    if c == '\"':
        return "complete"
    elif c == '\n':
        return "failure"
    else:
        return "still going"


def buildUnrecognizedCharacterToken(charString, line):
    newToken = Token()
    newToken.line = line
    newToken.name = charString
    newToken.hasError = True
    newToken.errorType = "unrecognized char"
    return newToken

def buildToken(tokenString, line, colStart, colEnd):
    #print("BUILDING TOKEN " + tokenString)
    newToken = Token()

    newToken.name = tokenString
    if len(tokenString) > 31:
        print("WE GOT AN ERROR BOYS")
        newToken.hasError = True
        newToken.errorType = "too long"

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
    elif tokenString[0] == '\"' and tokenString[len(tokenString)-1] == '\"' and len(tokenString) > 1:
        newToken.flavor = "T_StringConstant"
    elif tokenString[0] == '\"' and (tokenString[len(tokenString)-1] != '\"' or len(tokenString) == 1):
        newToken.hasError = True
        newToken.errorType = "unterminated string"
    else:
        newToken.flavor = "T_Identifier"
    return newToken


def buildTokenList(fileContents):
    stringMode = False
    commentMode = False
    tokenList = []
    #iterate over file contents
    goingMerry = ""
    line = 1
    colStart = -1
    colEnd = -1
    col = 0
    for c in fileContents:
        col += 1
        #check for spooky characters
        if stringMode:
            status = checkForStringEnd(c)
            if status == "complete":
                stringMode = False
                goingMerry += str(c)
                colEnd = col
                #package string
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""
            elif status == "still going":
                goingMerry += str(c)
            elif status == "failure":
                stringMode = False
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""
                line += 1
                col = 0
                colStart = -1
                colEnd = -1
                #package string with error
        elif c == '\"':
            if len(goingMerry) > 0:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""
            colStart = col
            goingMerry += str(c);
            stringMode = True
        elif not (c).isalpha() and not c.isdigit() and not c in symbolChars and not c in breakChars:
            if len(goingMerry) > 0:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""
            tokenList.append(buildUnrecognizedCharacterToken(c,line))
            goingMerry = ""
        elif c in breakChars:
            #print("BREAKING, PACK IT UP")
            #package up what we have
            if len(goingMerry) > 0:
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                goingMerry = ""

            if c == '\n':
                #print("RESETTING COL")
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
                #print("ASSIGNED COL START: " + str(colStart))
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
            if len(goingMerry) > 0 and (goingMerry[0].isdigit() or goingMerry[0] in symbolChars):
                colEnd = col-1
                tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
                colStart = col
                goingMerry = ""
                goingMerry += str(c)
            else:
                goingMerry += str(c)
                #print(goingMerry)

                    
        #increment values

    if len(goingMerry) > 0:
        colEnd = col
        tokenList.append(buildToken(goingMerry,line,colStart,colEnd))
    return tokenList

    #print("building token list")
