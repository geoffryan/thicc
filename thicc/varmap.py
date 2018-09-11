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
        self.size = 0
        if superMap is not None:
            self.superMap = superMap
            self.stackIndex = superMap.stackIndex
        else:
            self.superMap = None
            self.stackIndex = -word
    
    def add(self, tok, size=8):
        if not isinstance(tok, token.Identifier):
            raise InvalidIdentifierError(tok.val)
        name = tok.val
        if name in self.map.keys():
            raise DuplicateIdentifierError(tok.val)
        self.map[name] = self.stackIndex
        self.stackIndex -= size
        self.size += size

    def getOffset(self, tok):
        try:
            offset = self.map[tok.val]
        except KeyError:
            if self.superMap is not None:
                offset = self.superMap.getOffset(tok)
            else:
                raise UnknownIdentifierError(tok.val)

        return offset

    def getDepth(self):
        if self.superMap is None:
            return 0
        else:
            return self.superMap.getDepth() + 1

    def __str__(self):
        if self.superMap is None:
            out = ""
        else:
            out = self.superMap.__str__()
        space = 4*" "
        level = self.getDepth()
        buf0 = level * space
        buf1 = (level+1) * space
        out += buf0 + "vmap (size={0:d}, stackIndex={1:d})\n".format(
                        self.size, self.stackIndex)
        for key in self.map.keys():
            out += buf1 + "{0:s}: {1:d}\n".format(key, self.map[key])

        return out
        
