from . import token
from . import symbol
from . import exception

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

        ast.validate()

        return ast

    def parseProgram(self, tokens):

        decs = []
        while len(tokens) > 0:
            decs.append(self.parseDeclaration(tokens))

        prog = symbol.Program(decs)

        return prog

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
            raise symbol.InvalidStatementError(tok)

        if len(tokens) == 0:
            raise symbol.UnmatchedBraceError()

        items = []
        while not isinstance(tokens[-1], token.ClosedBrace):
            item = self.parseBlockItem(tokens)
            items.append(item)
            if len(tokens)==0:
                raise symbol.UnmatchedBraceError()
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
        
        typetok = tokens[-1]
        if not isinstance(typetok, token.Int):
            raise symbol.InvalidDeclarationError(typetok)

        idTok = tokens[-2]
        if not isinstance(idTok, token.Identifier):
            raise symbol.InvalidDeclarationError(tok.val)

        tok = tokens[-3]
        if isinstance(tok, token.OpenParentheses):
            dec = self.parseFunctionDec(tokens)
        elif isinstance(tok, token.Assign) or isinstance(tok, token.Semicolon):
            dec = self.parseVariableDec(tokens)
        else:
            raise symbol.MissingSemicolonError(tok)
        
        return dec

    def parseVariableDec(self, tokens):
        
        typetok = tokens.pop()
        if not isinstance(typetok, token.Int):
            raise symbol.InvalidDeclarationError(tok)

        idTok = tokens.pop()
        if not isinstance(idTok, token.Identifier):
            raise symbol.InvalidDeclarationError(tok.val)

        tok = tokens[-1]
        if isinstance(tokens[-1], token.Assign):
            tokens.pop()
            expr = self.parseExpression(tokens)     
        else:
            expr = None

        dec = symbol.VariableD(idTok, expr)

        endTok = tokens.pop()
        if not isinstance(endTok, token.Semicolon):
            raise symbol.MissingSemicolonError(tok)
        
        return dec

    def parseFunctionDec(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.Int):
            raise symbol.InvalidFunctionError(tok.val)

        ident = tokens.pop()
        if not isinstance(ident, token.Identifier):
            raise symbol.InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParentheses):
            raise symbol.InvalidFunctionError(tok.val)

        tok = tokens.pop()
        if not isinstance(tok, token.ClosedParentheses):
            raise symbol.InvalidFunctionError(tok.val)

        tok = tokens[-1]
        if isinstance(tok, token.OpenBrace):
            body = self.parseCompoundStatement(tokens)
        elif isinstance(tok, token.Semicolon):
            tokens.pop()
            body = None
        else:
            raise symbol.InvalidFunctionError(tok)

        return symbol.FunctionD(ident, None, body)


    def parseStatement(self, tokens):
        tok = tokens[-1]
        #Check this is a return statement
        if isinstance(tok, token.Return):
            tokens.pop()
            expr = self.parseExpression(tokens)
            stmnt = symbol.ReturnS(expr)

            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise symbol.MissingSemicolonError(tok.val)
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
                raise symbol.MissingSemicolonError(tok.val)

        return stmnt

    def parseConditionalStmnt(self, tokens):

        tok = tokens.pop()
        if not isinstance(tok, token.If):
            raise symbol.InvalidStatementError(tok)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParentheses):
            raise symbol.ExpectedParenthesesError(tok)
        
        cond = self.parseExpression(tokens)
        
        tok = tokens.pop()
        if not isinstance(tok, token.ClosedParentheses):
            raise symbol.UnmatchedParenthesesError(tok)
        
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
            raise symbol.MissingSemicolonError(tok)
        return symbol.ExpressionS(None)

    def parseBreakStatement(self, tokens):
        if len(tokens) < 2:
            raise symbol.InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.Break):
            raise symbol.InvalidStatementError(tok)
        if not isinstance(tok2, token.Semicolon):
            raise symbol.MissingSemicolonError(tok)
        return symbol.BreakS()

    def parseContinueStatement(self, tokens):
        if len(tokens) < 2:
            raise symbol.InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.Continue):
            raise symbol.InvalidStatementError(tok)
        if not isinstance(tok2, token.Semicolon):
            raise symbol.MissingSemicolonError(tok)
        return symbol.ContinueS()

    def parseWhileStatement(self, tokens):
        if len(tokens) < 3:
            raise symbol.InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        tok2 = tokens.pop()
        if not isinstance(tok1, token.While):
            raise symbol.InvalidStatementError(tok1)
        if not isinstance(tok2, token.OpenParentheses):
            raise symbol.ExpectedParenthesesError(tok2)
        
        cond = self.parseExpression(tokens)

        if len(tokens) < 2:
            raise symbol.InvalidStatementError(tokens[-1])

        tok3 = tokens.pop()
        if not isinstance(tok3, token.ClosedParentheses):
            raise symbol.UnmatchedParenthesesError(tok3)

        body = self.parseStatement(tokens)

        stmnt = symbol.WhileS(cond, body)

        return stmnt

    def parseDoStatement(self, tokens):
        if len(tokens) < 2:
            raise symbol.InvalidStatementError(tokens[-1])
        tok1 = tokens.pop()
        if not isinstance(tok1, token.Do):
            raise symbol.InvalidStatementError(tok1)
        
        body = self.parseStatement(tokens)

        if len(tokens) < 3:
            raise symbol.InvalidStatementError(tokens[-1])
        
        tok2 = tokens.pop()
        tok3 = tokens.pop()
        if not isinstance(tok2, token.While):
            raise symbol.InvalidStatementError(tok2)
        if not isinstance(tok3, token.OpenParentheses):
            raise symbol.ExpectedParenthesesError(tok3)

        cond = self.parseExpression(tokens)

        if len(tokens) < 2:
            raise symbol.InvalidStatementError(tokens[-1])
        
        tok4 = tokens.pop()
        tok5 = tokens.pop()
        if not isinstance(tok4, token.ClosedParentheses):
            raise symbol.UnmatchedParenthesesError(tok4)
        if not isinstance(tok5, token.Semicolon):
            raise symbol.MissingSemicolonError(tok5)

        stmnt = symbol.DoS(cond, body)

        return stmnt
    
    def parseForStatement(self, tokens):
        tok = tokens.pop()
        if not isinstance(tok, token.For):
            raise symbol.InvalidStatementError(tok)

        tok = tokens.pop()
        if not isinstance(tok, token.OpenParentheses):
            raise symbol.ExpectedParenthesesError(tok)

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
                raise symbol.MissingSemicolonError(tok)

        tok = tokens[-1]
        if isinstance(tok, token.Semicolon):
            tokens.pop()
            cond = symbol.ConstantE(token.IntC("1"))
        else:
            cond = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.Semicolon):
                raise symbol.MissingSemicolonError(tok)
        
        tok = tokens[-1]
        if isinstance(tok, token.ClosedParentheses):
            tokens.pop()
            post = None
        else:
            post = self.parseExpression(tokens)
            tok = tokens.pop()
            if not isinstance(tok, token.ClosedParentheses):
                raise symbol.UnmatchedParenthesesError(tok)

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
                raise symbol.IncompleteConditionalExpressionError(tok)

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
                raise symbol.UnmatchedParthenthesesError(tok.val)
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
        raise symbol.InvalidExpressionError(tok.val)

    def parseVariable(self, tokens):
        tok = tokens.pop()
        if isinstance(tok, token.Identifier):
            expr = symbol.VarRefE(tok)
        else:
            raise symbol.InvalidVariableRefError(tok.val)
        return expr


