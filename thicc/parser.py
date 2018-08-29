from . import token
from . import symbol

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

class UnmatchedParenthesesError(ParseError):
    def __init__(self, expr, message="Parentheses block is not closed"):
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
        return symbol.Program(func)

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

        return symbol.Function(ident, body)

    def parseStatement(self, tokens):
        tok = tokens.pop()
        #Check this is a return statement
        if not isinstance(tok, token.ReturnK):
            raise InvalidStatementError(tok.val)

        expr = self.parseExpression(tokens)

        tok = tokens.pop()
        if not isinstance(tok, token.SemicolonP):
            raise InvalidStatementError(tok.val)

        return symbol.ReturnS(expr)

    def parseExpression(self, tokens):
        expr = self.parseTerm(tokens)
        if len(tokens) > 0:
            tok = tokens.pop()
            while isinstance(tok,token.AddP) or isinstance(tok,token.NegP):
                term = self.parseTerm(tokens)
                expr = symbol.BinaryOpE(tok, expr, term)
                if len(tokens) > 0:
                    tok = tokens.pop()
                else:
                    tok = None
                    break
            if tok is not None:
                tokens.append(tok)

        return expr

    def parseTerm(self, tokens):
        term = self.parseFactor(tokens)
        if len(tokens) > 0:
            tok = tokens.pop()
            while isinstance(tok,token.MultP) or isinstance(tok,token.DivP):
                fac = self.parseFactor(tokens)
                term = symbol.BinaryOpE(tok, term, fac)
                if len(tokens) > 0:
                    tok = tokens.pop()
                else:
                    tok = None
                    break
            if tok is not None:
                tokens.append(tok)

        return term

    def parseFactor(self, tokens):
        tok = tokens.pop()
        if isinstance(tok, token.OpenParenthesesP):
            fac = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.ClosedParenthesesP):
                raise UnmatchedParthenthesesError(tok.val)
            return fac
        elif isinstance(tok, token.UnaryOpP):
            fac = self.parseFactor(tokens)
            return symbol.UnaryOpE(tok, fac)
        elif isinstance(tok, token.Constant):
            return symbol.ConstantE(tok)
        raise InvalidExpressionError(tok.val)

