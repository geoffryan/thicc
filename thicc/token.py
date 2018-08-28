
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

class BraceP(Punctuator):
    pass

class SemicolonP(Punctuator):
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

