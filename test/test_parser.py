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
        ast = parser.parseBlockItem(toks[::-1])
        self.assertEqual(ast, ast0)

    def compareFunction(self, toks, ast0):
        parser = thicc.parser.Parser()
        ast = parser.parseFunctionDec(toks[::-1])
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

    def test_orderOfOperations(self):
        # 5 || 10 && 5 == 10 >= 5 << 10 + 5 * -10
        t5 = token.IntC("5")
        s5 = symbol.ConstantE(t5)
        t10 = token.IntC("10")
        s10 = symbol.ConstantE(t10)
        ta = token.Identifier("a")
        sa = symbol.VarRefE(ta)
        toks = [t5, token.Or(), t10, token.And(), t5, token.Equal(), t10,
                token.GreaterThanEqual(), t5, token.BitShiftL(), t10,
                token.Add(), t5, token.Mult(), token.Neg(), t10]
        sym = symbol.BinaryOpE(token.Or(), s5,
                symbol.BinaryOpE(token.And(), s10,
                symbol.BinaryOpE(token.Equal(), s5,
                symbol.BinaryOpE(token.GreaterThanEqual(), s10,
                symbol.BinaryOpE(token.BitShiftL(), s5,
                symbol.BinaryOpE(token.Add(), s10,
                symbol.BinaryOpE(token.Mult(), s5,
                symbol.UnaryOpE(token.Neg(), s10))))))))
        self.compareExpression(toks, sym)

        # -5 % 10 - 5 >> 10 < 5 != 10 && 5 || 10
        toks = [token.Neg(), t5, token.Mod(), t10, token.Neg(), t5, 
                token.BitShiftR(), t10, token.LessThan(), t5, 
                token.NotEqual(), t10, token.And(), t5, token.Or(), t10]
        sym = symbol.BinaryOpE(token.Or(),
                symbol.BinaryOpE(token.And(),
                symbol.BinaryOpE(token.NotEqual(), 
                symbol.BinaryOpE(token.LessThan(),
                symbol.BinaryOpE(token.BitShiftR(),
                symbol.BinaryOpE(token.Neg(), 
                symbol.BinaryOpE(token.Mod(),
                symbol.UnaryOpE(token.Neg(), s5), s10), s5), s10), s5), s10),
                    s5), s10)
        self.compareExpression(toks, sym)

        # 5 - 10 + 5
        toks = [t5, token.Neg(), t10, token.Add(), t5]
        sym = symbol.BinaryOpE(token.Add(), 
                symbol.BinaryOpE(token.Neg(), s5, s10), s5)
        self.compareExpression(toks, sym)

        # 5 + ++a
        toks = [t5, token.Add(), token.Increment(), ta]
        sym = symbol.BinaryOpE(token.Add(),
                s5, symbol.IncrementPreE(token.Increment(), sa))
        self.compareExpression(toks, sym)

        # 5 + a++
        toks = [t5, token.Add(), ta, token.Increment()]
        sym = symbol.BinaryOpE(token.Add(),
                s5, symbol.IncrementPostE(token.Increment(), sa))
        self.compareExpression(toks, sym)

        # a-- - 5
        toks = [ta, token.Decrement(), token.Neg(), t5]
        sym = symbol.BinaryOpE(token.Neg(),
                symbol.IncrementPostE(token.Decrement(), sa), s5)
        self.compareExpression(toks, sym)


    def test_assignment(self):

        # y
        toks = [token.Identifier("y")]
        sym = symbol.VarRefE(token.Identifier("y"))
        self.compareExpression(toks, sym)

        # a = 42
        toks = [token.Identifier("a"), token.Assign(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.Assign(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a += 42
        toks = [token.Identifier("a"), token.AssignAdd(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignAdd(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a -= 42
        toks = [token.Identifier("a"), token.AssignSub(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignSub(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a *= 42
        toks = [token.Identifier("a"), token.AssignMult(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignMult(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a /= 42
        toks = [token.Identifier("a"), token.AssignDiv(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignDiv(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a %= 42
        toks = [token.Identifier("a"), token.AssignMod(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignMod(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a <<= 42
        toks = [token.Identifier("a"), token.AssignBShiftL(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignBShiftL(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a >>= 42
        toks = [token.Identifier("a"), token.AssignBShiftR(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignBShiftR(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a &= 42
        toks = [token.Identifier("a"), token.AssignBAnd(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignBAnd(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a |= 42
        toks = [token.Identifier("a"), token.AssignBOr(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignBOr(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a ^= 42
        toks = [token.Identifier("a"), token.AssignBXor(), token.IntC("42")]
        sym = symbol.AssignE(token.Identifier("a"), token.AssignBXor(), 
                                symbol.ConstantE(token.IntC("42")))
        self.compareExpression(toks, sym)

        # a++
        toks = [token.Identifier("a"), token.Increment()]
        sym = symbol.IncrementPostE(token.Increment(),
                        symbol.VarRefE(token.Identifier("a")))
        self.compareExpression(toks, sym)
    
        # --a
        toks = [token.Decrement(), token.Identifier("a")]
        sym = symbol.IncrementPreE(token.Decrement(),
                        symbol.VarRefE(token.Identifier("a")))
        self.compareExpression(toks, sym)
    
        # y;
        toks = [token.Identifier("y"), token.Semicolon()]
        sym = symbol.ExpressionS(symbol.VarRefE(token.Identifier("y")))
        self.compareStatement(toks, sym)

        # int x;
        toks = [token.Int(), token.Identifier("x"), token.Semicolon()]
        sym = symbol.VariableD(token.Identifier("x"))
        self.compareStatement(toks, sym)

        # int a = 33;
        toks = [token.Int(), token.Identifier("a"), token.Assign(),
                token.IntC("33"), token.Semicolon()]
        sym = symbol.VariableD(token.Identifier("a"), 
                symbol.ConstantE(token.IntC("33")))
        self.compareStatement(toks, sym)

    def test_conditional(self):
        toks = [token.If(), token.OpenParentheses(), token.Identifier("a"), 
                token.ClosedParentheses(), token.Return(), token.IntC("5"),
                token.Semicolon()]
        sym = symbol.ConditionalS(symbol.VarRefE(token.Identifier("a")),
                symbol.ReturnS(symbol.ConstantE(token.IntC("5"))))
        self.compareStatement(toks, sym)

        toks = [token.If(), token.OpenParentheses(), token.Identifier("a"), 
                token.ClosedParentheses(), token.Return(), token.IntC("5"),
                token.Semicolon(), token.Else(), token.Return(), 
                token.IntC("4"), token.Semicolon()]
        sym = symbol.ConditionalS(symbol.VarRefE(token.Identifier("a")),
                symbol.ReturnS(symbol.ConstantE(token.IntC("5"))),
                symbol.ReturnS(symbol.ConstantE(token.IntC("4"))))
        self.compareStatement(toks, sym)

        toks = [token.Identifier("a"), token.QuestionMark(), 
                token.Identifier("b"), token.Colon(), token.Identifier("c")]
        sym = symbol.ConditionalE(symbol.VarRefE(token.Identifier("a")),
                                    symbol.VarRefE(token.Identifier("b")),
                                    symbol.VarRefE(token.Identifier("c")))
        self.compareExpression(toks, sym)

        ta = token.Identifier("a")
        tb = token.Identifier("b")
        tc = token.Identifier("c")
        td = token.Identifier("d")
        te = token.Identifier("e")
        tf = token.Identifier("f")
        tg = token.Identifier("g")
        sa = symbol.VarRefE(ta)
        sb = symbol.VarRefE(tb)
        sc = symbol.VarRefE(tc)
        sd = symbol.VarRefE(td)
        se = symbol.VarRefE(te)
        sf = symbol.VarRefE(tf)
        sg = symbol.VarRefE(tg)

        toks = [ta, token.Or(), tb, token.QuestionMark(), 
                tc, token.AssignAdd(), td, token.Colon(),
                te, token.QuestionMark(), tf, token.Colon(), tg]
        sym = symbol.ConditionalE(
                symbol.BinaryOpE(token.Or(), sa, sb),
                symbol.AssignE(sc.id, token.AssignAdd(), sd),
                symbol.ConditionalE(se, sf, sg))
        self.compareExpression(toks, sym)

    def test_statement(self):

        toks = [token.Return(), token.IntC("36"), token.Semicolon()]
        sym36 = symbol.ConstantE(token.IntC("36"))
        sym = symbol.ReturnS(sym36)
        self.compareStatement(toks, sym)

    def test_function(self):

        toks = [token.Int(), token.Identifier("foo"), token.OpenParentheses(),
                token.ClosedParentheses(), token.OpenBrace(), token.Return(),
                token.IntC("88"), token.Semicolon(), token.ClosedBrace()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.FunctionD(tokFoo,None, 
                                symbol.CompoundS([symbol.ReturnS(symbol.ConstantE(tok88))]))

        self.compareFunction(toks, sym)

        toks = [token.Int(), token.Identifier("foo"), token.OpenParentheses(),
                token.ClosedParentheses(), token.OpenBrace(), 
                
                token.Int(), token.Identifier("b"), token.Assign(),
                token.IntC("56"),token.Semicolon(),
                
                token.Return(), token.Identifier("b"), token.Semicolon(), 
                token.ClosedBrace()]
        tokFoo = token.Identifier("foo")
        tok56 = token.IntC("56")
        tokb = token.Identifier("b")
        sym = symbol.FunctionD(tokFoo, None,
            symbol.CompoundS([
                symbol.VariableD(tokb, symbol.ConstantE(tok56)),
                symbol.ReturnS(symbol.VarRefE(tokb))]))

        self.compareFunction(toks, sym)

    def test_program(self):

        toks = [token.Int(), token.Identifier("foo"), token.OpenParentheses(),
                token.ClosedParentheses(), token.OpenBrace(), token.Return(),
                token.IntC("88"), token.Semicolon(), token.ClosedBrace()]
        tokFoo = token.Identifier("foo")
        tok88 = token.IntC("88")
        sym = symbol.Program(
                [symbol.FunctionD(tokFoo, None,
                    symbol.CompoundS(
                        [symbol.ReturnS(symbol.ConstantE(tok88))]))])

        self.compareProgram(toks, sym)


if __name__ == "__main__":
    unittest.main()
