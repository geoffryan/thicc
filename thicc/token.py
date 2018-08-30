
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

class Semicolon(Punctuator):
    def __init__(self):
        self.val = ';'

class Brace(Punctuator):
    pass

class OpenBrace(Brace):
    def __init__(self):
        self.val = '}'

class ClosedBrace(Brace):
    def __init__(self):
        self.val = '}'

class Parentheses(Punctuator):
    pass

class OpenParentheses(Parentheses):
    def __init__(self):
        self.val = '('

class ClosedParentheses(Parentheses):
    def __init__(self):
        self.val = ')'

# Operators

class Operator(Punctuator):
    pass

class UnaryOp(Operator):
    pass

class BinaryOp(Operator):
    pass

# Unary Operations

class Not(UnaryOp):
    def __init__(self):
        self.val = '!'

class Neg(UnaryOp,BinaryOp):
    def __init__(self):
        self.val = '-'

class Complement(UnaryOp):
    def __init__(self):
        self.val = '~'

#Binary Operations

class Add(BinaryOp):
    def __init__(self):
        self.val = '+'

class Mult(BinaryOp):
    def __init__(self):
        self.val = '*'

class Div(BinaryOp):
    def __init__(self):
        self.val = '/'

class Mod(BinaryOp):
    def __init__(self):
        self.val = '%'

class BitShiftL(BinaryOp):
    def __init__(self):
        self.val = '<<'

class BitShiftR(BinaryOp):
    def __init__(self):
        self.val = '>>'

class LessThan(BinaryOp):
    def __init__(self):
        self.val = '<'

class LessThanEqual(BinaryOp):
    def __init__(self):
        self.val = '<='

class GreaterThan(BinaryOp):
    def __init__(self):
        self.val = '>'

class GreaterThanEqual(BinaryOp):
    def __init__(self):
        self.val = '>='

class Equal(BinaryOp):
    def __init__(self):
        self.val = '=='

class NotEqual(BinaryOp):
    def __init__(self):
        self.val = '!='

class BitAnd(BinaryOp):
    def __init__(self):
        self.val = '&'

class BitOr(BinaryOp):
    def __init__(self):
        self.val = '|'

class BitXor(BinaryOp):
    def __init__(self):
        self.val = '^'

class And(BinaryOp):
    def __init__(self):
        self.val = '&&'

class Or(BinaryOp):
    def __init__(self):
        self.val = '||'

