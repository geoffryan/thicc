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

        toks = [token.NegP(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.NegP(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.NotP(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.NotP(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.ComplementP(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.ComplementP(), sym5)
        self.compareExpression(toks, sym)

        toks = [token.ComplementP(), token.NegP(), token.IntC("5")]
        sym = symbol.UnaryOpE(token.ComplementP(), 
                                symbol.UnaryOpE(token.NegP(), sym5))
        self.compareExpression(toks, sym)

    def test_binaryOp_add(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.NegP(), sym5)

        # 5+10
        toks = [token.IntC("5"), token.AddP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.AddP(), sym5, sym10)
        self.compareExpression(toks, sym)

        # 5-10
        toks = [token.IntC("5"), token.NegP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.NegP(), sym5, sym10)
        self.compareExpression(toks, sym)

        # -5+10
        toks = [token.NegP(), token.IntC("5"), token.AddP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.AddP(), symm5, sym10)
        self.compareExpression(toks, sym)

        # 10+-5
        toks = [token.IntC("10"), token.AddP(), token.NegP(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.AddP(), sym10, symm5)
        self.compareExpression(toks, sym)
        
        # 5-10+10
        toks = [token.IntC("5"), token.NegP(), token.IntC("10"),
                token.AddP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.AddP(), 
                            symbol.BinaryOpE(token.NegP(), sym5, sym10), sym10)
        self.compareExpression(toks, sym)


    def test_binaryOp_mult(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.NegP(), sym5)

        # 5*10
        toks = [token.IntC("5"), token.MultP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.MultP(), sym5, sym10)
        self.compareExpression(toks, sym)

        # 5/10
        toks = [token.IntC("5"), token.DivP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.DivP(), sym5, sym10)
        self.compareExpression(toks, sym)

        # -5*10
        toks = [token.NegP(), token.IntC("5"), token.MultP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.MultP(), symm5, sym10)
        self.compareExpression(toks, sym)

        # 10*-5
        toks = [token.IntC("10"), token.MultP(), token.NegP(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.MultP(), sym10, symm5)
        self.compareExpression(toks, sym)
        
        # 5/10*10
        toks = [token.IntC("5"), token.DivP(), token.IntC("10"), 
                    token.MultP(), token.IntC("10")]
        sym = symbol.BinaryOpE(token.MultP(), 
                            symbol.BinaryOpE(token.DivP(), sym5, sym10), sym10)
        self.compareExpression(toks, sym)

    def test_parentheses(self):

        sym5 = symbol.ConstantE(token.IntC("5"))
        sym10 = symbol.ConstantE(token.IntC("10"))
        symm5 = symbol.UnaryOpE(token.NegP(), sym5)

        # (5)
        toks = [token.OpenParenthesesP(), token.IntC("5"), 
                    token.ClosedParenthesesP()]
        sym = sym5
        self.compareExpression(toks, sym)

        # ((5))
        toks = [token.OpenParenthesesP(), token.OpenParenthesesP(), 
                token.IntC("5"), token.ClosedParenthesesP(), 
                token.ClosedParenthesesP()]
        sym = sym5
        self.compareExpression(toks, sym)

        # -(5)
        toks = [token.NegP(), token.OpenParenthesesP(), token.IntC("5"), 
                    token.ClosedParenthesesP()]
        sym = symbol.UnaryOpE(token.NegP(), sym5)
        self.compareExpression(toks, sym)

        # (-5)
        toks = [token.OpenParenthesesP(), token.NegP(), token.IntC("5"), 
                    token.ClosedParenthesesP()]
        sym = symbol.UnaryOpE(token.NegP(), sym5)
        self.compareExpression(toks, sym)

        # (10)*5
        toks = [token.OpenParenthesesP(), token.IntC("10"), 
                token.ClosedParenthesesP(), token.MultP(), token.IntC("5")]
        sym = symbol.BinaryOpE(token.MultP(), sym10, sym5)
        self.compareExpression(toks, sym)

        # 5*(10-5)
        toks = [token.IntC("5"), token.MultP(), token.OpenParenthesesP(), 
                token.IntC("10"), token.NegP(), token.IntC("5"),
                token.ClosedParenthesesP()]
        sym = symbol.BinaryOpE(token.MultP(), sym5, 
                symbol.BinaryOpE(token.NegP(), sym10, sym5))
        self.compareExpression(toks, sym)

    def test_statement(self):

        toks = [token.ReturnK(), token.IntC("36"), token.SemicolonP()]
        sym36 = symbol.ConstantE(token.IntC("36"))
        sym = symbol.ReturnS(sym36)

        self.compareStatement(toks, sym)

    def test_function(self):

        toks = [token.IntK(), token.Identifier("foo"), token.OpenParenthesesP(),
                token.ClosedParenthesesP(), token.OpenBraceP(), token.ReturnK(),
                token.IntC("88"), token.SemicolonP(), token.ClosedBraceP()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.Function(tokFoo, symbol.ReturnS(symbol.ConstantE(tok88)))

        self.compareFunction(toks, sym)

    def test_program(self):

        toks = [token.IntK(), token.Identifier("foo"), token.OpenParenthesesP(),
                token.ClosedParenthesesP(), token.OpenBraceP(), token.ReturnK(),
                token.IntC("88"), token.SemicolonP(), token.ClosedBraceP()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.Program(
                symbol.Function(tokFoo, 
                    symbol.ReturnS(symbol.ConstantE(tok88))))

        self.compareProgram(toks, sym)


if __name__ == "__main__":
    unittest.main()
