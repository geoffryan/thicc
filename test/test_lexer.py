import unittest
import thicc.lexer

class TestLexer(unittest.TestCase):

    def test_1(self):
        file1 = """\
int main()
{
    return 0;
}"""
        tok1_exp = ['int', 'main', '(', ')', '{', 'return', '0', ';', '}']
        
        lex = thicc.lexer.Lexer()
        tok1 = lex.tokenize(file1)
        self.assertTrue(len(tok1) == len(tok1_exp) and         
                        all([tok1[i].val==tok1_exp[i] 
                                for i in range(len(tok1))]))

if __name__ == "__main__":
    unittest.main()
