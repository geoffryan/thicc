
class Token():

    def __init__(self):
        self.val = None

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        if isinstance(other, self.__class__)\
                and self.val==other.val:
            return True
        return False

#
# Top-level Grammar Elements
#

class Keyword(Token):
    pass

class Identifier(Token):
    def __init__(self, val):
        self.val = val

class Constant(Token):
    def __init__(self, val):
        self.val = val

class StringLtrl(Token):
    pass

class Punctuator(Token):
    pass

#
# Keywords
#

class ReturnK(Keyword):
    def __init__(self):
        self.val = 'return'

class IntK(Keyword):
    def __init__(self):
        self.val = 'int'

#
# Constants
#

class IntC(Constant):
    pass

#
# Punctuators
#

class SemicolonP(Punctuator):
    def __init__(self):
        self.val = ';'

class BraceP(Punctuator):
    pass

class OpenBraceP(BraceP):
    def __init__(self):
        self.val = '}'

class ClosedBraceP(BraceP):
    def __init__(self):
        self.val = '}'

class ParenthesesP(Punctuator):
    pass

class OpenParenthesesP(ParenthesesP):
    def __init__(self):
        self.val = '('

class ClosedParenthesesP(ParenthesesP):
    def __init__(self):
        self.val = ')'

# Operators

class OperatorP(Punctuator):
    pass

class UnaryOpP(OperatorP):
    pass

class BinaryOpP(OperatorP):
    pass

# Unary Operations

class NotP(UnaryOpP):
    def __init__(self):
        self.val = '!'

class NegP(UnaryOpP,BinaryOpP):
    def __init__(self):
        self.val = '-'

class ComplementP(UnaryOpP):
    def __init__(self):
        self.val = '~'

#Binary Operations

class AddP(BinaryOpP):
    def __init__(self):
        self.val = '+'

class MultP(BinaryOpP):
    def __init__(self):
        self.val = '*'

class DivP(BinaryOpP):
    def __init__(self):
        self.val = '/'
