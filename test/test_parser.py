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
