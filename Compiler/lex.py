from token import Token

class StateDeets:
    pos = 0 #positon of the character we are looking ahead at
    line = 1
    col = 1
    fileContents = ""
    tokenList = []
    breakChars = [' ', '\n','','\t']
    symbolChars = ['+', '-', '*', '/', '%', '<', "<=", '>', ">=", '=', "==","!=","&&","||","!",";",",",'.',"(",")","{","}"]
    def updateDeets(self,c):
        self.pos+=1
        self.col += 1
        if c == '\n':
            self.line+=1
            self.col = 1


def printTokens(_tokenList):
    for token in _tokenList:
        printToken(token)

def printToken(token):
    outTokenString = ""
    if token.hasError:
        printErrorToken(token)
    else:
        outTokenString += token.text
        outTokenString += "         "
        outTokenString += " line " + str(token.line)
        outTokenString += " cols " + str(token.colStart) + "-" +str(token.colEnd)
        outTokenString += " is"
        outTokenString += " " + token.flavor
        if "Constant" in token.flavor:
            outTokenString += "(value = " + token.text + ")"
        print(outTokenString)


def printErrorToken(token):
    print("\n")
    print("*** Error line " + str(token.line) + ".")
    if token.errorType == "too long":
        print("*** Identifier too long: " + "\"" + token.text + "\"" )
        print("")
        print(token.text + "line " + str(token.line) + " cols " + str(token.colStart) + "-" + str(token.colEnd) + " is " + token.flavor + " (truncated to " + token.text[0:31] +")")

def buildToken(text, flavor, line, colStart,colEnd,stateDeets):

    newToken = Token()
    newToken.text = text
    newToken.flavor = flavor
    newToken.line = line
    newToken.colStart = colStart
    newToken.colEnd = colEnd

    #check for errors
    if len(newToken.text) > 31:
        newToken.hasError = True
        newToken.errorType = "too long"

    stateDeets.tokenList.append(newToken)
    return stateDeets
    #print(len(tokenList))


def alphaStart(stateDeets):
    done = False
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    
    goingMerry += str(c)
    colStart = stateDeets.col
    colEnd = -1
    line = stateDeets.line

    stateDeets.updateDeets(c)
    while not done:
        #break on breakchar or symbol
        if stateDeets.pos >= len(stateDeets.fileContents)-1:
            return buildToken(goingMerry, "T_Identifier", line,colStart,colEnd,stateDeets)

        c = stateDeets.fileContents[stateDeets.pos]
        
        if c in stateDeets.breakChars or c in stateDeets.symbolChars:
            colEnd = stateDeets.col - 1
            return buildToken(goingMerry, "T_Identifier", line,colStart,colEnd,stateDeets)
        else:
            goingMerry += str(c)
            colEnd = stateDeets.col -1
            stateDeets.updateDeets(c)
        
        
        
def symbolCharStart(stateDeets):
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    goingMerry += str(c)
    colStart = stateDeets.col
    colEnd = -1
    line = stateDeets.line

    stateDeets.updateDeets(c)

    if stateDeets.pos == len(stateDeets.fileContents)-1:
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colStart,stateDeets)


    nextC = stateDeets.fileContents[stateDeets.pos]
    if goingMerry + str(nextC) in stateDeets.symbolChars:
        goingMerry += str(nextC)
        colEnd = stateDeets.colEnd
        stateDeets.updateDeets(nextC)
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colEnd,stateDeets)
    else:
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colStart,stateDeets)
        
def digitStart(stateDeets):
    done = False
    hasDot = False
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    goingMerry += str(c)
    colStart = stateDeets.col
    colEnd = -1
    line = stateDeets.line
    stateDeets.updateDeets(c)
    while not done:
        if stateDeets.pos >= len(stateDeets.fileContents)-1:
            done = True
            break
        # print(stateDeets.pos)
        #print(len(stateDeets.fileContents))
        c = stateDeets.fileContents[stateDeets.pos]
        #we can take numbers, a single .
        if c == "." and not hasDot:
            hasDot = True
            goingMerry += str(c)
            colEnd = stateDeets.col - 1
            stateDeets.updateDeets(c)
        elif c in stateDeets.breakChars or c in stateDeets.symbolChars:
            done = True
        elif c.isdigit():
            goingMerry += str(c)
            colEnd = stateDeets.col - 1
            stateDeets.updateDeets(c)
        else:
            done = True
    
    colEnd = stateDeets.col -1
    if hasDot:
        return buildToken(goingMerry, "T_DoubleConstant", line,colStart,colEnd,stateDeets)
    else:
        return buildToken(goingMerry, "T_IntConstant", line,colStart,colEnd,stateDeets)





def buildTokenList(_fileContents):
    stateDeets = StateDeets()
    stateDeets.fileContents = _fileContents

    while stateDeets.pos < len(stateDeets.fileContents):
        c = stateDeets.fileContents[stateDeets.pos]
        #print(c)
        if c in stateDeets.breakChars:
            stateDeets.updateDeets(c)
            #print("a")
        elif c.isalpha():
            #print("b")
            stateDeets = alphaStart(stateDeets)
        elif c in stateDeets.symbolChars:
            #print("c")
            stateDeets = symbolCharStart(stateDeets)
        elif c.isdigit():
            stateDeets = digitStart(stateDeets)
        else:
            #print("d")
            stateDeets.updateDeets(c)
          
        #print(c)  
    return stateDeets.tokenList
        



