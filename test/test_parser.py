import unittest
import thicc.token as token
import thicc.symbol as symbol
import thicc.parser

class TestParser(unittest.TestCase):

    def compareExpression(self, toks, ast0):
        parser = thicc.parser.Parser()
        ast = parser.parseExpression(toks[::-1])
        self.assertEqual(ast, ast0)

    def compareStatement(self, toks, ast0):
        parser = thicc.parser.Parser()
        ast = parser.parseStatement(toks[::-1])
        self.assertEqual(ast, ast0)

    def compareFunction(self, toks, ast0):
        parser = thicc.parser.Parser()
        ast = parser.parseFunction(toks[::-1])
        self.assertEqual(ast, ast0)

    def compareProgram(self, toks, ast0):
        parser = thicc.parser.Parser()
        ast = parser.parseProgram(toks[::-1])
        self.assertEqual(ast, ast0)

    def test_expression(self):

        toks = [token.IntC("5")]
        sym5 = symbol.ConstantE(token.IntC("5"))
        self.compareExpression(toks, sym5)

        toks = [token.Neg(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.Neg(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.Not(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.Not(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.Complement(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.Complement(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.Complement(), token.Neg(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.Complement(), 
                                symbol.UnaryOpE(token.Neg(), sym5))
        self.compareExpression(toks, sym)

    def test_binaryOp_add(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.Neg(), sym5)

        # 5+10
        toks = [token.IntC("5"), token.Add(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Add(), sym5, sym10)
        self.compareExpression(toks, sym)

        # 5-10
        toks = [token.IntC("5"), token.Neg(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Neg(), sym5, sym10)
        self.compareExpression(toks, sym)

        # -5+10
        toks = [token.Neg(), token.IntC("5"), token.Add(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Add(), symm5, sym10)
        self.compareExpression(toks, sym)

        # 10+-5
        toks = [token.IntC("10"), token.Add(), token.Neg(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.Add(), sym10, symm5)
        self.compareExpression(toks, sym)
        
        # 5-10+10
        toks = [token.IntC("5"), token.Neg(), token.IntC("10"),
                token.Add(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Add(), 
                            symbol.BinaryOpE(token.Neg(), sym5, sym10), sym10)
        self.compareExpression(toks, sym)


    def test_binaryOp_mult(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.Neg(), sym5)

        # 5*10
        toks = [token.IntC("5"), token.Mult(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Mult(), sym5, sym10)
        self.compareExpression(toks, sym)

        # 5/10
        toks = [token.IntC("5"), token.Div(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Div(), sym5, sym10)
        self.compareExpression(toks, sym)

        # -5*10
        toks = [token.Neg(), token.IntC("5"), token.Mult(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Mult(), symm5, sym10)
        self.compareExpression(toks, sym)

        # 10*-5
        toks = [token.IntC("10"), token.Mult(), token.Neg(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.Mult(), sym10, symm5)
        self.compareExpression(toks, sym)
        
        # 5/10*10
        toks = [token.IntC("5"), token.Div(), token.IntC("10"), 
                    token.Mult(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.Mult(), 
                            symbol.BinaryOpE(token.Div(), sym5, sym10), sym10)
        self.compareExpression(toks, sym)

    def test_parentheses(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.Neg(), sym5)

        # (5)
        toks = [token.OpenParentheses(), token.IntC("5"), 
                    token.ClosedParentheses()]
        sym = sym5
        self.compareExpression(toks, sym)

        # ((5))
        toks = [token.OpenParentheses(), token.OpenParentheses(), 
                token.IntC("5"), token.ClosedParentheses(), 
                token.ClosedParentheses()]
        sym = sym5
        self.compareExpression(toks, sym)

        # -(5)
        toks = [token.Neg(), token.OpenParentheses(), token.IntC("5"), 
                    token.ClosedParentheses()]
        sym = symbol.UnaryOpE(token.Neg(), sym5)
        self.compareExpression(toks, sym)

        # (-5)
        toks = [token.OpenParentheses(), token.Neg(), token.IntC("5"), 
                    token.ClosedParentheses()]
        sym = symbol.UnaryOpE(token.Neg(), sym5)
        self.compareExpression(toks, sym)

        # (10)*5
        toks = [token.OpenParentheses(), token.IntC("10"), 
                token.ClosedParentheses(), token.Mult(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.Mult(), sym10, sym5)
        self.compareExpression(toks, sym)

        # 5*(10-5)
        toks = [token.IntC("5"), token.Mult(), token.OpenParentheses(), 
                token.IntC("10"), token.Neg(), token.IntC("5"),
                token.ClosedParentheses()]
        sym = symbol.BinaryOpE(token.Mult(), sym5, 
                symbol.BinaryOpE(token.Neg(), sym10, sym5))
        self.compareExpression(toks, sym)

    def test_statement(self):

        toks = [token.ReturnK(), token.IntC("36"), token.Semicolon()]
        sym36 = symbol.ConstantE(token.IntC("36"))
        sym = symbol.ReturnS(sym36)

        self.compareStatement(toks, sym)

    def test_function(self):

        toks = [token.IntK(), token.Identifier("foo"), token.OpenParentheses(),
                token.ClosedParentheses(), token.OpenBrace(), token.ReturnK(),
                token.IntC("88"), token.Semicolon(), token.ClosedBrace()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.Function(tokFoo, symbol.ReturnS(symbol.ConstantE(tok88)))

        self.compareFunction(toks, sym)

    def test_program(self):

        toks = [token.IntK(), token.Identifier("foo"), token.OpenParentheses(),
                token.ClosedParentheses(), token.OpenBrace(), token.ReturnK(),
                token.IntC("88"), token.Semicolon(), token.ClosedBrace()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.Program(
                symbol.Function(tokFoo, 
                    symbol.ReturnS(symbol.ConstantE(tok88))))

        self.compareProgram(toks, sym)


if __name__ == "__main__":
    unittest.main()
