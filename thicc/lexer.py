from . import token

class LexError(Exception):
    pass

class LexIllegalCharError(LexError):
    def __init__(self, char, message="Illegal character"):
        self.expression = char
        self.message = message

class LexInvalidLiteralError(LexError):
    def __init__(self, lit, message="Illegal literal format"):
        self.expression = lit
        self.message = message

class Lexer():

    def __init__(self):
        self.punct = {';':token.SemicolonP, 
                    '(':token.OpenParenthesesP,
                    ')':token.ClosedParenthesesP,
                    '{':token.OpenBraceP,
                    '}':token.ClosedBraceP,
                    '!':token.NotP,
                    '~':token.ComplementP,
                    '-':token.NegationP}
        self.keywords = {'int':token.IntK,
                        'return':token.ReturnK}
        self.intchars = '0123456789'

    def tokenize(self, inputStr):
        toks = []
        start = 0
        reading = False
        readingLiteral = False
        for i in range(len(inputStr)):
            c = inputStr[i]
            if c in self.punct.keys():
                if reading:
                    toks.append(self._tokExp(inputStr[start:i]))
                    reading = False
                toks.append(self.punct[c](c))
            elif c.isspace():
                if reading:
                    toks.append(self._tokExp(inputStr[start:i]))
                    reading = False
            elif not c.isalnum():
                raise LexIllegalCharError(c)

            elif reading:
                if readingLiteral:
                    if c not in self.intchars:
                        raise LexInvalidLiteralError(inputStr[start:i+1])
            else:
                start = i
                reading = True
                if c in self.intchars:
                    readingLiteral = True
                else:
                    readingLiteral = False
        if reading:
            toks.append(self._tokExp(inputStr[start:]))

        return toks


    def _tokExp(self, exp):
        if exp in self.keywords.keys():
            return self.keywords[exp](exp)
        elif all([c in self.intchars for c in exp]):
            return token.IntC(exp)
        else:
            return token.Identifier(exp)

