from . import lexer
from . import parser
from . import generator

class Compiler():

    def __init__(self):
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        self.generator = generator.Generator()

    def compileC(self, text):
        toks = self.lexer.tokenize(text)
        ast = self.parser.parse(toks)
        code = self.generator.generate(ast)
        return code

    def parse(self, text):
        toks = self.lexer.tokenize(text)
        ast = self.parser.parse(toks)
        return ast

    def lex(self, text):
        toks = self.lexer.tokenize(text)
        return toks

def compileC(text):
    compiler = Compiler()
    code = compiler.compileC(text)
    return code

def parse(text):
    compiler = Compiler()
    ast = compiler.parse(text)
    return code

def lex(text):
    compiler = Compiler()
    tok = compiler.lex(text)
    return code
