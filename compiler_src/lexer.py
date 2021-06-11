import re
from .tokens import Token, TokenType
from .errors import LexerError

class Lexeme(object):
    def __init__(self, value, lineno, column):
        self.value = value
        self.lineno = lineno
        self.column = column

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.lineno = 1
        self.column = 1

    def error(self):
        m = "Lexer error on '{lexeme}' (at {lineno}:{column})".format(
            lexeme=self.current_char,
            lineno=self.lineno,
            column=self.column,
        )
        raise LexerError(message=m)

    def _advance(self):
        if self.current_char == "\n":
            self.lineno += 1
            self.column = 1
        
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def get_match(self, pattern):
        match = re.search(pattern, self.text)
        res = Lexeme(self.text[match.start():match.end()], self.lineno, self.column)
        match_length = match.end() - match.start()
        for _ in range(0, match_length):
            self._advance()
        return res

    def get_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char.isspace():
                self.get_match(r'\s+')
            
            elif self.current_char.isdigit():
                number = self.get_match(r'-?(0|([1-9]\d*))(\.\d+)?((e|E)(\+|-)?\d+)?')
                tokens.append(Token(TokenType.NUMBER, number.value, number.lineno, number.column))

            elif self.current_char == "(":
                lparen = self.get_match(r'\(')
                tokens.append(Token(TokenType.LPAREN, lparen.value, lparen.lineno, lparen.column))

            elif self.current_char == ")":
                rparen = self.get_match(r'\)')
                tokens.append(Token(TokenType.RPAREN, rparen.value, rparen.lineno, rparen.column))

            elif self.current_char == ";":
                semi = self.get_match(r';')
                tokens.append(Token(TokenType.SEMI, semi.value, semi.lineno, semi.column))

            elif self.current_char == ":":
                colon = self.get_match(r':')
                tokens.append(Token(TokenType.COLON, colon.value, colon.lineno, colon.column))

            elif self.current_char == ",":
                comma = self.get_match(r',')
                tokens.append(Token(TokenType.COMMA, comma.value, comma.lineno, comma.column))

            elif self.current_char == "+":
                plus = self.get_match(r'\+')
                tokens.append(Token(TokenType.PLUS, plus.value, plus.lineno, plus.column))

            elif self.current_char == "-":
                minus = self.get_match(r'-')
                tokens.append(Token(TokenType.MINUS, minus.value, minus.lineno, minus.column))

            elif self.current_char == "*":
                mul = self.get_match(r'\*')
                tokens.append(Token(TokenType.MUL, mul.value, mul.lineno, mul.column))

            elif self.current_char == "/":
                div = self.get_match(r'/')
                tokens.append(Token(TokenType.DIV, div.value, div.lineno, div.column))

            elif self.current_char == "%":
                mod = self.get_match(r'%')
                tokens.append(Token(TokenType.MOD, mod.value, mod.lineno, mod.column))
            
            else:
                self.error()

        tokens.append(Token(TokenType.EOF, None, self.lineno, self.column))
        return tokens

        