from . import lexer
from . import parser
from . import generator

class Compiler():

    def __init__(self, genType="m64"):
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        if genType == "m32":
            self.generator = generator.Generator_x86()
        else:
            self.generator = generator.Generator_x86_64()

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

def compileC(text, genType="m64"):
    compiler = Compiler(genType)
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
