from . import token
from . import symbol
from . import exception
from . import context

class GeneratorError(exception.ThiccError):
    pass

class UnknownStatementError(GeneratorError):
    def __init__(self, expr, message="Unknown type of statement"):
        self.expression = expr
        self.message = message

class UnknownExpressionError(GeneratorError):
    def __init__(self, expr, message="Unknown type of expression"):
        self.expression = expr
        self.message = message

class UnknownIncrementOperatorError(GeneratorError):
    def __init__(self, expr, message="Unknown type of increment operator"):
        self.expression = expr
        self.message = message

class InvalidASTHeadError(GeneratorError):
    def __init__(self, expr, message="Cannot generate code from AST Head"):
        self.expression = expr
        self.message = message

class InvalidBlockItemError(GeneratorError):
    def __init__(self, expr, message="Object is not block item."):
        self.expression = expr
        self.message = message

class InvalidBreakContextError(GeneratorError):
    def __init__(self, expr=None, message="Break statement not in valid context."):
        self.expression = expr
        self.message = message

class InvalidContinueContextError(GeneratorError):
    def __init__(self, expr=None, message="Continue statement not in valid context."):
        self.expression = expr
        self.message = message

class Generator():

    def __init__(self):
        self.counter = 0
        self.indent = 4*" "
        self.argCol = 8

    def makeLabel(self):
        lbl = "_lbl{0:d}".format(self.counter)
        self.counter += 1 
        return lbl

    def label(self, lbl):
        line = lbl + ":"
        return line

    def instruct(self, instruction, arg1=None, arg2=None):

        line = self.indent + instruction
        if arg1 is not None:
            space = (self.argCol - len(instruction)) * " "
            line += space + arg1
            if arg2 is not None:
                line += ", " + arg2
        return line


    def generate(self, ast):
        if(isinstance(ast, symbol.Program)):
            code = self.generateProgram(ast)
        elif(isinstance(ast, symbol.Declaration)):
            code = self.generateDeclaration(ast)
        elif(isinstance(ast, symbol.Statement)):
            code = self.generateStatement(ast)
        else:
            raise InvalidASTHeadError(ast)

        codeStr = "\n".join(code)

        return codeStr

    def generateProgram(self, prog):
        code = []
        for decl in prog.declarations:
            code += self.generateDeclaration(decl, None)
        return code

    def generateFunction(self, func):

        name = func.name.val
        head1 = [   ".globl _{0:s}".format(name)]
        head2 = [   "_{0:s}:".format(name)]
        prologue = [self.instruct("push", "%rbp"),
                    self.instruct("movq", "%rsp", "%rbp")]

        """
        if len(func.body) == 0\
                or not isinstance(func.body[-1], symbol.ReturnS):
            ret0 = symbol.ReturnS(symbol.ConstantE(token.IntC("0")))
            func.body.append(ret0)
        """

        body = self.generateCompoundStatement(func.body, None, dealloc=False)
        
        if len(func.body) == 0\
                or not isinstance(func.body[-1], symbol.ReturnS):
            ret0 = symbol.ReturnS(symbol.ConstantE(token.IntC("0")))
            body += self.generateStatement(ret0, None)

        code = head1 + head2 + prologue + body
        return code

    def generateCompoundStatement(self, stmnt, superCont, dealloc=True):

        cont = context.Context(superContext=superCont)
        code = []
        for item in stmnt:
            if isinstance(item, symbol.Declaration):
                code += self.generateDeclaration(item, cont)
            elif isinstance(item, symbol.Statement):
                code += self.generateStatement(item, cont)
            else:
                raise InvalidBlockItemError(item)

        if dealloc:
            # Deallocate variables from the stack
            # ie. Move the stack pointer back by the amount it has changed
            #     in this block.
            bytesAdded = "${0:d}".format(cont.vmap.size)
            deallocCode = [self.instruct("addq", bytesAdded, "%rsp")]

            code += deallocCode

        return code

    def generateDeclaration(self, declaration, cont):
        if isinstance(declaration, symbol.VariableD):
            if declaration.expr is not None:
                init = self.generateExpression(declaration.expr, cont)
            else:
                init = [self.instruct("movq","$0","%rax")]
            declare  = [self.instruct("push","%rax")]
            cont.addVar(declaration.id)
            code = init+declare
        elif isinstance(declaration, symbol.FunctionD):
            code = self.generateFunction(declaration)
        else:
            raise UnknownDeclarationError(declaration)

        return code

    def generateStatement(self, statement, cont):
        if isinstance(statement, symbol.ReturnS):
            setValue = self.generateExpression(statement.value, cont)
            epilogue = [self.instruct("movq","%rbp","%rsp"),
                        self.instruct("pop","%rbp")]
            returnLine = [self.instruct("ret")]
            code = setValue + epilogue + returnLine
        elif isinstance(statement, symbol.ExpressionS):
            code = self.generateExpression(statement.expr, cont)
        elif isinstance(statement, symbol.ConditionalS):
            code = self.conditionalStmntCode(statement, cont)
        elif isinstance(statement, symbol.CompoundS):
            code = self.generateCompoundStatement(statement, cont)
        elif isinstance(statement, symbol.WhileS):
            code = self.whileStmntCode(statement, cont)
        elif isinstance(statement, symbol.DoS):
            code = self.doStmntCode(statement, cont)
        elif isinstance(statement, symbol.ForS):
            code = self.forStmntCode(statement, cont)
        elif isinstance(statement, symbol.ContinueS):
            code = self.continueStmntCode(statement, cont)
        elif isinstance(statement, symbol.BreakS):
            code = self.breakStmntCode(statement, cont)
        else:
            raise UnknownStatementError(statement)

        return code

    def generateExpression(self, expr, cont):
        if expr is None:
            code = []
        elif isinstance(expr, symbol.ConstantE):
            code = self.constExprCode(expr)
        elif isinstance(expr, symbol.VarRefE):
            code = self.varRefCode(expr, cont)
        elif isinstance(expr, symbol.IncrementPostE):
            code = self.incrementPostCode(expr, cont)
        elif isinstance(expr, symbol.IncrementPreE):
            code = self.incrementPreCode(expr, cont)
        elif isinstance(expr, symbol.UnaryOpE):
            code = self.unaryOpCode(expr, cont)
        elif isinstance(expr, symbol.BinaryOpE):
            code = self.binaryOpCode(expr, cont)
        elif isinstance(expr, symbol.AssignE):
            code = self.assignOpCode(expr, cont)
        elif isinstance(expr, symbol.ConditionalE):
            code = self.conditionalExprCode(expr, cont)
        else:
            raise UnknownExpressionError(expr)

        return code

class Generator_x86_64(Generator):

    def constExprCode(self, expr):
        val = expr.value.val
        code = [self.instruct("movq","${0:s}".format(val),"%rax")]
        return code

    def varRefCode(self, expr, cont):
        offset = cont.varLoc(expr.id)
        var = "{0:d}(%rbp)".format(offset)
        code = [self.instruct("movq",var,"%rax")]
        return code

    def incrementPostCode(self, expr, cont):
        refCode = self.varRefCode(expr.var, cont)
        offset = cont.varLoc(expr.var.id)
        var = "{0:d}(%rbp)".format(offset)
        if isinstance(expr.op, token.Increment):
            incCode = [self.instruct("incq",var)]
        elif isinstance(expr.op, token.Decrement):
            incCode = [self.instruct("decq",var)]
        else:
            raise UnknownIncrementOperatorError(expr.op)
        code = refCode + incCode
        return code

    def incrementPreCode(self, expr, cont):
        offset = cont.varLoc(expr.var.id)
        var = "{0:d}(%rbp)".format(offset)
        if isinstance(expr.op, token.Increment):
            incCode = [self.instruct("incq",var)]
        elif isinstance(expr.op, token.Decrement):
            incCode = [self.instruct("decq",var)]
        else:
            raise UnknownIncrementOperatorError(expr.op)
        refCode = self.varRefCode(expr.var, cont)
        code = incCode + refCode
        return code


    def unaryOpCode(self, expr, cont):

        codeSet = self.generateExpression(expr.expr, cont)
        op = expr.op
        if isinstance(op, token.Not):
            codeOp = [  self.instruct("cmpl", "$0", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("sete", "%al")]
        elif isinstance(op, token.Neg):
            codeOp =  [ self.instruct("neg", "%eax")]
        elif isinstance(op, token.Complement):
            codeOp =  [ self.instruct("not", "%eax")]
        else:
            raise UnknownExpressionError(expr)
        code = codeSet+codeOp

        return code

    def binaryOpCode(self, expr, cont):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1, cont)
        codePush1 = [   self.instruct("pushq", "%rax")]
        codeSet2 = self.generateExpression(e2, cont)
        codeSet2 += [   self.instruct("movl", "%eax", "%ecx")]
        codePop1  = [   self.instruct("popq", "%rax")]

        if isinstance(op, token.Add):
            codeOp = [  self.instruct("addl", "%ecx", "%eax")]
        elif isinstance(op, token.Neg):
            codeOp = [  self.instruct("subl", "%ecx", "%eax")]
        elif isinstance(op, token.Mult):
            codeOp = [  self.instruct("imull", "%ecx", "%eax")]
        elif isinstance(op, token.Div):
            #zero out rdx and divide
            codeOp = [  self.instruct("movl", "$0", "%edx"),
                        self.instruct("idivl", "%ecx")]
        elif isinstance(op, token.Mod):
            #zero out rdx and divide
            codeOp =  [ self.instruct("movl", "$0", "%edx"),
                        self.instruct("idivl", "%ecx"),
                        self.instruct("movl", "%edx", "%eax")]
        elif isinstance(op, token.BitShiftL):
            codeOp =  [ self.instruct("shll", "%cl", "%eax")]
        elif isinstance(op, token.BitShiftR):
            codeOp =  [ self.instruct("shrl", "%cl", "%eax")]
        elif isinstance(op, token.BitAnd):
            codeOp =  [ self.instruct("andl", "%ecx", "%eax")]
        elif isinstance(op, token.BitOr):
            codeOp =  [ self.instruct("orl", "%ecx", "%eax")]
        elif isinstance(op, token.BitXor):
            codeOp =  [ self.instruct("xorl", "%ecx", "%eax")]
        elif isinstance(op, token.Equal):
            codeOp =  [ self.instruct("cmpl", "%eax", "%ecx"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("sete", "%al")]
        elif isinstance(op, token.NotEqual):
            codeOp =  [ self.instruct("cmpl", "%eax", "%ecx"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("setne", "%al")]
        elif isinstance(op, token.LessThan):
            codeOp =  [ self.instruct("cmpl", "%ecx", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("sets", "%al")]
        elif isinstance(op, token.GreaterThan):
            codeOp =  [ self.instruct("cmpl", "%eax", "%ecx"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("sets", "%al")]
        elif isinstance(op, token.LessThanEqual):
            codeOp =  [ self.instruct("cmpl", "%eax", "%ecx"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("setns", "%al")]
        elif isinstance(op, token.GreaterThanEqual):
            codeOp =  [ self.instruct("cmpl", "%ecx", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("setns", "%al")]
        elif isinstance(op, token.And):
            codeOp =  [ self.instruct("cmpl", "$0", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("setne", "%al"),
                        self.instruct("cmpl", "$0", "%ecx"),
                        self.instruct("movl", "$0", "%ecx"),
                        self.instruct("setne", "%cl"),
                        self.instruct("andl", "%ecx", "%eax")]
        elif isinstance(op, token.Or):
            codeOp =  [ self.instruct("orl", "%ecx", "%eax"),
                        self.instruct("cmpl", "$0", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("setne", "%al")]
        else:
            raise UnknownExpressionError(expr)

        code = codeSet1+codePush1+codeSet2+codePop1+codeOp
        return code

    def assignOpCode(self, expr, cont):
        offset = cont.varLoc(expr.id)
        calc = self.generateExpression(expr.expr, cont)
        var = "{0:d}(%rbp)".format(offset)
        if isinstance(expr.op, token.Assign):
            assign = [  self.instruct("movq", "%rax", var)]
        elif isinstance(expr.op, token.AssignAdd):
            assign = [  self.instruct("addq", "%rax", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignSub):
            assign = [  self.instruct("subq", "%rax", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignMult):
            assign = [  self.instruct("imulq",var),
                        self.instruct("movq", "%rax", var)]
        elif isinstance(expr.op, token.AssignDiv):
            assign = [  self.instruct("movq", "%rax", "%rcx"),
                        self.instruct("movq", var, "%rax"),
                        self.instruct("movq", "$0", "%rdx"),
                        self.instruct("idivq", "%rcx"),
                        self.instruct("movq", "%rax", var)]
        elif isinstance(expr.op, token.AssignMod):
            assign = [  self.instruct("movq", "%rax", "%rcx"),
                        self.instruct("movq", var, "%rax"),
                        self.instruct("movq", "$0", "%rdx"),
                        self.instruct("idivq", "%rcx"),
                        self.instruct("movq", "%rdx", var),
                        self.instruct("movq", "%rdx", "%rax")]
        elif isinstance(expr.op, token.AssignBShiftL):
            assign = [  self.instruct("movq", "%rax", "%rcx"),
                        self.instruct("shlq", "%cl", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignBShiftR):
            assign = [  self.instruct("movq", "%rax", "%rcx"),
                        self.instruct("shrq", "%cl", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignBAnd):
            assign = [  self.instruct("andq", "%rax", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignBOr):
            assign = [  self.instruct("orq", "%rax", var),
                        self.instruct("movq", var, "%rax")]
        elif isinstance(expr.op, token.AssignBXor):
            assign = [  self.instruct("xorq", "%rax", var),
                        self.instruct("movq", var, "%rax")]
        else:
            raise UnknownExpressionError(expr)
        code = calc + assign
        return code

    def conditionalExprCode(self, expr, cont):

        evalCond = self.generateExpression(expr.cond, cont)
        evalTrue = self.generateExpression(expr.true, cont)
        evalFalse = self.generateExpression(expr.false, cont)
        falseLabel = self.makeLabel()
        endLabel = self.makeLabel()

        checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                        self.instruct("je", falseLabel)]

        jmpEnd = [  self.instruct("jmp", endLabel)]
        lblFalse = [    self.label(falseLabel)]
        lblEnd = [    self.label(endLabel)]

        code = evalCond + checkCond + evalTrue + jmpEnd\
                + lblFalse + evalFalse + lblEnd

        return code

    def conditionalStmntCode(self, stmnt, cont):

        evalCond = self.generateExpression(stmnt.cond, cont)
        evalTrue = self.generateStatement(stmnt.ifS, cont)
        
        if stmnt.elseS is not None:
            evalFalse = self.generateStatement(stmnt.elseS, cont)
            falseLabel = self.makeLabel()
            endLabel = self.makeLabel()

            checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                            self.instruct("je", falseLabel)]

            jmpEnd = [  self.instruct("jmp", endLabel)]
            lblFalse = [    self.label(falseLabel)]
            lblEnd = [    self.label(endLabel)]

            code = evalCond + checkCond + evalTrue + jmpEnd\
                    + lblFalse + evalFalse + lblEnd
        else:
            endLabel = self.makeLabel()

            checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                            self.instruct("je", endLabel)]

            lblEnd = [    self.label(endLabel)]

            code = evalCond + checkCond + evalTrue + lblEnd

        return code

    def whileStmntCode(self, stmnt, superCont):
        cont = context.Context(superContext=superCont)
        startLabel = self.makeLabel()
        endLabel = self.makeLabel()
        cont.continueLabel = startLabel
        cont.breakLabel = endLabel

        lblStart =  [   self.label(startLabel)]

        evalCond = self.generateExpression(stmnt.cond, cont)

        checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                        self.instruct("je", endLabel)]

        evalStmnt = self.generateStatement(stmnt.body, cont)

        loop =      [   self.instruct("jmp", startLabel)]

        lblEnd =    [   self.label(endLabel)]

        stmnt = lblStart + evalCond + checkCond + evalStmnt + loop + lblEnd

        return stmnt

    def doStmntCode(self, stmnt, superCont):
        cont = context.Context(superContext=superCont)
        startLabel = self.makeLabel()
        condLabel = self.makeLabel()
        endLabel = self.makeLabel()
        cont.continueLabel = condLabel
        cont.breakLabel = endLabel

        lblStart =  [   self.label(startLabel)]

        evalStmnt = self.generateStatement(stmnt.body, cont)

        lblCond =   [   self.label(condLabel)]

        evalCond = self.generateExpression(stmnt.cond, cont)
        
        checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                        self.instruct("je", endLabel)]

        loop =      [   self.instruct("jmp", startLabel)]

        lblEnd =    [   self.label(endLabel)]

        stmnt = lblStart + evalStmnt + evalCond + checkCond + loop + lblEnd

        return stmnt

    def forStmntCode(self, stmnt, superCont):
        cont = context.Context(superContext=superCont)
        startLabel = self.makeLabel()
        postLabel = self.makeLabel()
        endLabel = self.makeLabel()
        cont.continueLabel = postLabel
        cont.breakLabel = endLabel

        if stmnt.init is None:
            evalInit = []
        elif isinstance(stmnt.init, symbol.Declaration):
            evalInit = self.generateDeclaration(stmnt.init, cont)
        else:
            evalInit = self.generateExpression(stmnt.init, cont)

        lblStart =  [   self.label(startLabel)]

        evalCond = self.generateExpression(stmnt.cond, cont)

        checkCond = [   self.instruct("cmpq", "$0", "%rax"),
                        self.instruct("je", endLabel)]

        evalStmnt = self.generateStatement(stmnt.body, cont)

        lblPost =   [   self.label(postLabel)]

        if stmnt.post is None:
            evalPost = []
        else:
            evalPost = self.generateExpression(stmnt.post, cont)

        loop =      [   self.instruct("jmp", startLabel)]

        lblEnd =    [   self.label(endLabel)]
        
        if isinstance(stmnt.init, symbol.Declaration):
            bytesAdded = "${0:d}".format(cont.vmap.size)
            dealloc = [ self.instruct("addq", bytesAdded, "%rsp")]
        else:
            dealloc = []

        stmnt = evalInit + lblStart + evalCond + checkCond + evalStmnt\
                + lblPost + evalPost + loop + lblEnd + dealloc

        return stmnt

    def breakStmntCode(self, stmnt, cont):
        if cont.breakLabel is None:
            raise InvalidBreakContextError()

        stmnt =  [   self.instruct("jmp", cont.breakLabel)]

        return stmnt
        
    def continueStmntCode(self, stmnt, cont):
        if cont.continueLabel is None:
            raise InvalidContinueContextError()

        stmnt =  [   self.instruct("jmp", cont.continueLabel)]

        return stmnt
        

"""
class Generator_x86(Generator):

    def constExprCode(self, expr):
        val = expr.value.val
        code = ["movl     ${0:s}, %eax".format(val)]
        return code

    def unaryOpCode(self, expr):

        codeSet = self.generateExpression(expr.expr)
        op = expr.op
        if isinstance(op, token.Not):
            codeOp  = [ self.instruct("cmpl", "$0", "%eax"),
                        self.instruct("movl", "$0", "%eax"),
                        self.instruct("sete", "%al")]
        elif isinstance(op, token.Neg):
            codeOp =  [ self.instruct("neg", "%eax")]
        elif isinstance(op, token.Complement):
            codeOp =  [ self.instruct("not", "%eax")]
        else:
            raise UnknownExpressionError(expr)
        code = codeSet+codeOp

        return code

    def binaryOpCode(self, expr):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1)
        codePush1 = [   self.instruct("pushl", "%eax")]
        codeSet2 = self.generateExpression(e2)
        codePop1  = [   self.instruct("popl", "%ecx")]

        if isinstance(op, token.Add):
            codeOp = [  self.instruct("addl", "%ecx", "%eax")]
        elif isinstance(op, token.Neg):
            codeOp = [  self.instruct("subl", "%eax", "%ecx"),
                        self.instruct("movl", "%ecx", "%eax")]
        elif isinstance(op, token.Mult):
            codeOp = [  self.instruct("imull", "%ecx", "%eax")]
        elif isinstance(op, token.Div):
            #swap e2 and e1 so e1 is in eax
            codeOp  = [ self.instruct("movl", "%ecx", "%edx"),
                        self.instruct("movl", "%eax", "%ecx"),
                        self.instruct("movl", "%edx", "%eax"),
            #zero out rdx
                        self.instruct("movl", "$0", "%edx"),
            #divide!
                        self.instruct("idivl", "%ecx")]
        else:
            raise UnknownExpressionError(expr)

        code = codeSet1+codePush1+codeSet2+codePop1+codeOp
        return code
"""
