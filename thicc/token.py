
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

class Return(Keyword):
    def __init__(self):
        self.val = 'return'

class Int(Keyword):
    def __init__(self):
        self.val = 'int'

class If(Keyword):
    def __init__(self):
        self.val = 'if'

class Else(Keyword):
    def __init__(self):
        self.val = 'else'

class For(Keyword):
    def __init__(self):
        self.val = 'for'

class While(Keyword):
    def __init__(self):
        self.val = 'while'

class Do(Keyword):
    def __init__(self):
        self.val = 'do'

class Break(Keyword):
    def __init__(self):
        self.val = 'break'

class Continue(Keyword):
    def __init__(self):
        self.val = 'continue'


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

class TernaryOp(Operator):
    pass

class AssignmentOp(Operator):
    pass

# Assignment Operators

class Assign(AssignmentOp):
    def __init__(self):
        self.val = '='

class CompoundAssignmentOp(AssignmentOp):
    pass

class AssignAdd(CompoundAssignmentOp):
    def __init__(self):
        self.val = '+='

class AssignSub(CompoundAssignmentOp):
    def __init__(self):
        self.val = '-='

class AssignMult(CompoundAssignmentOp):
    def __init__(self):
        self.val = '*='

class AssignDiv(CompoundAssignmentOp):
    def __init__(self):
        self.val = '/='

class AssignMod(CompoundAssignmentOp):
    def __init__(self):
        self.val = '%='

class AssignBShiftL(CompoundAssignmentOp):
    def __init__(self):
        self.val = '<<='

class AssignBShiftR(CompoundAssignmentOp):
    def __init__(self):
        self.val = '>>='

class AssignBAnd(CompoundAssignmentOp):
    def __init__(self):
        self.val = '&='

class AssignBOr(CompoundAssignmentOp):
    def __init__(self):
        self.val = '|='

class AssignBXor(CompoundAssignmentOp):
    def __init__(self):
        self.val = '^='

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

class IncrementOp(UnaryOp):
    pass

class Increment(IncrementOp):
    def __init__(self):
        self.val = "++"

class Decrement(IncrementOp):
    def __init__(self):
        self.val = "--"
        
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

# Ternary Operator

class TernaryA(TernaryOp):
    pass

class TernaryB(TernaryOp):
    pass

class QuestionMark(TernaryA):
    def __init__(self):
        self.val = '?'

class Colon(TernaryB):
    def __init__(self):
        self.val = ':'
