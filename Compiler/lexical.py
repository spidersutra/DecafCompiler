from token import Token

breakChars = [' ', '\n']

def buildToken(tokenString):
    newToken = Token()
    newToken.name = tokenString
    return newToken

def buildTokenList(fileContents):
    tokenList = []
    #iterate over file contents
    goingMerry = ""
    for c in fileContents:
        if c in breakChars and len(goingMerry) > 0:
            #package up what we have
            tokenList.append(buildToken(goingMerry))
            goingMerry = ""
        elif c in breakChars:
            i = 1+1
        else:
            goingMerry += str(c)
    return tokenList

    #print("building token list")
