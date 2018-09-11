from . import token
from . import symbol
from . import exception

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

        if len(tokens) != 0:
            raise TrailingCharactersProgramError(tokens[-1].val)

        return symbol.Program(func)

    def parseFunction(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.Int):
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

        body = self.parseCompoundStatement(tokens)

        return symbol.Function(ident, body)

    def parseBlock(self, tokens):
        # return a list of statements.  If the block begins with a brace "{"
        # read statements until "}".  Otherise parse a single statement and
        # return it in a list

        tok = tokens[-1]

        if isinstance(tok, token.OpenBrace):
            block = self.parseCompoundStatement(tokens)
        else:
            block = self.parseStatement(tokens)

        return block

    def parseCompoundStatement(self, tokens):
        
        tok = tokens.pop()
        if not isinstance(tok, token.OpenBrace):
            raise InvalidStatementError(tok)

        if len(tokens) == 0:
            raise UnmatchedBraceError()

        items = []
        while not isinstance(tokens[-1], token.ClosedBrace):
            item = self.parseBlockItem(tokens)
            items.append(item)
            if len(tokens)==0:
                raise UnmatchedBraceError()
        tokens.pop()    #Remove }

        stmnt = symbol.CompoundS(items)

        return stmnt

    def parseBlockItem(self, tokens):
        tok = tokens[-1]
        if isinstance(tok, token.Int):
            item = self.parseDeclaration(tokens)
        else:
            item = self.parseStatement(tokens)
        return item

    def parseDeclaration(self, tokens):
        
        tok = tokens.pop()
        if not isinstance(tok, token.Int):
            raise InvalidDeclarationError(tok)

        idTok = tokens.pop()
        if not isinstance(idTok, token.Identifier):
            raise InvalidDeclarationError(tok.val)

        if isinstance(tokens[-1], token.Assign):
            tokens.pop()
            expr = self.parseExpression(tokens)     
        else:
            expr = None

        stmnt = symbol.VariableD(idTok, expr)

        endTok = tokens.pop()
        if not isinstance(endTok, token.Semicolon):
            raise MissingSemicolonError(tok)
        
        return stmnt


    def parseStatement(self, tokens):
        tok = tokens[-1]
        #Check this is a return statement
        if isinstance(tok, token.Return):
            tokens.pop()
            expr = self.parseExpression(tokens)
            stmnt = symbol.ReturnS(expr)

            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise MissingSemicolonError(tok.val)
        #Maybe a conditional
        elif isinstance(tok, token.If):
            stmnt = self.parseConditionalStmnt(tokens)
        #Or a compound?
        elif isinstance(tok, token.OpenBrace):
            stmnt = self.parseCompoundStatement(tokens)
        #Try loop stuff!
        elif isinstance(tok, token.For):
            stmnt = self.parseForStatement(tokens)
        elif isinstance(tok, token.While):
            stmnt = self.parseWhileStatement(tokens)
        elif isinstance(tok, token.Do):
            stmnt = self.parseDoStatement(tokens)
        elif isinstance(tok, token.Break):
            stmnt = self.parseBreakStatement(tokens)
        elif isinstance(tok, token.Continue):
            stmnt = self.parseContinueStatement(tokens)
        elif isinstance(tok, token.Semicolon):
            stmnt = self.parseNullStatement(tokens)
        #Try just an expression
        else:
            expr = self.parseExpression(tokens)
            stmnt = symbol.ExpressionS(expr)

            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise MissingSemicolonError(tok.val)

        return stmnt

    def parseConditionalStmnt(self, tokens):

        tok = tokens.pop()
        if not isinstance(tok, token.If):
            raise InvalidStatementError(tok)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParentheses):
            raise ExpectedParenthesesError(tok)
        
        cond = self.parseExpression(tokens)
        
        tok = tokens.pop()
        if not isinstance(tok, token.ClosedParentheses):
            raise UnmatchedParenthesesError(tok)
        
        stmntTrue = self.parseStatement(tokens)

        if len(tokens) > 0 and isinstance(tokens[-1], token.Else):
            tokens.pop()
            stmntFalse = self.parseStatement(tokens)
        else:
            stmntFalse = None
            
        stmnt = symbol.ConditionalS(cond, stmntTrue, stmntFalse)

        return stmnt

    def parseNullStatement(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.Semicolon):
            raise MissingSemicolonError(tok)
        return symbol.ExpressionS(None)

    def parseBreakStatement(self, tokens):
        if len(tokens) < 2:
            raise InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.Break):
            raise InvalidStatementError(tok)
        if not isinstance(tok2, token.Semicolon):
            raise MissingSemicolonError(tok)
        return symbol.BreakS()

    def parseContinueStatement(self, tokens):
        if len(tokens) < 2:
            raise InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.Continue):
            raise InvalidStatementError(tok)
        if not isinstance(tok2, token.Semicolon):
            raise MissingSemicolonError(tok)
        return symbol.ContinueS()

    def parseWhileStatement(self, tokens):
        if len(tokens) < 3:
            raise InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.While):
            raise InvalidStatementError(tok1)
        if not isinstance(tok2, token.OpenParentheses):
            raise ExpectedParenthesesError(tok2)
        
        cond = self.parseExpression(tokens)

        if len(tokens) < 2:
            raise InvalidStatementError(tokens[-1])

        tok3 = tokens.pop()
        if not isinstance(tok3, token.ClosedParentheses):
            raise UnmatchedParenthesesError(tok3)

        body = self.parseStatement(tokens)

        stmnt = symbol.WhileS(cond, body)

        return stmnt

    def parseDoStatement(self, tokens):
        if len(tokens) < 2:
            raise InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        if not isinstance(tok1, token.Do):
            raise InvalidStatementError(tok1)
        
        body = self.parseStatement(tokens)

        if len(tokens) < 3:
            raise InvalidStatementError(tokens[-1])
        
        tok2 = tokens.pop()
        tok3 = tokens.pop()
        if not isinstance(tok2, token.While):
            raise InvalidStatementError(tok2)
        if not isinstance(tok3, token.OpenParentheses):
            raise ExpectedParenthesesError(tok3)

        cond = self.parseExpression(tokens)

        if len(tokens) < 2:
            raise InvalidStatementError(tokens[-1])
        
        tok4 = tokens.pop()
        tok5 = tokens.pop()
        if not isinstance(tok4, token.ClosedParentheses):
            raise UnmatchedParenthesesError(tok4)
        if not isinstance(tok5, token.Semicolon):
            raise MissingSemicolonError(tok5)

        stmnt = symbol.DoS(cond, body)

        return stmnt
    
    def parseForStatement(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.For):
            raise InvalidStatementError(tok)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParentheses):
            raise ExpectedParenthesesError(tok)

        tok = tokens[-1]

        if isinstance(tok, token.Int):
            init = self.parseDeclaration(tokens)
        elif isinstance(tok, token.Semicolon):
            tokens.pop()
            init = None
        else:
            init = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise MissingSemicolonError(tok)

        tok = tokens[-1]
        if isinstance(tok, token.Semicolon):
            tokens.pop()
            cond = symbol.ConstantE(token.IntC("1"))
        else:
            cond = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise MissingSemicolonError(tok)
        
        tok = tokens[-1]
        if isinstance(tok, token.ClosedParentheses):
            tokens.pop()
            post = None
        else:
            post = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.ClosedParentheses):
                raise UnmatchedParenthesesError(tok)

        body = self.parseStatement(tokens)

        stmnt = symbol.ForS(init, cond, post, body)

        return stmnt

    def parseExpression(self, tokens):
        expr = self.parseAssignExpr(tokens)
        return expr

    def parseAssignExpr(self, tokens):

        expr = None

        #Check if assignmentExpr
        if len(tokens) >= 3 and isinstance(tokens[-1],token.Identifier)\
                and isinstance(tokens[-2], token.AssignmentOp):
            tokId = tokens.pop()
            tokOp = tokens.pop()
            expr = self.parseExpression(tokens)
            expr = symbol.AssignE(tokId, tokOp, expr)
        
        #If not, try the rest
        if expr is None:
            expr = self.parseConditionalExpr(tokens)
        return expr

    def parseConditionalExpr(self, tokens):

        expr = self.parseBinOp(tokens, self.binOpOrder)

        if len(tokens)>0 and isinstance(tokens[-1], token.TernaryA):
            tokens.pop()
            exprTrue = self.parseExpression(tokens)

            tok = tokens.pop()
            if not isinstance(tok, token.TernaryB):
                raise IncompleteConditionalExpressionError(tok)

            exprFalse = self.parseConditionalExpr(tokens)

            expr = symbol.ConditionalE(expr, exprTrue, exprFalse)

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


