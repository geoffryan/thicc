
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
        for stmnt in body:
            out += stmnt.__str__(level=level+1)
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

class BinaryOpE(Expression):
    def __init__(self, opTok, expr1, expr2):
        super().__init__()
        self.op = opTok
        self.expr1 = expr1
        self.expr2 = expr2

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(BinaryOp): " + self.op.val + '\n'
        out += self.expr1.__str__(level=level+1)
        out += self.expr2.__str__(level=level+1)
        return out

class ConstantE(Expression):
    def __init__(self, tok):
        super().__init__()
        self.terminal = True
        self.value = tok
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Constant): " + self.value.val + '\n'
        return out

class VarRefE(Expression):
    def __init__(self, idTok):
        super().__init__()
        self.id = idTok
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Variable): " + self.id.val + '\n'
        return out

class AssignE(Expression):
    def __init__(self, idTok, opTok, expr):
        super().__init__()
        self.id = idTok
        self.op = opTok
        self.expr = expr
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Assign): {0:s} {1:s}\n".format(
                                            self.id.val, self.op.val)
        out += self.expr.__str__(level=level+1)
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

class IncrementPreE(Expression):
    def __init__(self, opTok, var):
        super().__init__()
        self.op = opTok
        self.var = var
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(IncrementPre): " + self.op.val + '\n'
        out += self.var.__str__(level=level+1)
        return out

class IncrementPostE(Expression):
    def __init__(self, opTok, var):
        super().__init__()
        self.op = opTok
        self.var = var
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(IncrementPost): " + self.op.val + '\n'
        out += self.var.__str__(level=level+1)
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

class ExpressionS(Statement):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Expression):"+'\n'
        out += self.value.__str__(level=level+1)
        return out

class DeclareS(Statement):
    def __init__(self, idTok, expr=None):
        super().__init__()
        self.id = idTok
        self.expr = expr

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Declare):" + self.id.val+'\n'
        if self.expr is not None:
            out += self.value.__str__(level=level+1)
        return out

