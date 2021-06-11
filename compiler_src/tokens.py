from enum import Enum

class TokenType(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMI = "SEMI"
    COLON = "COLON"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    NUMBER = "NUMBER"
    EOF = "EOF"


class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        return 'Token({type}, {value}, lineno={lineno}, column={column})'.format(
            type=self.type,
            value=self.value,
            lineno=self.lineno,
            column=self.column
        )

    __repr__ = __str__