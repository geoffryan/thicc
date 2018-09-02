from . import token
from . import exception

class LexError(exception.ThiccError):
    pass

class LexIllegalCharError(LexError):
    def __init__(self, char, message="Illegal character"):
        self.expression = char
        self.message = message

class LexInvalidIdentifierError(LexError):
    def __init__(self, lit, message="Illegal identifier format"):
        self.expression = lit
        self.message = message

class LexInvalidPunctuatorError(LexError):
    def __init__(self, lit, message="Cannot lex punctuators"):
        self.expression = lit
        self.message = message

class Lexer():

    def __init__(self):
        self.punct = {';':token.Semicolon, 
                    '(':token.OpenParentheses,
                    ')':token.ClosedParentheses,
                    '{':token.OpenBrace,
                    '}':token.ClosedBrace,
                    '!':token.Not,
                    '~':token.Complement,
                    '-':token.Neg,
                    '+':token.Add,
                    '*':token.Mult,
                    '/':token.Div,
                    '%':token.Mod,
                    '<<':token.BitShiftL,
                    '>>':token.BitShiftR,
                    '<':token.LessThan,
                    '<=':token.LessThanEqual,
                    '>':token.GreaterThan,
                    '>=':token.GreaterThanEqual,
                    '==':token.Equal,
                    '!=':token.NotEqual,
                    '&':token.BitAnd,
                    '|':token.BitOr,
                    '^':token.BitXor,
                    '&&':token.And,
                    '||':token.Or,
                    "=":token.Assign}
        self.keywords = {'int':token.IntK,
                        'return':token.ReturnK}
        self.comments = {   '//': '\n',
                            '/*': '*/'}
        self.intchars = '0123456789'
        self.alchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alnumchars = self.intchars + self.alchars
        self.punctchars = "".join(self.punct)
        self.maxPunctLen = max([len(p) for p in self.punct])

    def tokenize(self, inputStr):
        toks = []
        start = 0
        readingComment = False
        commentEnd = None
        commentStart = None
        readingExpression = False
        readingPunct = False

        i = 0
        while i < len(inputStr):
            #Handle comments
            if readingComment:
                if commentEnd == inputStr[i:i+len(commentEnd)]:
                    i += len(commentEnd)
                    commentStart = None
                    commentEnd = None
                    readingComment = False
                    continue
                else:
                    i += 1
                    continue
            else:
                for com in self.comments.keys():
                    if inputStr[i:i+len(com)] == com:
                        if readingExpression:
                            toks.append(self._tokExp(inputStr[start:i]))
                            readingExpression = False
                        elif readingPunct:
                            toks += self._tokPunct(inputStr[start:i])
                            readingPunct = False
                        commentStart = com
                        commentEnd = self.comments[com]
                        readingComment = True
                        break
                if readingComment:
                    i += len(commentStart)
                    continue

            c = inputStr[i]
            if c.isspace():
                if readingExpression:
                    toks.append(self._tokExp(inputStr[start:i]))
                    readingExpression = False
                elif readingPunct:
                    toks += self._tokPunct(inputStr[start:i])
                    readingPunct = False
            elif readingPunct:
                if c in self.alnumchars:
                    toks += self._tokPunct(inputStr[start:i])
                    readingPunct = False
                    readingExpression = True
                    start = i
                elif c not in self.punctchars:
                    raise LexIllegalCharError(c)
            elif readingExpression:
                if c in self.punctchars:
                    toks.append(self._tokExp(inputStr[start:i]))
                    readingExpression = False
                    readingPunct = True
                    start = i
                elif c not in self.alnumchars:
                    raise LexIllegalCharError(c)
            else:
                if c in self.alnumchars:
                    readingExpression = True
                    start = i
                elif c in self.punctchars:
                    readingPunct = True
                    start = i
                else:
                    raise LexIllegalCharError(c)
            i += 1
        if readingExpression:
            toks.append(self._tokExp(inputStr[start:]))
        elif readingPunct:
            toks += self._tokPunct(inputStr[start:])


        return toks

    def _tokPunct(self, puncts):
        #Lex a string containing only Punctuation characters into
        #(possibly several) tokens

        # This seems way too complicated. The issue is how to distinguish
        # '!' and '!='.  The method is to begin at index = 0 of the string
        # and look for matches with the LONGEST punctuators. If no matches are
        # found, try the next shortest punctuators, continue until a match is
        # found, then increment the index by the length of the match. If no
        # match is found, raise an error.
        toks = []

        l = len(puncts)
        i=0
        while i < l:
            n = min(l-i, self.maxPunctLen)
            found = False
            for k in range(n,0,-1):
                val = puncts[i:i+k]
                if val in self.punct.keys():
                    toks.append(self.punct[val]())
                    i += k
                    found = True
                    break
            if not found:
                raise LexInvalidPunctuatorError(puncts)
        return toks

    def _tokExp(self, exp):
        if exp in self.keywords.keys():
            return self.keywords[exp]()
        elif all([c in self.intchars for c in exp]):
            return token.IntC(exp)
        else:
            if exp[0] in self.alchars:
                return token.Identifier(exp)
            else:
                raise LexInvalidIdentifierError(exp)

