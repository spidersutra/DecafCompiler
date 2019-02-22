from enum import Enum

class Token:
    name = ""
    text = ""
    identifier = ""
    colStart = -1
    colEnd = -1
    line = -1
    flavor = "NO_FLAVOR_SPECIFIED"
    errorType = ""
    hasError = False
