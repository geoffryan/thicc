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

class InvalidExpressionError(ParseError):
    def __init__(self, expr, message="Invalid Variable ref"):
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
        tokens.append(tok)

        #body is a list of statements, the braces have been removed
        body = self.parseBlock(tokens)

        return symbol.Function(ident, body)

    def parseBlock(self, tokens):
        # return a list of statements.  If the block begins with a brace "{"
        # read statements until "}".  Otherise parse a single statement and
        # return it in a list [stmnt]

        tok = tokens.pop()

        if isinstance(tok, token.OpenBrace):
            block = []
            tok = tokens.pop()
            while not isinstance(tok, token.ClosedBrace):
                tokens.append(tok)
                stmnt = self.parseStatement(tokens)
                block.append(stmnt)
                if len(tokens)==0:
                    raise UnmatchedBraceError()
                tok = tokens.pop()
        else:
            tokens.append(tok)
            stmnt = self.parseStatement(tokens)
            block = [stmnt]

        return block

    def parseStatement(self, tokens):
        tok = tokens.pop()
        #Check this is a return statement
        if isinstance(tok, token.ReturnK):
            expr = self.parseExpression(tokens)
            stmnt = symbol.ReturnS(expr)
        #Maybe a variable declaration?
        elif isinstance(tok, token.IntK):
            idTok = tokens.pop()
            if not isinstance(idTok, token.Identifier):
                raise InvalidStatementError(tok.val)
            assignTok = tokens.pop()
            if isinstance(assignTok, token.Assign):
                expr = self.parseExpression(tokens)
            elif isinstance(assignTok, token.Semicolon):
                expr = None
                tokens.append(assignTok)
            else:
                raise InvalidStatementError(tok.val)
            stmnt = symbol.DeclareS(idTok, expr)
        #Try just an expression, put back the first token first
        else:
            tokens.append(tok)
            expr = self.parseExpression(tokens)
            stmnt = symbol.ExpressionS(expr)

        tok = tokens.pop()
        if not isinstance(tok, token.Semicolon):
            raise InvalidStatementError(tok.val)

        return stmnt
    
    def parseExpression(self, tokens):
        expr = self.parseAssignExpr(tokens)
        return expr

    def parseAssignExpr(self, tokens):

        expr = None

        #Check if assignmentExpr
        if len(tokens) >= 3:
            tok1 = tokens.pop()
            tok2 = tokens.pop()
            if isinstance(tok1,token.Identifier)\
                    and isinstance(tok2, token.AssignmentOp):
                expr = self.parseExpression(tokens)
                expr = symbol.AssignE(tok1, tok2, expr)
            else:
                tokens.append(tok2)
                tokens.append(tok1)
        
        #If not, try the rest
        if expr is None:
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
            if isinstance(tok, token.IncrementOp):
                var = self.parseVariable(tokens)
                return symbol.IncrementPreE(tok, var)
            else:
                fac = self.parseFactor(tokens)
                return symbol.UnaryOpE(tok, fac)
        elif isinstance(tok, token.Constant):
            return symbol.ConstantE(tok)
        elif isinstance(tok, token.Identifier):
            tokens.append(tok)
            var = self.parseVariable(tokens)
            if len(tokens) > 0:
                tok = tokens.pop()
                if isinstance(tok, token.IncrementOp):
                    return symbol.IncrementPostE(tok, var)
                else:
                    tokens.append(tok)
            return var
        raise InvalidExpressionError(tok.val)

    def parseVariable(self, tokens):
        tok = tokens.pop()
        if isinstance(tok, token.Identifier):
            expr = symbol.VarRefE(tok)
        else:
            raise InvalidVariableRefError(tok.val)
        return expr


