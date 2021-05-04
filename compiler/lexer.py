from enum import Enum
from .error import *
import re

class TokenType(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMI = "SEMI"
    COLON = "COLON"
    COMMA = "COMMA"
    LAMBDA = "LAMBDA"
    SET = "SET"
    ID = "ID"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    NUMBER = "NUMBER"
    STRING = "STRING"
    EOF = "EOF"

class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
    
    def __str__(self):
        return "Token({type}, {value}, lineno={lineno}, column={column})".format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column
        )   
    
    __repr__ = __str__

class Lexer(object):
    RESERVED_KEYWORDS = {
        'lambda': Token(TokenType.LAMBDA, 'lambda'),
        'set': Token(TokenType.SET, 'set'),
    }


    def __init__(self, text):
        self.text = text
        self.current_char = self.text[0]
        self.lineno = 1
        self.column = 1

    def error(self):
        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
            lexeme=self.current_char,
            lineno=self.lineno,
            column=self.column
        )
        raise LexerError(message=s)

    def _advance(self):
        if self.current_char == "\n":
            self.lineno += 1
            self.column = 1

        self.text = self.text[1:]        

        if len(self.text) < 1:
            self.current_char = None
        else:
            self.current_char = self.text[0]
            self.column += 1

    def get_match(self, pattern):
        result = re.search(pattern, self.text)
        length = result.span()[1] - result.span()[0]
        for i in range(length):
            self._advance()
        return result.group()

    def get_tokens(self):
        tokens = []
        while self.current_char is not None:

            if self.current_char.isspace():
                self.get_match(r'\s*')

            elif self.current_char.isalpha() or self.current_char == "_":
                id = self.get_match(r'[a-zA-Z_]\w*')
                token = self.RESERVED_KEYWORDS.get(id, Token(TokenType.ID, id))
                token.lineno = self.lineno
                token.column = self.column
                tokens.append(token)

            elif self.current_char.isdigit():
                num = self.get_match(r'-?(0|([1-9]\d*))(\.\d+)?((e|E)(\+|-)?\d+)?')
                tokens.append(Token(TokenType.NUMBER, num))
            
            elif self.current_char == '"':
                string = self.get_match(r'".*"')
                tokens.append(Token(TokenType.STRING, string[1:-1], self.lineno, self.column))

            elif self.current_char == "(":
                lparen = self.get_match(r'\(')
                tokens.append(Token(TokenType.LPAREN, lparen, self.lineno, self.column))
            
            elif self.current_char == ")":
                rparen = self.get_match(r'\)')
                tokens.append(Token(TokenType.RPAREN, rparen, self.lineno, self.column))

            elif self.current_char == ";":
                semi = self.get_match(r';')
                tokens.append(Token(TokenType.SEMI, semi, self.lineno, self.column))

            elif self.current_char == ":":
                colon = self.get_match(r':')
                tokens.append(Token(TokenType.COLON, colon, self.lineno, self.column))

            elif self.current_char == ",":
                comma = self.get_match(r',')
                tokens.append(Token(TokenType.COMMA, comma, self.lineno, self.column))

            elif self.current_char == "+":
                plus = self.get_match(r'\+')
                tokens.append(Token(TokenType.PLUS, plus, self.lineno, self.column))

            elif self.current_char == "-":
                minus = self.get_match(r'-')
                tokens.append(Token(TokenType.MINUS, minus, self.lineno, self.column))

            elif self.current_char == "*":
                mul = self.get_match(r'\*')
                tokens.append(Token(TokenType.MUL, mul, self.lineno, self.column))

            elif self.current_char == "/":
                div = self.get_match(r'/')
                tokens.append(Token(TokenType.DIV, div, self.lineno, self.column))

            elif self.current_char == "%":
                mod = self.get_match(r'%')
                tokens.append(Token(TokenType.MOD, mod, self.lineno, self.column))
            
            else:
                self.error()

        tokens.append(Token(TokenType.EOF, None, self.lineno, self.column))
        return tokens