from . import token
from . import symbol
from . import exception

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

class InvalidASTHeadError(GeneratorError):
    def __init__(self, expr, message="Cannot generate code from AST Head"):
        self.expression = expr
        self.message = message

class Generator():

    def __init__(self):
        pass

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
        name = func.name.val
        head1 = [".globl _{0:s}".format(name)]
        head2 = ["_{0:s}:".format(name)]
        body = self.generateStatement(func.body)

        code = head1 + head2 + body
        return code

    def generateStatement(self, statement):
        if isinstance(statement, symbol.ReturnS):
            setValue = self.generateExpression(statement.value)
            returnLine = ["ret"]
            code = setValue+returnLine
        else:
            raise UnknownStatementError(statement)

        return code

    def generateExpression(self, expr):
        if isinstance(expr, symbol.ConstantE):
            code = self.constExprCode(expr)
        elif isinstance(expr, symbol.UnaryOpE):
            code = self.unaryOpCode(expr)
        elif isinstance(expr, symbol.BinaryOpE):
            code = self.binaryOpCode(expr)
        else:
            raise UnknownExpressionError(expr)

        return code

    def constExprCode(self, expr):
        pass
    def unaryOpCode(self, expr):
        pass
    def binaryOpCode(self, expr):
        pass

class Generator_x86_64(Generator):

    def constExprCode(self, expr):
        val = expr.value.val
        code = ["movl     ${0:s}, %eax".format(val)]
        return code

    def unaryOpCode(self, expr):

        codeSet = self.generateExpression(expr.expr)
        op = expr.op
        if isinstance(op, token.Not):
            codeOp = [  "cmpl     $0, %eax",
                        "movl     $0, %eax",
                        "sete     %al"]
        elif isinstance(op, token.Neg):
            codeOp =  [ "neg      %eax"]
        elif isinstance(op, token.Complement):
            codeOp =  [ "not      %eax"]
        else:
            raise UnknownExpressionError(expr)
        code = codeSet+codeOp

        return code

    def binaryOpCode(self, expr):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1)
        codePush1 = [   "pushq    %rax"]
        codeSet2 = self.generateExpression(e2)
        codeSet2 += [   "movl     %eax, %ecx"]
        codePop1  = [   "popq     %rax"]

        if isinstance(op, token.Add):
            codeOp = [  "addl     %ecx, %eax"]
        elif isinstance(op, token.Neg):
            codeOp = [  "subl     %ecx, %eax"]
        elif isinstance(op, token.Mult):
            codeOp = [  "imull    %ecx, %eax"]
        elif isinstance(op, token.Div):
            #zero out rdx and divide
            codeOp = [  "movl     $0, %edx",
                        "idivl    %ecx"]
        elif isinstance(op, token.Mod):
            #zero out rdx and divide
            codeOp =  [ "movl     $0, %edx",
                        "idivl    %ecx",
                        "movl     %edx, %eax"]
        elif isinstance(op, token.BitShiftL):
            codeOp =  [ "shll     %cl, %eax"]
        elif isinstance(op, token.BitShiftR):
            codeOp =  [ "shrl     %cl, %eax"]
        elif isinstance(op, token.BitAnd):
            codeOp =  [ "and      %ecx, %eax"]
        elif isinstance(op, token.BitOr):
            codeOp =  [ "orl      %ecx, %eax"]
        elif isinstance(op, token.BitXor):
            codeOp =  [ "xorl     %ecx, %eax"]
        elif isinstance(op, token.Equal):
            codeOp =  [ "cmpl     %eax, %ecx",
                        "movl     $0, %eax",
                        "sete     %al"]
        elif isinstance(op, token.NotEqual):
            codeOp =  [ "cmpl     %eax, %ecx",
                        "movl     $0, %eax",
                        "setne    %al"]
        elif isinstance(op, token.LessThan):
            codeOp =  [ "cmpl     %ecx, %eax",
                        "movl     $0, %eax",
                        "sets     %al"]
        elif isinstance(op, token.GreaterThan):
            codeOp =  [ "cmpl     %eax, %ecx",
                        "movl     $0, %eax",
                        "sets     %al"]
        elif isinstance(op, token.LessThanEqual):
            codeOp =  [ "cmpl     %eax, %ecx",
                        "movl     $0, %eax",
                        "setns    %al"]
        elif isinstance(op, token.GreaterThanEqual):
            codeOp =  [ "cmpl     %ecx, %eax",
                        "movl     $0, %eax",
                        "setns    %al"]
        elif isinstance(op, token.And):
            codeOp =  [ "cmpl     $0, %eax",
                        "movl     $0, %eax",
                        "setne    %al",
                        "cmpl     $0, %ecx",
                        "movl     $0, %ecx",
                        "setne    %cl",
                        "andl     %ecx, %eax"]
        elif isinstance(op, token.Or):
            codeOp =  [ "orl      %ecx, %eax",
                        "cmpl     $0, %eax",
                        "movl     $0, %eax",
                        "setne    %al"]
        else:
            raise UnknownExpressionError(expr)

        code = codeSet1+codePush1+codeSet2+codePop1+codeOp
        return code


class Generator_x86(Generator):

    def constExprCode(self, expr):
        val = expr.value.val
        code = ["movl     ${0:s}, %eax".format(val)]
        return code

    def unaryOpCode(self, expr):

        codeSet = self.generateExpression(expr.expr)
        op = expr.op
        if isinstance(op, token.Not):
            codeOp  = [ "cmpl     $0, %eax",
                        "movl     $0, %eax",
                        "sete     %al"]
        elif isinstance(op, token.Neg):
            codeOp =  [ "neg      %eax"]
        elif isinstance(op, token.Complement):
            codeOp =  [ "not      %eax"]
        else:
            raise UnknownExpressionError(expr)
        code = codeSet+codeOp

        return code

    def binaryOpCode(self, expr):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1)
        codePush1 = [   "pushl    %eax"]
        codeSet2 = self.generateExpression(e2)
        codePop1  = [   "popl     %ecx"]

        if isinstance(op, token.Add):
            codeOp = [  "addl     %ecx, %eax"]
        elif isinstance(op, token.Neg):
            codeOp = [  "subl     %eax, %ecx",
                        "movl     %ecx, %eax"]
        elif isinstance(op, token.Mult):
            codeOp = [  "imull    %ecx, %eax"]
        elif isinstance(op, token.Div):
            #swap e2 and e1 so e1 is in eax
            codeOp  = [ "movl     %ecx, %edx",
                        "movl     %eax, %ecx",
                        "movl     %edx, %eax",
            #zero out rdx
                        "movl     $0, %edx",
            #divide!
                        "idivl    %ecx"]
        else:
            raise UnknownExpressionError(expr)

        code = codeSet1+codePush1+codeSet2+codePop1+codeOp
        return code
