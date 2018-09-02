from . import token
from . import exception

class VariableMapError(exception.ThiccError):
    pass

class UnknownIdentifierError(VariableMapError):
    def __init__(self, expr, message="Variable identifier unknown"):
        self.expression = expr
        self.message = message

class DuplicateIdentifierError(VariableMapError):
    def __init__(self, expr, 
            message="Variable identifier already exists in scope."):
        self.expression = expr
        self.message = message

class InvalidIdentifierError(VariableMapError):
    def __init__(self, expr, 
            message="Variable name not a valid identifier"):
        self.expression = expr
        self.message = message


class VarMap():
    def __init__(self, superMap=None, word=8):
        self.map = {}
        self.superMap = superMap
        self.stackIndex = -word
    
    def add(self, tok, size=8):
        if not isinstance(tok, token.Identifier):
            raise InvalidIdentifierError(tok.val)
        name = tok.val
        if name in self.map.keys():
            raise DuplicateIdentifierError(tok.val)
        self.map[name] = self.stackIndex
        self.stackIndex -= size

    def getOffset(self, tok):
        try:
            offset = self.map[tok.val]
        except KeyError:
            if self.superMap is not None:
                offset = self.superMap.getOffset(tok)
            else:
                raise UnknownIdentifierError(tok.val)
        return offset





