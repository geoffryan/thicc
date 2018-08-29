
class ASTNode():
    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__)\
                and self.__dict__==other.__dict__:
            return True
        return False

class Expression(ASTNode):
    def __init__(self):
        self.terminal = False
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression"
        return out

class Statement(ASTNode):
    def __init__(self):
        self.terminal = False

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement"
        return out

class Function(ASTNode):
    def __init__(self, name, body):
        self.terminal = False
        self.name = name
        self.body = body

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Function: " + self.name.val + '\n'
        out += self.body.__str__(level=level+1)
        return out


class Program(ASTNode):
    def __init__(self, function):
        self.terminal = False
        self.function = function

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Program" + "\n"
        func = self.function.__str__(level=level+1)
        out += func
        return out

#
# Expressions
#

class ConstantE(Expression):
    def __init__(self, tok):
        super().__init__()
        self.terminal = True
        self.value = tok
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Constant): " + self.value.val
        return out

class UnaryOpE(Expression):
    def __init__(self, opTok, expr):
        super().__init__()
        self.op = opTok
        self.expr = expr
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(UnaryOp): " + self.op.val + '\n'
        out += self.expr.__str__(level=level+1)
        return out


#
# Statements
#

class ReturnS(Statement):
    def __init__(self, expr):
        super().__init__()
        self.value = expr

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Return):" + '\n'
        out += self.value.__str__(level=level+1)
        return out

