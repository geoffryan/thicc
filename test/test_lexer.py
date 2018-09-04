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
        self.compareSingleToken(';', token.Semicolon)
        self.compareSingleToken('{', token.OpenBrace)
        self.compareSingleToken('}', token.ClosedBrace)
        self.compareSingleToken('(', token.OpenParentheses)
        self.compareSingleToken(')', token.ClosedParentheses)
        self.compareSingleToken('!', token.Not)
        self.compareSingleToken('-', token.Neg)
        self.compareSingleToken('~', token.Complement)
        self.compareSingleToken('+', token.Add)
        self.compareSingleToken('*', token.Mult)
        self.compareSingleToken('/', token.Div)
        self.compareSingleToken('%', token.Mod)
        self.compareSingleToken('<<', token.BitShiftL)
        self.compareSingleToken('>>', token.BitShiftR)
        self.compareSingleToken('<', token.LessThan)
        self.compareSingleToken('<=', token.LessThanEqual)
        self.compareSingleToken('>', token.GreaterThan)
        self.compareSingleToken('>=', token.GreaterThanEqual)
        self.compareSingleToken('==', token.Equal)
        self.compareSingleToken('!=', token.NotEqual)
        self.compareSingleToken('&', token.BitAnd)
        self.compareSingleToken('|', token.BitOr)
        self.compareSingleToken('^', token.BitXor)
        self.compareSingleToken('&&', token.And)
        self.compareSingleToken('||', token.Or)
        self.compareSingleToken('=', token.Assign)
        self.compareSingleToken(':', token.TernaryA)
        self.compareSingleToken('?', token.TernaryB)

    def test_keywork_single(self):
        self.compareSingleToken('return', token.Return)
        self.compareSingleToken('int', token.Int)
        self.compareSingleToken('if', token.If)
        self.compareSingleToken('else', token.Else)

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

    def test_assignmentOp(self):
        txt = "a=3"
        cls = [token.Identifier, token.Assign, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a+=3"
        cls = [token.Identifier, token.AssignAdd, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a-=3"
        cls = [token.Identifier, token.AssignSub, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a*=3"
        cls = [token.Identifier, token.AssignMult, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a/=3"
        cls = [token.Identifier, token.AssignDiv, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a%=3"
        cls = [token.Identifier, token.AssignMod, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a<<=3"
        cls = [token.Identifier, token.AssignBShiftL, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a>>=3"
        cls = [token.Identifier, token.AssignBShiftR, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a&=3"
        cls = [token.Identifier, token.AssignBAnd, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a|=3"
        cls = [token.Identifier, token.AssignBOr, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a^=3"
        cls = [token.Identifier, token.AssignBXor, token.IntC]
        val = ["a", "", "3"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "a++"
        cls = [token.Identifier, token.Increment]
        val = ["a", ""]
        self.compareMultiToken(txt, cls, val)
        
        txt = "--a"
        cls = [token.Decrement, token.Identifier]
        val = ["", "a"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "+++a"
        cls = [token.Increment, token.Add, token.Identifier]
        val = ["", "", "a"]
        self.compareMultiToken(txt, cls, val)
        
        txt = "int x = 34;"
        cls = [token.IntK, token.Identifier, token.Assign, token.IntC,
                token.Semicolon]
        val = ["", "x", "", "34", ""]
        self.compareMultiToken(txt, cls, val)

    def test_unaryOp(self):
        txt = "!a"
        cls = [token.Not, token.Identifier]
        val = ["", 'a']
        self.compareMultiToken(txt, cls, val)
        txt = "~ 5"
        cls = [token.Complement, token.IntC]
        val = ["", "5"]
        self.compareMultiToken(txt, cls, val)
        txt = " a-\t4 "
        cls = [token.Identifier, token.Neg, token.IntC]
        val = ["a", "", "4"]
        self.compareMultiToken(txt, cls, val)
        txt = "!!a"
        cls = [token.Not, token.Not, token.Identifier]
        val = ["", "", 'a']
        self.compareMultiToken(txt, cls, val)

    def test_binaryOp(self):
        txt = "1+3"
        cls = [token.IntC, token.Add, token.IntC]
        val = ["1", "", "3"]
        self.compareMultiToken(txt, cls, val)
        txt = " a * b\t"
        cls = [token.Identifier, token.Mult, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "42/x"
        cls = [token.IntC, token.Div, token.Identifier]
        val = ["42", "", "x"]
        self.compareMultiToken(txt, cls, val)
        txt = "a%b"
        cls = [token.Identifier, token.Mod, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a<<b"
        cls = [token.Identifier, token.BitShiftL, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a>>b"
        cls = [token.Identifier, token.BitShiftR, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a<b"
        cls = [token.Identifier, token.LessThan, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a<=b"
        cls = [token.Identifier, token.LessThanEqual, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a>b"
        cls = [token.Identifier, token.GreaterThan, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a>=b"
        cls = [token.Identifier, token.GreaterThanEqual, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a==b"
        cls = [token.Identifier, token.Equal, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a!=b"
        cls = [token.Identifier, token.NotEqual, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a&b"
        cls = [token.Identifier, token.BitAnd, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a|b"
        cls = [token.Identifier, token.BitOr, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a^b"
        cls = [token.Identifier, token.BitXor, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a&&b"
        cls = [token.Identifier, token.And, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)
        txt = "a||b"
        cls = [token.Identifier, token.Or, token.Identifier]
        val = ["a", "", "b"]
        self.compareMultiToken(txt, cls, val)

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
        self.compareException("2x", thicc.lexer.LexInvalidIdentifierError)

    def test_multi(self):
        txt = "hex{"
        val = ["hex", ""]
        cls = [token.Identifier, token.OpenBrace]
        self.compareMultiToken(txt, cls, val)
        txt = "( duck"
        val = ["", "duck"]
        cls = [token.OpenParentheses, token.Identifier]
        self.compareMultiToken(txt, cls, val)
        txt = "return;"
        val = ["", ""]
        cls = [token.ReturnK, token.Semicolon]
        self.compareMultiToken(txt, cls, val)
        txt = "\tint\t7"
        val = ["", "7"]
        cls = [token.IntK, token.IntC]
        self.compareMultiToken(txt, cls, val)
        txt = "int func(int a)\n{\n\treturn -365;\n}\n"
        val = ["","func","","","a","","","","","365","",""]
        cls = [token.IntK, token.Identifier, token.OpenParentheses,
                token.IntK, token.Identifier, token.ClosedParentheses,
                token.OpenBrace, token.ReturnK, token.Neg, token.IntC,
                token.Semicolon, token.ClosedBrace]
        self.compareMultiToken(txt, cls, val)


if __name__ == "__main__":
    unittest.main()
