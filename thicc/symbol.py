import collections
from . import exception
from . import token

class ParseError(exception.ThiccError):
    pass

class InvalidExpressionError(ParseError):
    def __init__(self, expr, message="Invalid Expression"):
        self.expression = expr
        self.message = message

class InvalidDeclarationError(ParseError):
    def __init__(self, expr, message="Invalid Declaration"):
        self.expression = expr
        self.message = message

class InvalidStatementError(ParseError):
    def __init__(self, expr, message="Invalid Statement"):
        self.expression = expr
        self.message = message

class InvalidFunctionError(ParseError):
    def __init__(self, expr, message="Invalid Function"):
        self.expression = expr
        self.message = message

class InvalidProgramError(ParseError):
    def __init__(self, expr, message="Invalid Program"):
        self.expression = expr
        self.message = message

class ExpectedParenthesesError(ParseError):
    def __init__(self, expr, message="Expected a ("):
        self.expression = expr
        self.message = message

class UnmatchedParenthesesError(ParseError):
    def __init__(self, expr, message="Parentheses block is not closed"):
        self.expression = expr
        self.message = message

class UnmatchedBraceError(ParseError):
    def __init__(self, expr="", message="Expected a }"):
        self.expression = "No }"
        self.message = message

class InvalidVariableRefError(ParseError):
    def __init__(self, expr, message="Invalid Variable ref"):
        self.expression = expr
        self.message = message

class MissingSemicolonError(ParseError):
    def __init__(self, expr, message="Missing ;"):
        self.expression = expr
        self.message = message

class IncompleteConditionalExpressionError(ParseError):
    def __init__(self, expr, message="Missing ?"):
        self.expression = expr
        self.message = message

class TrailingCharactersProgramError(ParseError):
    def __init__(self, expr, message="Trailing characters in program"):
        self.expression = expr
        self.message = message

class ValidationError(ParseError):
    def __init__(self, expr):
        self.expression = expr

class NonDeclarationInProgram(ValidationError):
    pass
class NonBinaryOperatorInExpression(ValidationError):
    pass
class BinaryOperandNotExpression(ValidationError):
    pass
class NotConstant(ValidationError):
    pass
class NotExpression(ValidationError):
    pass
class VariableIDNotIdentifier(ValidationError):
    pass
class FunctionNameNotIdentifier(ValidationError):
    pass
class NotAssignmentOperator(ValidationError):
    pass
class AssignOperandNotExpression(ValidationError):
    pass
class NotUnaryOperator(ValidationError):
    pass
class UnaryOperandNotExpression(ValidationError):
    pass
class IncrementOperandNotVariableRef(ValidationError):
    pass
class NotIncrementOperator(ValidationError):
    pass
class ConditionNotExpression(ValidationError):
    pass
class IfBlockNotStatement(ValidationError):
    pass
class ElseBlockNotStatement(ValidationError):
    pass
class TernaryIfNotExpression(ValidationError):
    pass
class TernaryElseNotExpression(ValidationError):
    pass
class ReturnValueNotExpression(ValidationError):
    pass
class NonBlockItemInCompoundStatement(ValidationError):
    pass
class IllegalFunctionDefinition(ValidationError):
    pass
class InvalidForInit(ValidationError):
    pass
class InvalidForPost(ValidationError):
    pass
class IterBodyNotStatement(ValidationError):
    pass
class VariableInitializerNotExpression(ValidationError):
    pass
class FunctionParameterNotIdentifier(ValidationError):
    pass
class FunctionBodyNotCompoundStatement(ValidationError):
    pass
class MultipleDefinitionsOfFunction(ValidationError):
    pass
class MultipleDeclarationsInScope(ValidationError):
    pass


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

class BlockItem(ASTNode):
    pass

class Declaration(BlockItem):
    def __init__(self):
        self.terminal = False

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Declaration"
        return out

class Statement(BlockItem):
    def __init__(self):
        self.terminal = False

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement"
        return out


class Program(ASTNode):
    def __init__(self, declarations):
        self.terminal = False
        if declarations is None:
            self.declarations = []
        else:
            self.declarations = declarations

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Program" + "\n"
        for d in self.declarations:
            out += d.__str__(level=level+1)
        return out

    def validate(self):
        funcDefs = []
        for d in self.declarations:
            if not isinstance(d, Declaration):
                raise NonDeclarationInProgram(d)
            if isinstance(d, FunctionD) and d.body is not None:
                if d.name in funcDefs:
                    raise MultipleDefinitionsOfFunction(d)
                funcDefs.append(d.name)
            d.validate()

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

    def validate(self):
        if not isinstance(self.op, token.BinaryOp):
            raise NonBinaryOperatorInExpression(self.op)
        if not isinstance(self.expr1, Expression):
            raise BinaryOperandNotExpression(self.expr1)
        self.expr1.validate()
        if not isinstance(self.expr2, Expression):
            raise BinaryOperandNotExpression(self.expr1)
        self.expr2.validate()

class ConstantE(Expression):
    def __init__(self, tok):
        super().__init__()
        self.terminal = True
        self.value = tok
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Constant): " + self.value.val + '\n'
        return out

    def validate(self):
        if not isinstance(self.value, token.Constant):
            raise NotConstant(self.op)

class VarRefE(Expression):
    def __init__(self, idTok):
        super().__init__()
        self.id = idTok
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Variable): " + self.id.val + '\n'
        return out
    def validate(self):
        if not isinstance(self.id, token.Identifier):
            raise VariableIDNotIdentifier(self.id)

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
    def validate(self):
        if not isinstance(self.id, token.Identifier):
            raise VariableIDNotIdentifier(self.id)
        if not isinstance(self.op, token.AssignmentOp):
            raise NotAssignmentOperator(self.op)
        if not isinstance(self.expr, Expression):
            raise AssignOperandNotExpression(self.expr)
        self.expr.validate()

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

    def validate(self):
        if not isinstance(self.op, token.UnaryOp):
            raise NotUnaryOperator(self.op)
        if not isinstance(self.expr, Expression):
            raise UnaryOperandNotExpression(self.expr)
        self.expr.validate()

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
    def validate(self):
        if not isinstance(self.op, token.IncrementOp):
            raise NotIncrementOperator(self.op)
        if not isinstance(self.var, VarRefE):
            raise IncrementOperandNotVariableRef(self.var)
        self.var.validate()

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
    def validate(self):
        if not isinstance(self.op, token.IncrementOp):
            raise NotIncrementOperator(self.op)
        if not isinstance(self.var, VarRefE):
            raise IncrementOperandNotVariableRef(self.var)
        self.var.validate()

class ConditionalE(Expression):
    def __init__(self, condExpr, trueExpr, falseExpr):
        self.cond = condExpr
        self.true = trueExpr
        self.false = falseExpr
    
    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Expression(Conditional): " + '\n'
        out += self.cond.__str__(level=level+1)
        out += self.true.__str__(level=level+1)
        out += self.false.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.cond, Expression):
            raise ConditionNotExpression(self.cond)
        self.cond.validate()
        if not isinstance(self.true, Expression):
            raise TernaryIfNotExpression(self.true)
        self.true.validate()
        if not isinstance(self.false, Expression):
            raise TernaryElseNotExpression(self.false)
        self.false.validate()

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

    def validate(self):
        if not isinstance(self.value, Expression):
            raise ReturnValueNotExpression(self.value)
        self.value.validate()

class ExpressionS(Statement):
    def __init__(self, expr=None):
        super().__init__()
        self.expr = expr

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Expression):"+'\n'
        if self.expr is None:
            out += self.expr.__str__(level=level+1)
        else:
            out += buf + "   " + "NULL\n"
        return out

    def validate(self):
        if not isinstance(self.expr, Expression):
            raise NotExpression(self.expr)
        self.expr.validate()

class ConditionalS(Statement):
    def __init__(self, condExpr, ifStmnt, elseStmnt=None):
        super().__init__()
        self.cond = condExpr
        self.ifS = ifStmnt
        self.elseS = elseStmnt

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Conditional):"+'\n'
        out += self.ifS.__str__(level=level+1)
        if elseS is not None:
            out += self.elseS.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.cond, Expression):
            raise ConditionNotExpression(self.cond)
        self.cond.validate()
        if not isinstance(self.ifS, Statement):
            raise IfBlockNotStatement(self.ifS)
        self.ifS.validate()
        if self.elseS is not None:
            if not isinstance(self.elseS, Statement):
                raise ElseBlockNotStatement(self.elseS)
            self.elseS.validate()

class CompoundS(Statement, collections.UserList):
    def __init__(self, items=[]):
        super().__init__()
        self.data = items

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Compound):"+'\n'
        for item in self.data:
            out += item.__str__(level=level+1)
        return out

    def validate(self):
        decs = []
        for bi in self.data:
            if not isinstance(bi, Statement)\
                    and not isinstance(bi, Declaration):
                raise NonBlockItemInCompoundStatement(bi)
            if isinstance(bi, FunctionD) and bi.body is not None:
                raise IllegalFunctionDefinition(bi)
            if isinstance(bi, VariableD):
                if bi.id in decs:
                    raise MultipleDeclarationsInScope(bi)
                decs.append(bi.id)
            if isinstance(bi, FunctionD):
                if bi.name in decs:
                    raise MultipleDeclarationsInScope(bi)
                decs.append(bi.name)
            bi.validate()

class IterationS(Statement):
    pass

class ForS(IterationS):
    def __init__(self, init, cond, post, body):
        super().__init__()
        self.init = init
        self.cond = cond
        self.post = post
        self.body = body

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(For):"+'\n'
        out += self.init.__str__(level=level+1)
        out += self.cond.__str__(level=level+1)
        out += self.post.__str__(level=level+1)
        out += self.body.__str__(level=level+1)
        return out

    def validate(self):
        if self.init is not None and not isinstance(self.init, Expression)\
                and not isinstance(self.init, VariableD):
            raise InvalidForInit(self.cond)
        if self.init is not None:
            self.init.validate()
        if not isinstance(self.cond, Expression):
            raise ConditionNotExpression(self.cond)
        self.cond.validate()
        if self.post is not None and not isinstance(self.post, Expression):
            raise InvalidForPost(self.post)
        if self.post is not None:
            self.post.validate()
        if not isinstance(self.body, Statement):
            raise IterBodyNotStatement(self.body)
        self.body.validate()


class WhileS(IterationS):
    def __init__(self, cond, body):
        super().__init__()
        self.cond = cond
        self.body = body

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(While):"+'\n'
        out += self.cond.__str__(level=level+1)
        out += self.body.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.cond, Expression):
            raise ConditionNotExpression(self.cond)
        self.cond.validate()
        if not isinstance(self.body, Statement):
            raise IterBodyNotStatement(self.body)
        self.body.validate()

class DoS(IterationS):
    def __init__(self, cond, body):
        super().__init__()
        self.cond = cond
        self.body = body

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Do):"+'\n'
        out += self.body.__str__(level=level+1)
        out += self.cond.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.cond, Expression):
            raise ConditionNotExpression(self.cond)
        self.cond.validate()
        if not isinstance(self.body, Statement):
            raise IterBodyNotStatement(self.body)
        self.body.validate()

class JumpS(Statement):
    pass

class BreakS(JumpS):
    def __init__(self):
        super().__init__()

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Break)" + '\n'
        return out

    def validate(self):
        pass

class ContinueS(JumpS):
    def __init__(self):
        super().__init__()

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Statement(Continue)" + '\n'
        return out

    def validate(self):
        pass



#
# Declarations
#

class VariableD(Declaration):
    def __init__(self, idTok, expr=None):
        super().__init__()
        self.id = idTok
        self.expr = expr

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Declaration(Variable): " + self.id.val+'\n'
        if self.expr is not None:
            out += self.expr.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.id, token.Identifier):
            raise VariableIDNotIdentifier(self.id)
        if self.expr is not None:
            if not isinstance(self.expr, Expression):
                raise VariableInitializerNotExpression(self.expr)
            self.expr.validate()

class FunctionD(Declaration):
    def __init__(self, name, pars, body=None):
        super().__init__()
        self.name = name
        if pars is None:
            self.pars = []
        else:
            self.pars = pars
        self.body = body

    def __str__(self, level=0):
        buf = level * "   "
        out = buf + "Function: " + self.name.val + '('\
                + ', '.join([tok.val for tok in self.pars]) + ')\n'
        for item in self.body:
            out += item.__str__(level=level+1)
        return out

    def validate(self):
        if not isinstance(self.name, token.Identifier):
            raise FunctionNameNotIdentifier(self.name)
        for p in self.pars:
            if not isinstance(p, token.Identifier):
                raise FunctionParameterNotIdentifier(p)
        if self.body is not None:
            if not isinstance(self.body, CompoundS):
                raise FunctionBodyNotCompoundStatement(self.expr)
            self.body.validate()

