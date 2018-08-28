from . import token
from . import ast

class ParseError(Exception):
    pass

class InvalidExpressionError(ParseError):
    def __init__(self, expr, message="Invalid Expression"):
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

class Parser():

    def __init__(self):
        pass

    def parse(self, toks):

        reverseTokens = toks[::-1]

        ast = self.parseProgram(reverseTokens)

        return ast

    def parseProgram(self, tokens):
        func = self.parseFunction(tokens)
        return ast.Program(func)

    def parseFunction(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.IntK):
            raise InvalidFunctionError(tok.val)

        ident = tokens.pop()
        if not isinstance(ident, token.Identifier):
            raise InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParenthesesP):
            raise InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.ClosedParenthesesP):
            raise InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenBraceP):
            raise InvalidFunctionError(tok.val)

        body = self.parseStatement(tokens)

        tok = tokens.pop()
        if not isinstance(tok, token.ClosedBraceP):
            raise InvalidFunctionError(tok.val)

        return ast.Function(ident, body)

    def parseStatement(self, tokens):
        tok = tokens.pop()
        #Check this is a return statement
        if not isinstance(tok, token.ReturnK):
            raise InvalidStatementError(tok.val)

        expr = self.parseExpression(tokens)

        tok = tokens.pop()
        if not isinstance(tok, token.SemicolonP):
            raise InvalidStatementError(tok.val)

        return ast.ReturnS(expr)


    def parseExpression(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.Constant):
            raise InvalidExpressionError(tok.val)
        return ast.ConstantE(tok)


