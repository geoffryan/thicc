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

    punct = [';', '(', ')', '{', '}']
    keywords = ['int', 'return']
    intchars = ['0123456789']

    def __init__(self):
        return

    def tokenize(self, inputStr):
        toks = []
        start = 0
        reading = False
        readingLiteral = False
        for i in range(len(inputStr)):
            c = inputStr[i]
            if c in self.punct:
                if reading:
                    toks.append(self._tokExp(inputStr[start:i]))
                    reading = False
                toks.append(Token(c))
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

        return toks


    def _tokExp(self, exp):
        if exp in self.keywords:
            return Token(exp)
        else:
            return Token(exp)


class Token():
    val = None
    def __init__(self, val=None):
        self.val = val

    def __repr__(self):
        return str(self.val)

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        fname = sys.argv[1]

        print("Hello")

        with open(fname, "r") as f:
            text = f.read()

        print(text)

        lex = Lexer()
        toks = lex.tokenize(text)
        print(toks)
