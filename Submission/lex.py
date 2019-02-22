from token import Token
from decimal import Decimal

class StateDeets:
    pos = 0 #positon of the character we are looking ahead at
    line = 1
    col = 1
    fileContents = ""
    tokenList = []
    breakChars = [' ', '\n','','\t']
    symbolChars = ['+', '-', '*', '/', '%', '<', "<=", '>', ">=", '=', "==","!=","&&","||","!",";",",",'.',"(",")","{","}"]
    nonSoloSymbolChars = ['&','|']
    reservedWords = ["void","int","double","bool","string","null","for","while","if","else","return","break","Print","ReadInteger","ReadLine"]
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
        if "Constant" in token.flavor and 'E' not in token.text:
            outTokenString += " (value = " + token.text + ")"
        elif "Constant" in token.flavor and 'E' in token.text:
            i=1
            # break down to get the real value
            #print(token.text)
            #print(token.text.split('E')[0])
            baseNum = Decimal(token.text.split('E')[0])
            exponent = int(token.text.split('+')[1])
            outTokenString += " (value = " + str(baseNum * 10**exponent) + ")"

            
        print(outTokenString)


def printErrorToken(token):
    print("")
    print("*** Error line " + str(token.line) + ".")
    if token.errorType == "too long":
        print("*** Identifier too long: " + "\"" + token.text + "\"" )
        print("")
        print(token.text + " line " + str(token.line) + " cols " + str(token.colStart) + "-" + str(token.colEnd) + " is " + token.flavor + " (truncated to " + token.text[0:31] +")")
    elif token.errorType == "unrecognized character":
        print("*** Unrecognized char: " + "\'" + token.text + "\'")
        print("")
    elif token.errorType == "unterminated string":
        print("*** Unterminated string constant: " + token.text)
        print("")

def buildToken(text, flavor, line, colStart,colEnd,stateDeets):

    newToken = Token()
    newToken.text = text
    newToken.flavor = flavor
    newToken.line = line
    newToken.colStart = colStart
    newToken.colEnd = colEnd

    #check for reserved ops
    if newToken.text in stateDeets.reservedWords:
        newToken.flavor = "T_" + str(newToken.text[0]).upper() + newToken.text[1:]
    elif newToken.text == "true" or newToken.text == "false":
        newToken.flavor = "T_BoolConstant"

    #check for errors
    if len(newToken.text) > 31 and "Constant" not in newToken.flavor:
        newToken.hasError = True
        newToken.errorType = "too long"
    elif newToken.flavor == "Unrecognized":
        newToken.hasError = True
        newToken.errorType = "unrecognized character"
    elif newToken.flavor == "unterminated string":
        newToken.hasError = True
        newToken.errorType = "unterminated string"

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
        if stateDeets.pos >= len(stateDeets.fileContents):
            return buildToken(goingMerry, "T_Identifier", line,colStart,colEnd,stateDeets)

        c = stateDeets.fileContents[stateDeets.pos]
        
        if c in stateDeets.breakChars or c in stateDeets.symbolChars or c == '\"':
            colEnd = stateDeets.col - 1
            return buildToken(goingMerry, "T_Identifier", line,colStart,colEnd,stateDeets)
        else:
            goingMerry += str(c)
            colEnd = stateDeets.col -1
            stateDeets.updateDeets(c)
            #if stateDeets.pos >= len(stateDeets.fileContents)-1:
            #    return buildToken(goingMerry, "T_Identifier", line,colStart,colEnd,stateDeets)
        
def singleLineCommentStart(stateDeets):
    #search for end of line then pass back control
    done = False
    while not done:
        if stateDeets.pos >= len(stateDeets.fileContents): # ask about this behavior
            return stateDeets
        c = stateDeets.fileContents[stateDeets.pos]
        stateDeets.updateDeets(c)
        if c == '\n':
            return stateDeets
            

def multiLineCommentStart(stateDeets):
    #search for string "*/" then pass back control
    done = False
    endingPrimed = False
    while not done:
        if stateDeets.pos >= len(stateDeets.fileContents): # ask about this behavior
            return stateDeets
        c = stateDeets.fileContents[stateDeets.pos]
        stateDeets.updateDeets(c)
        if c == '*':
            endingPrimed = True
        elif c == '/' and endingPrimed:
            return stateDeets 
        elif c != '*':
            endingPrimed = False #we need to find a * directly before our /
        
        
def symbolCharStart(stateDeets):
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    goingMerry += str(c)
    colStart = stateDeets.col
    colEnd = -1
    line = stateDeets.line

    #determine if we're looking at a comment
    if c == '/':
        if stateDeets.pos < len(stateDeets.fileContents) - 1: #ensure we aren't at end of file
            nextC = stateDeets.fileContents[stateDeets.pos + 1] 
            if nextC == '/':
                #go to single line comment
                stateDeets.updateDeets(c)
                return singleLineCommentStart(stateDeets)
            elif nextC == '*':
                #go to multi line comment
                stateDeets.updateDeets(c)
                return multiLineCommentStart(stateDeets)

    elif stateDeets.pos < len(stateDeets.fileContents) - 1:
        nextC = stateDeets.fileContents[stateDeets.pos + 1]
        colEnd = stateDeets.col 
        if c == '=':
            #check ==
            if nextC == '=':
                stateDeets.updateDeets(c)
                colEnd = stateDeets.col 
                stateDeets.updateDeets(nextC)
                return buildToken("==", "==",line,colStart,colEnd,stateDeets)
        elif c == '>':
            #check >=
            if nextC == '=':
                stateDeets.updateDeets(c)
                colEnd = stateDeets.col 
                stateDeets.updateDeets(nextC)
                return buildToken(">=", ">=",line,colStart,colEnd,stateDeets)
        elif c == '<':
            #check <=
            if nextC == '=':
                stateDeets.updateDeets(c)
                colEnd = stateDeets.col 
                stateDeets.updateDeets(nextC)
                return buildToken("<=", "<=",line,colStart,colEnd,stateDeets)
        elif c == '!':
            #check !=
            if nextC == '=':
                stateDeets.updateDeets(c)
                colEnd = stateDeets.col 
                stateDeets.updateDeets(nextC)
                return buildToken("!=", "!=",line,colStart,colEnd,stateDeets)
        elif c == '&':
            #check &&
            if nextC == '&':
                stateDeets.updateDeets(c)
                colEnd = stateDeets.col 
                stateDeets.updateDeets(nextC)
                return buildToken("&&", "&&",line,colStart,colEnd,stateDeets)

    stateDeets.updateDeets(c)

    if stateDeets.pos == len(stateDeets.fileContents)-1:
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colStart,stateDeets)


    nextC = stateDeets.fileContents[stateDeets.pos]
    if goingMerry + str(nextC) in stateDeets.symbolChars:
        goingMerry += str(nextC)
        colEnd = stateDeets.col
        stateDeets.updateDeets(nextC)
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colEnd,stateDeets)
    else:
        return buildToken(goingMerry,"\'" + goingMerry + "\'",line,colStart,colStart,stateDeets)

def stringStart(stateDeets):
    done = False
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    goingMerry += str(c)
    colStart = stateDeets.col
    colEnd = -1
    line = stateDeets.line

    stateDeets.updateDeets(c)
    while not done:
        if stateDeets.pos >= len(stateDeets.fileContents): #error, we got to the end of a file before the string was finished
            return buildToken(goingMerry, "unterminated string", line,colStart,colEnd,stateDeets)
        c = stateDeets.fileContents[stateDeets.pos]
        if c == '\n': #error, we skipped to a new line before the string was finished
            return buildToken(goingMerry, "unterminated string", line,colStart,colEnd,stateDeets)
        else: #return terminated string
            goingMerry += str(c)
            colEnd = stateDeets.col
            stateDeets.updateDeets(c)
            if c == '\"':
                return buildToken(goingMerry, "T_StringConstant", line,colStart,colEnd, stateDeets)

def digitStart(stateDeets):
    done = False
    hasDot = False
    hasE = False
    hasPlus = False
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
        if c == '.' and not hasDot:
            hasDot = True
            goingMerry += str(c)
            colEnd = stateDeets.col - 1
            stateDeets.updateDeets(c)
        elif c == 'E' and hasDot and not hasE and stateDeets.pos < len(stateDeets.fileContents)-2: #look ahead to ensure we have +NUM after this
            cShouldBePlus = stateDeets.fileContents[stateDeets.pos+1]
            cShouldBeNum = stateDeets.fileContents[stateDeets.pos+2]
            if cShouldBePlus == '+' and cShouldBeNum.isdigit():
                #yay, we can keep going
                goingMerry += str(c)
                goingMerry += str(cShouldBePlus)
                goingMerry += str(cShouldBeNum)
                stateDeets.updateDeets(c)
                stateDeets.updateDeets(cShouldBePlus)
                stateDeets.updateDeets(cShouldBePlus)
                colEnd = stateDeets.col -1
                hasE = True
            else: #boo, straight into the trash it goes
                done = True
            
            hasE = True
            #goingMerry += str(c)
            #colEnd = stateDeets.col -1
            
            
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


def spookyStart(stateDeets):
    c = stateDeets.fileContents[stateDeets.pos]
    goingMerry = ""
    goingMerry += str(c)
    line = stateDeets.line
    stateDeets.updateDeets(c)
    return buildToken(goingMerry,"Unrecognized",line,-1,-1,stateDeets)





def buildTokenList(_fileContents):
    stateDeets = StateDeets()
    stateDeets.fileContents = _fileContents

    while stateDeets.pos < len(stateDeets.fileContents):
        c = stateDeets.fileContents[stateDeets.pos]
        if c in stateDeets.breakChars:
            stateDeets.updateDeets(c)
        elif c.isalpha():
            stateDeets = alphaStart(stateDeets)
        elif (c in stateDeets.symbolChars or c in stateDeets.nonSoloSymbolChars) and c is not '\"':
            stateDeets = symbolCharStart(stateDeets)
        elif c == '\"':
            stateDeets = stringStart(stateDeets)
        elif c.isdigit():
            stateDeets = digitStart(stateDeets)
        else:
            stateDeets = spookyStart(stateDeets)  
    return stateDeets.tokenList
        



