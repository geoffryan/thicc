from . import token
from . import symbol
from . import exception

class ParseError(exception.ThiccError):
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
        self.binOpOrder = [[token.Or],
                            [token.And],
                            [token.BitOr],
                            [token.BitXor],
                            [token.BitAnd],
                            [token.Equal, token.NotEqual],
                            [token.LessThan, token.LessThanEqual,
                                token.GreaterThan, token.GreaterThanEqual],
                            [token.BitShiftL, token.BitShiftR],
                            [token.Add, token.Neg],
                            [token.Mult, token.Div, token.Mod]]

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
        if not isinstance(tok, token.OpenParentheses):
            raise InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.ClosedParentheses):
            raise InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenBrace):
            raise InvalidFunctionError(tok.val)

        body = self.parseStatement(tokens)

        tok = tokens.pop()
        if not isinstance(tok, token.ClosedBrace):
            raise InvalidFunctionError(tok.val)

        return symbol.Function(ident, body)

    def parseStatement(self, tokens):
        tok = tokens.pop()
        #Check this is a return statement
        if not isinstance(tok, token.ReturnK):
            raise InvalidStatementError(tok.val)

        expr = self.parseExpression(tokens)

        tok = tokens.pop()
        if not isinstance(tok, token.Semicolon):
            raise InvalidStatementError(tok.val)

        return symbol.ReturnS(expr)
    
    def parseExpression(self, tokens):
        expr = self.parseBinOp(tokens, self.binOpOrder)
        return expr

    def parseBinOp(self, tokens, opOrder):
        parseFunc = self.parseBinOp
        if len(opOrder) == 1:
            parseFunc = self.parseFactor
        ops = opOrder[0]
        table = opOrder[1:]

        expr = parseFunc(tokens, table)
        if len(tokens) > 0:
            tok = tokens.pop()
            while any([isinstance(tok,opCls) for opCls in ops]):
                el = parseFunc(tokens, table)
                expr = symbol.BinaryOpE(tok, expr, el)
                if len(tokens) > 0:
                    tok = tokens.pop()
                else:
                    tok = None
                    break
            if tok is not None:
                tokens.append(tok)
        return expr

    def parseFactor(self, tokens, empty=None):
        tok = tokens.pop()
        if isinstance(tok, token.OpenParentheses):
            fac = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.ClosedParentheses):
                raise UnmatchedParthenthesesError(tok.val)
            return fac
        elif isinstance(tok, token.UnaryOp):
            fac = self.parseFactor(tokens)
            return symbol.UnaryOpE(tok, fac)
        elif isinstance(tok, token.Constant):
            return symbol.ConstantE(tok)
        raise InvalidExpressionError(tok.val)

