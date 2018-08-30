from . import token
from . import symbol

class GeneratorError(Exception):
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

        return code

    def generateProgram(self, prog):
        code = self.generateFunction(prog.function)
        return code

    def generateFunction(self, func):
        name = func.name.val
        head1 = ".globl _{0:s}\n".format(name)
        head2 = "_{0:s}:\n".format(name)
        body = self.generateStatement(func.body)

        code = head1 + head2 + body
        return code

    def generateStatement(self, statement):
        if isinstance(statement, symbol.ReturnS):
            setValue = self.generateExpression(statement.value)
            returnLine = "ret\n"
            code = setValue+returnLine
        else:
            raise UnknownStatementError(statement)

        return code

    def generateExpression(self, expr):
        if isinstance(expr, symbol.ConstantE):
            val = expr.value.val
            code = "movl     ${0:s}, %eax\n".format(val)
        elif isinstance(expr, symbol.UnaryOpE):
            code = self.unaryOpCode(expr)
        elif isinstance(expr, symbol.BinaryOpE):
            code = self.binaryOpCode(expr)
        else:
            raise UnknownExpressionError(expr)

        return code

    def unaryOpCode(self, expr):

        codeSet = self.generateExpression(expr.expr)
        op = expr.op
        if isinstance(op, token.Not):
            codeOp  = "cmpl     $0, %eax\n"
            codeOp += "movl     $0, %eax\n"
            codeOp += "sete     %al\n"
        elif isinstance(op, token.Neg):
            codeOp =  "neg      %eax\n"
        elif isinstance(op, token.Complement):
            codeOp =  "not      %eax\n"
        else:
            raise UnknownExpressionError(expr)
        code = codeSet+codeOp

        return code

    def binaryOpCode(self, expr):

        op = expr.op
        e1 = expr.expr1
        e2 = expr.expr2

        codeSet1 = self.generateExpression(e1)
        codePush1 = "pushq    %rax\n"
        codeSet2 = self.generateExpression(e2)
        codePop1  = "popq     %rcx\n"

        if isinstance(op, token.Add):
            codeOp = "addl     %ecx, %eax\n"
        elif isinstance(op, token.Neg):
            codeOp = "subl     %eax, %ecx\n"
            codeOp += "movl     %ecx, %eax\n"
        elif isinstance(op, token.Mult):
            codeOp = "imull    %ecx, %eax\n"
        elif isinstance(op, token.Div):
            #swap e2 and e1 so e1 is in eax
            codeOp  = "movl     %ecx, %edx\n"
            codeOp += "movl     %eax, %ecx\n"
            codeOp += "movl     %edx, %eax\n"
            #zero out rdx
            codeOp += "movl     $0, %edx\n"
            #divide!
            codeOp += "idivl    %ecx\n"
        else:
            raise UnknownExpressionError(expr)

        code = codeSet1+codePush1+codeSet2+codePop1+codeOp
        return code




