from . import token
from . import symbol

class GeneratorError(Exception):
    pass

class UnknownStatementError(GeneratorError):
    def __init__(self, expr, message="Unknown type of statement"):
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
            val = statement.value.value.val
            line1 = "movl\t${0:s}, %eax\n".format(val)
            line2 = "ret\n"
            code = line1+line2
        else:
            raise UnknownStatementError(statement)

        return code


