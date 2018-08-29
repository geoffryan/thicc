import unittest
import thicc.lexer
import thicc.token as token

class TestLexer(unittest.TestCase):

    def compareSingleToken(self, txt, cls):
        lexer = thicc.lexer.Lexer()
        toks = lexer.tokenize(txt)
        self.assertEqual(len(toks), 1)
        self.assertIsInstance(toks[0], cls)
        if isinstance(toks[0], token.Identifier)\
            or isinstance(toks[0], token.Constant)\
            or isinstance(toks[0], token.StringLtrl):
            self.assertEqual(toks[0].val, txt)

    def compareMultiToken(self, txt, cls, val):
        lexer = thicc.lexer.Lexer()
        toks = lexer.tokenize(txt)
        self.assertEqual(len(toks), len(cls))
        for i,tok in enumerate(toks):
            self.assertIsInstance(tok, cls[i])
            if isinstance(tok, token.Identifier)\
                or isinstance(tok, token.Constant)\
                or isinstance(tok, token.StringLtrl):
                self.assertEqual(tok.val, val[i])

    def compareException(self, txt, e):
        lexer = thicc.lexer.Lexer()
        self.assertRaises(e, lexer.tokenize, txt)

    def test_punct_single(self):
        self.compareSingleToken(';', token.SemicolonP)
        self.compareSingleToken('{', token.OpenBraceP)
        self.compareSingleToken('}', token.ClosedBraceP)
        self.compareSingleToken('(', token.OpenParenthesesP)
        self.compareSingleToken(')', token.ClosedParenthesesP)

    def test_keywork_single(self):
        self.compareSingleToken('return', token.ReturnK)
        self.compareSingleToken('int', token.IntK)

    def test_const_single(self):
        self.compareSingleToken('0', token.IntC)
        self.compareSingleToken('3', token.IntC)
        self.compareSingleToken('42', token.IntC)
        self.compareSingleToken('8463', token.IntC)
    
    def test_ident_single(self):
        self.compareSingleToken('x', token.Identifier)
        self.compareSingleToken('abc', token.Identifier)
        self.compareSingleToken('DEF', token.Identifier)
        self.compareSingleToken('x2', token.Identifier)

    def test_whitespace(self):
        cls = [token.Identifier]
        val = ["abc"]
        txt = "  abc"
        self.compareMultiToken(txt, cls, val)
        txt = "abc  "
        self.compareMultiToken(txt, cls, val)
        txt = "\tabc"
        self.compareMultiToken(txt, cls, val)
        txt = "abc\t"
        self.compareMultiToken(txt, cls, val)

    def test_exception(self):
        self.compareException("2x", thicc.lexer.LexInvalidLiteralError)

    def test_multi(self):
        txt = "hex{"
        val = ["hex", ""]
        cls = [token.Identifier, token.OpenBraceP]
        self.compareMultiToken(txt, cls, val)
        txt = "( duck"
        val = ["", "duck"]
        cls = [token.OpenParenthesesP, token.Identifier]
        self.compareMultiToken(txt, cls, val)
        txt = "return;"
        val = ["", ""]
        cls = [token.ReturnK, token.SemicolonP]
        self.compareMultiToken(txt, cls, val)
        txt = "\tint\t7"
        val = ["", "7"]
        cls = [token.IntK, token.IntC]
        self.compareMultiToken(txt, cls, val)
        txt = "int func(int a)\n{\n\treturn 365;\n}\n"
        val = ["","func","","","a","","","","365","",""]
        cls = [token.IntK, token.Identifier, token.OpenParenthesesP,
                token.IntK, token.Identifier, token.ClosedParenthesesP,
                token.OpenBraceP, token.ReturnK, token.IntC, token.SemicolonP,
                token.ClosedBraceP]
        self.compareMultiToken(txt, cls, val)


if __name__ == "__main__":
    unittest.main()
