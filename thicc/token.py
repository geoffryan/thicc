
class Token():
    def __init__(self, val=None):
        self.val = val

    def __str__(self):
        return str(self.val)

#
# Top-level Grammar Elements
#

class Keyword(Token):
    pass

class Identifier(Token):
    pass

class Constant(Token):
    pass

class StringLtrl(Token):
    pass

class Punctuator(Token):
    pass

#
# Keywords
#

class ReturnK(Keyword):
    pass

class IntK(Keyword):
    pass

#
# Constants
#

class IntC(Constant):
    pass

#
# Punctuators
#

class SemicolonP(Punctuator):
    pass

class BraceP(Punctuator):
    pass

class OpenBraceP(BraceP):
    pass

class ClosedBraceP(BraceP):
    pass

class ParenthesesP(Punctuator):
    pass

class OpenParenthesesP(ParenthesesP):
    pass

class ClosedParenthesesP(ParenthesesP):
    pass

class UnaryOpP(Punctuator):
    pass

class NotP(UnaryOpP):
    pass

class NegationP(UnaryOpP):
    pass

class ComplementP(UnaryOpP):
    pass
