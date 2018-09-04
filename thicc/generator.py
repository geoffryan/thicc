from . import token
from . import symbol
from . import exception
from . import varmap

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
        elif(isinstance(ast, symbol.Function)):
            code = self.generateFunction(ast)
        elif(isinstance(ast, symbol.Statement)):
            code = self.generateStatement(ast)
        else:
            raise InvalidASTHeadError(ast)

        codeStr = "\n".join(code)

        return codeStr

    def generateProgram(self, prog):
        code = self.generateFunction(prog.function)
        return code

    def generateFunction(self, func):

        vmap = varmap.VarMap()

        name = func.name.val
        head1 = [   ".globl _{0:s}".format(name)]
        head2 = [   "_{0:s}:".format(name)]
        prologue = [self.instruct("push", "%rbp"),
                    self.instruct("movq", "%rsp", "%rbp")]
        prologue = [self.instruct("push", "%rbp"),
                    self.instruct("movq", "%rsp", "%rbp")]
        body = []
        for item in func.body:
            if isinstance(item, symbol.Declaration):
                body += self.generateDeclaration(item, vmap)
            elif isinstance(item, symbol.Statement):
                body += self.generateStatement(item, vmap)
            else:
                raise InvalidBlockItemError(item)

        if len(func.body) == 0\
                or not isinstance(func.body[-1], symbol.ReturnS):
            ret0 = symbol.ReturnS(symbol.ConstantE(token.IntC("0")))
            body += self.generateStatement(ret0, vmap)

        code = head1 + head2 + prologue + body
        return code

    def generateDeclaration(self, declaration, vmap):
        if isinstance(declaration, symbol.VariableD):
            if declaration.expr is not None:
                init = self.generateExpression(declaration.expr, vmap)
            else:
                init = [self.instruct("movq","$0","%rax")]
            declare  = [self.instruct("push","%rax")]
            vmap.add(declaration.id)
            code = init+declare
        else:
            raise UnknownDeclarationError(declaration)

        return code

    def generateStatement(self, statement, vmap):
        if isinstance(statement, symbol.ReturnS):
            setValue = self.generateExpression(statement.value, vmap)
            epilogue = [self.instruct("movq","%rbp","%rsp"),
                        self.instruct("pop","%rbp")]
            returnLine = [self.instruct("ret")]
            code = setValue + epilogue + returnLine
        elif isinstance(statement, symbol.ExpressionS):
            code = self.generateExpression(statement.expr, vmap)
        elif isinstance(statement, symbol.ConditionalS):
            code = self.conditionalStmntCode(statement, vmap)
        else:
            raise UnknownStatementError(statement)

        return code

    def generateExpression(self, expr, vmap):
        if isinstance(expr, symbol.ConstantE):
            code = self.constExprCode(expr)
        elif isinstance(expr, symbol.VarRefE):
            code = self.varRefCode(expr, vmap)
        elif isinstance(expr, symbol.IncrementPostE):
            code = self.incrementPostCode(expr, vmap)
        elif isinstance(expr, symbol.IncrementPreE):
            code = self.incrementPreCode(expr, vmap)
        elif isinstance(expr, symbol.UnaryOpE):
            code = self.unaryOpCode(expr, vmap)
        elif isinstance(expr, symbol.BinaryOpE):
            code = self.binaryOpCode(expr, vmap)
        elif isinstance(expr, symbol.AssignE):
            code = self.assignOpCode(expr, vmap)
        elif isinstance(expr, symbol.ConditionalE):
            code = self.conditionalExprCode(expr, vmap)
        else:
            raise UnknownExpressionError(expr)

        return code

    def constExprCode(self, expr):
        pass
    def varRefCode(self, expr, vmap):
        pass
    def unaryOpCode(self, expr, vmap):
        pass
    def binaryOpCode(self, expr, vmap):
        pass
    def assignOpCode(self, expr, vmap):
        pass

class Generator_x86_64(Generator):

    def constExprCode(self, expr):
        val = expr.value.val
        code = [self.instruct("movl","${0:s}".format(val),"%eax")]
        return code

    def varRefCode(self, expr, vmap):
        offset = vmap.getOffset(expr.id)
        var = "{0:d}(%rbp)".format(offset)
        code = [self.instruct("movq",var,"%rax")]
        return code

    def incrementPostCode(self, expr, vmap):
        refCode = self.varRefCode(expr.var, vmap)
        offset = vmap.getOffset(expr.var.id)
        var = "{0:d}(%rbp)".format(offset)
        if isinstance(expr.op, token.Increment):
            incCode = [self.instruct("incq",var)]
        elif isinstance(expr.op, token.Decrement):
            incCode = [self.instruct("decq",var)]
        else:
            raise UnknownIncrementOperatorError(expr.op)
        code = refCode + incCode
        return code

    def incrementPreCode(self, expr, vmap):
        offset = vmap.getOffset(expr.var.id)
        var = "{0:d}(%rbp)".format(offset)
        if isinstance(expr.op, token.Increment):
            incCode = [self.instruct("incq",var)]
        elif isinstance(expr.op, token.Decrement):
            incCode = [self.instruct("decq",var)]
        else:
            raise UnknownIncrementOperatorError(expr.op)
        refCode = self.varRefCode(expr.var, vmap)
        code = incCode + refCode
        return code


    def unaryOpCode(self, expr, vmap):

        codeSet = self.generateExpression(expr.expr, vmap)
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

    def binaryOpCode(self, expr, vmap):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1, vmap)
        codePush1 = [   self.instruct("pushq", "%rax")]
        codeSet2 = self.generateExpression(e2, vmap)
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

    def assignOpCode(self, expr, vmap):
        offset = vmap.getOffset(expr.id)
        calc = self.generateExpression(expr.expr, vmap)
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

    def conditionalExprCode(self, expr, vmap):

        evalCond = self.generateExpression(expr.cond, vmap)
        evalTrue = self.generateExpression(expr.true, vmap)
        evalFalse = self.generateExpression(expr.false, vmap)
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

    def conditionalStmntCode(self, stmnt, vmap):

        evalCond = self.generateExpression(stmnt.cond, vmap)
        evalTrue = self.generateStatement(stmnt.ifS, vmap)
        
        if stmnt.elseS is not None:
            evalFalse = self.generateStatement(stmnt.elseS, vmap)
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
